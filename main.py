# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session

from flask_login import LoginManager, login_user,logout_user,current_user, login_required

import userdao
import corsodao
import clientidao
import initdb
from models import User

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
    idUser = current_user.id
    idCorso = request.form['idcorso']
    corsodao.iscriverti(idCorso, idUser)
    return redirect(url_for('corsoById', id=idCorso))


# vota
@app.route("/vota", methods=["POST"])
@login_required
def vota():
    vuoto = request.form['voto']
    idCorso = request.form['idcorso']
    corsodao.vota(current_user.id, idCorso, vuoto)
    return redirect(url_for('corsoById', id=idCorso))


@app.route("/clienti")
@login_required
def clienti():
    users = clientidao.getClienti()
    return render_template('clienti.html', session=getSession(), clienti=users)

@app.route("/")
def index():
    role = None
    if current_user.is_authenticated and current_user.ruolo:
        role = current_user.ruolo
    listacorsi = corsodao.getCorsi(role)
    return render_template('corsi.html', session=getSession(), listacorsi=listacorsi)


def getSession () :
    if current_user.is_authenticated:
        return userdao.getAccountByEmail(current_user.id)
    return None

@app.route("/corsi/<int:id>")
def corsoById(id,message=""):
    role = None
    idUser = None
    if current_user.is_authenticated:
        idUser = current_user.id
        role = current_user.ruolo
    listacorsi = corsodao.getCorsi(role)
    res = corsodao.getCorsoById(id, idUser, role)
    if not current_user.is_authenticated:
        return render_template('corsi.html', session=getSession(), listacorsi=listacorsi, corso=res['corso'])
    # user logato
    return render_template('corsi.html', session=getSession(), listacorsi=listacorsi, corso=res['corso'])

# ok
@app.route("/nuovo-corso", methods=['GET', 'POST'])
@login_required
def nuovoCorso():
    if request.method == "GET":
        return render_template('nuovoCorso.html',session=getSession())
    else:
        res = corsodao.creaNuovoCorso(request)
        return render_template('nuovoCorso.html', session=getSession(), result=res)


@app.route("/abbonamento", methods=['GET', 'POST'])
@login_required
def abbonamento():
    userId = current_user.id
    if request.method == "GET":
        info = clientidao.getAbbonamentoInf(userId)
        return render_template('abbonamento.html', session=getSession(), abbonamento=info)
    else:
        clientidao.deAbbonna(userId)
        info = clientidao.getAbbonamentoInf(userId)
        return render_template('abbonamento.html',session=getSession(), abbonamento=info)



@app.route("/logout", methods= ['GET', 'POST'])
@login_required
def logout():
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
           user = User(id=res['id'], email=res['email'], password=res['password'],
                       ruolo=res['ruolo'], nome=res['nome'], cognome=res['cognome'])
           login_user(user, True)
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
def load_user(userId):
    utente1 = userdao.getAccountByEmail(userId)
    utente2 = userdao.getAccountByEmail(userId)
    if utente1:
        return User(id=utente1['id'], email=utente1['email'], password=utente1['password'],
                       ruolo=utente1['ruolo'], nome=utente1['nome'], cognome=utente1['cognome'])
    if utente2:
        return User(id=utente2['id'], email=utente2['email'], password=utente2['password'],
                       ruolo=utente2['ruolo'], nome=utente2['nome'], cognome=utente2['cognome'])
    return None

if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
