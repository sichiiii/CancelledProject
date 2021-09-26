import json, app_logger

from flask import render_template, request
from app import app, commutation
from models.data import RowReports, Report

@app.route("/get_form_tracts", methods=['POST', 'GET'])
def get_form_tracts():
    try:
        if request.method == 'POST':
            pass
        elif request.method == 'GET':
            q = RowReports.query.filter(Report.id == 1)

            row = Report.query.filter(Report.id == 1).first()
            print(row)
            row = row.to_json()
            row["rows"]= [z.to_json() for z in q]


          #  return json.dumps(row)
            return render_template('report_result.html', reports=row)
    except Exception as ex:
        print(str(ex))
        logger.error(str(ex))
        return {'status': 'error', 'message': str(ex)}

@app.route("/get_form_channels", methods=['POST', 'GET'])
def get_form_channels():
    try:
        if request.method == 'POST':
            pass
        elif request.method == 'GET':
            return render_template('get_form_channels.html')
    except Exception as ex:
        logger.error(str(ex))
        return {'status':'error', 'message':str(ex)}