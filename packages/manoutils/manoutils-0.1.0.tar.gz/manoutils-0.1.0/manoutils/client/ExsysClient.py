# -*- coding: utf-8 -*-
from manoutils.config.ConfigManager import configMgr
from manoutils.common.common import ignore_case_get
from manoutils.client.exsys.HttpBackend import HttpBackend
from manoutils.client.exsys.RedisBackend import RedisBackend

logger = configMgr.getLogger()


class ExsysTools(object):
    def filter(self, infos, key, val):
        newInfos = []
        if (not key) or (not val):
            return infos
        for info in infos:
            if str(val).lower() == str(ignore_case_get(info, key)).lower():
                newInfos.append(info)
        return newInfos


class ExsysClient(object):
    def __init__(self):
        self._backend = configMgr.getConfigItem("EXSYS_CLIENT_BACKEND", "redis")

    def makeExsysType(self, exsysType):
        if exsysType.lower() in ["cmoss", "pmoss", "fmoss"]:
            exsysType = "oss"
        return exsysType

    def getBackend(self):
        if self._backend.lower() == "redis":
            backend = RedisBackend()
        else:
            backend = HttpBackend()
        return backend

    def getExsys(self, exsysType, exsysId, exsysTenant=""):
        exsysType = self.makeExsysType(exsysType=exsysType)
        backend = self.getBackend()
        return backend.getExsys(exsysType=exsysType, exsysId=exsysId, exsysTenant=exsysTenant)

    def getExsyses(self, exsysType, exsysId=""):
        exsysType = self.makeExsysType(exsysType=exsysType)
        backend = self.getBackend()
        if exsysType.lower() == "pim":
            exsyses = backend.getExsyses(exsysType="vim", exsysId=exsysId)
            exsyses = ExsysTools().filter(infos=exsyses, key="VPimMode", val="true")
            exsyses = exsyses + backend.getExsyses(exsysType="pim", exsysId=exsysId)
        else:
            exsyses = backend.getExsyses(exsysType=exsysType, exsysId=exsysId)
        return exsyses

    def getExsysIds(self, exsysType):
        exsysType = self.makeExsysType(exsysType=exsysType)
        exsysIds = list()
        exsyses = self.getExsyses(exsysType=exsysType)
        for exsys in exsyses:
            if exsysType.lower() == "pim":
                if ignore_case_get(exsys, "pimid"):
                    exsysId = ignore_case_get(exsys, "pimid")
                else:
                    exsysId = ignore_case_get(exsys, "vimid")
            else:
                exsysId = ignore_case_get(exsys, "{}id".format(exsysType))
            exsysIds.append(exsysId)
            exsysIds = list(set(exsysIds))
        return exsysIds

    def getLocalSystemInfo(self):
        LOCAL_SYS_TYPE = configMgr.getConfigItem("LOCAL_SYS_TYPE", "NFVO")
        return self.getExsyses(exsysType=LOCAL_SYS_TYPE)[0]

    def getLocalSystemId(self):
        LOCAL_SYS_TYPE = configMgr.getConfigItem("LOCAL_SYS_TYPE", "NFVO")
        sysInfo = self.getExsyses(exsysType=LOCAL_SYS_TYPE)[0]
        return ignore_case_get(sysInfo, "{}id".format(LOCAL_SYS_TYPE))
