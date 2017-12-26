import sys
import logging

# (bool) Talking much ?
VERBOSE = False

# (bool) Or not ?
QUIET = False

# Crashes the program, always shown
# ARG err_str (str) : The string to show
def error(err_str):
  logging.error(err_str)
  print("ERROR : %s" % err_str)
  sys.exit(1)

# Always shown, use for potential problems
# ARG warn_str (str) : The string to show
def warn(warn_str):
  logging.warning(warn_str)
  print("Warning : %s" % warn_str)

# Not shown with -q
# ARG info_str (str) : The string to show
def info(info_str):
  logging.info(info_str)
  if not QUIET:
    print(info_str)

# Only shown with -v
# ARG debug_str (str) : The string to show
def debug(debug_str):
  if VERBOSE:
    logging.debug(debug_str)
    print(debug_str)