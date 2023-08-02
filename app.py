# from re import template
import os
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from application.database import db
from application.models import *
from application.config import LocalDevelopmentConfig

# import model from folder
from face_recognition_and_liveness.face_liveness_detection.face_recognition_liveness_app import recognition_liveness

# app = Flask(__name__)
# app.secret_key = 'web_app_for_face_recognition_and_liveness' 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Users(db.Model):
#     __tablename__ = "users"
#     username = db.Column(db.String(100), primary_key=True)
#     name = db.Column(db.String(100))
#     password = db.Column(db.String(100))

app = None

def create_app():
  app = Flask(__name__, template_folder="templates")
  app.secret_key = 'web_app_for_face_recognition_and_liveness'
  if os.getenv('ENV', "development") == "production":
    raise Exception("Currently no production config is setup.")
  else:
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
  db.init_app(app)
  app.app_context().push()
  return app

app = create_app()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('name', None)
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        # user = {username:'rajesh',password:'123456789'}
        print(user)
        if user is not None and user.password == password:
            session['name'] = user.name # store variable in session
            detected_name, label_name = recognition_liveness('face_recognition_and_liveness/face_liveness_detection/liveness.model',
                                                    'face_recognition_and_liveness/face_liveness_detection/label_encoder.pickle',
                                                    'face_recognition_and_liveness/face_liveness_detection/face_detector',
                                                    'face_recognition_and_liveness/face_recognition/encoded_faces.pickle',
                                                    confidence=0.7)
            if user.name == detected_name and label_name == 'real':
                return redirect("https://earnest-entremet-6c5225.netlify.app/")
            else:
                return render_template('login_page.html', invalid_user=True, username=username)
        else:
            return render_template('login_page.html', incorrect=True)

    return render_template('login_page.html')

@app.route('/main', methods=['GET'])
def main():
    name = session['name']
    return render_template('main_page.html', name=name)

if __name__ == '__main__':
    # db.create_all()

    # add users to database

    # new_user = Users(username='Akshay', password='123456789', name='Akshay')
    # db.session.add(new_user)

   

    app.run(host='0.0.0.0',port=5000,debug=True)