from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0817janice@localhost/petservice'
db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)
##connect mySQL


#import mysql.connector
#mydb = mysql.connector.connect(
#    host = "localhost",
#    user = "root",
#    password = "++++"
#)

#my_cursor = mydb.cursor()
#my_cursor.execute("CREATE DATABASE test")
#my_cursor.execute("SHOW DATABASES")
#for db in my_cursor:
#    print(db)


login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from backend import routes