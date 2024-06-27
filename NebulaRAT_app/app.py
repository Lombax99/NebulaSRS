#from generateCertificate import *
from settings import postgresql as settings
from flask import Flask, render_template, request, jsonify
from queryexe import execute_query
from queryexe import execute_query
#import yaml
#import os
app = Flask(__name__)

@app.route('/')
def root():
    print('Request for index page received')
    return render_template('index.html')

##def load_firewall_config():
#    current_directory = os.path.dirname(os.path.abspath(__file__))
#     config_file_path = os.path.join(current_directory, 'config2.yaml')
#    with open(config_file_path, 'r') as file:
#        config = yaml.safe_load(file)
#    return config

#def format_firewall_rules(rules, direction):
#    formatted_rules = f"<strong>Firewall {direction} rules:</strong><br>"
#    for rule in rules:
#        action = rule.get('action', 'undefined')
#        proto = rule.get('proto', 'any')
#        port = rule.get('port', 'any')
#        host = rule.get('host', 'any')
#        groups = rule.get('groups', [])
#        local_cidr = rule.get('local_cidr', 'any')
#        formatted_rules += f"  - Action: <strong>{action}</strong>, Protocol: <strong>{proto}</strong>, Port: <strong>{port}</strong>, Host: <strong>{host}</strong>, Groups: <strong>{groups}</strong>, Local CIDR: <strong>{local_cidr}</strong><br>"
#    return formatted_rules

#@app.route('/print_firewall_rules', methods=['GET'])
#def print_firewall_rules():
#    config = load_firewall_config()
#    rules_text = ""
#    if 'firewall' in config:
#        if 'inbound' in config['firewall']:
#            rules_text += format_firewall_rules(config['firewall']['inbound'], 'inbound')
#        if 'outbound' in config['firewall']:
#            rules_text += format_firewall_rules(config['firewall']['outbound'], 'outbound')
#        if 'outbound_action' in config['firewall']:
#            rules_text += f"Default outbound action: <strong>{config['firewall']['outbound_action']}</strong><br>"
#        if 'inbound_action' in config['firewall']:
#            rules_text += f"Default inbound action: <strong>{config['firewall']['inbound_action']}</strong><br>"
#    else:
#        rules_text = "No firewall rules found in the configuration."
#    return rules_text

@app.route('/login')
def login():
    print('Request for index page received')
    return render_template('login.html')

@app.route('/signup')
def signup():
    print('Request for index page received')
    return render_template('signup.html')

@app.route('/404')
def errorPage():
    print('Request for index page received')
    return render_template('404.html')

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
    #return get_certificate(machineName + ".crt")
    return "ciao"

@app.route('/test-python-function-DB')
def testPythonFunctionDB():
    return execute_query()



if __name__ == '__main__':
   app.run(debug=True)


