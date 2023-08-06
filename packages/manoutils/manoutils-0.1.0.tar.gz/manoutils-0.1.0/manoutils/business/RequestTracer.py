# -*- coding: utf-8 -*-
import inspect

from manoutils.config.ConfigManager import configMgr

logger = configMgr.getLogger()

class RequestTracer(object):
    def hasFather(self, instance=None, fatherName=None, cls=None):
        if (not instance) and (not cls):
            return False
        if instance:
            cls = getattr(instance, "__class__")
        name = getattr(cls, "__name__")
        if fatherName == name:
            return True
        if hasattr(cls, "__base__"):
            cls = getattr(cls, "__base__")
            return self.hasFather(fatherName=fatherName, cls=cls)
        return False

    def findRequestId(self,frame=None):
        try:
            if not frame:
                frame = inspect.currentframe()
            locals = frame.f_locals
            if "self" in locals.keys():
                instance = locals["self"]
                if self.hasFather(instance=instance, fatherName="APIView"):
                    if hasattr(locals,"request"):
                        req = locals["request"]
                        requestId = req.META.get("HTTP_X_MANO_REQUEST_ID")
                        return requestId
            if frame.f_back:
                return  self.findRequestId(frame.f_back)
            return ""
        except Exception as e:
            logger.error(e)
            return ""
