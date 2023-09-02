
def doLogin(request):
    email = request.form['email']
    password = request.form['password']
    print("llllllllllllllllllllllll")
    if email == 'a@aa.a' and password == 'a':
        return True
    return False



def getAccount(email):
    return {
        'email': email,
        'ruolo': 'CLIENTE',
        'nome': 'Mario',
        'cognome' :'Rossi'
    }


