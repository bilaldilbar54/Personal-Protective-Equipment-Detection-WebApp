import os
import cv2
from flask import Flask, render_template, request, redirect, Response, jsonify, session
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, DecimalRangeField, IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, NumberRange
from Yolo_Construction_Video_Detection import const_video_detection
from Yolo_Medical_Video_Detection import med_video_detection
from Yolo_Custom_Video_Detection import custom_video_detection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gbc-fsds'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Run')


def const_generate_frames(path_x=''):
    yolo_output = const_video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def med_generate_frames(path_x=''):
    yolo_output = med_video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def custom_generate_frames(path_x=''):
    yolo_output = custom_video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def const_generate_frames_web(path_x):
    yolo_output = const_video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def med_generate_frames_web(path_x):
    yolo_output = med_video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def custom_generate_frames_web(path_x):
    yolo_output = custom_video_detection(path_x)
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


@app.route('/const_webcam_det', methods=['GET', 'POST'])
def const_webcam():
    session.clear()
    return render_template('const_webcam_detection.html')


@app.route('/const_video_det', methods=['GET', 'POST'])
def const_video():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('const_video_detection.html', form=form)


@app.route('/const_video_feed', methods=['GET', 'POST'])
def const_video_feed():
    return Response(const_generate_frames(path_x=session.get('video_path', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/const_webcam_feed', methods=['GET', 'POST'])
def const_webcam_feed():
    return Response(const_generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/med_webcam_det', methods=['GET', 'POST'])
def med_webcam():
    session.clear()
    return render_template('med_webcam_detection.html')


@app.route('/med_video_det', methods=['GET', 'POST'])
def med_video():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('med_video_detection.html', form=form)


@app.route('/med_video_feed', methods=['GET', 'POST'])
def med_video_feed():
    return Response(med_generate_frames(path_x=session.get('video_path', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/med_webcam_feed', methods=['GET', 'POST'])
def med_webcam_feed():
    return Response(med_generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/custom_webcam_feed', methods=['GET', 'POST'])
def custom_webcam_feed():
    return Response(custom_generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/custom_webcam_det', methods=['GET', 'POST'])
def custom_webcam():
    session.clear()
    return render_template('custom_webcam_detection.html')


@app.route('/custom_video_det', methods=['GET', 'POST'])
def custom_video():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('custom_video_detection.html', form=form)


@app.route('/custom_video_feed', methods=['GET', 'POST'])
def custom_video_feed():
    return Response(custom_generate_frames(path_x=session.get('video_path', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    session.clear()
    return render_template('contact_us.html')


if __name__ == '__main__':
    app.run(debug=True)
