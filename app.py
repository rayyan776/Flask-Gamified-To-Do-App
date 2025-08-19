from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# In-memory task store
tasks = []

@app.route('/')
def index():
    # Serve the main HTML webpage
    return render_template('index.html')

# REST API: GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# REST API: POST create new task
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'done': False
    }
    tasks.append(task)
    return jsonify(task), 201

# REST API: PUT update task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = data.get('done', task['done'])
            task['title'] = data.get('title', task['title'])
            return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

# REST API: DELETE task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)
