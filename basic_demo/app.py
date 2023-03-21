# === IMPORTS ===
from flask import Flask
from flask import request # now we can also use different HTTP methods
from flask import render_template # for rendering html templates
from utils.math import fact, fasterCryptarithm

# === SETUP ===
app = Flask('some random app (・∇・)')
# the convention is to use __name__, but we're not packaging the app so whatever

# === ROUTES ===
@app.route("/")
def root_route():
    pass

# Note that Flask will redirect you to `/projects`
@app.route('/projects/')
def projects():
    pass

# Note that accessing `/about/` will be 404
@app.route('/about')
def about():
    pass

# capturing variable
@app.route('/user/<username>')
# There are more advanced capturing rules, but we can "type check" manually for now. 
def user_profile(username):
    pass

# we can return useful things
@app.route('/fact/<int:n>')
def fact_page(n):
    result = fact(n)
    pass

# method detection
@app.route('/getorpost', methods=["GET", "POST"])
def getorpost():
    if request.method == 'POST':
        pass
    else:
        pass

# template rendering
@app.route('/template')
def template():
    # render atemplate.html
    pass

# template rendering with variable
@app.route('/sayhello/<name>')
def sayhello(name):
    # render sayhello.html with name
    pass

# JSON api
@app.route("/api")
def api() -> dict[str, str]:
    return {
        "foo": "fooo",
        "bar": "barr",
        "quote": "hello world",
    }

# JSON api with arg
# route /api/<string>, and do something with string
@app.route("/api/<string>")
def api_with_arg(string) -> dict[str, str]:
    pass

# cryptarithm solver!
@app.route("/api/cryptarithm/<puzzle>")
def cryptarithm_api(puzzle):
    solution = fasterCryptarithm(puzzle)
    
    if solution != None:
        return {
            "puzzle": puzzle,
            "solved": True,
            "solution": solution,
        }
    else:
        return {
            "puzzle": puzzle,
            "solved": False,
            "solution": None,
        }

import art as art
# get art
@app.route("/art/<text>")
def make_art(text):
    output = art.text2art(text)
    return f"<pre>{output}</pre>"

# import requests, re
# Something crazy
@app.route("/api/scholar/<query>")
def scholar(query):
    # scrape google scholar and return article listing
    return 418

# >>> Ad hoc route begins >>>

# ... any question/idea for some live coding? else demo project time

# <<<  Ad hoc route ends  <<<

# === RUNNING ===
if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 5000)
    # app.run(host='0.0.0.0', port = 5000) # this makes it public