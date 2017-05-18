import logging

from player import Player
from c import Console
from botnet import Botnet
import time
import locale

locale.setlocale(locale.LC_ALL, '')

a = Console()
p = Player()
bot = Botnet()

logging.basicConfig(filename='/home/scott/Projects/Coding/vHackAPI-Python/vhack.log', level=logging.INFO)
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
