from __future__ import annotations
import logging, logging.config, os, atexit
from .format import YELLOW, RED, BOLD_RED


class CountHandler(logging.Handler):
    level_fmts = {
        'WARNING':  YELLOW,
        'ERROR':    RED,
        'CRITICAL': BOLD_RED,
    }

    def __init__(self, level=logging.WARNING):
        self.counts: dict[int, int] = {}
        atexit.register(self.print_counts)
        super().__init__(level=level)

    def print_counts(self):
        msg = ""

        levelnos = sorted(self.counts.keys(), reverse=True)
        for levelno in levelnos:
            levelname = logging.getLevelName(levelno)
            colorfmt = self.level_fmts.get(levelname, '%s')
            msg += (", " if msg else "") + colorfmt % levelname + ": %d" % self.counts[levelno]

        if msg:
            print("Logged " + msg)

    def emit(self, record: logging.LogRecord):
        if record.levelno >= self.level:
            if not record.levelno in self.counts:
                self.counts[record.levelno] = 1
            else:
                self.counts[record.levelno] += 1


def get_logging_dictconfig(level: int|str = None, default_level: int|str = None, nocount: bool = False, config: dict = None):
    if config:
        config = {key: value for key, value in config.items()}
    else:
        config = {}

    if not 'version' in config:
        config['version'] = 1

    if not 'disable_existing_loggers' in config:
        config['disable_existing_loggers'] = False

    # ---------- Formatters ----------
    
    if not 'formatters' in config:
        config['formatters'] = {}

    if not 'color' in config['formatters']:
        config['formatters']['color'] = {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)-8s%(reset)s %(cyan)s[%(name)s]%(reset)s %(log_color)s%(message)s%(reset)s',
            'log_colors': {
                'DEBUG':    'fg_light_black',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',
            },
        }

    # ---------- Handlers ----------

    if not 'handlers' in config:
        config['handlers'] = {}

    if not 'console' in config['handlers']:
        config['handlers']['console'] = {
            'class': 'colorlog.StreamHandler',
            'formatter': 'color',
        }

    if not nocount and not 'count' in config['handlers']:
        config['handlers']['count'] = {
            'class': 'zut.logging.CountHandler',
            'level': 'WARNING',
        }

    # ---------- Root logger ----------

    if not 'root' in config:
        config['root'] = {}

    if not 'handlers' in config['root']:
        config['root']['handlers'] = ['console']
        if not nocount:
            config['root']['handlers'].append('count')

    if level is not None or not 'level' in config['root']:
        if level is None:
            level = os.environ.get('LOG_LEVEL', '').upper()
            if not level:
                level = default_level if default_level else 'INFO'
        
        if isinstance(level, int):
            level = logging.getLevelName(level)

        config['root']['level'] = level

    # ---------- Specific loggers ----------

    if not 'loggers' in config:
        config['loggers'] = {}

    if not 'django' in config['loggers']:
        config['loggers']['django'] = {
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO').upper(),
            'propagate': False,
        }

    return config


def configure_logging(level: int|str = None, default_level: int|str = None, nocount: bool = False, config: dict = None):
    config = get_logging_dictconfig(level=level, default_level=default_level, nocount=nocount, config=config)
    logging.config.dictConfig(config)
