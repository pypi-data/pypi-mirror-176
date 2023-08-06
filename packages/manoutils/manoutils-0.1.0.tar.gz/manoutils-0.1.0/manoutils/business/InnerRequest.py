# -*- coding: utf-8 -*-
import requests
import json

from urlparse import urljoin
from manoutils.log.LogTemplate import LogTemplate
from manoutils.config.ConfigManager import configMgr
from manoutils.business.RequestTracer import RequestTracer

logger = configMgr.getLogger()


class InnerRequest(object):
    def __init__(self):
        self.innerIp = configMgr.getManoIp()
        self.innerPort = configMgr.getManoPort()
        self.innerBaseUrl = "http://{}:{}".format(self.innerIp, self.innerPort)
        self.innerServiceType = ""
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

    def getServiceUrl(self):
        pass

    def getRomteServiceName(self):
        LOCAL_SYS_TYPE = configMgr.getConfigItem("LOCAL_SYS_TYPE", "NFVO")
        return configMgr.getConfigItem(name="SERVICE_NAME", defaultVal=LOCAL_SYS_TYPE)

    def getLocalServiceName(self):
        LOCAL_SYS_TYPE = configMgr.getConfigItem("LOCAL_SYS_TYPE", "NFVO")
        return configMgr.getConfigItem(name="SERVICE_NAME", defaultVal=LOCAL_SYS_TYPE)

    def makeSSLArgs(self):
        return {"verify": False}

    def makeUrl(self, resource='', url=''):
        if url:
            return url
        if resource:
            url = urljoin(self.innerBaseUrl, resource)
        else:
            url = self.innerBaseUrl
        return url

    def makeHeaders(self, headers):
        if headers:
            return headers
        else:
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            requestId = RequestTracer().findRequestId()
            headers.update({'HTTP_X_MANO_REQUEST_ID': requestId})
            return headers

    def makeDesc(self, desc):
        if desc:
            if "->" not in desc:
                desc = "{}->{} {}".format(self.getLocalServiceName(), self.getRomteServiceName(), desc)
        else:
            desc = "{}->{} ".format(self.getLocalServiceName(), self.getRomteServiceName())
        return desc

    def makeBody(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        return data
