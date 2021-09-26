import requests, logging
import app_logger

class OGM:
    def __init__(self, config):

        self.logger = app_logger.get_logger(__name__)
        self.host = config.get('ogm', 'host')
        self.urlForPlata = '127.0.0.1'
        self.urlForDevice = 'test'
        self.urlForCommand = '<URL>'
        self.urlForCom = '<URL>'
        self.urlForByteCommand = '<URL>'
        self.urlForSetTable = '<URL>'
        self.urlForGetTable = '<URL>'
        self.setRepeat = '<URL>'

    def responseFromPlata(self, ip, plata):
        try:
            response = requests.post(self.urlForPlata, data={'ip': ip, 'plata': plata})
            return response
        except requests.Timeout as ex:
            self.logger.error(str(ex))
        except requests.HTTPError as ex:
            if response.status_code == 403:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 404:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 500:
                self.logger.error(str(ex))
                raise
            else:
                self.logger.error(str(ex))
                raise

    def responseFromDevice(self, ip):
        try:
            response = requests.post(self.urlForDevice, data={'ip': ip})
            return response
        except requests.Timeout as ex:
            self.logger.error(str(ex))
        except requests.HTTPError as ex:
            if response.status_code == 403:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 404:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 500:
                self.logger.error(str(ex))
                raise
            else:
                self.logger.error(str(ex))
                raise

    def send_byte_command(self, ip, command):
        try:
            response = requests.post(self.urlForCommand, data={'ip': ip, 'command': command})
            return response
        except requests.Timeout as ex:
            self.logger.error(str(ex))
        except requests.HTTPError as ex:
            if response.status_code == 403:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 404:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 500:
                self.logger.error(str(ex))
                raise
            else:
                self.logger.error(str(ex))
                raise

    def send_command(self, ip, plata, command, value):
        try:
            response = requests.post(self.urlForCommand,
                                     data={'ip': ip, 'plata': plata, 'command': command, 'value': value})
            return response
        except requests.Timeout as ex:
            self.logger.error({"message": ex.message})
        except requests.HTTPError as ex:
            if response.status_code == 403:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 404:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 500:
                self.logger.error(str(ex))
                raise
            else:
                self.logger.error(str(ex))
                raise

    def changeCom(self, ip, fromToList):
        try:
            response = requests.post(self.urlForCom, data={'ip': ip, 'list': fromToList})
            return response
        except requests.Timeout as ex:
            self.logger.error({"message": ex.message})
        except requests.HTTPError as ex:
            if response.status_code == 403:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 404:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 500:
                self.logger.error(str(ex))
                raise
            else:
                self.logger.error(str(ex))
                raise


    def commutation_table(self, ip, plata):
        try:
            response = requests.post(self.urlForCom, data={'ip': ip, 'plata': plata})
            return response
        except Exception as ex:
            self.logger.error(str(ex))

    def set_table(self, ip, table):
        try:
            response = requests.post(self.urlForSetTable, data = {'ip':ip, 'table':table})
            return response
        except requests.Timeout as ex:
            self.logger.error(str(ex))
        except requests.HTTPError as ex:
            if response.status_code == 403:
                self.logger.error(str(ex))
                raise
            elif response.status_code == 404:
                self.logger.error(str(ex)) 
                raise
            elif response.status_code == 500:
                self.logger.error(str(ex))
                raise               
            else:
                self.logger.error(str(ex))
                raise

    def set_plume(self, name, port, direction, activity):
        try:
            response = requests.post(self.setRepeat, data = {'name':name, 'port':port, 'direction':direction, 'activity':activity})
            return response
        except Exception as ex:
            self.logger.error(str(ex))