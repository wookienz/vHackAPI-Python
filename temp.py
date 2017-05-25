from utils import Utils
import c
import json
import logging
logging.basicConfig(filename='vhack.log', level=logging.DEBUG)
logging.info('Starting Temp.py file')
#ut = Utils()
#d = c.Console()
#uhash = d._gethash()

from tasks import Tasks
from player import Player
p = Player()
t = Tasks(p)
# t.finishTask(t.tasks[0])
# t.finishAll()
t.filltaskqueue()
