from utils import Utils


class Update:

    ut = Utils()

    def getTasks(self):
        temp = self.ut.requestString("user::::pass::::uhash",
                                self.username + "::::" + self.password + "::::" + "userHash_not_needed",
                                "vh_tasks.php")
        return temp

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

    def getTaskAmount(self):
        temp = self.getTasks()
        return len(temp.split("taskid")) - 1

    def getTaskIDs(self):
        temp = self.getTasks()
        tasks = temp.split('"taskid":"')[1:]
        n = []
        for i1 in tasks:
            n.append(i1.split('"')[0])
        return n

    def startTask(self, type):
        temp = self.ut.requestString("user::::pass::::uhash::::utype",
                                self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + type,
                                "vh_addUpdate.php")
        if "result" in temp:
            return temp.split('result":"')[1].split('"')[0]
        return "2"

    def finishTask(self, taskID):
        temp = self.ut.requestString("user::::pass::::uhash::::taskid",
                                self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + taskID,
                                "vh_finishTask.php")
        if "4" in temp:
            return True
        else:
            return False

    def finishAll(self):
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

    def __init__(self, obj):
        self.username = obj.username
        self.password = obj.password
