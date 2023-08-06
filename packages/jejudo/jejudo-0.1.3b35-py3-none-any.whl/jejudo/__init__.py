import logging
from ._version import __version__
from .core.jejudo import Jejudo
from os.path import isfile, isdir
from os import makedirs, listdir
from pickle import load, dump
import os
import json


logging.basicConfig(level=logging.INFO, format='[%(levelname)s | %(asctime)s] %(message)s', datefmt ='%Y-%m-%d %I:%M:%S')
logging.basicConfig(level=logging.ERROR, format='[%(levelname)s | %(asctime)s] %(message)s', datefmt ='%Y-%m-%d %I:%M:%S') # DEBUG/INFO/WARNING/ERROR/CRITICAL
logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[%(levelname)s | %(asctime)s] %(message)s', datefmt ='%Y-%m-%d %I:%M:%S'))
logger.addHandler(handler)

try:
    Directory = os.path.dirname(os.path.realpath(__file__))
    if not isfile(f'{Directory}/core/data.json'):
        sdd = {
            "jejudo": {
                "tag": "jejudo",
                "value": "**jejudo project for py-cord**\n```py\npip install -U jejudo\n```\n```py\nbot.load_extension('jejudo')\n# or\nawait bot.load_extension('jejudo')\n```"
            } 
        }
    with open(f"{Directory}/core/data.json", "w",encoding="utf-8-sig") as json_file:
        json.dump(sdd,json_file,ensure_ascii = False, indent=4)
except:

    logger.info("[ jejudo ] The initial setup was skipped because the file was already created.")

def setup(bot):
    bot.add_cog(Jejudo(bot))