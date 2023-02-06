import cv2
from flask import render_template, flash, redirect, url_for, Response
from app import app, cap
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)


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


# @app.route('/forward/<int:inchesCount>')
# def forward(inchesCount):
#     motor.MotorForward(inchesCount)
#     return "Going forward"
#     return jsonify({'forward': inchesCount, 'success': True})
#     motor.MotorStop(0)
#     motor.MotorStop(1)
#
#
# @app.route("/reverse/<int:inchesCount>")
# def reverse(inchesCount):
#     motor.MotorReverse(inchesCount)
#     return "Going back"
#     return jsonify({'reverse': inchesCount, 'success': True})
#     motor.MotorStop(0)
#     motor.MotorStop(1)
#
#
# @app.route("/left/<int:turnCount>")
# def left(turnCount):
#     motor.MotorLeft(turnCount)
#     return "Going left"
#     return jsonify({'left': turnCount, 'success': True})
#     motor.MotorStop(0)
#     motor.MotorStop(1)
#
#
# @app.route("/right/<int:turnCount>")
# def right(turnCount):
#     motor.MotorRight(turnCount)
#     return "Going right"
#     return jsonify({'right': turnCount, 'success': True})
#     motor.MotorStop(0)
#     motor.MotorStop(1)
#
#
# @app.route("/stop")
# def stop():
#     motor.MotorStop(0)
#     motor.MotorStop(1)
#     return jsonify({'stop': 0, 'success': True})


def gen_frame():
    """Video streaming generator function."""
    while cap:
        frame = cap.read()
        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')  # concate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
