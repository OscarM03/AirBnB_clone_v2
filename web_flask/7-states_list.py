#!/usr/bin/python3
"""
A script that start an application
"""
from flask import Flask
from models import storage
from flask import render_template
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def tear_down(exception):
    """Tear_down"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_print():
    """Fetches data from the storage and displays it out"""
    states = storage.all(State)
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
