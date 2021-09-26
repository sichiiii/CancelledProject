import app_logger
import json
import requests


from zabbix_api import ZabbixAPI

class ZABBIX:
    s = requests.Session()

    def __init__(self, config):

        self.host = config.get('zabbix', 'host')
        self.login = config.get('zabbix', 'login')
        self.password = config.get('zabbix', 'password')
        self.logger = app_logger.get_logger(__name__)
        self.url = 'http://' + self.host + '/zabbix/api_jsonrpc.php'
        self.headers = {
            'Content-Type': 'application/json-rpc'
        }
        self.zapi = ZabbixAPI(server=self.url)
        self.zapi.login(self.login, self.password)
        self.auth()

    def auth(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.login,
                "password": self.password},
            "id": 1
        }
        req = self.s.post(self.url, data=json.dumps(data), headers=self.headers)
        if (req.status_code == 200):
            js = json.loads(req.text)
            self.auth_code = (js['result'])
        else:
            self.logger.error(req.text)

    def check_triggers(self):
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "extend",
                "active": True,
                "expandComment": True,
                "expandDescription": True,
                "selectHosts": 'extend'

            },
            "id": 2,
            "auth": self.auth_code
        }

        try:
            req = self.s.post(self.url, data=json.dumps(data), headers=self.headers)
            js = json.loads(req.text)

            return js

        except Exception as ex:
            self.logger.error(str(ex))

    def get_data_from_device(self):

        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": [
                        "A81"
                    ]
                },
                'selectTriggers':'extend'
            },
            "id": 2,
            "auth": self.auth_code
        }

        try:
            req = self.s.post(self.url, data=json.dumps(data), headers=self.headers)
            js = json.loads(req.text)

            return js

        except Exception as ex:
            self.logger.error(str(ex))

    def get_hardware(self):
        try:
            hardware = []
            hosts = self.zapi.host.get({"output": ["name", "host"]})
            print(hosts)
            data = {
            "jsonrpc": "2.0",
            "method": "hostinterface.get",
            "params": {
                "output": "extend",
                "hostids": "10084"
                },
                "id": 2,
                "auth": self.auth_code
            }

            req = self.s.post(self.url, data=json.dumps(data), headers=self.headers)
            for i in hosts:
                if i['name'][0:3] == 'ОМД' or i['name'][0:3] == 'ОГМ':
                    data = {
                        "jsonrpc": "2.0",
                        "method": "hostinterface.get",
                        "params": {
                            "selectInterfaces" : "extend",
                            "output": "extend",
                            "hostids": i['hostid']
                                  },
                        "id": 2,
                        "auth": self.auth_code
                    }
                    req = self.s.post(self.url, data=json.dumps(data), headers=self.headers)
                    r = json.loads(req.text)
                    buff = {"name":i['name'], "ip":r['result'][0]['ip'], "port":r['result'][0]['port']}
                    hardware.append(buff) 
                    print(buff)
            return hardware

        except Exception as ex:
            self.logger.error(str(ex))

if __name__ == '__main__':
    config_path = './config.ini'
    from config import Configuration

    config = Configuration()
    config.load(config_path)

    zab = ZABBIX(config)
    data = zab.check_triggers()

    result = {}
    for i in data.get('result', []):
        result.setdefault(i.get('hosts', [])[0].get('host'), []).append({'description': i['description'],
                                                                         'priority': i['priority']})
    print(result)
