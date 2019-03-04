from flask import Flask, render_template, request, jsonify, url_for, json, redirect, make_response
import os
import requests
from app.models import User, Todo_item
from app import app

@app.route('/')
def index():
  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(SITE_ROOT, "data", "data.json")
  data = json.load(open(json_url))
  return render_template('index.html', todos=data)

@app.route('/login', methods=['GET', 'POST'])
def login():

  return render_template('login.html')

@app.route('/logout')
def logout():
  return render_template('logout.html')

@app.route('/createuser', methods=['GET', 'POST'])
def createUser():
  if request.method == 'POST':
    username = request.form['username']
    
  return render_template('createUser.html')

@app.route('/add', methods=['POST'])
def add():

  return render_template('login.html')
    
@app.route('/completed', methods=['POST'])
def completed():
 
  return render_template('index.html')

@app.route('/delete', methods=['POST'])
def delete():

  return render_template('index.html')

def get_todo_list(cookie_jar):

  return 

