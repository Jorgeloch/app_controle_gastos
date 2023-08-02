import sqlite3
from flask import Flask, request, render_template, redirect, jsonify, g

app = Flask(__name__)

DB = "gastos.db"

# inicializa o banco de dados
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    db.row_factory = make_dicts
    return db
# encerra o banco de dados assim que o contexto da aplicação se encerra
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
# Funçao para auxiliar na criação de dicionarios, para facilitar o uso dos dados recolhidos nas buscas
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
# Funçao para facilitar a execução de queries no DB
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def home():
    costs = query_db("SELECT name, value, descrpition, card_number, flag FROM people JOIN (costs JOIN cards ON costs.card_id = cards.id) ON people.id = costs.person_id;")
    return render_template("index.html", costs=costs)

@app.route("/people", methods=["GET", "POST"])
def people():
    people = query_db("SELECT * FROM people")
    return jsonify(people)

@app.route("/costs", methods=["GET", "POST"])
def costs():
    costs = query_db("SELECT * FROM costs")
    return jsonify(costs)

# @app.route("/delete")
# def delete():
#     r