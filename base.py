from tornado.web import RequestHandler


class BaseHandler(RequestHandler):


    per_page = 24
    user = None
    session_key = None
    input = None
    db = None
    yd = None

    def data_received(self, chunk):
        super(BaseHandler, self).data_received(chunk)

    def initialize(self):

        setattr(self, 'db', self.application.settings['db'])
        setattr(self, 'yd', self.application.settings['yd'])
    
    def prepare(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.set_header("Access-Control-Expose-Headers", "Origin, Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Headers", 'Origin, Content-Type, Authorization')