from flask import Flask, render_template, request
from server_code.options.get_strategies import get_strategies

app = Flask(__name__)

@app.route("/")
def render_home():
  return render_template('home.html')

@app.route("/options/")
def render_options():
  return render_template('options_suggestor.html')

@app.route("/options/get_strategies/")
def fetch_strategies():
  strategies = get_strategies(1000)
  return strategies
  

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
