## Performance test for the Simple Task Queue Processing Service

This repository includes the necessary files and scripts to conduct performance testing on the Simple Task Queue Processing Service. It provides a Locust test script designed to simulate load on the service, enabling the evaluation of its performance under various conditions. Additionally, the repository contains detailed documentation, including setup instructions, usage guidelines, and a comprehensive performance test report.

### How to run the test

This repository contains test script for Locust to generate load for task queue processing service.
Locust doc: https://docs.locust.io/en/stable/index.html
Test script is here: task_queue_processing_locustfile.py

Steps to run test:
1. Make sure Python 3 is installed (python3 -V). Locust is supported on Python 3.9 or later. 

2. Create and activate a virtual environment (optional):
```
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```
pip3 install -r requirements.txt
```

4. Test can be run in distributed mode using master and slaves (one slave per each processor core).
Command to run test:
```
locust -f task_queue_processing_locust_file.py --logfile log --master&
locust -f task_queue_processing_locust_file.py --logfile log --worker& 
```
(repeat the second line per each processor core)

--logfile - optional parameter if log should go to specified file. If not set, log will go to stdout/stderr.

5. Once test has started, open Web UI on http://localhost:8089 (if you are running Locust locally).

6. Enter values into start form and press the button 'Start swarming'.

### Simple Task Queue Processing Service Description

[Simple Task Queue Processing Service](task-queue-processing-service/)

### Test Report

[Performance Test Report](performance-test-report.md)
