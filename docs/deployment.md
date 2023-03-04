# Deployment

## PythonAnywhere

The demo app is hosted on [PythonAnywhere](https://www.pythonanywhere.com), which is free and simple to use. To run your Flask app, do these:

1. Go to [PythonAnywhere](https://www.pythonanywhere.com) and register for an account
2. Under `Dashboard > Consoles`, you can open up a terminal to install dependencies. For our app, do `pip install tinydb`
3. Click `Web apps`, then `Add a new web app`, then `Next`
4. Select `Flask` and use `Python 3.10`
5. Set a path to where your app is on the remote file system
6. You should now see "Hello from Flask!" in the site that was just created. Start modifying the python code!


## Other options

- Vercel: supports continuous deployment from git but doesn't allow writing to disk
- VPS: you'll have to set things up on a server, but it's fun