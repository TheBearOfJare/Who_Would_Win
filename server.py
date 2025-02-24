from gevent.pywsgi import WSGIServer
from main import app  # Import your Flask app

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()