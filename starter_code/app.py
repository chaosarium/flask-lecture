# === IMPORTS ===
from flask import Flask
from flask import request # now we can also use different HTTP methods
from flask import render_template # for rendering html templates
from flask import redirect # lets you send visitor to some other url
from flask import session # this is how we keep users logged in
from flask import flash # flashing messages to user
from tinydb import TinyDB, where # database

# === SETUP ===
app = Flask(__name__)
app.secret_key = 'secret' # put something actually secret here
# db = TinyDB('db.json') # uncomment if you need a database

# === DATABASE (helper functions) ===
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
    
# === ROUTES ===
@app.route("/")
def index():
    return render_template(
        "some_template.html", 
        message="Hello World", 
    )

# TODO more routes here

# === RUNNING ===
if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 15113)