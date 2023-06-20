from pymongo import MongoClient

class Task:
    def __init__(self, id, title, description, status):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

class TaskDB:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['taskdb']
        self.collection = self.db['tasks']

    def get_all_tasks(self):
        tasks = self.collection.find()
        return [self._document_to_task(task) for task in tasks]

    def get_task_by_id(self, task_id):
        task = self.collection.find_one({'_id': task_id})
        if task:
            return self._document_to_task(task)
        else:
            return None

    def save_task(self, task):
        task_dict = self._task_to_document(task)
        self.collection.insert_one(task_dict)

    def update_task(self, task):
        task_dict = self._task_to_document(task)
        self.collection.update_one({'_id': task.id}, {'$set': task_dict})

    def delete_task(self, task):
        self.collection.delete_one({'_id': task.id})

    def _task_to_document(self, task):
        return {
            '_id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status
        }

    def _document_to_task(self, document):
        return Task(
            id=document['_id'],
            title=document['title'],
            description=document['description'],
            status=document['status']
        )

