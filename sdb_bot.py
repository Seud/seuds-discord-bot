import os
import discord

import sdb_cfg
import sdb_log
from sdb_log import error
from sdb_log import warn
from sdb_log import info
from sdb_log import debug

import sdb.commands

# Wrapper class for the bot
class SDBot:
  
  # (discord.Client) Client instance
  client = ''
  
  # Initiate the bot
  def __init__(self):
    debug("Initiating the bot")
    
    # Prepare the token
    self.token = os.getenv('BOT_TOKEN')
    
    # Create the client and add events
    client = discord.Client()
    
    client.event(self.on_ready)
    client.event(self.on_message)
    
    self.client = client
    
  # Start the bot
  async def run(self):
    debug("Starting the bot")
    await self.client.start(self.token)
  
  # Logout the bot
  async def logout(self):
    await self.client.logout()
  
  # ----- EVENTS -----
  
  # Fires when the bot is ready
  async def on_ready(self):
    info("Bot ready !")
  
  # Fires when the bot reads a new message
  # ARG Message (Discord.Message) : The received message
  async def on_message(self, message):
    debug("Message caught...")
    
    # Do not parse self
    if message.author == self.client.user:
      debug("Self message, ignoring")
      return
    
    # Do not parse other bots messages
    if message.author.bot:
      debug("Bot message, ignoring")
      return
    
    mtext = message.content.strip()
    
    # Checks if the message starts with the command
    prefix = sdb_cfg.cfg['bot.command']
    if not mtext.lower().startswith(prefix.lower()):
      debug("Not a command, ignoring")
      return
    
    orig_channel = message.channel
    full_command = mtext.lower().split()
    # Pop the prefix
    full_command.pop(0)
    
    # Checks that a command exists
    if len(full_command) > 0:
      command = full_command.pop(0)
    else:
      command = ''
    
    # Execute the command !
    info("Received command : {0} with args {1}".format(command, full_command))
    await sdb.commands.command(self.client, command, full_command, orig_channel, message)
