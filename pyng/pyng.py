# -*- coding: utf-8 -*-

# system
import json
import sys
# pipped
from jsonschema import validate
# local
from .celerycontroller import CeleryController
from .config import LOG, PYNG_DOTFILE, DOTFILE_SCHEMA


class PyngApp(object):
    """ The pyng application object, doing stuff casually. """

    dotfile = PYNG_DOTFILE


    def check_args(self, argv):
        """ Check user-given arguments integrity and construct app context. """
        pass


    def run(self):
        """ Launch the beauty beast. """

        try:
            with open(self.dotfile, 'r') as dotfile:
                json_data = json.loads(dotfile.read())
                self.validate_dotfile(json_data)
                for pyng in json_data['pyng']:
                    pass
                #command = None
                #if len(argv) == 2:
                    #command = argv[1]
                #ctl = CeleryController()
                #if command == 'start':
                    #ctl.start()
                #elif command == 'stop':
                    #ctl.stop()
                #elif command == 'restart':
                    #ctl.restart()
                #elif command == 'look':
                    #ctl.running_celerys()

        except IOError:
            sys.exit("You need a config file: {}".format(self.dotfile))


    def validate_dotfile(self, json_data):
        """ Validate the .pyng.json against official structure. """
        try:
            validate(json_data, DOTFILE_SCHEMA)
            LOG.debug("Config file is valid")
        except jsonschema.exceptions.ValidationError:
            LOG.error("Invalid config file")
            sys.exit("ERROR: Your config file is not valid!")

