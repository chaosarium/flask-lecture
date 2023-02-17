# === TASK ===
"""
We will build a topic list for 15113. People can submit topics and people with
the right password can promote or reject topics.
"""

# === IMPORTS ===
from flask import Flask
from flask import url_for # helps you get route from function name
from flask import request # now we can also use different HTTP methods
from flask import render_template # for rendering html templates
from flask import redirect
from tinydb import TinyDB, where, Query # database

# === SETUP ===
app = Flask(__name__)
db = TinyDB('db.json')

# === DATABASE ===
# insert one dic as entry
def insert_entry(entry):
    assert(isinstance(entry, dict))
    # entry should look like {'field1': val1, 'field2': val2}
    return db.insert(entry) # returns the id associated with record

# return array of results
def query_entry(field_name, value):
    return db.search(where(field_name) == value)

# returns id of one match
def get_entry_id(field_name, value):
    elem = db.get(where(field_name) == value) # gets one
    return None if elem == None else elem.doc_id

# remove entry by doc_id
def remove_entry(doc_id):
    assert(db.contains(doc_id=doc_id))
    return db.remove(doc_ids=[doc_id]) # returns a list of all removed ids

# update value of key by doc_id
def update_entry(doc_id, field_name, new_value):
    assert(db.contains(doc_id=doc_id))
    return db.update({field_name: new_value}, doc_ids=[doc_id])
    
# === tests ===
print(get_entry_id('int', 2))
# print(remove_entry(4))
print(update_entry(12, 'topic', 'super topic+'))

# === ROUTES ===
@app.route("/")
def index():
    proposed_entries = query_entry('status', 'proposed')
    planned_entries = query_entry('status', 'planned')
    rejected_entries = query_entry('status', 'rejected')
    return f"""
        <h1> topic list </h1> 
        <p>Proposed: {proposed_entries}</p> 
        <p>Planned: {planned_entries}</p>
        <p>Rejected: {rejected_entries}</p>
        <form action="/add" method="POST"> 
            <input name="topic" placeholder="topic here">
            <input type="submit" value="submit topic">
        </form>
        <form action="/reject" method="POST"> 
            <input name="topic" placeholder="topic here">
            <input name="password" type="password" placeholder="password here">
            <input type="submit" value="reject topic">
        </form>
        <form action="/promote" method="POST"> 
            <input name="topic" placeholder="topic here">
            <input name="password" type="password" placeholder="password here">
            <input type="submit" value="promote topic">
        </form>
    """

@app.route("/add", methods=["POST"])
def add_topic():
    print(request.form) # this is how we get what they put in the form
    
    topic = str(request.form['topic'])
    print(f'we got new proposed topic: {topic}')
    # security vulnerability!! but we're skipping safety check
    
    if get_entry_id('topic', topic) != None:
        # topic already exists
        print('topic already exists, not inserting')
        return redirect("/")
    else:
        # insert topic as proposed
        insert_entry({'topic': topic, 'status': 'proposed'})
        print(f'inserted topic {topic}')
        return redirect("/")

@app.route("/reject", methods=["POST"])
def reject_topic():
    print(request.form) # this is how we get what they put in the form
    
    topic = str(request.form['topic'])
    password = str(request.form['password'])
    print(f'someone tries to reject topic {topic} with password {password}')
    
    if password != "15113": return "go away"
    
    if get_entry_id('topic', topic) == None:
        # topic does not exist
        print('topic DNE, not rejecting')
        return redirect("/")
    else:
        # reject topic 
        id = get_entry_id('topic', topic)
        update_entry(id, 'status', 'rejected')
        print(f'rejected topic {topic}')
        return redirect("/")

@app.route("/promote", methods=["POST"])
def promote_topic():
    print(request.form) # this is how we get what they put in the form
    
    topic = str(request.form['topic'])
    password = str(request.form['password'])
    print(f'someone tries to promote topic {topic} with password {password}')
    
    if password != "15113": return "go away"
    
    if get_entry_id('topic', topic) == None:
        # topic does not exist
        print('topic DNE, not promoteing')
        return redirect("/")
    else:
        # promote topic 
        id = get_entry_id('topic', topic)
        update_entry(id, 'status', 'planned')
        print(f'promoteed topic {topic}')
        return redirect("/")


# === RUNNING ===
if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 15113)