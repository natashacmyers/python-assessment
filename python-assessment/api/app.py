from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import create_db

import sqlite3

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python Tech Test API"
    }
)
app.register_blueprint(swaggerui_blueprint)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# TODO - you will need to implement the other endpoints
# GET /api/person/{id} - get person with given id                               Done
# POST /api/people - create 1 person
# PUT /api/person/{id} - Update a person with the given id
# DELETE /api/person/{id} - Delete a person with a given id

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        id = request.form["id"]
        return redirect(url_for("get_person", id=id))
    return render_template("home.html")


@app.route("/api/people", methods=["GET", "POST"])

def getall_people():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    if request.method == "POST":
        id = request.form["id"]
        fname = request.form["fname"]
        sname = request.form["sname"]
        if request.form["enabled"] == 'Yes':
            enab = 1
        else:
            enab = 0 
        if request.form["auth"] == 'Yes':
            auth = 1
        else:
            auth = 0 
        values = [auth, enab, fname, id, sname]
        sql = 'INSERT INTO Person (authorised, enabled, firstName, id, lastName)VALUES(?, ?, ?, ?, ?);'
        cur.execute(sql, values)

        return redirect(url_for("home"))
    all_people = cur.execute('SELECT * FROM Person;').fetchall()

    return jsonify(all_people)


@app.route("/api/people/<id>",  methods=["GET", "POST"])
def get_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    if request.method == "POST":
        fname = request.form["fname"]
        sname = request.form["sname"]
        if request.form["enabled"] == 'Yes':
            enab = 1
        else:
            enab = 0 
        if request.form["auth"] == 'Yes':
            auth = 1
        else:
            auth = 0 
        values = (fname, sname, auth, enab, id)
        sql = 'UPDATE Person SET firstName = ?, lastName =?, authorised =?, enabled =? WHERE "id" = ?;'
        cur.execute(sql, values)
        return redirect(url_for("getall_people"))
    values = (id,)
    sql = 'SELECT * FROM Person WHERE "id" = ?;'
    person = cur.execute(sql, values).fetchall()

    return render_template("person.html", id=id, person=person)


@app.route("/api/people/delete_<id>",  methods=["GET", "POST"])
def delete_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    values = (id,)
    sql = 'DELETE FROM Person WHERE "id" = ?;'
    person = cur.execute(sql, values).fetchall()

    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
