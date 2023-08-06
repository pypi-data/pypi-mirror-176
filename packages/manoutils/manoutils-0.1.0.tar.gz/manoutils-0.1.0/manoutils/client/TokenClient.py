# -*- coding: utf-8 -*-
from manoutils.client.RedisClient import RedisClient
from manoutils.config.ConfigManager import configMgr

logger = configMgr.getLogger()


class TokenClient(object):
    def __init__(self):
        self._opr = RedisClient()
        self._redis_key = ""

    def getToken(self, exsysId, exsysType):
        self.makeExsysTokenKey(exsysId=exsysId, exsysType=exsysType)
        return self._opr.getString(self._redis_key)

    def checkToken(self, exsysId, exsysType, token):
        self.makeLocalsysTokenKey(exsysId=exsysId, exsysType=exsysType)
        if not token:
            return False
        if self._opr.getString(self._redis_key) == token:
            return True
        else:
            return False

    def makeExsysTokenKey(self, exsysId, exsysType):
        localSystemType = configMgr.getConfigItem("LOCAL_SYS_TYPE")
        localSystemType = localSystemType if localSystemType else "NFVO"
        localSystemType = localSystemType.upper()
        if exsysType.lower() == "oss":
            self._redis_key = "TOKEN_{}_2_{}_{}".format(localSystemType, "cmoss".upper(), exsysId)
        else:
            self._redis_key = "TOKEN_{}_2_{}_{}".format(localSystemType, exsysType.upper(), exsysId)

    def makeLocalsysTokenKey(self, exsysId, exsysType):
        localSystemType = configMgr.getConfigItem("LOCAL_SYS_TYPE")
        localSystemType = localSystemType if localSystemType else "NFVO"
        localSystemType = localSystemType.upper()
        if exsysType.lower() == "oss":
            self._redis_key = "TOKEN_{}_2_{}_{}".format("cmoss".upper(), localSystemType, exsysId)
        else:
            self._redis_key = "TOKEN_{}_2_{}_{}".format(exsysType.upper(), localSystemType, exsysId)