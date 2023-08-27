from conf.database import Config
from gevent.pywsgi import WSGIServer
from factory import create_app
from flask_cors import CORS
app = create_app()
app.config['CORS_METHODS'] = Config.CORS_METHODS
app.config['CORS_ORIGINS'] = Config.CORS_ORIGINS
CORS(app)


if __name__ == '__main__' :
    """
    uncomment them when you want to debug 
    app.debug=True
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
    """

    http_server = WSGIServer(('0.0.0.0', int(Config.PORT)), app)
    http_server.serve_forever()
    print(f"Server running locally on port : {int(Config.PORT)}")
