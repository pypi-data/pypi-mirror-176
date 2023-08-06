# -*- coding: utf-8 -*-
import logging
import inspect

from manoutils.config.ConfigManager import configMgr
from manoutils.log.LogTemplate import LogTemplate

logger = configMgr.getLogger()

def develLogWrapper(func, logger=logger):
    def wrapper(*args, **kw):
        class_name = ""
        var_names = func.__code__.co_varnames
        func_name = func.__code__.co_name
        file_name = func.__code__.co_filename
        frame = inspect.currentframe()
        local_vars = frame.f_locals
        message="[function:{}] [args:".format(func_name)
        # message = "[file:{}] [function:{}] [args:".format(file_name, func_name)
        for i in range(0,len(local_vars["args"])):
            if str(var_names[i]) == "self":
                class_name = local_vars["args"][i].__class__.__name__
                message = "[class:{}] ".format(class_name) + message
        message_args = list()
        for arg in local_vars["args"]:
            if len(str(arg)) < configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_args.append(arg)
            else:
                message_args.append('***Arg too big to print***')
        message_kw = dict()
        for k,v in local_vars["kw"].items():
            if len(str(v)) < configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_kw.update({k: v})
            else:
                message_kw.update({k: '***Arg too big to print***'})
        message = message + ' args={}, kw={} '.format(message_args, message_kw)
        message = "Enter " + message + "]"
        logger.debug(message)
        ret = func(*args, **kw)
        message_ret = ret
        if len(str(message_ret)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
            message_ret = '***Return value too big to print***'
        if class_name:
            logger.debug("Leave [class:{}] [function:{}] [return:{}]".format(class_name, func_name, message_ret))
        else:
            logger.debug("Leave [function:{}] [return:{}]".format(func_name, message_ret))
        return ret
    return wrapper



def restfulLogWrapper(desc=""):
    def outerWrap(func):
        def innerWrap(*args, **kwargs):
            if len(args) < 1:
                return func(*args, **kwargs)
            request = args[1]
            if not (hasattr(request, "method") and hasattr(request, "META") and hasattr(request, "data")):
                return func(*args, **kwargs)
            LogTemplate().receive_req(desc=desc, request=request)
            response = func(*args, **kwargs)
            if not (hasattr(response, "data") and hasattr(response, "status_code") and hasattr(response, "_headers")):
                return func(*args, **kwargs)
            data = getattr(response, "data")
            data = data if data else {}
            headers = getattr(response, "_headers")
            headers = headers if headers else {}
            status = getattr(response, "status_code")
            status = status if status else ""
            LogTemplate().response_req(desc=desc, data=data, headers=headers, status=status)
            return response
        return innerWrap
    return outerWrap


def responseFormateWrapper(func):
    def innerWrap(*args, **kwargs):
        rspData = dict()
        response = func(*args, **kwargs)
        if  (not hasattr(response, "data") or (not hasattr(response, "status_code"))):
            return response
        data = getattr(response, "data")
        if data==None:
            return response
        if isinstance(data, dict):
            if "rspCode" in data.keys():
                return response
        status = getattr(response, "status_code")
        if str(status).startswith("2"):
            rspData.update({'rspCode': 0})
            rspData.update({'rspDesc': 'success'})
            rspData.update({'content': data})
        else:
            rspData.update({'rspCode': 1})
            rspData.update({'rspDesc': 'Failed'})
            rspData.update({'content': data})
        setattr(response,"data", rspData)
        return response
    return innerWrap


# def testWrap(func):
#     def wrap(*args, **kwargs):
#         print("args={}".format(args))
#         print("kwargs={}".format(kwargs))
#         return func(*args, **kwargs)
#     return wrap
#
# @testWrap
# def func(request, vnfid):
#     print("request={}".format(request))
#     print("vnfid={}".format(vnfid))
#
# func({"tag1":1}, vnfid=2)

