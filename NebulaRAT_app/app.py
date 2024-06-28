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

#def load_firewall_config():
#    current_directory = os.path.dirname(os.path.abspath(__file__))
#    config_file_path = os.path.join(current_directory, 'config2.yaml')
#    with open(config_file_path, 'r') as file:
#        config = yaml.safe_load(file)
#    return config

#def format_firewall_rules(rules, direction):
#    formatted_rules = f"<strong>Firewall {direction} rules:</strong><br>"
#    for rule in rules:
#        port = rule.get('port', 'any')
#        proto = rule.get('proto', 'any')
#        
#        if 'group' in rule:  # If 'group' is present, use it
#            groups = [rule['group']] if rule['group'] else ['any']
#        else:  # Otherwise, use 'groups' (default to empty list if not present)
#            groups = rule.get('groups', ['any']) if rule.get('groups') else ['any']
#        
#        cidr = rule.get('cidr', 'any')
#        ca_name = rule.get('ca_name', 'any')
#        
#        # Convert groups to a string representation
#        groups_str = ', '.join(groups) if groups != ['any'] else 'any'
#        
#        formatted_rules += f"  - Port: <strong>{port}</strong>, Protocol: <strong>{proto}</strong>, Groups: <strong>{groups_str}</strong>, CIDR: <strong>{cidr}</strong>, CA Name: <strong>{ca_name}</strong><br>"
#    
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

@app.route('/dashboard')
def dashboard():
    #cursor = cnx.cursor()
    #cursor.execute("SELECT id, descrizione, indirizzoip FROM MACCHINA_Disp")
    #macchine = cursor.fetchall()
    #cursor.close()
    print('Request for index page received')
    return render_template('dashboard.html') #Aggiungere macchine=macchine


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


