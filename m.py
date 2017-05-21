import logging
from player import Player
from c import Console
from botnet import Botnet
import time
import locale
from update import Update
import time
# 8seconds to import

locale.setlocale(locale.LC_ALL, '')
logging.basicConfig(filename='vhack.log', level=logging.INFO)

logging.info("...............Starting Up...............{0}".format(time.time))

a = Console()
p = Player()
bot = Botnet(p)
# 9 seconds to assign variables
up = Update(p)
logging.info("Player money: {0}".format(locale.currency(int(p.money))))

while True:
    up.SpywareInfo()
    bot.attack()
    time.sleep(3)
    bot.upgradebotnet()
    time.sleep(3)
    a.attack()
    for i in p.savedIPs:
        a.attack(i)
