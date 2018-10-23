# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
#!/usr/bin/python
from . import server
from . import logger
import os
from trytond.config import config
config.update_etc(os.environ.get('TRYTOND_CONFIG'))

PORT = config.getint('fedicom', 'port', default=1234)

logger.init_logger()
log = logger.Logger()
log.notifyChannel("service.py", logger.LOG_INFO,
    'Inicialitzant el Servidor de Comandes')

server = server.ServerThread('0.0.0.0', PORT)
server.start()
