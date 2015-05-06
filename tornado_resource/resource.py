import traceback
from tornado import httputil
from tornado.web import RequestHandler, HTTPError
from bson import json_util as json
from tornado.gen import coroutine
from .codes import codes
from yandex.direct import YandexDirectError


class Resource(RequestHandler):

    name = None
    schema = None
    per_page = 24
    Handler = RequestHandler

    def data_received(self, chunk):
        super(Resource, self).data_received(chunk)

    def initialize(self, **kwargs):
        setattr(self, "instance", self.Handler(self.application, self.request, **kwargs))
        setattr(self.instance, "auto_finish", False)

    def prepare(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.set_header("Access-Control-Expose-Headers", "Origin, Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Headers", 'Origin, Content-Type, Authorization')
        self.set_header("Content-Type", "application/json")

    def error(self, code, message, data=None, errors=None):
        self.set_status(code)
        response = {"status": "error", "code": code, "message": message, "data": data}
        if errors:
            response['errors'] = errors
        self.write(json.dumps(response))
        self.finish()

    def success(self, code=200, data=None):
        self.set_status(code)
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({"status": "success", "code": code, "data": data}))
        self.finish()

    @coroutine
    def handle_request(self, method="get", *args, **kwargs):
        try:
            response = yield self.instance.__getattribute__(method)(*args, **kwargs)
            if type(response) == tuple:
                self.success(response[0], response[1])
            else:
                print(response)
                raise Exception("Returns must include both status code and return data")
        except APIError as error:
            self.error(error.code, error.message, error.data, error.errors)
            return
        except HTTPError as error:
            self.error(error.status_code, httputil.responses.get(error.status_code, 'unknown error'))
        except YandexDirectError as error:
            self.error(500, error.message, error.code, error.error)
        except Exception:
            self.error(500, "Interal Server Error")
            print(traceback.format_exc())



    @coroutine
    def get(self, *args, **kwargs):
        yield self.handle_request("get", *args, **kwargs)
        return

    @coroutine
    def post(self, *args, **kwargs):
        yield self.handle_request("post", *args, **kwargs)
        return
    
    @coroutine
    def put(self, *args, **kwargs):
        yield self.handle_request("put", *args, **kwargs)
        return

    @coroutine
    def patch(self, *args, **kwargs):
        yield self.handle_request("patch", *args, **kwargs)
        return
    
    @coroutine
    def delete(self, *args, **kwargs):
        yield self.handle_request("delete", *args, **kwargs)
        return

    @coroutine
    def options(self, *args, **kwargs):
        yield self.handle_request("options", *args, **kwargs)
        return


class APIError(Exception):
    
    def __init__(self, code=500, data=None, message=None, errors=None):
        super(Exception, self).__init__(message)
        message = codes.get(code, "Undefined Server Error") if not message else message
        self.errors = errors
        self.code = code
        self.data = data
        self.message = message