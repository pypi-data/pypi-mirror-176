from flask import Flask
from threading import Thread

app = Flask(__name__)

def start(message=None):
  if message == None:
    message = '<html><head><style>*{font-family:system-ui;}</style></head><body><h1>You are using <b>replit keep alive from PyPi</b>.<br>Head over to a site like <a href="https://up.rdsl.ga/">up.rdsl.ga</a> to keep your repl alive with this webserver.</h1><p>Thanks for using me!</p></body></html>'
  @app.route('/')
  def home():
      return message 
    
  @app.route("/ping")
  def catch_all(): return "Pong"
  import logging
  log = logging.getLogger('werkzeug')
  log.setLevel(logging.ERROR)
  def run():
    print("[Replit keep alive] server is running on port 8080")
    app.run(host='0.0.0.0',port=8080, debug=False) #localhost doesn't work, thats why it is 0.0.0.0
    
  
  def keep_alive():  
      t = Thread(target=run)
      t.start()
  keep_alive()
# Keep alive using up.rdsl.ga!


def WaitressStart(message=None):
  if message == None:
    message = '<html><head><style>*{font-family:system-ui;}</style></head><body><h1>You are using <b>replit keep alive from PyPi</b>.<br>Head over to a site like <a href="https://up.rdsl.ga/">up.rdsl.ga</a> to keep your repl alive with this webserver.</h1><p>Thanks for using me! - waitress version</p></body></html>'
  @app.route('/')
  def home():
      return message 
  @app.route("/ping")
  def catch_all(): return "Pong"
    
  def run():
    
    try:
      import waitress
    except ImportError:
      print("[Replit keep alive] waitress is not installed. Installing it...")
      import subprocess
      import sys
      subprocess.check_call([sys.executable, "-m", "pip", "install", 'waitress'])
      print("[Replit keep alive] waitress is installed.")
    finally:
      import waitress
    print("[Replit keep alive] waitress is serving at port 8080")
    waitress.serve(app, host='0.0.0.0', port=8080) #localhost doesn't work, thats why it is 0.0.0.0
    

  
  def keep_alive():  
    
      t = Thread(target=run)
      
      t.start()
  keep_alive()
# Keep alive using up.rdsl.ga!