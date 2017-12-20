#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import sys
import os
import re
import traceback
import logging
import argparse

from bot import Bot

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

# -----

# Talking much ?
VERBOSE = False

# Or not ?
QUIET = False

# -----



# --- BASIC FUNCTIONS ---

# Stop the program on error and log it

# Crashes the program, always shown
def error(err_str):
  logging.error(err_str)
  print("ERROR : %s" % err_str)
  sys.exit(1)

# Always shown, use for potential problems
def warn(warn_str):
  logging.warning(warn_str)
  print("Warning : %s" % warn_str)

# Not shown with -q
def info(info_str):
  logging.info(info_str)
  if not QUIET:
    print(info_str)

# Only shown with -v
def debug(debug_str):
  if VERBOSE:
    logging.debug(debug_str)
    print(debug_str)

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
    global VERBOSE
    VERBOSE = True
    debug("-v option activated")
    
  if args.quiet:
    global QUIET
    QUIET = True
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
    if CLEAN_ME:
      info("Script starting...")
    else:
      error("Error during name cleaning, check that the script ends up with .py")
    
    # Main script logic
    main_script()
    
    # Yay, script over !
    info('Script finished !')
    
  except Exception as e:
    # Log exception and signal Zabbix something's wrong
    error("An uncaught exception occured\n%s" % ''.join(traceback.format_exception(e.__class__, e, sys.exc_info()[2])))

# --- LOGIC FUNCTIONS ---

# Main script function
def main_script():
  bot = Bot()
  bot.run()

if __name__ == "__main__":
  main()
