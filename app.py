import os
import sqlite3
from crypt import methods

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session)

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

error_msg = ''


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


USER_INPUTS = ["name", "month", "day"]


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()

    if request.method == "POST":
        try:
            for input in USER_INPUTS:
                if not request.form.get(input):
                    return render_template("error.html", message="Missing {}".format(input))

            conn.execute(
                "INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?);", (
                    request.form.get(USER_INPUTS[0]),
                    request.form.get(USER_INPUTS[1]),
                    request.form.get(USER_INPUTS[2])
                ))

            conn.commit()

        except:
            conn.rollback()
            global error_msg
            error_msg = "Error in INSERT operation"

        finally:
            conn.close()
            return redirect("/")

    else:
        try:
            birthdays = conn.execute("SELECT * FROM birthdays;").fetchall()

        except:
            error_msg = "Error in SELECT operation"

        finally:
            conn.close()
            return render_template("index.html", birthdays=birthdays, error_msg=error_msg)


@app.route("/delete", methods=["POST"])
def delete_peron():
    try:
        conn = get_db_connection()

        id = request.form.get("id")
        if id:
            conn.execute("DELETE FROM birthdays WHERE id = ?;", id)
            conn.commit()

    except:
        conn.rollback()
        global error_msg
        error_msg = "Error in DELETE operation"

    finally:
        conn.close()
        return redirect("/")
