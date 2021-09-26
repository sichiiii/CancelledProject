import app_logger

from flask import request, json, render_template
from app import app, db, commutation
from models.data import Diagnostic, DiagnosticDetail, OgmCommand, Report, RowReports, Tracts, Channel
from ogm import OGM
from sql import SQLITE
from sqlalchemy.orm import load_only

someobject = None
logger = app_logger.get_logger(__name__)


@app.route("/api/v1/reports/create_report", methods=['POST'])
def create_report():
    try:
        json_data = request.get_json()

        name = json_data['data']['name']
        text = json_data['data']['text']
        report = Report( name, text)

        #todo доделать
        db.session.add(report)
        db.session.commit()
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/reports/get_list_reports", methods=['POST'])
def get_list_reports():
    try:
        q = Report.query.all()
        return json.dumps({"data": [z.to_json() for z in q]})
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/reports/delete_report", methods=['POST'])
def delete():
    try:
        json_data = request.get_json()
        Report.query.filter_by(id=json_data['id']).delete()
        db.session.commit()
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/reports/get_report", methods=['GET', 'POST'])
def get_report():
    try:
        id = request.args.get('id', '')
        report = Report.query.filter_by(id=id).first()
        rows = RowReports.query.filter(RowReports.id == id)
        return json.dumps({"data": report.to_json(), "id": id, "rows":[row.to_json() for row in rows]})
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route("/api/v1/reports/update_params", methods=['POST'])
def update_params():
    try:
        json_data = request.get_json()
        Report.query.filter_by(id=json_data['data']['id']).update({'name': json_data['data']['name'], \
                                                                   'text': json_data['data']['text']})
        db.session.commit()
        return {'status': 0, 'message': 'Ok'}
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}
                                                                                                                                                                                                                                                                                                                      
@app.route('/api/v1/tracts_report_fields', methods=['GET', 'POST'])  #TODO
def tracts_report_fields():
    try:
        if request.method == 'POST':
            try:
                fields = request.form.getlist('fields')
                if not fields:
                    json_data = request.get_json()
                    fields = json_data['data']
            except Exception as ex:
                print(ex)



            sql = SQLITE()

            res = (sql.get_tracts_for_report(fields))
            print(res)
            trigers = commutation.get_active_triggers()
            warning = 0
            error = 0
            for item in trigers.values():
                for trig in item:
                    if int(trig['priority']) > 2:
                        print(trig)
                        error += 1
                    else:
                        warning += 1

            for i in res:
                i['channels'] = sql.get_chanels_with_tracts(i.get('id'))
                if 'reserve' in fields:
                    reserve = sql.get_reverse(i.get('id'))
                   # print(reserve)
                    i['reserve']=''
                    if reserve.get('master'):
                        i['reserve'] += ' Основной канал для ' + reserve.get('master')
                    if reserve.get('slave'):
                        if i['reserve'] != '':
                            i['reserve'] += "\n"
                        i['reserve'] += ' Резервный канал для ' + reserve.get('slave')

                i['damage'] = -1


            print(fields)
            rus = SQLITE().getRowsForReport(1)
            rusDict = {}
            for i in rus:
                rusDict[i[0]] = i[1]
            #    trigers = sql.get_trigers_for_tracts(i.get('id'))

            return render_template('tract_report_fields.html', fields=fields, data=res, len=len(res), warning=warning,
                                   error=error, rus=rusDict)
        else:
            fields = SQLITE().getRowsForReport(1)
            print(fields)
            return render_template('select_fields_tracts.html', fields=fields)
    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


@app.route('/api/v1/channels_report_fields', methods=['GET', 'POST'])   #TODO
def channels_report_fields():
    try:
        if request.method == 'POST':
            try:
                fields = request.form.getlist('fields')
                if not fields:
                    raise Exception
            except Exception as ex:
                json_data = request.get_json()
                fields = json_data['data']
                fields.insert(0, 'id')

            sql = SQLITE()

            res = (sql.get_channel_for_report(fields))
            print(res)
            rus = SQLITE().getRowsForReport(2)
            rusDict = {}
            for i in rus:
                rusDict[i[0]] = i[1]
            #    trigers = sql.get_trigers_for_tracts(i.get('id'))
            warning = 0
            error = 0
            return render_template('channels_report_fields.html', fields=fields, data=res, len=len(res), warning=warning,
                                   error=error, rus=rusDict)

        fields = SQLITE().getRowsForReport(2)
        print(fields)
        return render_template('select_fields_channels.html', fields=fields)

    except Exception as ex:
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}


