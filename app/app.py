from flask import Flask, render_template, request, jsonify, url_for, json, redirect, make_response
import os
import requests

# create flask app
app = Flask(__name__)

@app.route('/')
def index():
  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(SITE_ROOT, "data", "data.json")
  data = json.load(open(json_url))
  return render_template('index.html', todos=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    url = 'https://hunter-todo-api.herokuapp.com/auth'
    payload = {"username":username}
    r = requests.post(url, json=payload)
    print("Retrieved Cookie: ", r.cookies)
    jar = r.cookies
    
    if r.status_code == 200:
      todo_items_url = 'https://hunter-todo-api.herokuapp.com/todo-item'
      res = requests.get(todo_items_url, cookies=jar)
      print(res.text)
      todo_list = res.json()

      response = make_response(render_template('index.html', username=username, todo_list=todo_list))
      key = 'sillyauth'
      value = r.cookies[key]
      print(key, value)
      response.set_cookie(key, value)
      return response

  return  render_template('login.html')

@app.route('/createuser', methods=['GET', 'POST'])
def createUser():
  if request.method == 'POST':
    username = request.form['username']
    url = 'https://hunter-todo-api.herokuapp.com/user'
    payload = {'username': username}
    r = requests.post(url, json=payload)
    print(r.text)
    return render_template('login.html')
  return render_template('createUser.html')

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, threaded=True, debug=True)