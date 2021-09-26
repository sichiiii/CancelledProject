from flask import render_template

from app import app, commutation
from models.data import OgmCommand
from ogm import OGM
import requests
import json
from config import Configuration
from zabbix import ZABBIX

someobject = None
from flask import request
import app_logger

logger = app_logger.get_logger(__name__)
ogm = OGM(commutation.get_config())
import json
config = Configuration()
config.load('./config.ini')
zab = ZABBIX(config)

@app.route("/api/v1/ogm/send_byte_command", methods=['POST', 'GET'])
def send_byte_command():
    try:
        if request.method == 'POST':
            ip = request.form["ip"]
            command = request.form["byte_code"]

            result = ogm.send_byte_command(ip, command)
            return {'status': 'ok', 'message': result}
        elif request.method == 'GET':
            return render_template('send_byte_command.html')
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error', 'message':str(ex)}


@app.route("/api/v1/ogm/send_command", methods=['POST', 'GET'])
def send_command():
    try:
            if request.method == 'POST':
                ip = request.form["ip"]
                plata = request.form["plata"]
                command = request.form["comp_select"]
                value = request.form["value"]

                result = ogm.send_command(ip, plata, command, value)
            elif request.method == 'GET':
                return render_template('send_command.html',
                                    command_list=[x[0] for x in OgmCommand.query.with_entities(OgmCommand.name).all()])
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error', 'message':str(ex)}

@app.route("/api/v1/ogm/get_table", methods=['POST', 'GET'])
def get_table():
    try:
        if request.method == 'GET':
            result = zab.get_hardware()
            names = []
            for i in result:
                names.append(i['name'])
            return render_template('get_table.html', colours=names)
        elif request.method == 'POST':  
            result = zab.get_hardware()
            for i in result:
                if i['name'] == request.form['colours']:
                    ip = i['ip']
                    port = i['port']
            if request.form['submit_button'] == 'get-table':
                r = requests.post("http://localhost:8080/api/v1/get_table", data=json.dumps({"data":{"ip":ip, "port":port}}))
            logger.warning(r.text)
            names = []
            for i in result:
                names.append(i['name'])
            return render_template('get_table.html', colours=names)
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error'}
    
@app.route("/api/v1/ogm/get_settings", methods=['POST', 'GET'])
def get_settings():
    try:
        if request.method == 'GET':
            result = zab.get_hardware()
            names = []
            for i in result:
                names.append(i['name'])
            return render_template('get_settings.html', colours=names)
        elif request.method == 'POST':  
            result = zab.get_hardware()
            for i in result:
                if i['name'] == request.form['colours']:
                    ip = i['ip']
                    port = i['port']
            if request.form['submit_button'] == 'get-settings':
                r = requests.post("http://localhost:8080/api/v1/get_settings", data=json.dumps({"data":{"ip":ip, "port":port}}))
            logger.warning(r.text)
            names = []
            for i in result:
                names.append(i['name'])
            return render_template('get_settings.html', colours=names)
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error'}

@app.route("/api/v1/ogm/set_plume", methods=['GET', 'POST'])
def set_plume():
    try:
        if request.method == 'GET':
            result = zab.get_hardware()
            names = []
            for i in result:
                names.append(i['name'])
            return render_template('plume.html', colours=names)
        elif request.method == 'POST':  
            result = zab.get_hardware()
            for i in result:
                if i['name'] == request.form['colours']:
                    ip = i['ip']
                    port = i['port']
            data=json.dumps({"data": {"ip":ip, "plata":request.form['colours'], "port":port, "action":"loop-in", "value":1}})
            print(data)
            if request.form['submit_button'] == 'loop-in':
                r = requests.post("http://localhost:8080/api/v1/send_action", data=json.dumps({"data": {"ip":ip, "plata":request.form['colours'], "port":port, "action":"loop-in", "value":1}}))
            elif request.form['submit_button'] == 'loop-out':
                r = requests.post("http://localhost:8080/api/v1/send_action", data=json.dumps({"data": {"ip":ip, "plata":request.form['colours'], "port":port, "action":"loop-out", "value":1}}))
            ##elif request.form['submit_button'] == 'loop_matrix':
            ##    r = requests.post("http://localhost:8080/api/v1/send_action", data=json.dumps({"data": {"ip":"192.168.0.215", "plata":14, "port":2, "action":"loop-matrix", "value":1}}))
            elif request.form['submit_button'] == 'get-status':
                r = requests.post("http://localhost:8080/api/v1/get_data_from_plata", data=json.dumps({"data": {"ip":ip, "plata":request.form['colours']}}))
            logger.warning(r.text)
            names = []
            for i in result:
                names.append(i['name'])
            return render_template('plume.html', colours=names)
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error'}
