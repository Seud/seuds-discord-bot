import sys
import logging

# Talking much ?
VERBOSE = False

# Or not ?
QUIET = False

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