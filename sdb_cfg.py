import yaml

import sdb_log
from sdb_log import error
from sdb_log import warn
from sdb_log import info
from sdb_log import debug

# GLOBAL cfg (dict) : Contains the configuration variables

# (str) Config location
CFG_FILE = '/home/bot/discord/sdb_config.yml'

# Populate the 'cfg' variable using the config file
def read_cfg():
  debug("Reading config file")
  with open(CFG_FILE, 'r') as ymlfile:
    global cfg
    cfg = yaml.load(ymlfile)