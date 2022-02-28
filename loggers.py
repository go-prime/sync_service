from cmath import log
import os
import sys
import logging
from logging import handlers

log_file = os.path.join(os.getcwd(), "service.log")
if len(sys.argv) > 1:
    path = os.path.dirname(sys.argv[1])
    log_file = os.path.join(path, "service.log")

logger = logging.getLogger('service')
logger.setLevel(logging.DEBUG)

log_format = logging.Formatter("%(asctime)s [%(levelname)-5.5s ] %(message)s")
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)

file_handler = handlers.RotatingFileHandler(log_file, maxBytes=10000000, backupCount=10)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)
logger.addHandler(console_handler)