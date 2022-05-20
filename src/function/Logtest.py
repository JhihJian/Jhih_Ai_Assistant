import logging

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# filemode='w', 更早的消息消失
logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('simpleExample')
logger.addHandler(ch)
logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
