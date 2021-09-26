from datetime import datetime

from flask import json

from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import load_only

import app_logger

logger = app_logger.get_logger(__name__)

class SQLITE:

    def __init__(self):
        self.engine = create_engine('sqlite:///test.db')
        self.meta = MetaData(self.engine)

    def get_tracts(self):
        tracts = Table('tracts', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([tracts])
                rs = con.execute(stm)
                return [dict(elem.items()) for elem in rs.fetchall()]
        except Exception as ex:
            logger.error(str(ex))

    def get_channel_for_report(self, fields):
        channels = Table('channel', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([channels.c.id, channels.c.name, channels.c.comment, channels.c.state, \
                    channels.c.last_change_state, channels.c.iniciator, channels.c.type])
                rs = con.execute(stm)
                return [dict(elem.items()) for elem in rs.fetchall()]
        except Exception as ex:
            logger.error(str(ex))

    def get_tracts_for_report(self, fields):
        tracts = Table('tracts', self.meta, autoload=True)
        state = Table('tract_state', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([tracts.c.id, tracts.c.name, tracts.c.type,
                              (tracts.c.hard_from.label('hard_from')
                               + '/' + tracts.c.port_from.label('hard_from')).label('hard_from'),
                              (tracts.c.hard_to.label('hard_to')
                               + '/' + tracts.c.port_from.label('hard_to')).label('hard_to'),
                              state.c.data.label('state')]).select_from(
                    tracts.outerjoin(state, state.c.id == tracts.c.state))
                rs = con.execute(stm)
                return [dict(elem.items()) for elem in rs.fetchall()]
        except Exception as ex:
            logger.error(str(ex))

    def get_chanels_with_tracts(self, tract_id):
        tracts = Table('tracts_in_channel', self.meta, autoload=True, include_columns=['tract_id', 'channel_id'])
        try:
            with self.engine.connect() as con:
                stm = select([tracts]).where(tracts.c.tract_id == tract_id)
                rs = con.execute(stm)
                return ','.join([str(elem[0]) for elem in rs.fetchall()])
        except Exception as ex:
            logger.error(str(ex))

    def get_trigers_for_tracts(self, tract_id):
        tracts = Table('tract_zabbix_triggers', self.meta, autoload=True, include_columns=['tract_id', 'zabbix_id'])
        try:
            with self.engine.connect() as con:
                stm = select([tracts]).where(tracts.c.tract_id == tract_id)
                rs = con.execute(stm)
                return ','.join([str(elem[0]) for elem in rs.fetchall()])
        except Exception as ex:
            logger.error(str(ex))

    def get_reverse(self, tract_id):
        tracts = Table('reserve_tracts', self.meta, autoload=True,
                       include_columns=['tract_id_master', 'tract_id_slave'])
        try:
            with self.engine.connect() as con:
                temp = {}
                stm = select([tracts]).where(tracts.c.tract_id_master == tract_id)
                rs = con.execute(stm)
                res = rs.fetchall()
                temp['master'] = ','.join([str(elem[1]) for elem in res])
                stm = select([tracts]).where(tracts.c.tract_id_slave == tract_id)
                rs = con.execute(stm)
                res = rs.fetchall()
                temp['slave'] = ','.join([str(elem[0]) for elem in res])
                return temp
        except Exception as ex:
            logger.error(str(ex))

    def addTractHistory(self, tract, state):
        tracts = Table('tracts', self.meta, autoload=True)        
        tract_action_history = Table('tract_action_history', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([tracts.c.id, tracts.c.state]).where(or_(tracts.c.hard_to == tract, tracts.c.hard_from == tract))
                rows = con.execute(stm).fetchall()
                reason = 'zabbix'
                iniciator = 'zabbix'
                if len(rows) > 0:
                    stm = select([tract_action_history.c.stop_time]).where(tract_action_history.c.tract_id == rows[0][0])
                    start_time = con.execute(stm).fetchall()
                    if len(start_time) > 0:
                        stm = insert(tract_action_history).values(tract_id=rows[0][0], state=rows[0][1], \
                            start_time=start_time[0][0], stop_time=datetime.now(), reason=reason, iniciator=iniciator)
                    else:
                        stm = insert(tract_action_history).values(tract_id=rows[0][0], state=rows[0][1], \
                            stop_time=datetime.now(), reason=reason, iniciator=iniciator)
                    con.execute(stm)
        except Exception as ex:
            logger.error(str(ex))

    def setTractWarning(self, tract, state):
        tracts = Table('tracts', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = update(tracts).where(and_(or_((tracts.c.hard_to == tract),
                                                    (tracts.c.hard_from == tract)),
                                                tracts.c.state < state + 1)).values(state=state,
                                                                                    last_change_state=datetime.now())
                con.execute(stm)
        except Exception as ex:
            logger.error(str(ex))

    def getRowsForReport(self, report_id):
        rows = Table('row_reports', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([rows.c.name, rows.c.visible_name]).where(rows.c.report_id == report_id)
                rs = con.execute(stm)
                return rs.fetchall()
        except Exception as ex:
            logger.error(str(ex))
            print(ex)

    def getTracts(self):
        tracts = Table('tracts', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([tracts.c.id, tracts.c.port_from, tracts.c.hard_from, tracts.c.port_to, tracts.c.hard_to, tracts.c.type])
                rs = con.execute(stm)
                return [dict(elem.items()) for elem in rs.fetchall()]
        except Exception as ex:
            logger.error(str(ex))

    def getChannels(self):
        tracts_in_channel = Table('tracts_in_channel', self.meta, autoload=True)        
        tracts = Table('tracts', self.meta, autoload=True)
        channels = Table('channel', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([channels.c.id])
                channels_list = con.execute(stm)
                a =[dict(elem.items()) for elem in channels_list.fetchall()]
                for i in a:
                    stm = select([tracts_in_channel.c.tract_id]).where(tracts_in_channel.c.channel_id==i['id'])
                    tract_id = con.execute(stm).fetchall()
                    stm = select([channels.c.type]).where(channels.c.id==i['id'])
                    type = con.execute(stm).fetchall()
                    i['type_of_channel'] = type[0][0]
                    stm = select([tracts.c.hard_from, tracts.c.hard_to, tracts.c.type]).where(tracts.c.id==tract_id[0][0])
                    rs = con.execute(stm).fetchall()
                    i['hard_from'] = rs[0][0]
                    i['hard_to'] = rs[0][1]
                    i['type_of_connection'] = rs[0][2]
                return a
        except Exception as ex:
            logger.error(str(ex))

    def updateChannel(self, id, type, tasks):
        tracts_in_channel = Table('tracts_in_channel', self.meta, autoload=True)        
        tracts = Table('tracts', self.meta, autoload=True)
        channels = Table('channel', self.meta, autoload=True)
        task = Table('tasks', self.meta, autoload=True)
        task_channels = Table('task_channels', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = update(channels).where(channels.c.id==id).values(type=type)
                con.execute(stm)
                task_ids = []
                for i in tasks:
                    stm = insert(task).values(name=i)
                    con.execute(stm)
                    stm = select([task.c.id]).where(task.c.name==i)
                    task_id = con.execute(stm).fetchall()
                    task_ids.append(task_id[0][0])
                for i in task_ids:
                    stm = insert(task_channels).values(task_id=i, channel_id=id)
                    con.execute(stm)
                return {'status':'ok'}
        except Exception as ex:
            logger.error(str(ex))

    def getChannelState(self, id):
        channels = Table('channel', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([channels.c.state, channels.c.iniciator, channels.c.last_change_state]).where(channels.c.id==id)
                rs = con.execute(stm)
                return [dict(elem.items()) for elem in rs.fetchall()]
        except Exception as ex:
            logger.error(str(ex))

    def getChannelRoutes(self, id):
        tracts_in_channel = Table('tracts_in_channel', self.meta, autoload=True)
        reserve_tracts = Table('reserve_tracts', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([tracts_in_channel.c.tract_id]).where(tracts_in_channel.c.channel_id==id)
                rs = con.execute(stm).fetchall()
                reserve = []
                main = []
                for i in rs:
                    stm = select([reserve_tracts.c.tract_id_slave]).where(reserve_tracts.c.tract_id_slave==i[0])
                    res = con.execute(stm).fetchall()
                    if res != []:
                        reserve.append(i[0])
                    else:
                        main.append(i[0])
                a = {}
                a['0'] = main
                a['1'] = reserve
                return a
        except Exception as ex:
            logger.error(str(ex))

    def getTasks(self):
        channels = Table('tasks', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([channels.c.id, channels.c.name])
                rs = con.execute(stm)
                return rs.fetchall()
        except Exception as ex:
            logger.error(str(ex))
    def getHardwareNums(self, id):
        tracts_in_channel = Table('tracts_in_channel', self.meta, autoload=True)
        channels = Table('tasks', self.meta, autoload=True)
        tracts = Table('tracts', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([tracts_in_channel.c.tract_id]).where(tracts_in_channel.c.channel_id==id)
                rs = con.execute(stm)
                res = []
                for i in rs.fetchall():
                    stm = select([tracts.c.hard_from, tracts.c.hard_to]).where(tracts.c.id==i[0])
                    a = con.execute(stm).fetchall()
                    res.append(a[0][0])
                    res.append(a[0][1])
                return {'hardware':res}
        except Exception as ex:
            logger.error(str(ex))

    def channelCommand(self, id, activity):
        channels = Table('channel', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = update(channels).values(state=activity).where(channels.c.id==id)
                con.execute(stm)
                return {'status':'ok'}
        except Exception as ex:
            logger.error(str(ex))
            return {'status':str(ex)}
            
    def getTractState(self, id):
        tracts = Table('tracts', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([tracts.c.state, tracts.c.last_change_state]).where(tracts.c.id==id)
                res = con.execute(stm)
                a = [dict(elem.items()) for elem in res.fetchall()]
                a = a[0]
                a['reason'] = -1
                a['km'] = -1
                return a
        except Exception as ex:
            return {'status':str(ex)}
            logger.error(str(ex))
            print(ex)

    def getTractsInChannel(self, id):
        tracts_in_channel = Table('tracts_in_channel', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = select([tracts_in_channel.c.channel_id]).where(tracts_in_channel.c.tract_id==id)
                res = con.execute(stm).fetchall()
                a = []
                for i in res:
                    a.append(i[0])
                return {'channels':a}
        except Exception as ex:
            return {'status':str(ex)}
            logger.error(str(ex))
            print(ex)

    def getHardwareInTract(self, id):
        tracts = Table('tracts', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                res = []
                stm = select([tracts.c.hard_from, tracts.c.hard_to]).where(tracts.c.id==id)
                a = con.execute(stm).fetchall()
                res.append(a[0][0])
                res.append(a[0][1])
                return {'hardware':res}
        except Exception as ex:
            logger.error(str(ex))
            print(ex)

    def changeTract(self, id, new_id):
        tracts_in_channel = Table('tracts_in_channel', self.meta, autoload=True)
        try:
            with self.engine.connect() as con:
                stm = update(tracts_in_channel).where(tracts_in_channel.c.tract_id==id).values(tract_id=new_id)
                con.execute(stm)
            return {'status':"ok"}        
        except Exception as ex:
            logger.error(str(ex))
            print(ex)
            return {'status':str(ex)}

    def pairHardware(self):
        tracts = Table('tracts', self.meta, autoload=True)
        with self.engine.connect() as con:
            stm = select([tracts.c.hard_from.distinct()])
            hard_from = con.execute(stm)
            stm = select([tracts.c.hard_to.distinct()])
            hard_to = con.execute(stm)
            hard = []
            for i in hard_from.fetchall():
                hard.append(i[0])
            print(hard)
            for i in hard_to.fetchall():
                if i[0] not in hard:
                    hard.append(i[0])

    def checkActiveTaskStatus(self):
        channels = Table('channel', self.meta, autoload=True)
        task_channels = Table('task_channels', self.meta, autoload=True)
        with self.engine.connect() as con:
            stm = select([channels.c.id])
            ids = con.execute(stm).fetchall()
            for i in ids:
                stm = select([task_channels.c.id]).where(task_channels.c.channel_id==i[0])
                a = con.execute(stm).fetchall()  
                if len(a) < 1:
                    stm = update(channels).values(state=1).where(channels.c.id==i[0]) 
                    con.execute(stm)
        return {'status':'ok'}
        
if __name__ == '__main__':
    sql = SQLITE()

    # todo check аварии

    print(sql.get_tracts_for_report(1))
