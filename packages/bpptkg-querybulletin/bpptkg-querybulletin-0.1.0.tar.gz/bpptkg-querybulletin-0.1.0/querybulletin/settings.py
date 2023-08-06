import os
from .exceptions import ImproperlyConfigured

USER_HOME = os.path.expanduser('~')
BULLETIN_DIR = os.path.join(USER_HOME, '.bulletin')
CONFIG_DIR = os.path.join(BULLETIN_DIR, 'querybulletin')
if not os.path.isdir(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')
if not os.path.isfile(CONFIG_PATH):
    raise ImproperlyConfigured(
        'querybulletin config.json file is not found. Make sure you place it '
        'in the ~/.bulletin/querybulletin/ directory.')

DEFAULT_COLUMNS = [
    'eventid',
    'eventdate',
    'duration',
    'eventtype',
]

CSV_DELIMITER = '|'
