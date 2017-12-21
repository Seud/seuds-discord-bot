import os
import sys
import signal
import discord

from sdb_log import error
from sdb_log import warn
from sdb_log import info
from sdb_log import debug

class Bot:
  
  client = ''
  
  def __init__(self):
    self.token = os.getenv('BOT_TOKEN')
    self.client = discord.Client()
    signal.signal(signal.SIGINT, self.disconnect)
    signal.signal(signal.SIGTERM, self.disconnect)
  
  def disconnect(self, signum, frame):
    self.client.close()
    self.client.logout()
    sys.exit(0)
  
  def run(self):
    self.client = discord.Client()
    self.client.run(self.token)