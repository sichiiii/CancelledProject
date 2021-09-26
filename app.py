from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from commutation import Commutation

app = Flask(__name__)
db = SQLAlchemy(app)
commutation = Commutation()

if __name__ == "__main__":
    from com_routes import *
    from ogm_routes import *
    from diag_routes import *
    from zabbix_routes import *
    from report_routes import *
    from forms_routes import *
    from utils import *
    from kaus import *

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)
    app.run(debug=True, host='0.0.0.0')
