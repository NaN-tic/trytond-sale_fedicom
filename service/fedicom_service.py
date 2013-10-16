#!/usr/bin/python

import server
import logger

logger.init_logger()

log = logger.Logger()

log.notifyChannel("service.py", logger.LOG_INFO, 'Inicialitzant el Servidor de Comandes')

server =  server.ServerThread('0.0.0.0',60000)
server.start()
