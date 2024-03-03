import traceback


class Log500ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        print("\n----intercepted 500 error stack trace----")
        print(exception)
        print(type(exception))
        tb = exception.__traceback__
        print(traceback.format_exception(type(exception), exception, tb))
        print("----\n")
        return None
