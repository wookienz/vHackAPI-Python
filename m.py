#!/usr/bin/python2.7
# -*- coding: utf-8

import logging
from player import Player
from c import Console
from botnet import Botnet
import time

import config
import locale

logging.basicConfig(filename='vhack.log', level=logging.DEBUG)
locale.setlocale(locale.LC_ALL, '')
a = Console()
# p = Player()
bot = Botnet()

logging.info("Starting Up")

while True:
    # logging.info(p)
    bot.attack()
    time.sleep(3)
    bot.upgradebotnet()
    time.sleep(3)
    a.attack()
    for i in p.savedIPs:
        a.attack(i)

