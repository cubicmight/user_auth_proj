import json
import os.path

import cv2
import cvzone
from flask import render_template, flash, redirect, url_for, Response, request
from flask.scaffold import setupmethod
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, UserLogData

from roboclass import MotorDriver

motor = MotorDriver()
current_direction_image = None


@setupmethod
@app.before_first_request
def clear_user_data_table():
    global current_direction_image
    UserLogData.query.delete()
    db.session.commit()
    basedir = os.path.abspath(os.path.dirname(__file__))

    image_file_name = "direction_arrow.png"
    full_image_path = os.path.join(basedir, 'static', image_file_name)
    if os.path.exists(full_image_path):
        # validate the image
        current_direction_image = cv2.imread(full_image_path, cv2.IMREAD_UNCHANGED)
    else:
        print("cannot find image")


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/logs')
def logs():
    data = db.session.query(UserLogData.data).all()
    row = []
    for d in data:
        row.append(d[0])
    return row


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/forward/<user>/<int:inchesCount>')
def forward(user, inchesCount):
    username = current_user.username  ##use this username instead of getting passed in for security
    motor.MotorForward(inchesCount)

    details = {
        "user": username,
        "success": True,
        "movement": "Moving %s, by %d" % ('forward', inchesCount)
    }

    r = json.dumps(details)
    data = UserLogData(data=r)
    db.session.add(data)
    db.session.commit()

    motor.MotorStop(0)
    motor.MotorStop(1)

    return details


@app.route("/reverse/<user>/<int:inchesCount>")
def reverse(user, inchesCount):
    username = current_user.username  ##use this username instead of getting passed in for security
    motor.MotorReverse(inchesCount)

    details = {
        "user": username,
        "success": True,
        "movement": "Moving %s, by %d" % ('reverse', inchesCount)
    }
    data = UserLogData(data=json.dumps(details))

    db.session.add(data)
    db.session.commit()

    motor.MotorStop(0)
    motor.MotorStop(1)

    return details


@app.route("/left/<user>/<int:turn_count>")
def left(user, turn_count):

    username = current_user.username  ##use this username instead of getting passed in for security
    motor.MotorLeft(turn_count)

    details = {
        "user": username,
        "success": True,
        "movement": "Moving %s, by %d" % ('left', turn_count * 90)
    }
    data = UserLogData(data=json.dumps(details))

    db.session.add(data)
    db.session.commit()

    motor.MotorStop(0)
    motor.MotorStop(1)
    global current_direction_image
    current_direction_image = cvzone.rotateImage(current_direction_image, 90 * turn_count)

    return details


@app.route("/right/<user>/<int:turn_count>")
def right(user, turn_count):


    username = current_user.username  ##use this username instead of getting passed in for security
    motor.MotorRight(turn_count)

    details = {
        "user": username,
        "success": True,
        "movement": "Moving %s, by %d" % ('right', turn_count)
    }
    data = UserLogData(data=json.dumps(details))
    db.session.add(data)
    db.session.commit()

    motor.MotorStop(0)
    motor.MotorStop(1)
    global current_direction_image
    current_direction_image = cvzone.rotateImage(current_direction_image, 270 * turn_count)

    return details


def gen_frame():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)
    while cap:
        (grabbed, frame) = cap.read()
        if grabbed:
            global current_direction_image
            imgResult = cvzone.overlayPNG(frame, current_direction_image, [600, 400])  # 750, 400
            ret, buffer = cv2.imencode('.jpg', imgResult)

            if ret:
                convert = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')  # concate frame one by one and show result
    cap.release()


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
