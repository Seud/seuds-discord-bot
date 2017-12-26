#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import sys
import os
import re
import traceback
import logging
import argparse
import signal
import asyncio

import sdb_cfg
import sdb_log
from sdb_log import error
from sdb_log import warn
from sdb_log import info
from sdb_log import debug
from sdb_bot import SDBot

# Name of this script
ME = os.path.basename(__file__)

# Cleaned name of the script
CLEAN_ME = re.sub('.py', '', ME)

# Log level
LOG_LEVEL = 'DEBUG'

# Log directory
LOG_DIR = '/home/bot/discord/log/'

# Run directory
RUN_DIR = '/home/bot/discord/'

# --- GENERIC FUNCTIONS ---

# Initializes logging
def init_logging():
  # Preparing logging files
  if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
  logfile = '%s%s%s' % (LOG_DIR, CLEAN_ME, '.log')
  log_level = 20
  try:
    exec("log_level=logging.%s" % LOG_LEVEL)
    logging.basicConfig(filename=logfile, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='[%m/%d/%Y %H:%M:%S]', level=log_level)
  except AttributeError:
    print("Log level configuration is false")
    sys.exit(1)

# Parses arguments
def parse_args():
  debug("Parsing arguments")
  parser = argparse.ArgumentParser()
  
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-v", "--verbose", help='Prints and logs debug info', action="store_true")
  group.add_argument("-q", "--quiet", help='Only display warning and errors', action="store_true")
  
  args = parser.parse_args()
  
  if args.verbose:
    sdb_log.VERBOSE = True
    debug("-v option activated")
    
  if args.quiet:
    sdb_log.QUIET = True
    debug("-q option activated")

# True main function, executes init and end script tasks and wraps exceptions
def main():
  
  # Generic init tasks
  init_logging()
  if not os.path.exists(RUN_DIR):
    os.makedirs(RUN_DIR)

  try:
    # Parse arguments
    parse_args()
    
    # Name checking
    if not CLEAN_ME:
      error("Error during name cleaning, check that the script ends up with .py")
    
    # Main script logic
    main_script()
    
  except Exception as e:
    # Log exception and signal Zabbix something's wrong
    error("An uncaught exception occured\n%s" % ''.join(traceback.format_exception(e.__class__, e, sys.exc_info()[2])))

# --- LOGIC FUNCTIONS ---

def disconnect(signum, frame):
  raise KeyboardInterrupt

# Main script function
def main_script():
  
  # Read config
  sdb_cfg.read_cfg()
  
  # Register signals
  signal.signal(signal.SIGINT, disconnect)
  signal.signal(signal.SIGTERM, disconnect)
  
  # Loop is manually managed
  bot = SDBot()
  loop = asyncio.get_event_loop()
  
  try:
    loop.run_until_complete(bot.run())
  except KeyboardInterrupt:
    info("Received Interrupt, exiting")
    loop.run_until_complete(bot.logout())
  except Exception as e:
    error("An uncaught exception occured\n%s" % ''.join(traceback.format_exception(e.__class__, e, sys.exc_info()[2])))
    loop.run_until_complete(bot.logout())
  finally:
    loop.close()
  
  sys.exit(0)

if __name__ == "__main__":
  main()
