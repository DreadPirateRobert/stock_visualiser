import tornado.ioloop
import tornado.web

from stock_api import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Stock Visualisation, ")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/stock", stock),
        (r"/index", index),
    ])

if __name__ == "__main__":
    app = make_app()
    print ('Listening on port: 8888')
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    
#API key = PTJUBNEO2HLMPSQD