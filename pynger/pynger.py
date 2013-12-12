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
from .config import LOG, PYNGER_DOTFILE, DOTFILE_SCHEMA, TIME_MULTIPLIERS


class PyngerApp(object):
    """ The Pynger application object, doing stuff casually. """

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

    pynger_data = None

    def __init__(self):
        try:
            with open(PYNGER_DOTFILE, 'r') as dotfile:
                json_data = json.loads(dotfile.read())
                self.validate_dotfile(json_data)
                self.pynger_data = json_data['pynger']
        except IOError:
            sys.exit("You need a config file: {}".format(self.dotfile))


    def extract_notifiers(self, name):
        notifiers = []
        for json_pynger in self.pynger_data:
            if json_pynger['name'] == name:
                for notifier in json_pynger['notifiers']:
                    notifiers.append(notifier)
        return(notifiers)


    def extract_tasks(self):
        pynger_tasks = {}
        for json_pynger in self.pynger_data:
            tasks = self.read_monitors(json_pynger)
            pynger_tasks.update(tasks)
        return(pynger_tasks)


    def read_monitors(self, pynger_dict):
        tasks = {}
        try:
            for monitor in pynger_dict['monitors']:
                task_dict = self.create_monitor_task(monitor, pynger_dict['name'])
                tasks.update(task_dict)

        except KeyError:
            self.invalid_dotfile()

        return(tasks)


    def create_monitor_task(self, monitor, name):
        try:
            multiplier = TIME_MULTIPLIERS[monitor['freq'][-1]]
            freq_in_seconds = int(monitor['freq'][:-1]) * multiplier
        except:
            self.invalid_dotfile()

        task_dict = {
            monitor['url']: {
                'task': 'pynger.tasks.monitor',
                'schedule': timedelta(seconds=freq_in_seconds),
                'args': [name, monitor['url'], monitor['type']],
            }
        }
        return(task_dict)


    def validate_dotfile(self, json_data):
        """ Validate the .pynger.json against official structure. """
        try:
            validate(json_data, DOTFILE_SCHEMA)
            LOG.debug("Config file is valid")
        except jsonschema.exceptions.ValidationError:
            self.invalid_dotfile()


    def invalid_dotfile(self):
        """ Warn the user about the dotfile and exits. """
        LOG.error("Invalid config file")
        sys.exit("ERROR: Your config file is not valid!")
