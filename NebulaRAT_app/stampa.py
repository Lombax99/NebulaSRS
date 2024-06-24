import yaml
import os

# Ottieni il percorso assoluto del file di configurazione
current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, 'config2.yaml')

# Leggi il file di configurazione
with open(config_file_path, 'r') as file:
    config = yaml.safe_load(file)

# Funzione per stampare le regole di firewall
def print_firewall_rules(rules, direction):
    print(f"Firewall {direction} rules:")
    for rule in rules:
        action = rule.get('action', 'undefined')
        proto = rule.get('proto', 'any')
        port = rule.get('port', 'any')
        host = rule.get('host', 'any')
        groups = rule.get('groups', [])
        local_cidr = rule.get('local_cidr', 'any')
        #comment = rule.get('comment', '')
        print(f"  - Action: {action}, Protocol: {proto}, Port: {port}, Host: {host}, Groups: {groups}, Local CIDR: {local_cidr}")

# Stampa le regole inbound e outbound
if 'firewall' in config:
    if 'inbound' in config['firewall']:
        print_firewall_rules(config['firewall']['inbound'], 'inbound')
    if 'outbound' in config['firewall']:
        print_firewall_rules(config['firewall']['outbound'], 'outbound')
    if 'outbound_action' in config['firewall']:
        print(f"Default outbound action: {config['firewall']['outbound_action']}")
    if 'inbound_action' in config['firewall']:
        print(f"Default inbound action: {config['firewall']['inbound_action']}")
else:
    print("No firewall rules found in the configuration.")


