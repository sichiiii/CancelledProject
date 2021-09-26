import configparser, os

from logging.config import fileConfig
from typing import Dict, Optional

#from .exceptions import MissingConfiguration


class Configuration(configparser.RawConfigParser):

    def __init__(self) -> None:
        configparser.RawConfigParser.__init__(self, allow_no_value=True)
        self.path = None  # type: Optional[str]

    @property
    def include(self) -> str:
        return self.get('settings', 'include')

    def __load_section(self, conf: str) -> None:
        self.read(os.path.join(self.include, conf))

    def get_section(self, section: str) -> Dict[str, str]:
        if not self.has_section(section):
            raise MissingConfiguration(section)
        return dict(self[section])

    def load(self, path: str) -> None:
        self.path = path
        self.read(self.path)
        self.load_includes()

    def load_includes(self) -> None:
        try:
            include_dir = self.include
            for conf in filter(lambda p: p.endswith('.ini'), sorted(os.listdir(include_dir))):
                self.__load_section(conf)
        except (FileNotFoundError, configparser.NoOptionError):
            pass

