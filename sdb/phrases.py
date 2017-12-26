import requests
from bs4 import BeautifulSoup # Requires python-bs4

import sdb_cfg
import sdb_log
from sdb_log import error
from sdb_log import warn
from sdb_log import info
from sdb_log import debug

# Retrieves a random phrase from the generator
# RET str : The random phrase
def get_phrase():
  # Preparing POST URL and data
  phrases_url = sdb_cfg.cfg['phrases.url']
  phrases_data = {
    "nb": 1,
    "sok": "Lancer+!"
    }
  
  # Executing the request
  debug("Retrieving a phrase")
  r = requests.post(phrases_url, data=phrases_data)
  
  # Checking return code
  if not (r.status_code == requests.codes.ok):
    r.raise_for_status()
  
  # Extracting phrase
  soup = BeautifulSoup(r.text, 'html.parser')
  div = soup.find('div', class_='main')
  phrase = div.p.text.strip()
  debug("Found phrase : %s" % phrase)
  return phrase