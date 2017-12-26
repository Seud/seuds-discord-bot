import os
import sys
import signal
import asyncio
from asyncio import wait
import discord

import sdb_log
from sdb_log import error
from sdb_log import warn
from sdb_log import info
from sdb_log import debug

class Bot:
  
  client = ''
  
  def __init__(self):
    self.token = os.getenv('BOT_TOKEN')
    self.client = discord.Client()
  
  async def run(self):
    self.client = discord.Client()
    await self.client.start(self.token)
  
  async def logout(self):
    await self.client.logout()