import logging
logging.basicConfig(filename='vhack.log', level=logging.WARN)

from player import Player
from c import Console
from botnet import Botnet
import time
import locale
import os
import sys

locale.setlocale(locale.LC_ALL, '')

a = Console()
p = Player()
bot = Botnet()

logging.info("...............Starting Up...............")
logging.info("Player money: {0}".format(p.money))

while True:
    bot.attack()
    time.sleep(3)
    bot.upgradebotnet()
    time.sleep(3)
    a.attack()
    for i in p.savedIPs:
        a.attack(i)
