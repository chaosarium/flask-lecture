# === IMPORTS ===
from flask import Flask
from flask import url_for # helps you get route from function name
from flask import request # now we can also use different HTTP methods
from flask import render_template # for rendering html templates
from flask import redirect
from flask import session # this is how we keep users logged in
from flask import flash # flashing messages to user
from tinydb import TinyDB, where, Query # database

# === SETUP ===
app = Flask(__name__)
app.secret_key = 'lalala' # don't do this
db = TinyDB('db.json')

# === DATABASE ===
def get_table(table):
    return db.table(table)

# insert one dic as entry
def insert_entry(table, entry):
    assert(isinstance(entry, dict))
    # entry should look like {'field1': val1, 'field2': val2}
    return get_table(table).insert(entry) # returns the id associated with record

# return array of results
def query_entry(table, field_name, value):
    return get_table(table).search(where(field_name) == value)

# returns id of one match
def get_entry_id(table, field_name, value):
    elem = get_table(table).get(where(field_name) == value) # gets one
    return None if elem == None else elem.doc_id

# remove entry by doc_id
def remove_entry(table, doc_id):
    assert(get_table(table).contains(doc_id=doc_id))
    return get_table(table).remove(doc_ids=[doc_id]) # returns a list of all removed ids

# update value of key by doc_id
def update_entry(table, doc_id, field_name, new_value):
    assert(get_table(table).contains(doc_id=doc_id))
    return get_table(table).update({field_name: new_value}, doc_ids=[doc_id])
    
# === tests ===
# print(get_entry_id('int', 2))
# print(remove_entry(4))
# print(update_entry(12, 'topic', 'super topic+'))

# === ROUTES ===
@app.route("/")
def index():
    proposed_entries = query_entry("topics", 'status', 'proposed')
    planned_entries = query_entry("topics", 'status', 'planned')
    rejected_entries = query_entry("topics", 'status', 'rejected')
    
    print('session', session)
    if 'username' in session:
        logged_in = True
        logged_in_as = session["username"]
        if user_is_admin(logged_in_as):
            is_admin = True
        else:
            is_admin = False
    else:
        logged_in = False
        logged_in_as = None
        is_admin = False
    
    return render_template(
        "nicetopiclist.html", 
        proposed_entries=proposed_entries, 
        planned_entries=planned_entries, 
        rejected_entries=rejected_entries,
        logged_in=logged_in,
        logged_in_as=logged_in_as,
        is_admin=is_admin
    )

# === LOGIN MANAGEMENT === 
# (see also https://flask.palletsprojects.com/en/2.2.x/quickstart/#sessions)

def user_exists(username):
    return query_entry("users", "username", username) != []

def password_correct(username, password):
    return (user_exists(username)
            and 
            query_entry("users", "username", username)[0]['password'] == password)

def new_user(username, password):
    assert(not user_exists(username))
    insert_entry("users", {"username": username, "password": password, "admin": False}) 

def user_is_admin(username):
    return (user_exists(username) 
            and 
            query_entry("users", "username", username)[0]['admin'] == True)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if user_exists(username):
        if password_correct(username, password):
            session['username'] = request.form['username']
            flash('Log in successful')
            return redirect('/')
        else:
            flash('Wrong username or password')
            return redirect('/')
    else:
        flash('User does not exist')
        return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    if user_exists(username):
        flash('User already exists, please log in instead')
        return redirect('/')
    else:
        new_user(username, password)
        session['username'] = request.form['username']
        assert(user_exists(username))
        flash('Succenssfully registered')
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# === REQUEST HANDELLLING"

@app.route("/add", methods=["POST"])
def add_topic():
    print(request.form) # this is how we get what they put in the form
    
    topic = str(request.form['topic'])
    print(f'we got new proposed topic: {topic}')
    # security vulnerability!! but we're skipping safety check
    
    if ('username' in session) and (user_exists(session['username'])):
        if get_entry_id("topics", 'topic', topic) != None:
            # topic already exists
            print('topic already exists, not inserting')
            return redirect("/")
        else:
            # insert topic as proposed
            insert_entry("topics", {'topic': topic, 'status': 'proposed'})
            print(f'inserted topic {topic}')
            return redirect("/")
    return "you need to log in to propose topic"

@app.route("/reject", methods=["POST"])
def reject_topic():
    print(request.form) # this is how we get what they put in the form
      
    topic = str(request.form['topic'])
    
    if ('username' in session) and (user_exists(session['username'])) and user_is_admin(session['username']):
        if get_entry_id("topics", "topics", 'topic', topic) == None:
            # topic does not exist
            print('topic DNE, not rejecting')
            return redirect("/")
        else:
            # reject topic 
            id = get_entry_id("topics", 'topic', topic)
            update_entry("topics", id, 'status', 'rejected')
            print(f'rejected topic {topic}')
            return redirect("/")
        
    return "go away", 418

@app.route("/promote", methods=["POST"])
def promote_topic():
    print(request.form) # this is how we get what they put in the form
    
    topic = str(request.form['topic'])
    
    if ('username' in session) and (user_exists(session['username'])) and user_is_admin(session['username']):
        if get_entry_id("topics", 'topic', topic) == None:
            # topic does not exist
            print('topic DNE, not promoteing')
            return redirect("/")
        else:
            # promote topic 
            id = get_entry_id("topics", 'topic', topic)
            update_entry("topics", id, 'status', 'planned')
            print(f'promoteed topic {topic}')
            return redirect("/")
        
    return "go away", 418

# === RUNNING ===
if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 15113)