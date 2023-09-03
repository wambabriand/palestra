# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session

from flask_login import LoginManager, logout_user, login_required

import userdao
import corsodao
import clientidao
import initdb

initdb.initDb();

app = Flask(__name__)

app.config['SESSION_TYPE']= 'filesystem'
app.config['SESSION_PERMANENT']= False
Session(app)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# ok
@app.route("/iscrizione", methods=["POST"])
def iscrizione():
    idUser = session['id']
    idCorso = request.form['idcorso']
    corsodao.iscriverti(idCorso, idUser)
    return redirect(url_for('corsoById', id=idCorso))


# vota
@app.route("/vota", methods=["POST"])
@login_required
def vota():
    vuoto = request.form['voto']
    idCorso = request.form['idcorso']
    corsodao.vota(session['id'], idCorso, vuoto)
    return redirect(url_for('corsoById', id=idCorso))


@app.route("/clienti")
@login_required
def clienti():
    users = clientidao.getClienti()
    return render_template('clienti.html', clienti=users)

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
@login_required
def nuovoCorso():
    if request.method == "GET":
        return render_template('nuovoCorso.html')
    else:
        res = corsodao.creaNuovoCorso(request)
        return render_template('nuovoCorso.html', result=res)


@app.route("/abbonamento", methods=['GET', 'POST'])
@login_required
def abbonamento():
    userId = session['id']
    if request.method == "GET":
        info = clientidao.getAbbonamentoInf(userId)
        return render_template('abbonamento.html', abbonamento=info)
    else:
        clientidao.deAbbonna(userId)
        info = clientidao.getAbbonamentoInf(userId)
        return render_template('abbonamento.html', abbonamento=info)



@app.route("/logout", methods= ['GET', 'POST'])
def logout():
    session['id'] = None
    session['cognome'] = None
    session['email'] = None
    session['ruolo'] = None
    session['nome'] = None
    logout_user()
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
           return redirect(url_for('index'))



@app.route("/test")
@login_required
def apiperprova():
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

@login_manager.user_loader
def load_user():
    utente1 = userdao.getAccountByEmail(request.form['email'])
    utente2 = userdao.getAccountByEmail(request.form['id'])
    if utente1:
        return utente1
    return utente2


if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
