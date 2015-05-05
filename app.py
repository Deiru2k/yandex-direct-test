from tornado.web import Application
from motor import MotorClient
from settings import settings
from tornado.ioloop import IOLoop
from routes import v1
from yandex.direct import YandexDirect

client = MotorClient()
db = client['yandex-test']
yd = YandexDirect(**settings['yandex'])

app = Application(handlers=v1.routes, settings=settings, debug=True, db=db, yd=yd)

if __name__ == '__main__':

    print("Listening on 8080")
    if len(v1.routes) > 0:
        print("Routes:")
        for route in v1.routes:
            print("\t" + route[0])
    else:
        print("No Routes Defined")
    app.listen(8080)
    IOLoop.instance().start()
