from flask import Flask
from app.camera import CameraStream
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from roboclass import MotorDriver

app = Flask(__name__)
motor = MotorDriver()
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
cap = CameraStream().start() ###cv2.VideoCapture(0)

from app import routes, models