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
    if username:
      url = 'https://hunter-todo-api.herokuapp.com/auth'
      payload = {"username":username}
      r = requests.post(url, json=payload)
      print("Retrieved Cookie: ", r.cookies)
      jar = r.cookies
      
      #if authenticated then get user's todo list
      if r.status_code == 200:
        todo_list = get_todo_list(jar)

        #store cookie to server 
        response = make_response(render_template('index.html', username=username, todo_list=todo_list))
        key = 'sillyauth'
        val = r.cookies[key]
        #print(key, val)
        response.set_cookie(key, val)
        response.set_cookie('username', username)
        return response

  return render_template('login.html')

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

@app.route('/add', methods=['POST'])
def add():
  if request.method == 'POST':
    #retrieve stored cookie
    username = request.cookies.get('username')
    key = 'sillyauth'
    val = request.cookies.get(key)
    jar = requests.cookies.RequestsCookieJar()
    jar.set(key, val, domain='hunter-todo-api.herokuapp.com')
   
    #post the new item
    item = request.form['new_todo_item']
    #print(item)
    url = 'https://hunter-todo-api.herokuapp.com/todo-item'
    payload = {'content':item}
    r = requests.post(url, cookies=jar, json=payload)
    #print(r.status_code)

    #get updated todolist
    todo_list = get_todo_list(jar)

    #render index with new item
    if r.status_code == 201 and todo_list:
      return render_template('index.html', username=username, todo_list=todo_list)

  return render_template('login.html')
    
@app.route('/completed', methods=['POST'])
def completed():
  if request.method == 'POST':
    #retrieve stored cookie
    username = request.cookies.get('username')
    #print(username)
    key = 'sillyauth'
    val = request.cookies.get(key)
    jar = requests.cookies.RequestsCookieJar()
    jar.set(key, val, domain='hunter-todo-api.herokuapp.com')
    #print(jar)

    #get item id
    if request.form.get('item_id'):
      item_id = request.form['item_id']
      print("item_id", item_id)

      #mark item as completed
      url = 'https://hunter-todo-api.herokuapp.com/todo-item/' + item_id
      payload = {"completed":True}
      r = requests.put(url, json=payload, cookies=jar)

      #get updated todolist
      todo_list = get_todo_list(jar)

      return render_template('index.html', username=username, todo_list=todo_list)
  

  username = request.cookies.get('username')
  todo_list = get_todo_list(jar)
  return render_template('index.html', username=username, todo_list=todo_list)

@app.route('/delete', methods=['POST'])
def delete():
  if request.method == 'POST':
    #retrieve stored cookie
    username = request.cookies.get('username')
    key = 'sillyauth'
    val = request.cookies.get(key)
    jar = requests.cookies.RequestsCookieJar()
    jar.set(key, val, domain='hunter-todo-api.herokuapp.com')
   
    #get item id
    if request.form.get('item_id'):
      item_id = request.form['item_id']
      #print("item_id", item_id)

      #delete item
      url = 'https://hunter-todo-api.herokuapp.com/todo-item/' + item_id
      r = requests.delete(url, cookies=jar)

      #get updated todolist
      todo_list = get_todo_list(jar)

      return render_template('index.html', username=username, todo_list=todo_list)
  

  username = request.cookies.get('username')
  todo_list = get_todo_list(jar)
  return render_template('index.html', username=username, todo_list=todo_list)

def get_todo_list(cookie_jar):
  todo_items_url = 'https://hunter-todo-api.herokuapp.com/todo-item'
  r = requests.get(todo_items_url, cookies=cookie_jar)
  return r.json()


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, threaded=True, debug=True)