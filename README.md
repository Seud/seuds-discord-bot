# seuds-discord-bot

A simple Discord bot.

## Requirements

* A Linux OS (Optimized for Debian/Ubuntu-like distributions)
* Install **discord.py** and **pyyaml** pip packages
* The python-bs4 package (Or pip equivalent) for BeautifulSoup

## Launching

The launch.sh file provides a service-like way to manage the bot, although main.py can be run directly.
The "-v" switch can help in debugging problems, while the "-q" switch will silence most output and is well suited to daemonization (For example within a cron)
The recommended way to run this bot is as a dedicated user. By default, the script will expect a write-able '/home/bot/discord' directory, but this can be changed in launch.sh and main.py