import threading, app_logger

from time import sleep
from config import Configuration
from exceptions import PathNotFound
from ogm import OGM
from sql import SQLITE
from zabbix import ZABBIX
from multiprocessing import Process, Queue
from service_utils.graphs import Graph

config_path = './config.ini'

class Commutation:
    def __init__(self):
        self.logger = app_logger.get_logger(__name__)
        self.config = Configuration()
        self.config.load(config_path)
        self.sql = SQLITE()
        self.__type = self.config.get('start_params', 'type')
        self.radioSilence = self.config.get('start_params', 'radioSilence')
        self.ogm = OGM(self.config)
        self.zabbix = ZABBIX(self.config)
        threading.Thread(target=self.check_type, args=(), name='check radio').start()

    def create_all_graph(self):
        self.graph = Graph()
        tracts = self.sql.get_tracts()

        nodes = [item.get('hard_from') for item in tracts]
        nodes.extend([item.get('hard_to') for item in tracts])
        nodes = list(set(nodes))

        for node in nodes:
            self.graph.add_node(node)

        for i in tracts:
            self.graph.add_edge(i['hard_from'], i['hard_to'], 1)

        try:
            print(Graph.shortest_path(self.graph, tracts[256]['hard_to'], tracts[123]['hard_to']))
        except PathNotFound as ex:
            print(ex)

        print(1)

    def found_path(self, point1, point2):
        self.graph.shortest_path(self.graph, point1, point2)

    def get_config(self):
        return self.config

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    def check_type(self):
        while 1:
            sleep(10)
            trigers = self.get_active_triggers()
            for item, value in trigers.items():
                for trig in value:
                    temp = item + '/' + trig.get('description').split('/')[-1]
                    if int(trig['priority']) > 2:
                        self.sql.setTractWarning(temp, 5)
                        self.sql.addTractHistory(temp, 5)

                    else:
                        self.sql.setTractWarning(temp, 4)
                        self.sql.addTractHistory(temp, 4)
            self.create_all_graph()
            self.sql.checkActiveTaskStatus()

    def get_paths(self):
        pass

    def ogm_set_table(self, ip, table):
        return self.ogm.set_table(ip, table)

    def set_radio_silence(self, data):
        self.radioSilence = data

    def get_radio_silence(self):
        return self.radioSilence

    def get_active_triggers(self):
        data = self.zabbix.check_triggers()
        result = {}
        for i in data.get('result', []):
            result.setdefault(i.get('hosts', [])[0].get('host'), []).append({'description': i['description'],
                                                                             'priority': i['priority']})

        result.pop('Zabbix server')
        return result


    def set_ogm_repeat(self, state):
        ip = '127.0.0.1'
        plata = 1
        self.ogm.send_command(ip, plata, 'repeat', state)