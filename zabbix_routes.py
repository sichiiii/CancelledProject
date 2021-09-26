from flask.templating import render_template
from app import app

someobject = None
import app_logger
from zabbix import ZABBIX
from config import Configuration
logger = app_logger.get_logger(__name__)


@app.route("/api/v1/zabbix/update_items", methods=['GET'])
def update_items():
    pass