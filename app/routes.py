import cv2
from flask import render_template, flash, redirect, url_for, Response, jsonify, request
from flask.scaffold import setupmethod
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, UserLogData


# from roboclass import MotorDriver

# motor = MotorDriver()

@setupmethod
@app.before_first_request
def clear_user_data_table():
    UserLogData.query.delete()
    db.session.commit()


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
    # motor.MotorForward(inchesCount)
    data = UserLogData(data="forward: %d, success: %s\n" % (inchesCount, True))
    db.session.add(data)
    # db.session.commit()
    data = UserLogData(data=username + " is moving forward " + str(inchesCount) + "\n")
    db.session.add(data)
    db.session.commit()
    # motor.MotorStop(0)
    # motor.MotorStop(1)
    return jsonify({'forward': inchesCount, 'success': True})


@app.route("/reverse/<user>/<int:inchesCount>")
def reverse(user, inchesCount):
    username = current_user.username  ##use this username instead of getting passed in for security
    # motor.MotorReverse(inchesCount)
    data = UserLogData(data="reverse: %d, success: %s\n" % (inchesCount, True))
    db.session.add(data)
    # db.session.commit()
    data = UserLogData(data=username + " is reversing " + str(inchesCount) + "\n")
    db.session.add(data)
    db.session.commit()
    # motor.MotorStop(0)
    # motor.MotorStop(1)
    return jsonify({'reverse': inchesCount, 'success': True})


@app.route("/left/<user>/<int:turnCount>")
def left(user, turnCount):
    username = current_user.username  ##use this username instead of getting passed in for security
    # motor.MotorLeft(turnCount)
    data = UserLogData(data="left: %d, success: %s\n" % (turnCount, True))
    db.session.add(data)
    # db.session.commit()
    data = UserLogData(data=username + " is moving left " + str(turnCount) + "\n")
    db.session.add(data)
    db.session.commit()
    # motor.MotorStop(0)
    # motor.MotorStop(1)
    return jsonify({'left': turnCount * 90, 'success': True})


@app.route("/right/<user>/<int:turnCount>")
def right(user, turnCount):
    username = current_user.username  ##use this username instead of getting passed in for security
    # motor.MotorRight(turnCount)
    data = UserLogData(data="right: %d, success: %s\n" % (turnCount, True))
    db.session.add(data)
    # db.session.commit()
    data = UserLogData(data=username + " is moving right " + str(turnCount) + "\n")
    db.session.add(data)
    db.session.commit()
    # motor.MotorStop(0)
    # motor.MotorStop(1)

    # @app.route("/special")
    # def special(user):
    #     username = current_user.username  ##use this username instead of getting passed in for security
    #     motor.MotorForward(10)
    #     data = UserLogData(data="forward: %d, success: %s\n" % (10, True))
    #     db.session.add(data)
    #     db.session.commit()
    #     data = UserLogData(data=username + " is moving forward " + str(10) + "\n")
    #     db.session.add(data)
    #     db.session.commit()
    #     motor.MotorStop(0)
    #     motor.MotorStop(1)
    #     username = current_user.username  ##use this username instead of getting passed in for security
    #     motor.MotorLeft(turnCount)
    #     data = UserLogData(data="left: %d, success: %s\n" % (1, True))
    #     db.session.add(data)
    #     db.session.commit()
    #     data = UserLogData(data=username + " is turning " + str(90) + "\n")
    #     db.session.add(data)
    #     db.session.commit()
    #     motor.MotorStop(0)
    #     motor.MotorStop(1)
    #     username = current_user.username  ##use this username instead of getting passed in for security
    #     motor.MotorForward(10)
    #     data = UserLogData(data="forward: %d, success: %s\n" % (10, True))
    #     db.session.add(data)
    #     db.session.commit()
    #     data = UserLogData(data=username + " is moving forward " + str(10) + "\n")
    #     db.session.add(data)
    #     db.session.commit()
    #     motor.MotorStop(0)
    #     motor.MotorStop(1)
    #     username = current_user.username  ##use this username instead of getting passed in for security
    #     motor.MotorRight(turnCount)
    #     data = UserLogData(data="right: %d, success: %s\n" % (1, True))
    #     db.session.add(data)
    #     db.session.commit()
    #     data = UserLogData(data=username + " is moving right " + str(90) + "\n")
    #     db.session.add(data)
    #     db.session.commit()
    #     motor.MotorStop(0)
    #     motor.MotorStop(1)
    # motor.MotorRight(1)
    # moves.append(jsonify({'right': 1, 'success': True}))

    # motor.MotorForward(10)
    # moves.append(jsonify({'forward': 10, 'success': True}))
    # motor.MotorLeft(1)
    # moves.append(jsonify({'left': 1, 'success': True}))
    return jsonify({'special': True, 'success': True})


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


current_image = cv2.imread(
    "app/arrowpng.parspng.com-18 (1) resizer.png",
    cv2.IMREAD_UNCHANGED)


def gen_frame():
    """Video streaming generator function."""
    global current_image
    cap = cv2.VideoCapture(0)
    while cap:
        (grabbed, frame) = cap.read()
        if grabbed:
            # tester = cv2.imwrite(frame, current_image)
            ret, buffer = cv2.imencode('.jpg', frame)

            if ret:
                convert = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')  # concate frame one by one and show result
    cap.release()
    cv2.destroyAllWindows()


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# background = cv2.imread('field.jpg')
# overlay = cv2.imread('dice.png')
#
# added_image = cv2.addWeighted(background,0.4,overlay,0.1,0)
#
# cv2.imwrite('combined.png', added_image)

# def gen_frame():
#     """Video streaming generator function."""
#     global current_image
#     while cap:
#         img = cap.read()
#         imgResult = cvzone.overlayPNG(img, current_image, [450, 300])  ##450 300
#         cv2image = cv2.cvtColor(imgResult, cv2.COLOR_BGR2RGBA)
#         imgX = Image.fromarray(cv2image)
#         imgtk = ImageTk.PhotoImage(image=imgX)
#         robotPOV.imgtk = imgtk
#         robotPOV.configure(image=imgtk)
#         convert = cv2.imencode('.jpg', frame)[1].tobytes()
#         yield (b'--img\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')  # concate frame one by one and show result
#
#
# @app.route('/video_feed')
# def video_feed():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return Response(gen_frame(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
