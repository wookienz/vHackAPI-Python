#!/usr/bin/python2.7
# -*- coding: utf-8
import sys
import json
import ocr
import config
import base64
import hashlib
import time
import urllib2
import random
import logging


class Utils:
    def __init__(self):
        self.secret = config.secret
        self.url = config.baseurl
        self.username = config.user
        self.password = config.password

    def getTime(self):
        return int(round(time.time()))

    def md5hash(self, txt):
        m = hashlib.md5()
        m.update(txt)
        return m.hexdigest()

    def generateUser(self, bArr):
        return base64.b64encode(bArr).replace("=", "")

    def generateURL(self, format, data, php):
        split = format.split("::::")
        split2 = data.split("::::")
        currentTimeMillis = str(self.getTime())
        jsonString = "{"
        for i1 in range(0, len(split)):
            jsonString += "\"" + split[i1] + "\":"
            jsonString += "\"" + split2[i1] + "\","
        jsonString += "\"time\":\"" + currentTimeMillis + "\"}"
        a = self.generateUser(jsonString)
        a2 = self.md5hash(str(len(jsonString)) + self.md5hash(currentTimeMillis))
        str5 = split2[0] + self.md5hash(self.md5hash(split2[1]))
        str6 = self.md5hash(currentTimeMillis + jsonString)
        a3 = self.md5hash(self.secret + self.md5hash(self.md5hash(self.generateUser(a2))))
        str9 = self.generateUser(str5)
        str7 = self.generateUser(str6)
        str8 = self.md5hash(self.md5hash(a3 + self.md5hash(self.md5hash(str9) + str7)))
        return self.url + php + "?user=" + a + "&pass=" + str8

    def parse(self, string):
        return string[1:-1].replace("\"", "").split(",")

    def parseMulti(self, string):
        temp = string
        temp = temp.replace("[", "").replace("]", "")
        temp = temp[len(temp.split(":")[0]) + 1:-1]

        arr = temp.split("},{")
        n = []
        for i1 in arr:
            temp = i1
            if not temp.startswith("{"):
                temp = "{" + temp
            if not temp.endswith("}"):
                temp += "}"
            n.append(self.parse(temp))
        return n

    def requestString(self, form, data, php):
        time.sleep(random.randint(1, 2))
        r = None
        count = 0
        while r is None:
            try:
                r = urllib2.urlopen(self.generateURL(form, data, php))
                t = r.read()
                return t
            except Exception as err:
                count += 1
                logging.warn("network error, trying again. Count: {0}".format(count))
                time.sleep(count)
                if count == 10:
                    logging.warn("Network errors - Giving up. Dumping data: {0}, {1}, {2}".format(form, data, php))
                    sys.exit()

    def requestArray(self, form, data, php):
        temp = self.requestString(form, data, php)
        if temp != "null":
            return self.parse(temp)
        else:
            return []

    def upgradebot(self, id):
        """
        Supplied with a bot net computer ID, upgrade the computer.
        :param id: bot net computer id
        :return: str
        containing: {"money":"3479746","old":"13","costs":"4100000","lvl":"41","mm":"7579746","new":"42","strength":"42"}
        """
        response = self.requestString("user::::pass::::uhash::::bID",
                                      self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + str(
                                          id),
                                      "vh_upgradeBotnet.php")
        return response

    def botnetserverinfo(self):
        """
        return botnet info including if you can attack vHack servers and bot net pcs info.
        :return:
        """
        response = self.requestString("user::::pass::::uhash",
                                      self.username + "::::" + self.password + "::::" + "userHash_not_needed",
                                      "vh_botnetInfo.php")
        return response

    def attackbotnetserver(self, i):
        """
        Attack vHack servers
        :return: string
        """
        response = self.requestString("user::::pass::::uhash::::cID",
                                      self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "1",
                                      "vh_attackCompany.php")
        temp = self.requestString("user::::pass::::uhash::::cID",
                                  self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "2",
                                  "vh_attackCompany2.php")
        temp = self.requestString("user::::pass::::uhash::::cID",
                                  self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "3",
                                  "vh_attackCompany3.php")
        """temp = self.requestString("user::::pass::::uhash::::cID",
                                  self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "4",
                                     "vh_attackCompany4.php")"""
        return response

    def myinfo(self):
        """
        looks up and returns all data associated with player. Upgrades, moneym boosters, spyware active etc.
        See player class for detailed description
        :return: str
        """
        temp = self.requestString("user::::pass::::gcm::::uhash",
                                  self.username + "::::" + self.password + "::::" + "eW7lxzLY9bE:APA91bEO2sZd6aibQerL3Uy-wSp3gM7zLs93Xwoj4zIhnyNO8FLyfcODkIRC1dc7kkDymiWxy_dTQ-bXxUUPIhN6jCUBVvGqoNXkeHhRvEtqAtFuYJbknovB_0gItoXiTev7Lc5LJgP2" + "::::" + "userHash_not_needed",
                                  "vh_update.php")
        if len(temp) is 1:
            logging.error("Are Username and Password correct?")
            sys.exit()
        return temp

    def removespyware(self):
        arr = self.requestArray("user::::pass::::uhash:::::",
                                self.username + "::::" + self.password + "::::" + "UserHash_not_needed" + ":::::",
                                "vh_removeSpyware.php")
        return arr

    def gettargets(self, hash):
        """
        Initial scan of 6 hosts. It appears as an image. Return image for processing.
        :return: str
        """
        temp = self.requestString("user::::pass::::uhash::::by",
                                  self.username + "::::" + self.password + "::::" + str(
                                      hash) + "::::" + str(random.randint(0, 1)), "vh_getImg.php")
        return temp

    def scantarget(self, uhash, hostname):
        """
        Given a hash and hostname, scan target to get ip and vuln
        '{"hostname":"XT-VRAV7Z5.vHack.cc","ipaddress":"76.179.249.20","vuln":"1"}'
        :param uhash:
        :param hostname: hostname of the target "X7-H41995C.vHack.cc"
        :return: tgt data
        """
        temp = self.requestString("user::::pass::::uhash::::hostname",
                                  self.username + "::::" + self.password + "::::" + str(
                                      uhash) + "::::" + str(hostname), "vh_scanHost.php")
        return temp

    def gethash(self):
        """
        Return up to date hash
        :return: str
        """
        response = self.myinfo()
        try:
            uhash = json.loads(response)
            h = uhash['hash']
            return h
        except TypeError:
            logging.info("Getting hash blocked")
            return False

    def connectToRemoteHost(self, ip):
        """
        Load remote data of the host. String containing image and,
        "p1":6834,"p2":28181,"p3":14601,"p4":1559,"p5":52543,"p6":54969,"fw":347,"av":318,"spam":325,"sdk":283,
        "ipsp":296,"money":33210055,"savings":"0","anonymous":"NO","username":"153.98.35.119","winelo":0,"winchance":90,
        "spyware":"276","ipaddress":"153.98.35.119","cmember":"0"}'
        :return:
        """
        uhash = self.gethash()
        temp = self.requestString("user::::pass::::uhash::::target",
                                  self.username + "::::" + self.password + "::::" + str(
                                      uhash) + "::::" + ip, "vh_loadRemoteData.php")
        return temp

    def findportnumber(self, img):
        """
        Given an image or the port number, covert to str.
        :param img: base64 image
        :return: str
        """
        o = ocr.OCR()
        return o.getSolution(img)

    def transferTrojan(self, passwd, target, uhash):
        """

        :param passwd:
        :param target:
        :param uhash:
        :return:
         '{"result":"0","amount":4877810,"elo":2955,"eloch":1,"newmoney":5468422}'
        """
        temp = self.requestString("user::::pass::::port::::target::::uhash",
                                  self.username + "::::" + self.password + "::::" + str(
                                      passwd[1]) + "::::" + str(target) + "::::" + str(uhash),
                                  "vh_trTransfer.php")
        if 'time' in temp:
            logging.info("{0} under protection: {1}".format(str(target), temp))
            return False
        else:
            return temp

    def notepadIPs(self):
        """
        Retrieve IPs save on the notepad.
        :return: list
        """
        uhash = self.gethash()
        temp = self.requestString("user::::pass::::uhash",
                                  self.username + "::::" + self.password + "::::" +
                                  str(uhash), "vh_getNotepadData.php")
        j = json.loads(temp)
        ips = j['pad'].split('\n')
        logging.info("Saved IPs from Notepad: {0}".format(ips))
        return ips

    def SpywareInfo(self):
        """
        < type 'list' >: ['local:0', 'data:[{av:392', 'fw:417', 'money:42793029', 'spam:467', 'user:ShittyGame',
                           'ip:23.93.18.103', 'next:now.}]', 'remote:1', 'result:0']
        """
        arr = self.requestArray("user::::pass::::uhash:::::",
                                self.username + "::::" + self.password + "::::" + "UserHash_not_needed" + ":::::",
                                "vh_spywareInfo.php")
        return arr

    def getrunningtaskdata(self):
        """
        '{"data":[{"type":"sdk","start":"1495356942","end":"1495359788","wto":"1186","taskid":"110610282"}],
        "fAllCosts":"23","money":"17798567","inet":"10","hdd":"10","cpu":"10","ram":"14","fw":"350","av":"747",
        "sdk":"1185","ipsp":"151","spam":"204","scan":"575","adw":"210","netcoins":"9544","urmail":"0","score":"16254",
        "energy":"262260372","useboost":"2","boost":"336","status":"1","stime":"1495357017"}'
        :return: string
        """
        temp = self.requestString("user::::pass::::uhash",
                                self.username + "::::" + self.password + "::::" + "userHash_not_needed",
                                "vh_tasks.php")
        return temp

    def starttask(self, i):
        temp = self.requestString("user::::pass::::uhash::::utype",
                                self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + i,
                                "vh_addUpdate.php")
        return temp

    def finishtask(self, id):
        temp = self.requestString("user::::pass::::uhash::::taskid",
                                 self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + id,
                                 "vh_finishTask.php")
        logging.info("Finished task: {0}".format(id))
        return temp