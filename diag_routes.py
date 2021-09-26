import app_logger

from flask import json, request
from sqlalchemy.sql import text
from app import app, db, commutation
from models.data import Diagnostic, DiagnosticDetail


logger = app_logger.get_logger(__name__)

@app.route("/api/v1/diag/get_list", methods=['GET'])
def get_list():
    try:
        offs = int(request.args.get('offset', 0))
        ord = request.args.get('order', 'id')
        lim = int(request.args.get('limit', 50))
        q = Diagnostic.query.filter(text(ord)).offset(offs).limit(lim) 
        return json.dumps({"data": [z.to_json() for z in q], "offset": offs, "order": ord, "limit": lim})
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message':str(ex)}

@app.route("/api/v1/diag/create", methods=['POST'])
def create():
    try:
        json_data = request.get_json()
        name = json_data['data']['name']
        comment = json_data['data']['comment']
        diag = Diagnostic(name, comment)
        db.session.add(diag)
        db.session.flush()
        print(diag.id)
        for i in json_data['data']['steps']:
            i['diag'] = diag.id
            step = DiagnosticDetail(**i)
            db.session.add(step)
        db.session.commit()
        return {'status': 'ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}
        
@app.route("/api/v1/diag/get_steps", methods=['GET'])
def get_steps():
    try:
        id = request.args.get('id', '')
        q = DiagnosticDetail.query.filter(DiagnosticDetail.id == id)
        return json.dumps({"data": [z.to_json() for z in q], "data_len": DiagnosticDetail.query.count(), "diag_id": id})
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error', 'message':str(ex)}


@app.route("/api/v1/diag/delete_diag", methods=['POST'])
def delete_diag():
    try:
        json_data = request.get_json()
        Diagnostic.query.filter(DiagnosticDetail.id == json_data['id']).delete()
        db.session.commit()
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error', 'message':str(ex)}


@app.route("/api/v1/diag/update_step", methods=['POST'])
def update_step():
    try:
        json_data = request.get_json()
        DiagnosticDetail.query.filter_by(id=json_data['data']['id']).update({'name': json_data['data']['name'], \
                                                                             'text': json_data['data']['text'],
                                                                             'comment': json_data['data']['comment'],
                                                                             'action': json_data['data']['action'], \
                                                                             'diag': json_data['data']['diag']})
        db.session.commit()
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}

@app.route("/api/v1/diag/update_diag", methods=['POST'])
def update_diag():
    try:
        json_data = request.get_json()
        Diagnostic.query.filter_by(id=json_data['data']['id']).update({'name': json_data['data']['name'], \
                                                                       'comment': json_data['data']['comment']})
        db.session.commit()
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}

@app.route("/api/v1/diag/add_step", methods=['POST'])
def add_step():
    try:
        json_data = request.get_json()
        step = DiagnosticDetail(json_data['data']['name'], json_data['data']['text'], \
                                json_data['data']['comment'], json_data['data']['action'],
                                diag=json_data['data']['diag_id'])
        db.session.add(step)
        db.session.commit()
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/diag/del_step", methods=['POST'])
def del_step():
    try:
        json_data = request.get_json()
        DiagnosticDetail.query.filter(DiagnosticDetail.id == json_data['id']).delete()
        db.session.commit()
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}
