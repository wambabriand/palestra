# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
import userdao
import loginfile
import corsodao
import clientidao
import initdb

initdb.initDb();

app = Flask(__name__)

app.config['SESSION_TYPE']= 'filesystem'
app.config['SESSION_PERMANENT']= False
Session(app)

listacorsi = [{"nome": "Corso 1", "id": 1, "descrizione": "descrizione qundaaaa", "votoMedia": 4,
    "commenti" : [
        {"autore":"Mario Rossi", "commento":"il commento perfetto","voto": 5},
        {"autore":"Mario Rossi", "commento":"il commento perfetto","voto": 5},
        {"autore":"Mario Rossi", "commento":"il commento perfetto","voto": 5},
    ]}, {"nome": "Corso 2", "id": 2}, {"nome": "Corso 3", "id": 3}]
listauser = []


# ok
@app.route("/iscrizione", methods=["POST"])
def iscrizione():
    idUser = session['id']
    idCorso = request.form['idcorso']
    corsodao.iscriverti(idCorso, idUser)
    return redirect(url_for('corsoById', id=idCorso))


# vota
@app.route("/vota", methods=["POST"])
def vota():
    vuoto = request.form['voto']
    idCorso = request.form['idcorso']
    corsodao.vota(session['id'], idCorso, vuoto)
    return redirect(url_for('corsoById', id=idCorso))


@app.route("/clienti")
def clienti():
    users = clientidao.getClienti();

    print(users)
    return render_template('clienti.html', clienti=listacorsi)

@app.route("/")
def index():
    role = session['ruolo']
    listacorsi = corsodao.getCorsi(role)
    return render_template('corsi.html', session=session, listacorsi=listacorsi)



@app.route("/corsi/<int:id>")
def corsoById(id,message=""):

    res = corsodao.getCorsoById(id, session['id'],session['ruolo'])
    role = session['ruolo']
    listacorsi = corsodao.getCorsi(role)
    # anonimo
    if not session['ruolo']:
        return render_template('corsi.html', listacorsi=listacorsi, corso=res['corso'])
    # user logato
    return render_template('corsi.html', session=session, listacorsi=listacorsi, corso=res['corso'])

# ok
@app.route("/nuovo-corso", methods=['GET', 'POST'])
def nuovoCorso():
    if request.method == "GET":
        return render_template('nuovoCorso.html')
    else:
        res = corsodao.creaNuovoCorso(request)
        return render_template('nuovoCorso.html', result=res)


@app.route("/abbonamento", methods=['GET', 'POST'])
def abbonamento():
    userId = session['id']
    if request.method == "GET":
        info = clientidao.getAbbonamentoInf(userId)
        return render_template('abbonamento.html', abbonamento=info)
    else:
        clientidao.deAbbonna(userId)
        info = clientidao.getAbbonamentoInf(userId)
        return render_template('abbonamento.html', abbonamento=info)


@app.route("/user")
def userpage():
    usercorsi = []
    for corso in listacorsi:
        if corso['id'] == 1:
            corso['stato'] = "NUOVO"
        if corso['id'] == 2:
            corso['stato'] = "PRENOTATO"
        if corso['id'] == 3:
            corso['stato'] = "PASSATO"
        if corso['id'] == 4:
            corso['stato'] = "NOTATO"
        usercorsi.append(corso)
    print(session)
    return render_template('user.html', corsi = usercorsi)


def isValidSession ():
    if not session['email']:
        return False
    return True
@app.route("/personale")
def personalepage():
    if not isValidSession():
        return redirect(url_for("login"))
    # devono venire dal data base
    return render_template('personale.html', listacorsi=listacorsi)
@app.route("/personale/corsi")
def personaleCorsi():
    # devono venire dal data base
    return render_template('personale.html', listacorsi=listacorsi)



@app.route("/corsi", methods=['GET', 'POST'])
def corsi():

    print(session)
        # devono venire dal data base
    if request.method == "POST":
        return redirect(url_for('personalepage'))
    else:
        return render_template('corsi.html', listacorsi=listacorsi)

@app.route("/logout", methods= ['GET', 'POST'])
def logout():
    session['id'] = None
    session['cognome'] = None
    session['email'] = None
    session['ruolo'] = None
    session['nome'] = None
    return redirect(url_for('index'))

@app.route("/login", methods= ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
       #Se provenga da una POST => si vuole fare il login
       res = userdao.doLogin(request)
       if not res['result']:
           return render_template('login.html', message=res['message'])
       else:
           session['id'] = res['id']
           session['email'] = res['email']
           session['ruolo'] = res['ruolo']
           session['nome'] = res['nome']
           session['cognome'] = res['cognome']
           return redirect(url_for('corsi'))

@app.route("/test")
def totototo():
    listacorsi = corsodao.getCorsoById(1,None)
    print(listacorsi)
    return "Helloo"

@app.route("/register", methods= ['GET', 'POST'])
def register():
    if request.method == "POST":
        result = userdao.registerUser(request)
        if result['result']:
            return redirect(url_for("login"))
        else:
            return render_template('register.html', result=result)
    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
