from utils import Utils
import json
import logging


class Tasks:

    ut = Utils()

    def __init__(self, obj):
        self.username = obj.username
        self.password = obj.password
        self.runningtasks = 0
        self.taskpriority = obj.taskpri
        self.tasks = []
        self.money = obj.getmoney()
        self.ram = 0
        self.p = obj
        self.level = obj.nclevel
        self._init()

    def __repr__(self):
        return "".format(self.tasks)

    def _init(self):
        data = self.ut.getrunningtaskdata()
        j = json.loads(data)
        try:
            for i in j['data']:
                    self.addtask(i)
            self.runningtasks = len(self.tasks)
            self.ram = int(j['ram'])
            self._updatemoney(j['money'])
        except Exception:
            data = self.ut.myinfo()
            j = json.loads(data)
            self.ram = j['ram']
            self.money = self.p.getmoney()
            self.runningtasks = 0

    def addtask(self, j):
        """
        Add a task class to tasks holder
        :param j: {u'start': u'1495356942', u'end': u'1495359788', u'type': u'sdk', u'taskid': u'110610282',
        u'wto': u'1186'}
        :return:
        """
        self.tasks.append(Task(j['start'], j['end'], j['type'], j['taskid'], j['wto']))

    def getrunningtasks(self):
        """
        '{"data":[{"type":"sdk","start":"1495356942","end":"1495359788","wto":"1186","taskid":"110610282"}],
        "fAllCosts":"23","money":"17798567","inet":"10","hdd":"10","cpu":"10","ram":"14","fw":"350","av":"747",
        "sdk":"1185","ipsp":"151","spam":"204","scan":"575","adw":"210","netcoins":"9544","urmail":"0","score":"16254",
        "energy":"262260372","useboost":"2","boost":"336","status":"1","stime":"1495357017"}'

        ['data']
        [{u'start': u'1495356942', u'end': u'1495359788', u'type': u'sdk', u'taskid': u'110610282', u'wto': u'1186'},
         {u'start': u'1495357175', u'end': u'1495360024', u'type': u'sdk', u'taskid': u'110612494', u'wto': u'1187'}]

        :return:
        """
        temp = self.ut.getrunningtaskdata()
        j = json.loads(temp)
        return j['data']

    def SpywareInfo(self):
        """
        < type 'list' >: ['local:0', 'data:[{av:392', 'fw:417', 'money:42793029', 'spam:467', 'user:ShittyGame',
                           'ip:23.93.18.103', 'next:now.}]', 'remote:1', 'result:0']
        """
        r = self.ut.SpywareInfo()
        j = json.loads(r)
        return j

    def removeSpyware(self):
        r = self.ut.removespyware()
        j = json.loads(r)
        return j

    def _getTaskID(self, tasks=None):
        """
        Return a list of task ids
        [u'110610282', u'110612494']
        :param tasks string of json data
         ['data']
        [{u'start': u'1495356942', u'end': u'1495359788', u'type': u'sdk', u'taskid': u'110610282', u'wto': u'1186'},
         {u'start': u'1495357175', u'end': u'1495360024', u'type': u'sdk', u'taskid': u'110612494', u'wto': u'1187'}]
        :return: list
        """
        if not tasks:
            tasks = self.getrunningtasks()
        j = json.loads(tasks)
        return [x['taskid'] for x in j['data']]

    def startTask(self, typ):
        """
        Start a task. j['result'] = 3 when full queue, '1' if not enough money, '0 if successful,
        :param typ: string variable of task type, "adw","fw" etc. See config file.
        :return:
        """
        temp = self.ut.starttask(typ)
        j = json.loads(temp)
        if j['result'] == '0':
            self._updatemoney(j['money'])
            self._newtask()
            logging.info("Starting Task: {0}".format(typ))
            return True
        else:
            return False

    def _updatemoney(self, j):
        """
        Update player and Tasks class money variable
        :param j: string of money amount
        :return:
        """
        self.money = int(j)
        self.p.setmoney(int(j))
        logging.info("Updating money after adding task")

    def _newtask(self):
        """
        When a new task is added, no task id is passed back. Grab all tasks running, sort through task ids and
        add the new one to self.tasks
        jdata is a list as below:
        [{u'start': u'1495356942', u'end': u'1495359788', u'type': u'sdk', u'taskid': u'110610282', u'wto': u'1186'},
         {u'start': u'1495357175', u'end': u'1495360024', u'type': u'sdk', u'taskid': u'110612494', u'wto': u'1187'}]
        :return:
        """
        jdata = self.getrunningtasks()
        oldtasks = [x.id for x in self.tasks]
        for j in jdata:
            if j['taskid'] not in oldtasks:
                self.addtask(j)
                self.runningtasks = len(jdata)

    def finishTask(self, taskobj):
        """
        Finish single task with NetCoins
        :param taskobj: task object
        :return:
        """
        taskobj._finishtask()

    def finishAll(self):
        """
        Finish all tasks with netcoins.
        temp = '0' if all finished.
        :return:
        """
        temp = self.ut.requestString("user::::pass::::uhash",
                                self.username + "::::" + self.password + "::::" + "userHash_not_needed",
                                "vh_finishAll.php")
        if "0" in temp:
            self.runningtasks = 0
            return True
        else:
            return False

    def boosterplusnetcoins(self):
        """
        Use boosters until a level, then finish with netcoins.
        :return:
        """
        self.level = 1300  # at what netcoin amount to just finish all with NC instead of more boosters.
        netcoinstofinish = 1301
        while netcoinstofinish > self.level:
            logging.info("Netcoins completion still too high, using another booster")
            r = self.useBooster()
            j = json.loads(r)
            if int(j['status']) != 0:
                netcoinstofinish = int(j['fAllCosts'])
                logging.info("Netcoins to finish them all: {0}, level of netcoins to spend: {1}"
                             .format(netcoinstofinish, self.level))
            else:
                logging.info("No tasks left to use netcoins on")
                self.runningtasks = 0
                return
        self.finishAll()

    def useBooster(self):
        """
        if no tasks - {"boost":"2181","netcoins":"62539","status":"0"}
        if task running:
        {"data":[{"type":"av","start":"1498274673","end":"1498278365","wto":"3047","taskid":"127531860"},
            {"type":"av","start":"1498274677","end":"1498278368","wto":"3048","taskid":"127531883"},
            {"type":"av","start":"1498274681","end":"1498278372","wto":"3049","taskid":"127531897"},
            {"type":"av","start":"1498274686","end":"1498278375","wto":"3050","taskid":"127531927"}],
        "fAllCosts":"425","money":"680601793","inet":"10","hdd":"10","cpu":"10","ram":"14","fw":"1912","av":"3046",
        "sdk":"2984","ipsp":"458","spam":"568","scan":"1239","adw":"582","netcoins":"77875","urmail":"0",
        "score":"43053","energy":"0","useboost":"0","boost":"2139","status":"1","stime":"1498274745"}
        :return: string
        """
        temp = self.ut.requestString("user::::pass::::uhash::::boost",
                                self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "1",
                                "vh_tasks.php")
        logging.info("Used booster")
        return temp

    def filltaskqueue(self, upgrade=None):
        """
        Keep task queue up to date. Add task according to priority.
        :return:
        """
        if not upgrade:
            upgrade = self.taskpriority[0]
        while self.runningtasks < int(self.ram):
            result = self.startTask(upgrade)
            if not result: # False returned, either full queue or no money
                return False
            logging.info("Starting task upgrade of type: {0}".format(upgrade))
        return True


class Task:

    ut = Utils()

    def __init__(self, start, end, typ, taskid, lvl):
        """
        [{u'start': u'1495356942', u'end': u'1495359788', u'typ': u'sdk', u'taskid': u'110610282', u'wto': u'1186'},
        :param
        """
        self.start = start
        self.id = taskid
        self.lvl = lvl
        self.type = typ
        self.end = end

    def __repr__(self):
        return "Task id {0}, Type: {1}, Level: {2}".format(self.id, self.type, self.lvl)

    def _finishtask(self):
        """
        Finish self task with netcoins
        :return:
        """
        self.ut.finishtask(self.id)

    def gettaskid(self):
        return self.id
