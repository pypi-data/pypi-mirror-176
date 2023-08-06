# -*- coding: utf-8 -*-
import requests
import json

from enum import Enum
from urlparse import urljoin
from manoutils.config.ConfigManager import configMgr
from manoutils.client.CertClient import CertClient
from manoutils.client.ExsysClient import ExsysClient
from manoutils.client.TokenClient import TokenClient
from manoutils.log.LogTemplate import LogTemplate
from manoutils.common.common import ignore_case_get
from manoutils.business.RequestTracer import RequestTracer

logger = configMgr.getLogger()


class AuthType(Enum):
    NoAuth = 0
    OneAuth = 1
    TwoAuth = 2


class ExsysRequest(object):
    def __init__(self, exsysId, exsysType, exsysTenant=''):
        self.exsysId = exsysId
        self.exsysType = exsysType
        self.exsysTenant = exsysTenant
        self.exsystem = ExsysClient().getExsys(exsysType=exsysType, exsysId=exsysId, exsysTenant=exsysTenant)
        self.method = "get"

    def __getattr__(self, item):
        self.method = item
        return self._request

    def _request(self, resource='', data='', url='', headers='', timeout=10, desc='', ext_msg='', **kwargs):
        sslArgs = self.makeSSLArgs()
        kwargs.update(sslArgs)
        headers = self.makeHeaders(headers=headers)
        url = self.makeUrl(resource=resource, url=url)
        data = self.makeBody(data=data)
        desc = self.makeDesc(desc=desc)
        LogTemplate().before_send_req(desc=desc, method=self.method.upper(), url=url, data=data, headers=headers, ext_msg=ext_msg)
        rsp = requests.request(method=self.method.lower(), url=url, data=data, headers=headers, timeout=timeout, **kwargs)
        LogTemplate().after_send_req(desc=desc, request=rsp, ext_msg=ext_msg)
        return rsp

    def makeSSLArgs(self):
        try:
            authType = ignore_case_get(self.exsystem, "authType")
            certId = ignore_case_get(self.exsystem, "certId")
            args = {"verify": False}
            if self.exsysType == "sec":
                authType = authType.encode('cp936')
            if str(authType).lower() == str(AuthType.OneAuth.value):
                cert = CertClient().getCert(certId=certId)
                cacertPath = ignore_case_get(cert, "cacertPath")
                if not cacertPath:
                    raise Exception("get cacertPath error")
                args.update({"verify": cacertPath})
            elif str(authType).lower() == str(AuthType.TwoAuth.value):
                cert = CertClient().getCert(certId=certId)
                cacertPath = ignore_case_get(cert, "cacertPath")
                clientcertPath = ignore_case_get(cert, "clientcertPath")
                clientkeyPath = ignore_case_get(cert, "clientkeyPath")
                if not cacertPath:
                    raise Exception("get cacertPath error")
                if not clientcertPath:
                    raise Exception("get clientcertPath error")
                if not clientkeyPath:
                    raise Exception("get clientkeyPath error")
                args.update({"verify": cacertPath})
                args.update({"cert": (clientcertPath, clientkeyPath)})
            else:
                args.update({"verify": False})
            return args
        except Exception as e:
            logger.error(e.message)
            return {"verify": False}

    def makeUrl(self, resource='', url=''):
        if url:
            return url
        if not resource:
            if self.exsysType.lower() == "cmoss":
                url = ignore_case_get(self.exsystem, "cmUrl")
            elif self.exsysType.lower() == "pmoss":
                url = ignore_case_get(self.exsystem, "pmUrl")
            elif self.exsysType.lower() == "fmoss":
                url = ignore_case_get(self.exsystem, "fmUrl")
            elif self.exsysType.lower() == "oss":
                url = ignore_case_get(self.exsystem, "cmUrl")
            else:
                url = ignore_case_get(self.exsystem, "url")
            return url
        else:
            if self.exsysType.lower() == "cmoss":
                baseUrl = ignore_case_get(self.exsystem, "cmUrl")
            elif self.exsysType.lower() == "pmoss":
                baseUrl = ignore_case_get(self.exsystem, "pmUrl")
            elif self.exsysType.lower() == "fmoss":
                baseUrl = ignore_case_get(self.exsystem, "fmUrl")
            elif self.exsysType.lower() == "oss":
                baseUrl = ignore_case_get(self.exsystem, "cmUrl")
            else:
                baseUrl = ignore_case_get(self.exsystem, "url")
            url = urljoin(baseUrl, resource)
            return url

    def makeHeaders(self, headers):
        if headers:
            return headers
            # if ignore_case_get(headers, "X-Auth-Token"):
            #     return headers
            # else:
            #     token = TokenClient().getToken(exsysId=self.exsysId, exsysType=self.exsysType)
            #     headers.update({"X-Auth-Token": token})
            #     return headers
        else:
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            token = TokenClient().getToken(exsysId=self.exsysId, exsysType=self.exsysType)
            headers.update({"X-Auth-Token": token})
            requestId = RequestTracer().findRequestId()
            headers.update({'HTTP_X_MANO_REQUEST_ID': requestId})
            return headers

    def makeDesc(self, desc):
        LOCAL_SYS_TYPE = configMgr.getConfigItem("LOCAL_SYS_TYPE", "NFVO")
        if desc:
            if "->" not in desc:
                desc = "{}->{} {}".format(LOCAL_SYS_TYPE, self.exsysType.upper(), desc)
        else:
            desc = "{}->{} ".format(LOCAL_SYS_TYPE, self.exsysType.upper())
        if ("NFVO->VNFM" in desc) or ("VNFM->NFVO" in desc):
            desc = "C6 " + desc
        elif ("NFVO->VIM" in desc) or ("VIM->NFVO" in desc):
            desc = "C7 " + desc
        elif ("NFVO->PIM" in desc) or ("PIM->NFVO" in desc):
            desc = "C7 " + desc
        elif ("VNFM->OMC" in desc) or ("OMC->VNFM" in desc):
            desc = "C8 " + desc
        elif ("VNFM->VNF" in desc) or ("VNF->VNFM" in desc):
            desc = "C10 " + desc
        return desc

    def makeBody(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        return data
