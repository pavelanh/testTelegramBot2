import logging

import colorlog


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    log_format = '%(asctime)s - %(levelname)-8s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    c_format = '%(log_color)s' + log_format
    f = colorlog.ColoredFormatter(c_format, date_format,
                                  log_colors={'INFO': 'fg_green', 'DEBUG': 'white',
                                              'WARNING': 'bold_yellow', 'ERROR': 'bold_red',
                                              'CRITICAL': 'bold_red'})
    ch = logging.StreamHandler()
    ch.setFormatter(f)
    root.addHandler(ch)
