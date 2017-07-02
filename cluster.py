import utils

class Cluster:
    ut = utils.Utils()

    def __init__(self, obj):
        self.username = obj.username
        self.password = obj.password
        pass

    def getclusterddata(self):
        """
        Return json data with information about your cluster.
        :return: json
        """
        userHash = self.ut.gethash()
        r = self.ut.requestString("user::::pass::::uhash", self.username + "::::" + self.password + "::::" + userHash,
                                  "vh_ClusterData.php")

