### Simple Task Queue Processing Service

#### Description

A naive task queue processing system service. The service accepts different tasks and executes them asynchronously, ideally depending on the available resources. The task executions and results are persisted (by default, on local file system).

There are only 2 types of tasks in the system:
 - Compute factorial. The result of this task is just a factorial.
 - Fetch content by provided URL using HTTP. The result of this task is raw HTTP resource content.

The service exposes 3 API endpoints over HTTP protocol:
   - `POST /tasks/submissions`
   - `GET /tasks/submissions/{id}`
   - `GET /tasks/{id}`

The default server port is: `18991`

#### Service API

- `POST /tasks/submissions`
   
   The endpoint accepts (or rejects) a new task submission.

   Request:

    ```
    {
        "type": <type>,
        "args": {
            <arg>: <value>
        }
    }
    ```

    - `<type>` - the type of the task, one of `factorial`, `http-fetch`
    - `<arg>: <value>` - task specific arguments (see please examples below)

   Response:
    - on success, HTTP status code `202` is returned with `<id>` of the task

        ```
        {
            "id": <id>
        }
        ```
    - on error, one of HTTP status codes `400`, `500` or `503` could be returned

   Examples:

    - for factorial computation

        ```
        POST /tasks/submissions
        
        {
            "type": "factorial",
            "args": {
                "n": "50"
            }
        }
        ```

    - for HTTP URL content fetching (please be careful not DDoSing your favorite service)

        ```
        POST /tasks/submissions

        {
            "type": "http-fetch",
            "args": {
                "url": "https://spring.io"
            }
        }
        ```

- `GET /tasks/submissions/{id}`

   Returns the current status of the submitted task.


   Request: 
    
    ```
    <none>
    ```

   Responses:
    - on success, HTTP status code `200` is returned with `<id>` and `<status>` of the task

        ```
        {
            "id": <id>,
            "status": <status>
        }
        ``` 
   
        - `<id>` - the task identifier (equal to the one provided in request URL)
        - `<status>` - the task status, could have one of the following values: `QUEUED`, `RUNNING`, `FAILED`, `SUCCEEDED`, `REJECTED`
    
    - on error, HTTP status code `404` could be returned


- `GET /tasks/{id}`

   Returns the final result of the submitted task when it completes. The task is considered completed when it has transitioned into `SUCCEEDED` or `FAILED` status.

   Request: 
    
    ```
    <none>
    ```

   Response:

    - on success, HTTP status code `200` is returned with `<id>`, `<status>` of the task

        ```
        {
            "id": <id>,
            "status": <status>
            "result": <result>
        }
        ``` 

        - `<id>` - the task identifier (equal to the one provided in request URL)
        - `<status>` - the task status, could have one of the following values: `FAILED`, `SUCCEEDED`
        - `<result>` - the task specific results (see examples below please please)
    
    - on error, HTTP status code `404` or `400` could be returned

   Examples:

    - for HTTP URL content fetching (successful result)

        ```
        GET /tasks/8637eb37-f8e7-4755-80fb-2f59e91f090f

        {
            "id": "8637eb37-f8e7-4755-80fb-2f59e91f090f",
            "status": "SUCCEEDED",
            "result": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<title>Spring  ... </body></html>"
        }
        ```

    - for HTTP URL content fetching (failed execution)

        ```
        GET /tasks/b57aa934-145c-4ea4-a468-adc29fe02cf3

        {
            "id": "b57aa934-145c-4ea4-a468-adc29fe02cf3",
            "status": "FAILED",
            "result": {
                "cause": null,
                "stackTrace": [],
                "message": "Connection refused",
                "suppressed": [],
                "localizedMessage": "Connection refused"
            }
        }
        ```

    - for factorial computation

        ```
        GET /tasks/8637eb37-f8e7-4755-80fb-2f59e91f090f

        {
            "id": "990296b8-e299-4996-908a-ed70f6c72299",
            "status": "SUCCEEDED",
            "result": 30414093201713378043612608166064768844377641568960512000000000000
        }
        ```

#### How to run

The provided service instance could be run in two ways

- using `Docker` (needs more or less recent version of `Docker` to be installed)

    `docker load -i task-queue-processing-1.0-SNAPSHOT.tar `
    
    `docker run -p 18991:18991 -d behavox/task-queue-processing:1.0-SNAPSHOT`

- using `standalone jar` (needs JDK 11+ to be installed)

    `java -jar task-queue-processing-1.0-SNAPSHOT-standalone.jar`