from flask import Flask, render_template, request, jsonify, url_for, json
import os

# create flask app
app = Flask(__name__)

@app.route('/')
def home():
  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(SITE_ROOT, "data", "data.json")
  data = json.load(open(json_url))
  return render_template('index.html', todos=data)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, threaded=True, debug=True)