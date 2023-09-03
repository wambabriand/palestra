from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password, ruolo, nome, cognome):
        self.id = id
        self.email = email
        self.password = password
        self.ruolo = ruolo
        self.nome = nome
        self.cognome = cognome

