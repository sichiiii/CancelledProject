import datetime

from app import db
from sqlalchemy import DateTime


class Diagnostic(db.Model):
    __tablename__ = 'diagnostic'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    comment = db.Column(db.String())
    details = db.relationship('DiagnosticDetail', backref='diagnostic',
                              lazy='dynamic')

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

    def to_json(self):
        return dict(name=self.name, comment=self.comment)


class DiagnosticDetail(db.Model):
    __tablename__ = 'diagnostic_steps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    text = db.Column(db.String())
    comment = db.Column(db.String())
    action = db.Column(db.Boolean, default=False)
    diag = db.Column(db.Integer, db.ForeignKey('diagnostic.id'))

    def __init__(self, name, text, comment, action, diag):
        self.name = name
        self.text = text
        self.comment = comment
        self.action = action
        self.diag = diag

    def to_json(self):
        return {
            "name": self.name,
            "text": self.text,
            "comment": self.comment,
            "action": self.action,
            "diag": self.diag,
        }


class OgmCommand(db.Model):
    __tablename__ = 'ogm_commands'

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {"name": self.name}


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String())
    text = db.Column(db.String())
    raws = db.relationship('RowReports', backref='reports',
                           lazy='dynamic')

    def __init__(self, name, text):
        self.name = name
        self.text = text

    def to_json(self):
        return {
            "name": self.name,
            "text": self.text,
            "id": self.id,
        }


class RowReports(db.Model):
    __tablename__ = 'row_reports'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String())
    visible_name = db.Column(db.String())
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'))

    def __init__(self, name, visible_name, report_id):
        self.name = name
        self.report_id = report_id
        self.visible_name = visible_name

    def to_json(self):
        return {
            "name": self.name,
        }


# table 3
class HardwareState(db.Model):
    __tablename__ = 'hardware_state'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(), unique=True)

    def __init__(self, data):
        self.data = data


# table 4
class ChannelType(db.Model):
    __tablename__ = 'channel_type'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(), unique=True)

    def __init__(self, data):
        self.data = data


# table 5
class ConnectionType(db.Model):
    __tablename__ = 'connection_type'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(), unique=True)

    def __init__(self, data):
        self.data = data


# table 6
class TractType(db.Model):
    __tablename__ = 'tract_type'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(), unique=True)

    def __init__(self, data):
        self.data = data


# table 7
class ChannelState(db.Model):
    __tablename__ = 'channel_state'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(), unique=True)

    def __init__(self, data):
        self.data = data


# table 8
class ChannelIniciator(db.Model):
    __tablename__ = 'channel_iniciator'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(), unique=True)

    def __init__(self, data):
        self.data = data


# table 9
class DiagnosticParams(db.Model):
    __tablename__ = 'diagnostic_params'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), unique=True)
    size_name = db.Column(db.String())
    type = db.Column(db.String())
    code = db.Column(db.String())

    def __init__(self, name, size_name, type, code):
        self.name = name
        self.size_name = size_name
        self.type = type
        self.code = code


# table 10
class TractState(db.Model):
    __tablename__ = 'tract_state'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(), unique=True)

    def __init__(self, data):
        self.data = data


# table 11
class UserState(db.Model):
    __tablename__ = 'user_state'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(), unique=True)

    def __init__(self, data):
        self.data = data


# table 12
class ErrorChannel(db.Model):
    __tablename__ = 'error_channel'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(), unique=True)

    def __init__(self, data):
        self.data = data


class Tracts(db.Model):
    __tablename__ = 'tracts'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String())
    type = db.Column(db.String())
    comment = db.Column(db.String())
    state = db.Column(db.Integer())
    last_change_state = db.Column(db.DateTime())
    hard_from = db.Column(db.Integer(), db.ForeignKey('hardware.id'))
    hard_to = db.Column(db.Integer(), db.ForeignKey('hardware.id'))
    port_from = db.Column(db.String())
    port_to = db.Column(db.String())

    def __init__(self, name, type, comment, state, last_change_state, hard_from, hard_to, port_from, port_to):
        self.name = name
        self.type = type
        self.comment = comment
        self.state = state
        self.last_change_state = last_change_state
        self.hard_from = hard_from
        self.hard_to = hard_to
        self.port_from = port_from
        self.port_to = port_to


