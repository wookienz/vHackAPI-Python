import utils

class targets:

    def __init__(self):
        self.tgts = []
        self.index = 0
        self.qty = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index == 0:
            raise StopIteration
        self.index -= -1
        return self.tgts[self.index]

    def scantarget(self, hostname):
        pass

    def attacktarget(self, hostname):
        t = self.findtarget(hostname)
        t.attack()

    def removetarget(self, ip, hostname=None):
        for i in enumerate(self.tgts):
            for k, v in i[1]:
                if k == hostname or v == ip:
                    self.tgts.remove(i[1])
                    self.qty -= 1

    def addtarget(self, hostname, **kwargs):
        t = target(hostname)
        try:
            self.tgts.append({hostname: t})
            self.qty += 1
            self.index += 1
        except:
            pass
        self.changevalue(hostname, **kwargs)

    def changevalue(self, hostname, **kwargs):
        b = self.findtarget(hostname)
        for key, value in kwargs.iteritems():
            b.setvar(key, value)

    def findtarget(self, hostname):
        """
        Find target in the list of targets, return the target object. If not in the list, keyerror
        :param hostname: string value of the host
        :return: target object
        """
        for i in self.tgts:
            try:
                return i[hostname]
            except KeyError:
                pass

    def __repr__(self):
        return "Targets in array: {0}, ".format(self.tgts)


class target(targets):

    ut = utils. Utils()

    def __init__(self, hostname):
        targets.__init__(self)
        self.hostname = hostname
        self.ip = ''

    def setip(self, ip):
        self.ip = ip

    def getip(self):
        return self.ip

    def sethostname(self, h):
        self.hostname = h

    def gethostname(self):
        return self.hostname

    def setvar(self, key, value):
        setattr(self, key, value)

    def attack(self):
        """
        Attack the host detailed by self.
        :return:
        """
        r = self.ut.scantarget(self.hostname, self.ip)
        if self.ip:
            self.ut.connectToRemoteHost(self.ip)

    def __repr__(self):
        return "Hostname: {0}, IP: {1}".format(self.hostname, self.ip)