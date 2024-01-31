from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html.jinja')