from conf.database import Config
from gevent.pywsgi import WSGIServer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from factory import create_app
from flask_cors import CORS

app = create_app()
app.config["CORS_METHODS"] = Config.CORS_METHODS
app.config["CORS_ORIGINS"] = [Config.CORS_ORIGINS]
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

if __name__ == "__main__":
    """
    uncomment them when you want to debug
    app.debug=True
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
    """

    http_server = WSGIServer(("127.0.0.1", int(Config.PORT)), app)
    http_server.serve_forever()
    print(f"Server running locally on port : {int(Config.PORT)}")
