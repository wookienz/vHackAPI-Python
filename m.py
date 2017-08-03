import logging

logging.basicConfig(filename='vhack.log', level=logging.DEBUG)

import time

logging.debug(time.time())
import player
from c import Console
from botnet import Botnet
import locale
import time
# 8seconds to import
import tasks
from package import Package
from missions import Missions
from cluster import Cluster

locale.setlocale(locale.LC_ALL, '')
logging.basicConfig(filename='vhack.log', level=logging.INFO)

logging.info("...............Starting Up...............at time: {0}".format(time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                          time.localtime(time.time()))))
a = Console()
p = player.Player()
bot = Botnet()
t = tasks.Tasks(p)
package = Package()
mission = Missions()
cluster = Cluster()

while True:
    p.init()
    # p.saveIP('1.1.1.1', '')`
    """
    if t.filltaskqueue():
        t.boosterplusnetcoins()
    
    bot.attack()
    package.openallpackages()
    # time.sleep(3)
    bot.upgradebotnet()
    # time.sleep(3)
    a.localhostattack()
    """
    a.attack()
    # for i in p.savedIPs:
    #    a.attack(i)