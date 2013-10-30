# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

import logging
import os
import config
import sys


class Logger(object):
    def notifyChannel(self, name, level, msg):
        log = logging.getLogger(name)
        getattr(log, level)(msg)

LOG_DEBUG = 'debug'
LOG_INFO = 'info'
LOG_WARNING = 'warn'
LOG_ERROR = 'error'
LOG_CRITICAL = 'critical'


def init_logger():
    if True:
        logf = config.LOG
        # test if the directories exist, else create them
        try:
            if not os.path.exists(os.path.dirname(logf)):
                os.makedirs(os.path.dirname(logf))
            try:
                fd = open(logf, 'a')
                handler = logging.StreamHandler(fd)
            except IOError:
                sys.stderr.write("ERROR: couldn't open the logfile\n")
                handler = logging.StreamHandler(sys.stdout)
        except OSError:
            sys.stderr.write("ERROR: couldn't create the logfile directory\n")
            handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.StreamHandler(sys.stdout)

    # create a format for log messages and dates
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s: '
        '%(message)s', '%a, %d %b %Y %H:%M:%S')

    # tell the handler to use this format
    handler.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
