# app.py
import logging
import re
import uuid
from flask import Flask, jsonify, request
from task_db import TaskDB

app = Flask(__name__)

# Configure logging
logging.config.fileConfig('logging.conf')
error_logger = logging.getLogger('API_ERROR')
normal_logger = logging.getLogger('API_NORMAL')

def log_request_response(request, response, request_id):
    normal_logger.info('Request ID: %s', request_id)
    normal_logger.info('Request: %s %s', request.method, request.url)
    normal_logger.info('Request Body: %s', request.get_json())
    normal_logger.info('Response: %s', response.get_json())

def validate_input(f):
    def wrapper(*args, **kwargs):
        # Validate input payload for non-GET requests
        if request.method != 'GET':
            # Get the request payload
            data = request.get_json()

            # Check if data is present and is a dictionary
            if not data or not isinstance(data, dict):
                response = jsonify({'error': 'Invalid input data'})
                log_request_response(request, response, request_id)
                return response, 400

            # Check for HTML tags or special characters in the input payload
            pattern = re.compile(r'<[^>]+>|[&<>"\']')
            for key, value in data.items():
                if isinstance(value, str) and pattern.search(value):
                    response = jsonify({'error': 'Invalid characters in input data'})
                    log_request_response(request, response, request_id)
                    return response, 400

        return f(*args, **kwargs)

    return wrapper

@app.before_request
def set_request_id():
    request.request_id = str(uuid.uuid4())

@app.after_request
def log_response(response):
    log_request_response(request, response, request.request_id)
    return response

@app.route('/api/v1/tasks', methods=['GET'])
@validate_input
def get_tasks():
    # Perform validation on query parameters or path variables if needed
    # ...

    tasks = task_db.get_all_tasks()
    response = jsonify({'tasks': [task.__dict__ for task in tasks]})
    return response, 200

@app.route('/api/v1/tasks/<string:task_id>', methods=['GET'])
@validate_input
def get_task(task_id):
    # Perform validation on query parameters or path variables if needed
    # ...

    task = task_db.get_task_by_id(task_id)
    if task:
        response = jsonify(task.__dict__)
        return response, 200
    else:
        response = jsonify({'error': 'Task not found'})
        error_logger.error('Task not found. ID: %s', task_id)
        return response, 404

@app.route('/api/v1/tasks', methods=['POST'])
@validate_input
def create_task():
    data = request.get_json()
    task = Task(data.get('title'), data.get('description'), 'pending')
    task_db.save_task(task)
    response = jsonify(task.__dict__)
    return response, 201

@app.route('/api/v1/tasks/<string:task_id>', methods=['PUT'])
@validate_input
def update_task(task_id):
    task = task_db.get_task_by_id(task_id)
    if task:
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task_db.update_task(task)
        response = jsonify(task.__dict__)
        return response, 200
    else:
        response = jsonify({'error': 'Task not found'})
        error_logger.error('Task not found. ID: %s', task_id)
        return response, 404

@app.route('/api/v1/tasks/<string:task_id>', methods=['DELETE'])
@validate_input
def delete_task(task_id):
    task = task_db.get_task_by_id(task_id)
    if task:
        task_db.delete_task(task)
        response = jsonify({'message': 'Task deleted'})
        return response, 200
    else:
        response = jsonify({'error': 'Task not found'})
        error_logger.error('Task not found. ID: %s', task_id)
        return response, 404

if __name__ == '__main__':
    task_db = TaskDB()
    app.run(debug=True)

