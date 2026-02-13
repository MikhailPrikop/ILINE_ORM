#!/usr/bin/env python

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", 'postgresql://postgres@localhost/postgres')

db = SQLAlchemy(app)
