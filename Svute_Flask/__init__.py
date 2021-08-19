﻿###################### IMPORT ######################
# Update date: 07/08/2021
# Written by ngtrdai
# https://github.com/ngtrdai
import pyrebase
from flask import Flask
from flask_security.core import Security
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flaskext.markdown import Markdown
from flask_toastr import Toastr
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect
from flask_codemirror import CodeMirror
app = Flask(__name__)
# Khoi tao database
db = SQLAlchemy()
bcrypt = Bcrypt()
ckeditor = CKEditor()
DB_NAME = "database.db"

# Khoi tao LoginManager
loginManager = LoginManager()
loginManager.login_view = 'users.login'
loginManager.login_message = 'Xin vui lòng đăng nhập!'
loginManager.login_message_category = 'info'

# Khoi tao Firebase server
config = {
    "apiKey": "AIzaSyCM5TdQ8YJhkGfRtrk2p1Ps2LUyhtNYUnY",
    "authDomain": "svute-flask.firebaseapp.com",
    "databaseURL": "https://svute-flask-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "svute-flask",
    "storageBucket": "svute-flask.appspot.com",
    "messagingSenderId": "190697851265",
    "appId": "1:190697851265:web:d9638fa3765cb72ed84080",
    "measurementId": "G-R9FSK0DV4B"
}
firebase =  pyrebase.initialize_app(config)
storage = firebase.storage()



def Create_Database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

# Khoi tao Flask
def Create_App(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    md = Markdown(app, auto_escape=False, safe_mode=True)
    toastr = Toastr(app)
    codemirror = CodeMirror(app)
    ckeditor.init_app(app)
    csrf = CSRFProtect(app)    
    admin = Admin(app,template_mode='bootstrap4')
    from Svute_Flask.users.routes import users
    from Svute_Flask.main.routes import main
    from Svute_Flask.posts.routes import posts
    from Svute_Flask.notes.routes import notes
    from Svute_Flask.codes.routes import codes
    from Svute_Flask.calendars.routes import calendars
    from Svute_Flask.converts.routes import converts
    from Svute_Flask.models import User, Post,Role, Note, Comments, Category, Code, Calendar, Category_calendar, AdminView
    Create_Database(app)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(notes)
    app.register_blueprint(codes)
    app.register_blueprint(calendars)
    app.register_blueprint(converts)
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Post, db.session))
    admin.add_view(AdminView(Note, db.session))
    admin.add_view(AdminView(Comments, db.session))
    admin.add_view(AdminView(Category, db.session)) 
    admin.add_view(AdminView(Code, db.session))
    admin.add_view(AdminView(Calendar, db.session))
    admin.add_view(AdminView(Category_calendar, db.session))
    admin.add_view(AdminView(Role, db.session))
    return app  
