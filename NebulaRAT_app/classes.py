from app import db
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descrizione = db.Column(db.String(255))

    def __init__(self, descrizione=None):
        self.descrizione = descrizione
    
class Utente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(255))
    cognome = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, nome=None, cognome=None, username=None, password=None):
        self.nome = nome
        self.cognome = cognome
        self.nome = username
        self.password = password

class Macchina(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descrizione = db.Column(db.String(255))
    cert: Mapped["Cert"] = relationship(back_populates="macchina")
    conf: Mapped["Conf"] = relationship(back_populates="macchina")

    def __init__(self, descrizione=None, cert=None, conf=None):
        self.descrizione = descrizione
        self.cert = cert
        self.conf = conf

class Cert(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descrizione = db.Column(db.String(511))

    def __init__(self, descrizione=None):
        self.descrizione = descrizione

class Conf(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ip_addr = db.Column(db.String(20))
    tcp_timeout = db.Column(db.String(255))
    udp_timeout = db.Column(db.String(255))
    def_timeout = db.Column(db.String(255))

    def __init__(self, ip_addr=None, tcp_timeout=None, udp_timeout=None, def_timeout=None):
        self.ip_addr = ip_addr
        self.tcp_timeout = tcp_timeout
        self.udp_timeout = udp_timeout
        self.def_timeout = def_timeout

class Usa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    macchina_id: Mapped["Macchina"] = relationship(back_populates="macchina")
    utente_id: Mapped["Utente"] = relationship(back_populates="macchina")
    
    def __init__(self, macchina_id=None, utente_id=None):
        self.macchina_id = macchina_id
        self.utente_id = utente_id


class Regola(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ip_addr = db.Column(db.String(10))
    conf: Mapped["Conf"] = relationship(back_populates="macchina")
    port = db.Column(db.String(10))
    proto = db.Column(db.String(10))
    host = db.Column(db.String(255))
    ca_name = db.Column(db.String(255))
    gruppi = db.Column(db.String(500))
    cidr = db.Column(db.String(20))