import os
import sqlite3

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session)

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


def dict_factory(cursor, row):
    """Return dictionary instead of default tuple"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_connection():
    """Create connection to db"""
    connection = sqlite3.connect("birthdays.db")
    connection.row_factory = dict_factory

    return connection


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()

    if request.method == "POST":

        # TODO: Add the user's entry into the database

        return redirect("/")

    else:
        birthdays = conn.execute("SELECT * FROM birthdays").fetchall()
        conn.close()
        return render_template("index.html", birthdays=birthdays)
