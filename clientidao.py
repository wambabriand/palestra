import  sqlite3
import datetime

def getClienti ():
    # check if user have role
    conn = sqlite3.connect('db/palestra.db')
    cursor = conn.cursor()
    sql = 'SELECT nome, cognome FROM user WHERE ruolo = "CLIENTI"'
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


def deAbbonna (iduser):
    try:
        if isAbbonnatoAttivo(iduser):
            conn = sqlite3.connect('db/palestra.db')
            cursor = conn.cursor()
            sql = 'UPDATE user SET dataDeactivazione = ? WHERE id = ?'

            x = datetime.datetime.now()
            date = x.strftime("%Y-%m-%d")

            print(date)
            print(isAbbonnatoAttivo(iduser))
      #      cursor.execute(sql, (date, iduser))
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print('ERROR', str(e))


def isAbbonnatoAttivo(iduser):
    try:
        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        sql = 'SELECT dataDeactivazione FROM user WHERE id = ?'
        cursor.execute(sql, (iduser,))
        data = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        if data[0]:
            return True
        return False
    except Exception as e:
        print('ERROR', str(e))
    return False


def getAbbonamentoInf(iduser):
    try:
        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        sql = 'SELECT dataDeactivazione FROM user WHERE id = ?'
        cursor.execute(sql, (iduser,))
        data = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        print(data)
        if data[0]:
            return {"attivo": False, "desattivatedDate":data[0], "message": "Il tuo abbonamento è disattivato con successo"}
        return {"attivo": True}
    except Exception as e:
        print('ERROR', str(e))
    return False
