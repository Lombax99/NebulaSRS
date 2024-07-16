import json
import yaml
from app import bcrypt, db
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import text
import os

# App configuration
app = Flask(__name__)

# Retrieve environment variables for DB connection
db_user = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = '5432' 
db_name = os.environ.get('DB_PGDB')
secret = os.environ.get('FLASK_SECRET')


# Set up Flask app and DB
db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = secret
db = SQLAlchemy(app)

# Define SQLAlchemy models
class Cert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descrizione = db.Column(db.String(511), nullable=False)

class Macchina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descrizione = db.Column(db.String(255))
    ip_addr = db.Column(db.String(20), unique=True, nullable=False)
    cert = db.Column(db.Integer, db.ForeignKey('cert.id'), nullable=False)

class Regola(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inout = db.Column(db.String(10), nullable=False)
    macchina_id = db.Column(db.Integer, db.ForeignKey('macchina.id'), nullable=False)
    port = db.Column(db.String(10))
    proto = db.Column(db.String(10))
    host = db.Column(db.String(255))
    ca_name = db.Column(db.String(255))
    gruppi = db.Column(db.String(500))
    cidr = db.Column(db.String(20))

class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cognome = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    auth = db.Column(db.Integer, default=0)
    admin = db.Column(db.Integer, default=0)

class Usa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utente.id'), nullable=False)
    macchina_id = db.Column(db.Integer, db.ForeignKey('macchina.id'), nullable=False)
    db.UniqueConstraint('utente_id', 'macchina_id', name='unique_utente_macchina')

# Function to extract the certificate
def extract_description_from_cert_file(cert_file_path):
    with open(cert_file_path, 'r') as cert_file:
        cert_content = cert_file.read()
    return cert_content.strip()  # Remove whitespace at the beginning and end

# Function to populate UTENTE table from JSON file
def populate_utenti_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

        for entry in data:
            utente = Utente(
                nome=entry['nome'],
                cognome=entry['cognome'],
                username=entry['username'],
                password=entry['password_hash'].encode('utf-8'),
                auth=int(entry['auth']),
                admin=int(entry['admin'])
            )
            db.session.add(utente)
        db.session.commit()

# Function to populate tables from JSON files
def populate_tables_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

        for entry in data:
            # Populates the CERT table
            cert_descrizione = extract_description_from_cert_file(entry['cert'])
            cert = Cert(descrizione=cert_descrizione)
            db.session.add(cert)
            db.session.commit()

            # Populate the MACCHINA table
            macchina = Macchina(descrizione=entry['descrizione'],
                                ip_addr=entry['nebula_ip'],
                                cert=cert.id)
            db.session.add(macchina)
            db.session.commit()

            # Reads the YAML configuration file
            config_file_path = entry['config']
            with open(config_file_path, 'r') as config_file:
                config_data = yaml.safe_load(config_file)

            # Function to populate firewall rules
            def add_rules_from_yaml(rules, inout):
                for regola in rules:
                    new_regola = Regola(
                        inout=inout,
                        macchina_id=macchina.id,
                        port=regola.get('port', '/'),
                        proto=regola.get('proto', '/'),
                        host=regola.get('host', '/'),
                        ca_name=regola.get('ca_name', '/'),
                        gruppi=regola.get('group', '/'),
                        cidr=regola.get('cidr', '/')
                    )
                    db.session.add(new_regola)
                    db.session.commit()

            # Populate the inbound and outbound rules
            if 'firewall' in config_data:
                if 'outbound' in config_data['firewall']:
                    add_rules_from_yaml(config_data['firewall']['outbound'], 'outbound')
                if 'inbound' in config_data['firewall']:
                    add_rules_from_yaml(config_data['firewall']['inbound'], 'inbound')

# Function to drop tables if they exist and create new ones
def reset_tables():
    drop_statements = [
        text("DROP TABLE IF EXISTS usa;"),
        text("DROP TABLE IF EXISTS regola;"),
        text("DROP TABLE IF EXISTS macchina;"),
        text("DROP TABLE IF EXISTS cert;"),
        text("DROP TABLE IF EXISTS utente;")
    ]
    create_statements = [
        text("""
        CREATE TABLE UTENTE (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cognome VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            password BYTEA NOT NULL,
            auth INTEGER DEFAULT 0,
            admin INTEGER DEFAULT 0
        );
        """),
        text("""
        CREATE TABLE CERT (
            id SERIAL PRIMARY KEY,
            descrizione VARCHAR(511) NOT NULL
        );
        """),
        text("""
        CREATE TABLE MACCHINA (
            id SERIAL PRIMARY KEY,
            descrizione VARCHAR(255),
            ip_addr VARCHAR(20) UNIQUE NOT NULL,
            cert  INTEGER NOT NULL REFERENCES CERT(id)
        );
        """),
        text("""
        CREATE TABLE REGOLA(
            id SERIAL NOT NULL,
            inout varchar(10) NOT NULL,
            macchina_id INTEGER NOT NULL REFERENCES MACCHINA(id) ON DELETE CASCADE,
            port VARCHAR(10),
            proto VARCHAR(10),
            host VARCHAR(255),
            ca_name VARCHAR(255),
            gruppi VARCHAR(500),
            cidr VARCHAR(20)
        );
        """),
        text("""
        CREATE TABLE USA (
            id SERIAL PRIMARY KEY,
            utente_id INTEGER NOT NULL REFERENCES UTENTE(id) ON DELETE CASCADE,
            macchina_id INTEGER NOT NULL REFERENCES MACCHINA(id) ON DELETE CASCADE,
            UNIQUE (utente_id, macchina_id)
        );
        """)
    ]
    # Execute drop statements
    for statement in drop_statements:
        db.session.execute(statement)
    # Execute create statements
    for statement in create_statements:
        db.session.execute(statement)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Drop existing tables and create new ones
        reset_tables()

        # Populate UTENTE table from the specified JSON file
        utenti_json_file = 'nebulaFiles/users.json'
        populate_utenti_from_json(utenti_json_file)

        # Populate other tables from the specified JSON file
        network_config_json_file = 'nebulaFiles/networkConfig.json'
        populate_tables_from_json(network_config_json_file)

    print("Dati popolati con successo nelle tabelle UTENTE, CERT, MACCHINA, REGOLA.")
