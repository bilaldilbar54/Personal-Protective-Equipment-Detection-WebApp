from flask import Flask, render_template, request, redirect, Response, jsonify, session
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, DecimalRangeField, IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, NumberRange
import os
import cv2
from Yolo_Video_Detection import video_detection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gbc-fsds'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Run')


def generate_frames(path_x=''):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    return render_template('login.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    session.clear()
    return render_template('home_page.html')


@app.route('/construction-ppe', methods=['GET', 'POST'])
def construction_ppe():
    session.clear()
    return render_template('construction-ppe.html')


@app.route('/medical-ppe', methods=['GET', 'POST'])
def medical_ppe():
    session.clear()
    return render_template('medical-ppe.html')


@app.route('/webcam_det', methods=['GET', 'POST'])
def webcam():
    session.clear()
    return render_template('webcam_detection.html')


@app.route('/video_det', methods=['GET', 'POST'])
def video():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('video_detection.html', form=form)


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    return Response(generate_frames(path_x=session.get('video_path', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/webcam_feed', methods=['GET', 'POST'])
def webcam_feed():
    return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    session.clear()
    return render_template('contact_us.html')


if __name__ == '__main__':
    app.run(debug=True)
