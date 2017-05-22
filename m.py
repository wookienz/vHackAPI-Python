import logging
logging.basicConfig(filename='vhack.log', level=logging.DEBUG)
from player import Player
from c import Console
from botnet import Botnet
import locale
import time
# 8seconds to import

locale.setlocale(locale.LC_ALL, '')
logging.basicConfig(filename='vhack.log', level=logging.INFO)

logging.info("...............Starting Up...............{0}".format(time.time()))

a = Console()
p = Player()
bot = Botnet(p)
# 9 seconds to assign variables

logging.info("Player money: {0}".format(locale.currency(int(p.money))))

while True:
    bot.attack()
    time.sleep(3)
    bot.upgradebotnet()
    time.sleep(3)
    a.attack()
    for i in p.savedIPs:
        a.attack(i)
