import logging
import threading
import uuid

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

local = threading.local()


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.requestid = getattr(local, 'requestId', "none")
        return True


class RequestIdMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if "HTTP_X_MANO_REQUEST_ID" not in request.META.keys():
            requestId = uuid.uuid4().hex
            local.requestId = requestId
            request.META.update({'HTTP_X_MANO_REQUEST_ID': requestId})
        else:
            requestId = request.META.get('HTTP_X_MANO_REQUEST_ID', '')
            local.requestId = requestId

    def process_response(self, request, response):
        if "HTTP_X_MANO_REQUEST_ID" in request.META.keys():
            response['X-MANO-Request-ID'] = request.META.get('HTTP_X_MANO_REQUEST_ID', '')
        try:
            del local.requestId
        except AttributeError:
            pass
        return response
