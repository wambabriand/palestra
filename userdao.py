import  sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def validText(text):
    if text:
        return True
    return False

def registerUser(req):
    res = {}
    try:
        if not validText(req.form['nome']):
            res['result'] = False
            res['message'] = "Il nome non è valido"
            return res
        if not validText(req.form['cognome']):
            res['result'] = False
            res['message'] = "Il cognome non è valido"
            return res
        if not validText(req.form['email']):
            res['result'] = False
            res['message'] = "Il email non è valido"
            return res
        if not validText(req.form['ruolo']):
            res['result'] = False
            res['message'] = "Il ruolo non è valido"
            return res
        if not validText(req.form['password1']):
            res['result'] = False
            res['message'] = "Il password1 non è valido"
            return res
        if not validText(req.form['password2']):
            res['result'] = False
            res['message'] = "Il password2 non è valido"
            return res
        if req.form['password2'] != req.form['password2']:
            res['result'] = False
            res['message'] = "Le password sono diverso"
            return res

        id = getMaxUserId()
        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        sql = (""" INSERT INTO user(id,nome,cognome,email,ruolo,password) VALUES (?,?,?,?,?,?) """)
        cursor.execute(sql, (id,req.form['nome'], req.form['cognome'],
                             req.form['email'], req.form['ruolo'],
                             generate_password_hash(req.form['password1'], method='sha256') ))

        conn.commit()
        res['result'] = True
        res['message'] = "La registrazione andato a buone fine"
    except Exception as e:
        res['result'] = False
        res['message'] = str(e)
        print('ERROR', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return res


def getMaxUserId():
    conn = sqlite3.connect('palestra.db')
    cursor = conn.cursor()
    sql = (""" SELECT MAX(id) FROM user  """)
    cursor.execute(sql)
    data = cursor.fetchone()
    print(data)
    if data[0] == None:
        res = 1
    else:
        res = data[0]+1
    cursor.close()
    conn.close()
    return res

def doLogin(req):
    try:
        res = {}
        if not validText(req.form['email']):
            res['result'] = False
            res['message'] = "Email non è valido"
            return res
        if not validText(req.form['password']):
            res['result'] = False
            res['message'] = "La password non è valido"
            return res

        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        sql = (""" 
            SELECT id, email, password, nome, cognome, ruolo, password
            FROM user
            WHERE email = (?) 
        """)
        email = req.form['email']
        cursor.execute(sql, (email,))
        data = cursor.fetchone()

        #print( check_password_hash(data[2], req.form['password']) )
        if data == None:
            res['result'] = False
            res['message'] = "Email non esiste"
            return res
        if not check_password_hash(data[2], req.form['password']):
            res['result'] = False
            res['message'] = "Password sbagliata"
            return res

        res['result'] = True
        res['id'] = data[0]
        res['email'] = data[1]
        res['ruolo'] = data[5]
        res['nome'] = data[3]
        res['cognome'] = data[4]
        res['password'] = data[6]
    except Exception as e:
        res['result'] = False
        res['message'] = str(e)
    cursor.close()
    conn.close()
    return res



def getAccountByEmail(email):
    user = {}
    conn = sqlite3.connect('palestra.db')
    cursor = conn.cursor()
    sql = (""" 
                SELECT id, email, password, nome, cognome, ruolo
                FROM user
                WHERE email = (?)  OR id = (?)
            """)
    cursor.execute(sql, (email,email))
    data = cursor.fetchone()

    if data == None:
        return None

    user['id'] = data[0]
    user['email'] = data[1]
    user['password'] = data[2]
    user['ruolo'] = data[5]
    user['nome'] = data[3]
    user['cognome'] = data[4]

    return user

