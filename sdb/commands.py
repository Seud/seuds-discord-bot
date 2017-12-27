import discord
import sdb_cfg
import sdb_log
from sdb_log import error
from sdb_log import warn
from sdb_log import info
from sdb_log import debug

from sdb.phrases import get_phrase

# List of available commands and aliases, populated later
#f is the function to cast, u is usage syntax, d is the description and a says if it is an alias (Doesn't show up on help screen)
COMMANDS = {}
ALIASES = {}

# Populate commands
def populate_commands():
  global COMMANDS
  global ALIASES
  
  # Invalid command
  ALIASES['NONE'] = {'f':cinvalid, 'u':'', 'd':''}
  # Help command
  COMMANDS['help'] = {'f':chelp, 'u':'{c}', 'd':'Displays this message'}
  ALIASES['?'] = COMMANDS['help']
  
  # Credits command
  COMMANDS['credits'] = {'f':ccredits, 'u':'{c}', 'd':'See who made this bot !'}
  # Phrase command
  COMMANDS['phrase'] = {'f':cphrase, 'u':'{c}', 'd':'Generate a random phrase'}
  ALIASES['phrases'] = COMMANDS['phrase']
  # Stats command
  #ALIASES['stats'] = {'f':cstats, 'u':'{c} <command> or {c} help', 'd':'(WIP) Get the server stats'}
  #ALIASES['stat'] = ALIASES['stats']
  
  # Use aliases for parsing, commands for help
  ALIASES.update(COMMANDS)

# Custom exception for invalid command usage
class InvalidCommand(Exception):
  pass

# Struct for command data and util functions
class CommandData:
  
  # (discord.Client) Client instance
  client = ''
  # (str[]) Clean command arguments
  args = []
  # (discord.Channel) Channel to respond to
  channel = ''
  # (discord.Message) Original message
  message = ''
  
  # Create the data object
  def __init__(self, client, args, channel, message):
    self.client = client
    self.args = args
    self.channel = channel
    self.message = message
  
  # Say something using an Embed
  # ARG text (str) : The text to say
  # KWARGS : Args to pass to the Embed constructor
  async def say(self, text, **kwargs):
    em = discord.Embed(type='rich', description=text, **kwargs)
    await self.client.send_message(self.channel, embed=em)
  
  # Send typing option - useful for longer commands
  async def send_typing(self):
    await self.client.send_typing(self.channel)

# Metadata about a command
class Command:
  
  # (str) The name of the command
  name = ''
  # (function) The function to execute. Prototype : f(CommandData)
  function = ''
  # (str) Usage of the function
  usage = ''
  # (str) Short description of the function
  description = ''
  # (CommandData) Data for the command
  data = ''
  
  # Create the Command
  def __init__(self, name, usage, description, function, data):
    self.name = name
    self.function = function
    self.usage = usage
    self.description = description
    self.data = data
  
  # Get a formatted line about the command (Static)
  # ARG name (string) : The name of the command
  # ARG usage (string) : The syntax of the command
  # ARG name (string) : The name of the command
  # RET (string) The formatted string
  @staticmethod
  def sinfo(name, usage, description):
    return "**{usage}** : {desc}\n".format(name=name, usage=usage, desc=description)
  
  # Get a formatted line about the command
  # RET (string) The formatted string
  def info(self):
    return Command.sinfo(self.name, self.usage, self.decription)
  
  # Execute the command
  async def execute(self):
    try:
      await self.function(self.data)
      info("Command executed successfully !")
    except InvalidCommand:
      await self.data.say("Incorrect use of the command ! Usage : {p} {u}".format(p=sdb_cfg.cfg['bot.command'], u=self.usage), color=discord.Color.red())
    except Exception as e:
      await self.data.say("An error occured while processing the command.", color=discord.Color.red())
      raise
    return

# Execute a command
# ARG client (discord.Client) : The client instance
# ARG command_name (str) : The command name
# ARG args (str[]) : The additional args, if any
# ARG channel (discord.Channel) : The channel to respond to
# ARG message (discord.Message) : The full original message
async def command(client, command_name, args, channel, message):
  
  # Prepare objects
  data = CommandData(client, args, channel, message)
  populate_commands()
  
  # Find the requested command
  cdict = ALIASES.get(command_name)
  
  # Invalid (unknown) command check
  if cdict == None:
    info("Command not recognized !")
    cdict = ALIASES['NONE']
  
  command = Command(command_name, cdict['u'].format(c=command_name), cdict['d'], cdict['f'], data)
  await command.execute()

# *** Command functions ***
# All of these functions must take a CommandData as argument

# Triggers whenever an invalid command is detected
async def cinvalid(data):
  await data.say("Invalid command specified ! Use {p} help to get the list of commands".format(p=sdb_cfg.cfg['bot.command']), color=discord.Color.red())
  return

# Gives the list of functions of the bot
async def chelp(data):
  block = "Here is the list of available commands :\n\n"
  
  for key in COMMANDS:
    block += Command.sinfo(key, COMMANDS[key]['u'].format(c=key), COMMANDS[key]['d'])
  
  # Sending results
  await data.say(block, color=discord.Color.green())
  return

# Give credit where credit is due
async def ccredits(data):
  author_id = sdb_cfg.cfg['credits.author_id']
  phrases_url = sdb_cfg.cfg['phrases.url']
  github = sdb_cfg.cfg['credits.github']
  
  credits = '''
Bot made by <@{author_id}>

Random phrases generated from {phrases_url}

Bot Github : {github}
'''
  
  await data.say(credits.format(author_id=author_id, phrases_url=phrases_url, github=github), color=discord.Color.blue())
  
  return

# Generates a phrase !
async def cphrase(data):
  # Retrieve a phrase from the generator
  await data.send_typing()
  phrase = get_phrase()
  
  # Say the phrase !
  await data.say(phrase, color=discord.Color.green())
  return