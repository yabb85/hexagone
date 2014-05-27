#!/usr/bin/python
# -*-coding:Utf-8 -*
"""
Configuration manager module
"""

from ConfigParser import SafeConfigParser
import sfml as sf


class ConfigManager(object):

    class InternConfigManager(object):
        def __init__(self):
            """docstring for __init__"""
            self.parser = SafeConfigParser()

        def load(self, path):
            """docstring for load"""
            self.parser.read(path)

        def get(self, section, option):
            """get an option value for the named section"""
            return self.parser.get(section, option)

    __instance = None

    def __init__(self):
        """docstring for __ini__"""
        if ConfigManager.__instance is None:
            ConfigManager.__instance = ConfigManager.InternConfigManager()

    def load_config(self, path):
        """docstring for laod_config"""
        self.__instance.load(path)

    def get(self, section, option):
        """Get an option value for the named section"""
        return self.__instance.get(section, option)

    def get_color(self, name):
        """Get an color object for the named color"""
        val = self.__instance.get('color', name)
        val = val.split(',')
        return sf.Color(int(val[0]), int(val[1]), int(val[2]), int(val[3]))
