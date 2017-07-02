import utils
import logging

class Cluster:
    ut = utils.Utils()

    def __init__(self):
        pass

    def getclusterddata(self):
        """
        Return json data with information about your cluster.
        :return: json
        """
        r = self.ut.getclusterdata()
        logging.debug("Your cluster has the following information: {0}".format(r))
        return r