import app_logger

from flask import request, json, render_template
from app import app, db, commutation
from models.data import Task, Channel, TaskChannels
from sql import SQLITE

logger = app_logger.get_logger(__name__)
sql = SQLITE()

@app.route('/api/v1/create_task', methods=['GET', 'POST'])
def create_task():
    try:
        if request.method == 'POST':
            name = request.form['name']
            fields = request.form.getlist('fields')
            if not fields:                          #если дсон, то подаются айдишники каналов и имя задания
                json_data = request.get_json()
                fields = json_data['data']
                name = json_data['name']
            task = Task(name)
            db.session.add(task)
            db.session.flush()
            task_id = task.id
            for i in fields:
                task_channels = TaskChannels(task_id, int(i))
                db.session.add(task_channels)
            db.session.commit()
            return {'status' : 'ok'}
        fields = sql.getChannels()
        return render_template('create_task_fields.html', fields=fields)
    except Exception as ex:
        logger.error(str(ex))
        return {'status' : 'error', 'message' : str(ex)}

@app.route('/api/v1/delete_task', methods=['GET', 'POST'])
def delete_task():
    try:
        if request.method == 'POST':
            fields = request.form.getlist('fields')
            if not fields:                          #если дсон, то подаются айдишники каналов и имя задания
                json_data = request.get_json()
                fields = json_data['data']
            for i in fields:
                print(i)
                obj = Task.query.filter_by(id=i).delete()
                obj_channel = TaskChannels.query.filter_by(task_id=i).delete()
            db.session.commit()
            return {'status' : 'ok'}
        fields = sql.getTasks()
        return render_template('delete_task.html', fields=fields)
    except Exception as ex:
        logger.error(str(ex))
        return {'status' : 'error', 'message' : str(ex)}