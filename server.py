from gevent.pywsgi import WSGIServer
from main import app 
import ssl

# serve with https

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()
