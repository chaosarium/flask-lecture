# === IMPORTS ===
from flask import Flask
from flask import request # now we can also use different HTTP methods
from flask import render_template # for rendering html templates
from flask import redirect # lets you send visitor to some other url
from flask import session # this is how we keep users logged in
from flask import flash # flashing messages to user
from tinydb import TinyDB, where # database
from typing import Union

# === SETUP ===
app = Flask(__name__)
app.secret_key = 'lalala'
db = TinyDB('db.json')

# === DATABASE ===
# return a table
def get_table(table):
    return db.table(table)

# insert one dic as entry
# demo call: insert_entry('random', {'field1': 'hahahaha', 'field2': 'hehehehe'})
# demo call: insert_entry('random', {'field1': 'hahahaha', 'field2': 'hehehehehe'})
def insert_entry(table, entry) -> int:
    assert(isinstance(entry, dict))
    # entry should look like {'field1': val1, 'field2': val2}
    return get_table(table).insert(entry) # returns the id associated with record

# return array of results
# demo call: query_entry('random', 'field1', 'hahahaha')
def query_entry(table, field_name, value) -> list[dict]:
    return get_table(table).search(where(field_name) == value)

# returns id of one match
# demo call: get_entry_id('random', 'field1', 'hahahaha')
def get_entry_id(table, field_name, value) -> Union[None, int]:
    elem = get_table(table).get(where(field_name) == value) # gets one
    return None if elem == None else elem.doc_id

# remove entry by doc_id
def remove_entry(table, doc_id) -> int:
    assert(get_table(table).contains(doc_id=doc_id))
    return get_table(table).remove(doc_ids=[doc_id]) # returns a list of all removed ids

# update value of key by doc_id
def update_entry(table, doc_id, field_name, new_value):
    assert(get_table(table).contains(doc_id=doc_id))
    return get_table(table).update({field_name: new_value}, doc_ids=[doc_id])
    
# === LOGIN MANAGEMENT === (we'll come back to this later)
def user_exists(username):
    return query_entry("users", "username", username) != []

def password_correct(username, password):
    # return true if user exists and `query_entry("users", "username", username)[0]['password']` is indeed password else false
    raise NotImplemented
    
def new_user(username, password):
    # assert user not exist
    # insert an entry `{"username": username, "password": password, "admin": False})` into the "users" table
    raise NotImplemented

def user_is_admin(username):
    # return true if user exists and `query_entry("users", "username", username)[0]['admin'] == True`
    raise NotImplemented

@app.route('/login', methods=['POST'])
def login():
    
    # get username and password from the `request.form`, which is a dictionary
    
    # if user exists
        # if so, if password_correct
            # session['username'] = request.form['username']
            # flash success
            # redirect back to root
        # else
            # flash wrong password
            # redirect back to root
    # else
        # flash user DNE
        # redirect back to root

    raise NotImplemented

@app.route('/register', methods=['POST'])
def register():

    # get username and password from the `request.form`, which is a dictionary
    
    # if user exists
        # please log in
        # redirect
    # else
        # new_user(username, password)
        # session['username'] = request.form['username']
        # we can know for sure this user exists
        # success
        # redirect
        
    raise NotImplemented

@app.route('/logout')
def logout():
    # session.pop('username', None) # None is default if thing to pop not found
    # redirect
    
    raise NotImplemented

# === ROUTES ===
@app.route("/")
def index():
    
    proposed_entries: list[dict] = [] # some query in the 'topics table'
    planned_entries: list[dict] = [] # some query in the 'topics table'
    rejected_entries: list[dict] = [] # some query in the 'topics table'
    
    print('session', session)
    
    logged_in: bool = False
    logged_in_as: Union[list, bool] = None # if logged in it should be session["username"]
    is_admin: bool = False
    
    if 'username' in session:
        if user_is_admin(logged_in_as):
            pass
        else:
            pass
    else:
        pass
    
    return f"""
        <p>proposed_entries: {proposed_entries}</p>
        <p>planned_entries: {planned_entries}</p>
        <p>rejected_entries: {rejected_entries}</p>
        <p>logged_in: {logged_in}</p>
        <p>logged_in_as: {logged_in_as}</p>
        <p>is_admin: {is_admin}</p>
        
        <!-- a bunch of forms -->
        
        <form action="/add" method="POST"> 
            <input type="text" name="topic" placeholder="topic here">
            <input type="submit" value="submit topic">
        </form>
        
        <br>
        
        <form action="/reject" method="POST"> 
            <input type="text" name="topic" placeholder="topic here">
            <input type="submit" value="reject topic">
        </form>
        
        <br>

        <form action="/promote" method="POST"> 
            <input type="text" name="topic" placeholder="topic here">
            <input type="submit" value="promote topic">
        </form>
    """
    
    # region
    
    """ some login forms
    
    <form action="/logout">
        <input type="submit" value="logout">
    </form>

    <form method="post" action="/login">
        <input name="username" type="text" placeholder="username">
        <input name="password" type="password" placeholder="password">
        <input type="submit" value="login">
    </form>

    <form method="post" action="/register">
        <input name="username" type="text" placeholder="username">
        <input name="password" type="password" placeholder="password">
        <input type="submit" value="login">
    </form>

    """
    
    # a nicer way to render :)
    return render_template(
        "nicetopiclist.html", 
        proposed_entries=proposed_entries, 
        planned_entries=planned_entries, 
        rejected_entries=rejected_entries,
        logged_in=logged_in,
        logged_in_as=logged_in_as,
        is_admin=is_admin
    )
    
    # endregion

@app.route("/add", methods=["POST"])
def add_topic():
    print(request.form) # this is how we get what they put in the form
    
    topic = str('') # get 'topic' from request.form, which is a dict
    print(f'we got new proposed topic: {topic}')
    
    # security vulnerability!! but we're skipping safety check
    
    # if 1+1==2: # later: authentication check: ('username' in session) and (user_exists(session['username']))
    
    if 1+1==2: # check topic existance using get_entry_id(table, field, val). if topic exists it's not none
        # topic exists
        # redirect
        raise NotImplemented
    else:
        # insert topic as proposed using insert_entry to the 'topics' table, 
        # recall our entry looks like {'topic': _, 'status': '_'}
        # redirect
        raise NotImplemented
    
    # return "you need to log in to propose topic"

@app.route("/reject", methods=["POST"])
def reject_topic():
    print(request.form) # this is how we get what they put in the form
      
    topic: str = str(request.form['topic']) # we've done this before
    
    # if ('username' in session) and (user_exists(session['username'])) and user_is_admin(session['username']):
    
    if get_entry_id("topics", "topic", topic) == None:
        # topic does not exist
        print('topic DNE, not rejecting')
        return redirect("/")
    else:
        # get entry
        # update entry to set 'status' = 'rejected'
        # redirect
        raise NotImplemented
        
    # return "go away", 418

@app.route("/promote", methods=["POST"])
def promote_topic():
    # very similar to reject
    raise NotImplemented

# === RUNNING ===
if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 15113)