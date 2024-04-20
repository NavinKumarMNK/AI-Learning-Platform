import traceback
from pprint import pprint
import pdb


class Log500ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        pprint("\n----intercepted 500 error stack trace----")
        pprint(exception)
        pprint(type(exception))
        tb = exception.__traceback__
        pprint(traceback.format_exception(type(exception), exception, tb))
        pprint("----\n")
        return None


class DebugPauseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pdb.set_trace()
        response = self.get_response(request)
        return response
