import logging
logging.basicConfig(filename='vhack.log', level=logging.DEBUG)
from player import Player
from c import Console
from botnet import Botnet
import locale
import time
# 8seconds to import
import tasks

locale.setlocale(locale.LC_ALL, '')
logging.basicConfig(filename='vhack.log', level=logging.INFO)

logging.info("...............Starting Up...............at time: {0}".format(time.time()))

a = Console()
p = Player()
bot = Botnet(p)
# 9 seconds to assign variables
t = tasks.Tasks(p)

logging.info("Player money: {0}".format(locale.currency(int(p.money))))
logging.info("Player money: {0}".format(locale.format("%d", int(p.money), grouping=True)))


while True:
    while True:
        if t.filltaskqueue():
            t.boosterplusnetcoins()
        else:
            break
    bot.attack()
    time.sleep(3)
#    bot.upgradebotnet()
    time.sleep(3)
    a.attack()
    for i in p.savedIPs:
        a.attack(i)
