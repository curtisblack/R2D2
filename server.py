from flask import Flask, request
from R2D2 import *

r2 = R2D2()

app = Flask(__name__)

@app.route("/")
def index():
    return """<html>
  <head>
    <title>R2D2</title>
  </head>
  <body>
    <a href="/set/dome/on">Dome On</a>
    <a href="/set/dome/off">Dome Off</a>
    <form action="" method="get">
        <button name="dome" value="on">Dome On</button>
        <button name="dome" value="off">Dome Off</button>
    </form>
  </body>
</html>"""

@app.route("/set/<setting>/<value>")
def set(setting, value):
    if setting == "dome":
        if value == "on":
            r2.DomeLights.Enable()
        elif value == "off":
            r2.DomeLights.Disable()
    elif setting == "brightness":
        r2.Head.SetBrightness(int(value))
    return "R2D2"

@app.route("/get/<setting>")
def get(setting):
    if setting == "dome":
        return str(r2.DomeLights.Enabled)
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0")
