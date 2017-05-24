from utils import Utils
import c
import json
import logging
logging.basicConfig(filename='vhack.log', level=logging.DEBUG)
logging.info('Starting Temp file')
#ut = Utils()
#d = c.Console()
#uhash = d._gethash()
"""
ip = "XT7H41995C.vHack.cc"
temp = ut.requestString("user::::pass::::uhash::::target",
                                     a.getUsername() + "::::" + a.getPassword() + "::::" + str(
                                         uhash) + "::::" + ip, "vh_loadRemoteData.php")
j = json.loads(temp)
print j
"""
"""
r = d.attack()
print r
"""
from tasks import Tasks
from player import Player
p = Player()
t = Tasks(p)
t.startTask('fw')
print t.tasks
t.finishTask(t.tasks[0])
print t.tasks