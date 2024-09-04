from locust import HttpUser, task, between
import random
import time
import logging

logger = logging.getLogger(__name__)


class TaskException(Exception):
    pass


class AppUser(HttpUser):
    wait_time = between(5, 5)

    @task(1)
    def create_task_factorial(self):
        f_value = random.randrange(101)
        new_task = {"type": "factorial", "args": {"n": f"{f_value}"}}

        with self.client.post('/tasks/submissions', json=new_task, name='post task for factorial',
                              catch_response=True) as task_response:
            if task_response.status_code != 202:
                task_response.failure(f'Task creation failed with status code {task_response.status_code}')
                logger.error(f'Task creation failed with status code {task_response.status_code}')
            else:
                task_response.success()
                task_id = task_response.json().get('id')
                self.check_task(task_id)

    @task(5)
    def create_task_url(self):
        new_task = {"type": "http-fetch", "args": {"url": "https://www.google.com"}}

        with self.client.post('/tasks/submissions', json=new_task, name='post task for url',
                              catch_response=True) as task_response:
            if task_response.status_code != 202:
                task_response.failure(f'Task creation failed with status code {task_response.status_code}')
                logger.error(f'Task creation failed with status code {task_response.status_code}')
            else:
                task_response.success()
                task_id = task_response.json().get('id')
                self.check_task(task_id)

    def check_task(self, task_id):
        with self.client.get(f'/tasks/submissions/{task_id}', name='get task submission',
                             catch_response=True) as status_response:
            if status_response.status_code != 200:
                status_response.failure('Task status is not reachable')
                logger.error('Task status is not reachable')
            else:
                status = status_response.json().get('status')
                while status in ['QUEUED', 'RUNNING']:
                    time.sleep(1)
                    with self.client.get(f'/tasks/submissions/{task_id}', name='get task submission again',
                                         catch_response=True) as new_status_response:
                        if new_status_response.status_code != 200:
                            new_status_response.failure('Task status is not reachable')
                            logger.error('Task status is not reachable')
                            return
                        status = new_status_response.json().get('status')
                        logger.info(
                            f'Checking again after getting QUEUED or RUNNING status: '
                            f'now status is {status} for task_id {task_id}')
                if status == 'FAILED':
                    status_response.failure(f'Task status is {status}')
                    logger.error(f'Task status is {status} for task_id {task_id}')
                else:
                    status_response.success()

        with self.client.get(f'/tasks/{task_id}', catch_response=True, name='get task result') as result_response:
            if result_response.status_code != 200:
                result_response.failure('Task result is not reachable')
                logger.error('Task result is not reachable')
            else:
                status = result_response.json().get('status')
                if status == 'FAILED':
                    result = result_response.json().get('result')
                    result_response.failure(f'Task status is FAILED for task_id {task_id} with result: {result}')
                    logger.error(f'Task status is FAILED for task_id {task_id} with result: {result}')
                else:
                    result_response.success()
