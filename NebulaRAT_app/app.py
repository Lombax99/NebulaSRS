from flask import Flask, render_template, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from generateCertificate import *
import yaml
import os

"""import psycopg2
cnx = psycopg2.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db")
"""

app = Flask(__name__)

"""def prova():
    query = "SELECT * FROM TEST;"
    try:
        with cnx as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                machine_data = cur.fetchall()  # Fetch all rows at once
                return machine_data
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        conn.close()"""


"""@app.route('/')
def root():
    cursor = cnx.cursor()
    cursor.execute("SELECT id, descrizione, indirizzoip FROM MACCHINA_Disp")
    macchine = cursor.fetchall()
    cursor.close()
    print('Request for index page received')
    return render_template('index.html',macchine=macchine)
"""
"""def load_firewall_config():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_directory, 'config2.yaml')
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config"""

"""def format_firewall_rules(rules, direction):
    formatted_rules = f"<strong>Firewall {direction} rules:</strong><br>"
    for rule in rules:
        action = rule.get('action', 'undefined')
        proto = rule.get('proto', 'any')
        port = rule.get('port', 'any')
        host = rule.get('host', 'any')
        groups = rule.get('groups', [])
        local_cidr = rule.get('local_cidr', 'any')
        formatted_rules += f"  - Action: <strong>{action}</strong>, Protocol: <strong>{proto}</strong>, Port: <strong>{port}</strong>, Host: <strong>{host}</strong>, Groups: <strong>{groups}</strong>, Local CIDR: <strong>{local_cidr}</strong><br>"
    return formatted_rules"""

"""@app.route('/print_firewall_rules', methods=['GET'])
def print_firewall_rules():
    config = load_firewall_config()
    rules_text = ""
    if 'firewall' in config:
        if 'inbound' in config['firewall']:
            rules_text += format_firewall_rules(config['firewall']['inbound'], 'inbound')
        if 'outbound' in config['firewall']:
            rules_text += format_firewall_rules(config['firewall']['outbound'], 'outbound')
        if 'outbound_action' in config['firewall']:
            rules_text += f"Default outbound action: <strong>{config['firewall']['outbound_action']}</strong><br>"
        if 'inbound_action' in config['firewall']:
            rules_text += f"Default inbound action: <strong>{config['firewall']['inbound_action']}</strong><br>"
    else:
        rules_text = "No firewall rules found in the configuration."
    return rules_text"""


@app.route('/login')
def login():
    print('Request for index page received')
    return render_template('login.html')

@app.route('/signup')
def signup():
    print('Request for index page received')
    return render_template('signup.html')


@app.route('/test')
def testpage():
    print('Request for index page received')
    return render_template('test.html')

@app.route('/test-python-function-JSON')
def testPythonFunction():
    data = {
        'message': 'Hello, world!'
    }
    return jsonify(data)

@app.route('/test-python-function-string')
def testPythonFunctionString():
    return 'Hello, world!'

@app.route('/test-python-function-Certificate')
def testPythonFunctionCertificate():
    return get_certificate(machineName + ".crt")

@app.route('/test-python-function-DB')
def testPythonFunctionDB():
    return prova()




if __name__ == '__main__':
   app.run(debug=True)