class HadwareZabbixItems(db.Model):
    __tablename__ = 'hardware_zabbix_items'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    zabbix_id = db.Column(db.Integer())
    hadrware_id = db.Column(db.Integer(), db.ForeignKey('hardware.id'))

    def __init__(self, zabbix_id, tract_id):
        self.zabbix_id = zabbix_id
        self.tract_id = tract_id

    def to_json(self):
        return dict(zabbix_id=self.zabbix_id, tract_id=self.tract_id)


class HadwareZabbixTriggers(db.Model):
    __tablename__ = 'hardware_zabbix_triggers'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    zabbix_id = db.Column(db.Integer())
    hadrware_id = db.Column(db.Integer(), db.ForeignKey('hardware.id'))

    def __init__(self, zabbix_id, tract_id):
        self.zabbix_id = zabbix_id
        self.tract_id = tract_id

    def to_json(self):
        return dict(zabbix_id=self.zabbix_id, tract_id=self.tract_id)


class TractActionHistory(db.Model):
    __tablename__ = 'tract_action_history'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tract_id = db.Column(db.Integer(), db.ForeignKey('tracts.id'))
    state = db.Column(db.Integer, db.ForeignKey('tract_state.id'))
    start_time = db.Column(db.DateTime())
    stop_time = db.Column(db.DateTime())
    reason = db.Column(db.Integer())
    iniciator = db.Column(db.String(), db.ForeignKey('channel_iniciator.id'))

    def __init__(self, tract_id, state, start_time, stop_time, reason, iniciator):
        self.tract_id = tract_id
        self.state = state
        self.start_time = start_time
        self.stop_time = stop_time
        self.reason = reason
        self.iniciator = iniciator

    def to_json(self):
        return dict(tract_id=self.tract_id, state=self.state, \
                    start_time=self.start_time, stop_time=self.stop_time, \
                    reason=self.reason, iniciator=self.iniciator)


class Channel(db.Model):
    __tablename__ = 'channel'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String())
    comment = db.Column(db.String())
    state = db.Column(db.Integer, db.ForeignKey('tract_state.id'))
    last_change_state = db.Column(db.DateTime())
    iniciator = db.Column(db.Integer())
    type = db.Column(db.Integer())

    def __init__(self, name, comment, state, last_change_state, iniciator, type):
        self.name = name
        self.comment = comment
        self.state = state
        self.last_change_state = last_change_state
        self.iniciator = iniciator
        self.type = type


class ChannelActionHistory(db.Model):
    __tablename__ = 'channel_action_history'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    state = db.Column(db.Integer, db.ForeignKey('channel_state.id'))
    start_time = db.Column(db.DateTime())
    stop_time = db.Column(db.DateTime())
    reason = db.Column(db.Integer())
    iniciator = db.Column(db.String(), db.ForeignKey('channel_iniciator.id'))

    def __init__(self, channel_id, state, start_time, stop_time, reason, iniciator):
        self.channel_id = channel_id
        self.state = state
        self.start_time = start_time
        self.stop_time = stop_time
        self.reason = reason
        self.iniciator = iniciator

    def to_json(self):
        return dict(channel_id=self.channel_id, state=self.state, \
                    start_time=self.start_time, stop_time=self.stop_time, \
                    reason=self.reason, iniciator=self.iniciator)


class TractsInChannels(db.Model):
    __tablename__ = 'tracts_in_channel'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    channel_id = db.Column(db.Integer)
    tract_id = db.Column(db.Integer())

    def __init__(self, channel_id, tract_id):
        self.channel_id = channel_id
        self.tract_id = tract_id


class ReserveTracts(db.Model):
    __tablename__ = 'reserve_tracts'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    tract_id_master = db.Column(db.Integer())
    tract_id_slave = db.Column(db.Integer())

    def __init__(self, tract_id_master, tract_id_slave):
        self.tract_id_master = tract_id_master
        self.tract_id_slave = tract_id_slave


class Hardware(db.Model):
    __tablename__ = 'hardware'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String())
    type = db.Column(db.String())

    def __init__(self, name, type):
        self.name = name
        self.type = type

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

class TaskChannels(db.Model):
    __tablename__ = 'task_channels'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer())
    channel_id = db.Column(db.Integer())

    def __init__(self, task_id, channel_id):
        self.task_id = task_id
        self.channel_id = channel_id
