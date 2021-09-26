import app_logger
import json
import requests

class ServerManangment():
    def __init__(self, config):
        self.ip = config.get('kaus', 'ip')
        self.s = requests.Session()
        self.logger = app_logger.get_logger(__name__)

    def tableChannelCorrection(channel_id, activity):  #1
        try:
            data = {"channel_id":channel_id, "activity":activity}
            req = self.s.post(self.ip+'/tableChannelCorrection', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))

    def tableTractCorrection(tract_id, activity):   #2
        try:
            data = {"tract_id":tract_id, "activity":activity}
            req = self.s.post(self.ip+'/tableTractCorrection', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))

    def changeResult(status):    #3    #что за карта
        try:
            data = {"status":status}
            req = self.s.post(self.ip+'/change_result', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))

    def changeChannelState(channel_id):    #4
        try:
            data = {"channel_id":channel_id}
            req = self.s.post(self.ip+'/change_channel_state', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))

    def changeTractState(tract_id):    #5
        try:
            data = {"tract_id":tract_id}
            req = self.s.post(self.ip+'/change_tract_state', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))

    def changeConnectionState(con_id):    #6
        try:
            data = {"con_id":con_id}
            req = self.s.post(self.ip+'/change_connection_state', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))

    def localConnectionRequest(connection_nums):    #7
        try:
            data = {"connection_nums":connection_nums}
            req = self.s.post(self.ip+'/local_connection_request', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))

    def deletionConfirm(con_id):    #8
        try:
            data = {"con_id":con_id}
            req = self.s.post(self.ip+'/deletion_confirm', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))

    def notifConDeletion(con_id):    #9
        try:
            data = {"con_id":con_id}
            req = self.s.post(self.ip+'/notif_con_deletion', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))

    def requestRecoveryWays(con_id):    #10
        try:
            data = {"con_id":con_id}
            req = self.s.post(self.ip+'/con_id', data=json.dumps(data))
        except Exception as ex:
            self.logger.error(str(ex))