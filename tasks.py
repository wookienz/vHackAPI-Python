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
        self.ram = 0
        self.money = 0
        self._init()

    def __repr__(self):
        return "".format(self.tasks)

    def _init(self):
        data = self.ut.getrunningtaskdata()
        j = json.loads(data)
        try:
            self.ram = j['ram']
            for i in j['data']:
                    self.addtask(i)
            self.runningtasks = len(self.tasks)
            self.money = int(j['money'])
        except KeyError:
            logging.info("No tasks running currently")
            # self.runningtasks = []

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
        arr = self.ut.requestArray("user::::pass::::uhash:::::",
                              self.username + "::::" + self.password + "::::" + "UserHash_not_needed" + ":::::",
                              "vh_spywareInfo.php")
        return arr

    def removeSpyware(self):
        arr = self.ut.requestArray("user::::pass::::uhash:::::",
                              self.username + "::::" + self.password + "::::" + "UserHash_not_needed" + ":::::",
                              "vh_removeSpyware.php")
        return arr

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

    def startTask(self, type):
        """
        Start a task.
        :param type: string variable of task type, "adw","fw" etc. See config file.
        :return:
        """
        temp = self.ut.starttask(type)
        self.money = int(temp['money'])
        self._newtask()

    def _newtask(self):
        """
        When a new task is added, no task id is passed back. Grab all tasks running, sort through task ids and
        add the new one to self.tasks
        ['data']
        [{u'start': u'1495356942', u'end': u'1495359788', u'type': u'sdk', u'taskid': u'110610282', u'wto': u'1186'},
         {u'start': u'1495357175', u'end': u'1495360024', u'type': u'sdk', u'taskid': u'110612494', u'wto': u'1187'}]
        :return:
        """
        jdata = self.getrunningtasks()
        for i in self.tasks:
            for j in jdata['data']:
                if j['taskid'] not in i:
                    self.addtask(j)

    def finishTask(self, taskobj):
        """
        Finish single task.
        :param taskobj: task object
        :return:
        """
        taskobj._finishtask()

    def finishAll(self):
        """
        Finish all tasks for netcoins
        :return:
        """
        temp = self.ut.requestString("user::::pass::::uhash",
                                self.username + "::::" + self.password + "::::" + "userHash_not_needed",
                                "vh_finishAll.php")
        if "0" in temp:
            return True
        else:
            return False

    def useBooster(self):
        temp = self.ut.requestString("user::::pass::::uhash::::boost",
                                self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "1",
                                "vh_tasks.php")
        return temp

    def filltaskqueue(self):
        """
        Keep task queue up to date. Add task according to priority.
        :return:
        """

        while self.runningtasks < self.ram:
            self.startTask(self.taskpriority[0])
            # update tasks here


class Task:

    ut = Utils()

    def __init__(self, start, end, type, id, lvl):
        """
        [{u'start': u'1495356942', u'end': u'1495359788', u'type': u'sdk', u'taskid': u'110610282', u'wto': u'1186'},
        :param
        """
        self.start = start
        self.id = id
        self.lvl = lvl
        self.type = type
        self.end = end

    def __repr__(self):
        return "Task id {0}, Type: {1}, Level: {2}".format(self.id, self.type, self.lvl)

    def _finishtask(self):
        self.ut.finishtask(self.id)

    def gettaskid(self):
        return self.id
