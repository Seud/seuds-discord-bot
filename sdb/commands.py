import sdb_cfg
import sdb_log
from sdb_log import error
from sdb_log import warn
from sdb_log import info
from sdb_log import debug

# Execute a command
# ARG client (discord.Client) : The client instance
# ARG command (str) : The command
# ARG args (str[]) : The additional args, if any
# ARG message (discord.Message) : The full original message
async def command(client, command, args, message):
  
  # TODO
  # List of commands and associated functions
  #commands = {
  #  'help': chelp,
  #  'phrase': cphrase
  #  'phrases': cphrases
  #  }
  
  #cfunction = commands.get(command)
  
  #if cfunction == None:
    
  #else:
  #  (client, args, message)
  return