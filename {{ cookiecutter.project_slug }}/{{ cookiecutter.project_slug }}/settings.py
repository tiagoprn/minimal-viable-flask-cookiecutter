import logging
import logging.config

from decouple import config

from {{ cookiecutter.project_slug }}.commons import get_app_version

IS_DEV_APP = config('IS_DEV_APP', cast=bool)  # Queues

# Logging configuration
LOG_LEVEL = config('LOG_LEVEL', default='INFO', cast=str)
LOG_VARS = config('LOG_VARS', cast=str).replace("'", '').replace('"', '')
JSON_LOGS = config('JSON_LOGS', default=False, cast=bool)
if JSON_LOGS:
    log_format = ' '.join(
        ['%({0:s})'.format(variable) for variable in LOG_VARS.split()]
    )
else:
    log_format = ''
    for index, variable in enumerate(LOG_VARS.split()):
        if variable != 'asctime':
            log_format += ' '
        log_format += f'%({variable})s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': LOG_LEVEL, 'handlers': ['console']},
    'formatters': {
        'default': {'format': log_format, 'datefmt': '%Y%m%d.%H%M%S'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
            'formatter': 'default',
        }
    },
    'loggers': {
        # default for all undefined Python modules
        '': {'level': 'WARNING', 'handlers': ['console']},
        'rose': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'celery': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': True,
        },
    },
}
if JSON_LOGS:
    LOGGING['formatters']['default'][
        'class'
    ] = 'pythonjsonlogger.jsonlogger.JsonFormatter'

logging.config.dictConfig(LOGGING)

VERSION = get_app_version()

SWAGGER_TEMPLATE = {
    'swagger': '2.0',
    'info': {
        'title': '{{ cookiecutter.project_slug }}',
        'description': '{{ cookiecutter.description }}',
        'contact': {
            'responsibleOrganization': 'tiagopr.nl',
            'responsibleDeveloper': 'Tiago',
            'email': 'tiago@tiagoprnl.me',
            'url': 'https://tiagopr.nl',
        },
        'version': VERSION,
    },
    'schemes': ['http', 'https'],
}
