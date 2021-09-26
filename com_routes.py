from flask import request, json, render_template

from app import app, db, commutation
someobject = None
import app_logger

logger = app_logger.get_logger(__name__)

@app.route("/")
def index():
    return 'hi'

@app.route("/api/v1/get_status", methods=['GET'])
def get_status():
    try:
        status, text = someobject.get_status()
        return status, text
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error', 'message':str(ex)}


@app.route("/api/v1/set_path", methods=['POST'])
def set_path():
    try:
        json_data = request.get_json()
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error', 'message':str(ex)}


@app.route("/api/v1/set_type", methods=['POST'])
def set_type():
    try:
        commutation.set_type(1)
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error', 'message':str(ex)}


@app.route("/api/v1/get_type", methods=['GET'])
def get_type():
    try:
        return {'status': 0, 'type': commutation.get_type()}
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error', 'message':str(ex)}


@app.route("/api/v1/get_pathes", methods=['GET'])
def get_pathes():
    pass


