import logging

LEVEL = logging.INFO

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger