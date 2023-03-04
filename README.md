# Introduction to Flask

Demo project -> https://chaosarium.pythonanywhere.com
Code on GitHub -> https://github.com/chaosarium/flask-lecture
Docs -> https://chaosarium.gitbook.io/113-flask

Flask is a Python web framework, i.e. something that lets you build web apps!

One cool thing you can then do is to make different machines talk to each other — you can even have things written in different languages talk to each

But first, how does the web work? See [HTTP](docs/HTTP.md) if not already familiar.

## Setting up a Flask app

Create a file `app.py` (usually they call it that and it works)

Of course you import a bunch of things

```py
from flask import Flask
from flask import request # now we can also use different HTTP methods
from flask import render_template # for rendering html templates
...
```

This line creates a flask app

```py
app = Flask(__name__)
```

And this lets you run the app when you run `python app.py` in terminal

```py
if __name__ == '__main__':
    # here, 127.0.0.1 is the IP address for localhost, and port can be though of the channel at this address?
    app.run(host='127.0.0.1', port = 5000)
    # If you want your app to be available publically, you change the host to 0.0.0.0. Then people in your local network should be able to access your app via your computer's IP
    # Note that your computer probably doesn't have a public IP, so someone in, California, for example, won't be able to access your app (unless they go on CMU VPN(?))
    # If you want your app to be made public everywhere, you need a public IP.
```

But wait, we just created an app that doesn't "listen" to anything. We need to define functions so that it handles http requests like the one we saw earlier. 

Here's the code for a function that listens at `/` and responds by sending hello world. 

```py
@app.route("/")
def root_route():
    return "Hello, World!" 
```

Flask uses some sort of function decorator. We already said `app = Flask(__name__)`, so `app.route("...")` is creating a route for the app. And `"/"` just means root URL. Flasks makes it so that return sends our response. In this case we're just sending text. 

Putting it together, we have:

```py
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def root_route():
    return "Hello, World!" 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 5000)
```

## More routes

We can do more than just sending back hello world — we can get data from the request, do something with it, and send back something fancy!

We can have non-root url
```py
@app.route('/projects')
def projects():
    return 'The project page'
```

We can capture path pattern in url
```py
@app.route('/user/<username>')
def user_profile(username):
    print(username)
    return f'hmm, see console'
```

We can specify the type. Also we are returning some html here
@app.route('/fact/<int:n>')
```py
def fact_page(n):
    return f'<p style="overflow-wrap: anywhere;">{n}! = {fact(n)}</p>'
```

We can do something different depending on what type of request we got
```py
@app.route('/getorpost', methods=["GET", "POST"])
def getorpost():
    if request.method == 'POST':
        return "method was POST"
    else:
        return "method was GET"
```

We can render html file. This example captures `name` from the request url and puts it in a `sayhello` template, which flask will look for in the `./templates` directory.
```py
@app.route('/sayhello/<name>')
def sayhello(name):
    return render_template("sayhello.html", name = name)
```

We can return json too
```py
@app.route("/api")
def api():
    return {
        "foo": "fooo",
        "bar": "barr",
        "quote": "hello world",
    }
```

## Example project — a 15113 topic list

Demo link: https://chaosarium.pythonanywhere.com

What we need:

- Some database to store data. See [database](docs/database.md)
- A home page that displays data (`GET`)
- Places to update data using `POST`
  - `/add` topic
  - `/promote` topic
  - `/reject` topic
- Some interface to send `POST` requests
- UI design (maybe) (implemented on the [stylish-topiclist](https://github.com/chaosarium/flask-lecture/tree/stylish-topiclist) branch)

![pic](https://share.cleanshot.com/jm93GWWQlpxmyZPKy13f/download)

## Deployment

There are many options for deploying your Flask app. We'll use PythonAnywhere because of its simplicity.

See [deployment](docs/deployment.md)

## Lab project — TBD