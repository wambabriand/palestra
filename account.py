

def validText(text):
    if not text:
        return False
    return True

def validEmail(email):
    if not email:
        return False
    return True

def validPassword(password):
    if not password:
        return False
    return True

def creaAccount(request):

    if not validText(request.form['nome']):
        return False

    if not validText(request.form['cognome']):
        return False

    if not validText(request.form['email']):
        return False

    if not validText(request.form['ruolo']):
        return False

    if not validText(request.form['password1']):
        return False

    if not validText(request.form['password2']):
        return False

    if request.form['password2'] != request.form['password1']:
        return False

    return  True
