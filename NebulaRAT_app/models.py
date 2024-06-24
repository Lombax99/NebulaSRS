from app import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descrizione = db.Column(db.String(255))

    def __init__(self, descrizione=None):
        self.descrizione = descrizione