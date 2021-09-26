import app_logger

from flask import request, json, render_template, jsonify
from app import app, db, commutation
from models.data import Channel, Tracts
from sql import SQLITE
from sqlalchemy import func
from sqlalchemy.orm import load_only

logger = app_logger.get_logger(__name__)

sql = SQLITE()

@app.route("/api/v1/kaus/channels", methods=['POST', 'GET'])  # 3
def channels():
    try:
        res = sql.getChannels()
        return json.dumps(res)
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/time_channel", methods=['POST', 'GET'])  # 4
def time_channel():
    try:
        time = db.session.query(func.max(Channel.last_change_state)).scalar()
        return {'status': 0, 'time': time}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/update_channel", methods=['POST'])  # 5 
def update_channel():
    try:
        json_data = request.get_json()
        id = json_data['id']
        type = json_data['type']
        tasks = json_data['tasks']
        sql.updateChannel(id, type, tasks)
        return {'status': 0, 'message':'ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/tracts", methods=['POST', 'GET'])  # 6
def tracts():
    try:
        fields = ['id', 'hard_from', 'port_from', 'hard_to', 'port_to', 'type', 'reserve']
        res = sql.getTracts()
        for i in res:
            if 'reserve' in fields:
                reserve = sql.get_reverse(i.get('id'))
                i['reserve'] = ''
                if reserve.get('master'):
                    i['reserve'] += ' Основной канал для ' + reserve.get('master')
                if reserve.get('slave'):
                    if i['reserve'] != '':
                        i['reserve'] += "\n"
                    i['reserve'] += ' Резервный канал для ' + reserve.get('slave')
        print(res)
        return json.dumps(res)
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/time_tract", methods=['POST', 'GET'])  # 7
def time_tract():
    try:
        time = db.session.query(func.max(Tracts.last_change_state)).scalar()
        return {'status': 0, 'time': time}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/channel_state", methods=['POST'])  # 8   #TODO Добавить номер связи
def channel_state():
    try:
        json_data = request.get_json()
        id = json_data['id']
        res = sql.getChannelState(id)
        return json.dumps(res)
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/channel_routes", methods=['POST'])  # 9  
def channel_routes():
    try:
        json_data = request.get_json()
        id = json_data['id']
        res = sql.getChannelRoutes(id)
        return res
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/hardware_nums", methods=['POST'])  # 10   
def hardware_nums():
    try:
        json_data = request.get_json()
        id = json_data['id']
        res = sql.getHardwareNums(id)
        return res
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/channel_params", methods=['POST'])  # 11   #TODO
def channel_params():
    try: 
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/channel_command", methods=['POST'])  # 12 
def channel_command():
    try:
        json_data = request.get_json()
        id = json_data['id']
        activity = json_data['activity']
        res = sql.channelCommand(id, activity)
        return res
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/tracts_state", methods=['POST'])  # 13   #TODO Добавить признак и км линии
def tracts_state():
    try:
        json_data = request.get_json()
        id = json_data['id']
        res = sql.getTractState(id)
        return res
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/channels_in_tract", methods=['POST'])  # 14  
def channel_in_tract():
    try:
        json_data = request.get_json()
        id = json_data['id']
        res = sql.getTractsInChannel(id)
        return res
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/hardware_in_tract", methods=['POST'])  # 15 
def hardware_in_tract():
    try:
        json_data = request.get_json()
        id = json_data['id']
        res = sql.getHardwareInTract(id)
        return res
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/tract_params", methods=['POST'])  # 16   #TODO
def tract_params():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/change_tract", methods=['POST'])  # 17
def change_tract():
    try:
        json_data = request.get_json()
        id = json_data['id']
        new_id = json_data['new_id']
        res = sql.changeTract(id, new_id)
        return res
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/radiosilence_activity", methods=['POST', 'GET'])  # 18   
def radiosilence_activity():
    try:
        res = commutation.get_radio_silence()
        return res
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/set_radiosilence", methods=['POST'])  # 19 
def enable_radiosilence():
    try:
        json_data = request.get_json()
        status = json_data['status']
        res = commutation.set_radio_silence(status)
        return {'status':'ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/connections_list", methods=['POST'])  # 20   #TODO
def connections_list():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/disable_connection", methods=['POST'])  # 21   #TODO
def disable_connection():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/delete_connection", methods=['POST'])  # 22   #TODO
def delete_connection():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/recovery_request", methods=['POST'])  # 23   #TODO
def recovery_request():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/change_connection", methods=['POST'])  # 24   #TODO
def change_connection():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/request_options", methods=['POST'])  # 25   #TODO
def request_options():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/setup_option", methods=['POST'])  # 26   #TODO
def setup_option():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/connection_priority", methods=['POST'])  # 27   #TODO
def connection_priority():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/setup_connection_priority", methods=['POST'])  # 28   #TODO
def setup_connection_priority():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/return_default_priority", methods=['POST'])  # 29   #TODO
def return_default_priority():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/recovered_channel", methods=['POST'])  # 30   #TODO
def recovered_channel():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/recovered_tracts", methods=['POST'])  # 31   #TODO
def recovered_tracts():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/priority_channels", methods=['POST'])  # 32   #TODO
def priority_channels():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/kaus/unsuccesful_recovery_channels", methods=['POST'])  # 33   #TODO
def unsuccesful_recovery_channels():
    try:
        return 'Building bombs...'
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}
