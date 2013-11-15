# -*- coding: utf-8 -*-

# system
from datetime import timedelta
import json
import pprint
import sys
# pipped
from jsonschema import validate
# local
from .celerycontroller import CeleryController
from .config import LOG, PYNG_DOTFILE, DOTFILE_SCHEMA, TIME_MULTIPLIERS


class PyngApp(object):
    """ The pyng application object, doing stuff casually. """

    def execute(self, argv):
        """ Launch the beauty beast. """
        # validate parameters

        command = None
        if len(argv) == 2:
            command = argv[1]
        ctl = CeleryController()
        if command == 'start':
            ctl.start()
        elif command == 'stop':
            ctl.stop()
        elif command == 'restart':
            ctl.restart()
        elif command == 'look':
            ctl.running_celerys()


class DotfileReader(object):
    """ Extracts information from the user-given dotfile. """

    def read_dotfile(self):
        pyng_tasks = {}
        try:
            with open(PYNG_DOTFILE, 'r') as dotfile:
                json_data = json.loads(dotfile.read())
                self.validate_dotfile(json_data)
                for json_pynger in json_data['pyng']:
                    tasks = self.read_pynger(json_pynger)
                    pyng_tasks.update(tasks)
                    LOG.debug("pynger data:\n" + pprint.pformat(json_pynger))
        except IOError:
            sys.exit("You need a config file: {}".format(self.dotfile))

        return(pyng_tasks)


    def read_pynger(self, pynger_dict):
        tasks = {}
        try:
            self.name = pynger_dict['name']
            for monitor in pynger_dict['monitors']:
                task_dict = self.create_task(monitor['url'], monitor['freq'], monitor['type'])
                tasks.update(task_dict)

            #for notifier in pynger_dict['notifiers']:
                #notif = NOTIFIERS_TYPE[notifier['type']]()
                #notif.address = notifier['address']
                #self.notifiers.append(notif)
        except KeyError:
            self.invalid_dotfile()

        return(tasks)


    def create_task(self, url, freq_in_strings, mtype):
        try:
            multiplier = TIME_MULTIPLIERS[freq_in_strings[-1]]
            freq_in_seconds = int(freq_in_strings[:-1]) * multiplier
        except:
            self.invalid_dotfile()

        task_dict = {
            url: {
                'task': 'pyng.tasks.monitor',
                'schedule': timedelta(seconds=freq_in_seconds),
                'args': [url, mtype],
            }
        }
        return(task_dict)


    def validate_dotfile(self, json_data):
        """ Validate the .pyng.json against official structure. """
        try:
            validate(json_data, DOTFILE_SCHEMA)
            LOG.debug("Config file is valid")
        except jsonschema.exceptions.ValidationError:
            self.invalid_dotfile()


    def invalid_dotfile(self):
        """ Warn the user about the dotfile and exits. """
        LOG.error("Invalid config file")
        sys.exit("ERROR: Your config file is not valid!")


class PyngLogger(object):
    logger = None

    def __init__(self, logfile):
        import logging
        from logging.handlers import RotatingFileHandler
        self.logger = logging.getLogger('pyng')
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler(logfile, 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(steam_handler)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, args, kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, args, kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, args, kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, args, kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, args, kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, args, kwargs)
