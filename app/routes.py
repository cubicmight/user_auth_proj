import cv2
from flask import render_template, flash, redirect, url_for, Response, jsonify
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
        moves.append("Welcome " + user + "\n")
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


moves = ['test 1', 'test 2']


@app.route('/logs')
def logs():
    return moves


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
    username = current_user.username ##use this username instead of getting passed in for security
    motor.MotorForward(inchesCount)
    moves.append(jsonify({'forward': inchesCount, 'success': True}))
    moves.append(username + "is moving forward" + inchesCount)
    motor.MotorStop(0)
    motor.MotorStop(1)
    return "Going forward"
    # return jsonify({'forward': inchesCount, 'success': True})
    # motor.MotorStop(0)
    # motor.MotorStop(1)


@app.route("/reverse/<user>/<int:inchesCount>")
def reverse(user, inchesCount):
    # motor.MotorReverse(inchesCount)
    # moves.append(jsonify({'reverse': inchesCount, 'success': True}))
    # return "Going back"
    # return jsonify({'reverse': inchesCount, 'success': True})
    # motor.MotorStop(0)
    # motor.MotorStop(1)
    motor.MotorReverse(inchesCount)
    moves.append(jsonify({'reverse': inchesCount, 'success': True}))
    moves.append(user + "is moving reverse" + inchesCount)
    motor.MotorStop(0)
    motor.MotorStop(1)
    return "Going reverse"

@app.route("/left/<user>/<int:turnCount>")
def left(user, turnCount):
    # motor.MotorLeft(turnCount)
    # return "Going left"
    # return jsonify({'left': turnCount, 'success': True})
    # motor.MotorStop(0)
    # motor.MotorStop(1)
    motor.MotorLeft(turnCount)
    moves.append(jsonify({'left': turnCount, 'success': True}))
    moves.append(user + "is turning left" + turnCount * 90)
    motor.MotorStop(0)
    motor.MotorStop(1)
    return "Going left"

@app.route("/right/<user>/<int:turnCount>")
def right(user, turnCount):
    # motor.MotorRight(turnCount)
    # return "Going right"
    # return jsonify({'right': turnCount, 'success': True})
    # motor.MotorStop(0)
    # motor.MotorStop(1)
    motor.MotorRight(turnCount)
    moves.append(jsonify({'right': turnCount, 'success': True}))
    moves.append(user + "is turning right" + turnCount * 90)
    motor.MotorStop(0)
    motor.MotorStop(1)
    return "Going right"

@app.route("/special/<user>")
def special(user):
    motor.MotorForward(10)
    moves.append(jsonify({'forward': 10, 'success': True}))
    moves.append(user + "is moving forward 10")
    motor.MotorRight(1)
    moves.append(jsonify({'right': 1, 'success': True}))
    moves.append(user + "is turning right 90 degrees")
    motor.MotorForward(10)
    moves.append(jsonify({'forward': 10, 'success': True}))
    moves.append(user + "is moving forward 10")
    motor.MotorLeft(1)
    moves.append(jsonify({'left': 1, 'success': True}))
    moves.append(user + "is turning left 90 degrees")

# @app.route("/stop/<str:user>")
# def stop(user):
#     # motor.MotorStop(0)
#     # motor.MotorStop(1)
#     # return jsonify({'stop': 0, 'success': True})
#     # moves.append(jsonify({'stop': turnCount, 'success': True}))
#     moves.append(user + "is stopping the robot")
#     motor.MotorStop(0)
#     motor.MotorStop(1)
#     return "Stopping"

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
