# -*- coding: utf-8 -*-
from manoutils.config.ConfigManager import configMgr
from manoutils.client.RedisClient import RedisClient

logger = configMgr.getLogger()

class RedisBackend(object):
    def __init__(self):
        self._opr = RedisClient()

    def isLocalSystem(self, exsysType):
        LOCAL_SYS_TYPE = configMgr.getConfigItem("LOCAL_SYS_TYPE", "NFVO")
        if LOCAL_SYS_TYPE.lower() == exsysType.lower():
            return True
        else:
            return False

    def makeReidsKey(self, exsysType, exsysId, exsysTenant=None):
        if not exsysTenant:
            exsysTenant = "*"
        if exsysType.lower() in ["vim", "pim"]:
            if (not exsysId) or (exsysId=="*"):
                return "%s_*" % (exsysType)
            elif (not exsysTenant) or (exsysTenant=="*"):
                return "%s_%s_*" % (exsysType, exsysId)
            else:
                return "%s_%s_%s" % (exsysType, exsysId, exsysTenant)
        else:
            if (not exsysId) or (exsysId=="*"):
                return "%s_*" % (exsysType)
            else:
                return "%s_%s" % (exsysType, exsysId)

    def getExsys(self, exsysType, exsysId, exsysTenant=None):
        if self.isLocalSystem(exsysType=exsysType):
            redisKey = "{}{}".format(exsysType.lower(),"info")
            if self._opr.isKeyExists(redisKey):
                return self._opr.getJson(redisKey)
            else:
                return {}
        else:
            redisKey = self.makeReidsKey(exsysType=exsysType, exsysId=exsysId, exsysTenant=exsysTenant)
            # if "_*" in redisKey:
            #     return self._opr.getJsons(redisKey)
            if self._opr.isKeyExists(redisKey):
                return self._opr.getJson(redisKey)
            else:
                return {}

    def getExsyses(self, exsysType, exsysId=None):
        if not exsysId:
            exsysId = "*"
        if self.isLocalSystem(exsysType=exsysType):
            redisKey = "{}{}".format(exsysType.lower(),"info")
            if self._opr.isKeyExists(redisKey):
                return [self._opr.getJson(redisKey)]
            else:
                return list()
        else:
            redisKey = self.makeReidsKey(exsysType=exsysType, exsysId=exsysId)
            return self._opr.getJsons(redisKey)
