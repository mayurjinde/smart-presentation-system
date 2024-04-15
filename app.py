from flask import Flask ,render_template,jsonify, send_from_directory, Response
from flask_restful import Api, Resource, reqparse
from flask import request
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from camera import Video
import os 
from flask import * 
import pyautogui
# app.secret_key = "abc"  


TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')
app = Flask(__name__,template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = "abc"


@app.route("/")
def hello_world():
    return render_template('front_page.html')
    # return "<p>Hello, World!</p>"


@app.route("/start")
def hello_world1():
    return render_template('index.html')

@app.route("/display_ppt",methods=['GET','POST'])
def displayPPT():
    return render_template('face.html')
def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')

def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/upload",methods=['GET', 'POST'])  
def uploadfile():
    if request.method == 'POST':
        if 'file' in request.files:
            f = request.files['file']
            filePath = "./Temp/" + f.filename
            f.save(filePath)
            # flash("you are successfuly logged in")
            # flash("you are successfuly logged in")
            pyautogui.press('f11')
            return render_template('face.html')
            # return "good"
        else:
            print(request.files)
            return "fail" 

# @app.route('/upload', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'


# @app.route("/display_ppt",methods=['GET', 'POST'])  
# def dspl():
#     return "<p>Hello, World!</p>" 
if __name__=="__main__":
    app.run(debug=True)