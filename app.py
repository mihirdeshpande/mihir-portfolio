from flask import Flask, render_template, request

app = Flask(__name__)


@app.before_request
def before_request():
  print("IP Address: " + request.remote_addr)
  print("User Agent: " + request.headers.get('User-Agent'))

@app.route("/")
def hellow_world():
  return render_template('home.html')

@app.route("/test_config/")
def test_config():
  with open("/etc/secrets/try.txt", "r") as file:
    # Step 2: Read the contents of the file
    content = file.read()
  return content
  

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
