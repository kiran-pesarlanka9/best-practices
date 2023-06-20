import unittest
from flask import jsonify
from app import app

class TaskAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_tasks(self):
        response = self.app.get('/api/tasks')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_get_task_by_id(self):
        # Assuming there is a task with ID 'task_id' in the database
        task_id = 'task_id'
        response = self.app.get(f'/api/tasks/{task_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)

    def test_get_task_by_id_not_found(self):
        # Assuming there is no task with ID 'nonexistent_id' in the database
        task_id = 'nonexistent_id'
        response = self.app.get(f'/api/tasks/{task_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Task not found')

    def test_create_task(self):
        task_data = {
            'title': 'Task Title',
            'description': 'Task Description',
            'status': 'Task Status'
        }
        response = self.app.post('/api/tasks', json=task_data)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Task created successfully')
        self.assertIn('id', data)

    def test_update_task(self):
        # Assuming there is a task with ID 'task_id' in the database
        task_id = 'task_id'
        updated_task_data = {
            'title': 'Updated Task Title',
            'description': 'Updated Task Description',
            'status': 'Updated Task Status'
        }
        response = self.app.put(f'/api/tasks/{task_id}', json=updated_task_data)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Task updated successfully')

    def test_update_task_not_found(self):
        # Assuming there is no task with ID 'nonexistent_id' in the database
        task_id = 'nonexistent_id'
        updated_task_data = {
            'title': 'Updated Task Title',
            'description': 'Updated Task Description',
            'status': 'Updated Task Status'
        }
        response = self.app.put(f'/api/tasks/{task_id}', json=updated_task_data)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Task not found')

    def test_delete_task(self):
        # Assuming there is a task with ID 'task_id' in the database
        task_id = 'task_id'
        response = self.app.delete(f'/api/tasks/{task_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Task deleted successfully')

    def test_delete_task_not_found(self):
        # Assuming there is no task with ID 'nonexistent_id' in the database
        task_id = 'nonexistent_id'
        response = self.app.delete(f'/api/tasks/{task_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Task not found')


if __name__ == '__main__':
    unittest.main()

