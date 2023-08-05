from flask import Flask
from flask_scenario_testing.backend.initialise_scenario_testing import initialise_scenario_testing
from flask_scenario_testing.backend.modifiers.Sleep import Sleep

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, world!'


initialise_scenario_testing(app, [Sleep()])