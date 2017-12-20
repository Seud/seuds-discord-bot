import os
import discord

class Bot:
  def __init__(self):
    self.token = os.getenv('BOT_TOKEN')
  
  def run(self):
    client = discord.Client()
    client.run(self.token)