"""
This is the beginning of a Flask app.
If you haven't, make sure to install Flask. 
Also, make sure it's Flask 2.2.x. 1.something definitely have different things
"""

# === IMPORTS ===
from flask import Flask
from flask import request # now we can also use different HTTP methods
from flask import render_template # for rendering html templates
from utils.math import fact, fasterCryptarithm

# === SETUP ===
app = Flask(__name__)
# app = Flask(__name__, static_url_path="static", ...) # you can add config here

# === ROUTES ===
@app.route("/")
def root_route():
    return "Hello, World!" 
    # return string of html (default) to the browser (though this doesn't quite look like html yet)
    return "<h1>Hello, World!</h1>" # this looks more like html

# Note that Flask will redirect you to `/projects`
@app.route('/projects/')
def projects():
    return 'The project page'

# Note that accessing `/about/` will be 404
@app.route('/about')
def about():
    return 'The about page'

# capturing variable
@app.route('/user/<username>')
# There are more advanced capturing rules, but we can "type check" manually for now. 
def user_profile(username):
    print(username)
    return f'hmm, see console'

# we can return useful things
@app.route('/fact/<int:n>')
def fact_page(n):
    # return f'{n}! = {fact(n)}'
    return f'<p style="overflow-wrap: anywhere;">{n}! = {fact(n)}</p>'

# method detection
@app.route('/getorpost', methods=["GET", "POST"])
def getorpost():
    if request.method == 'POST':
        return "method was POST"
    else:
        return "method was GET"

# template rendering
@app.route('/template')
def template():
    return render_template("atemplate.html")

# template rendering with variable
@app.route('/sayhello/<name>')
def sayhello(name):
    return render_template("sayhello.html", name = name)

# JSON api
@app.route("/api")
def api():
    return {
        "foo": "fooo",
        "bar": "barr",
        "quote": "hello world",
    }

# JSON api with arg
@app.route("/api/<string>")
def api_with_arg(string):
    if string == 'world':
        return {
            "foo": "fooo",
            "bar": "barr",
            "quote": f"THE WORLD DOESN'T CARE",
        }

    return {
        "foo": "fooo",
        "bar": "barr",
        "quote": f"hello from {string.upper()}",
    }

# JSON api with arg
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

import requests, re
# Something crazy
@app.route("/api/scholar/<query>")
def scholar(query):
    # scrape google scholar and return article listing
    try:
        response = requests.get(
            url="https://scholar.google.com/scholar",
            params={
                "q": f"{query}",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        
        # return response.content # basically becomes proxy
        html_text = str(response.content)
        listing = re.findall('<div id="gs_res_ccl">.*<\/div>', html_text)[0]
        # https://regexper.com/#%3Cdiv%20id%3D%22gs_res_ccl%22%3E.*%3C%5C%2Fdiv%3E
        articles = re.findall('<h3 class="gs_rt".*?<\/h3>', listing) 
        # https://regexper.com/#%3Ch3%20class%3D%22gs_rt%22.*%3F%3C%5C%2Fh3%3E
        return str("<br>".join(articles))
        
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return "something went wrong. probably internet issue"

# === RUNNING ===
if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 5000)
    # app.run(host='0.0.0.0', port = 5000) # this makes it public