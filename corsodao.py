import  sqlite3
import util


def getMaxCorsoId():
    conn = sqlite3.connect('palestra.db')
    cursor = conn.cursor()
    sql = (""" SELECT MAX(id) FROM corso  """)
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

def creaNuovoCorso(req):
    res = {}
    try:
        if not util.validText(req.form['titolo']):
            res['result'] = False
            res['message'] = "Il Titole non è valido"
            return res
        if not util.validText(req.form['descrizione']):
            res['result'] = False
            res['message'] = "La descrizione non è valido"
            return res
        if not util.validText(req.form['istruttore']):
            res['result'] = False
            res['message'] = "L istruttore non è valido"
            return res
        if not util.validText(req.form['startTime']):
            res['result'] = False
            res['message'] = "La data di inizio non è valido"
            return res
        if not util.validText(req.form['endTime']):
            res['result'] = False
            res['message'] = "La data di fine non è valido"
            return res

        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()

        id = getMaxCorsoId()
        sql = (""" 
            INSERT INTO 
            corso(id,titolo,descrizione,istruttore,startTime,endTime) 
            VALUES (?,?,?,?,?,?) """)
        cursor.execute(sql, (id,req.form['titolo'], req.form['descrizione'],
                             req.form['istruttore'], req.form['startTime'], req.form['endTime']))

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


def mapper(d):
    data = {}
    data['id'] = d[0]
    data['titolo'] = d[1]
    data['descrizione'] = d[2]
    data['istruttore'] = d[3]
    data['startTime'] = d[4]
    data['endTime'] = d[5]
    return data


def getCorsi(role):
    res = {}
    try:
        sql = (""" 
                SELECT id,titolo,descrizione,istruttore,startTime,endTime
                FROM corso
            """)
        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        cursor.execute(sql)

        mapped = []
        for data in cursor.fetchall():
            mapped.append(mapper(data))

        res['result'] = True
        res['data'] = mapped
    except Exception as e:
        return []
        print('ERROR', str(e))
    cursor.close()
    conn.close()
    return mapped


def getCorsoById(id, idUser, ruolo):
    res = {}
    try:
        sql = (""" 
                SELECT id,titolo,descrizione,istruttore,startTime,endTime
                FROM corso
                WHERE id = ?
            """)
        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        data = mapper(cursor.fetchone())

        media = getMediaVoto(id, idUser)
        data['media'] = media
        res['corso'] = data
        commenti = getVoti(id)
        data['commenti'] = commenti

        if ruolo == "CLIENTE":
            userCorso = getUserCorso(idUser, id)
            if userCorso['result']:
                if not userCorso['voto']:
                    data['canGiveVoto'] = True
                else:
                    data['canGiveVoto'] = False
            else:
                data['canEnroll'] = True

            res['result'] = True
            res['corso'] = data
            return res

        if ruolo == "ADMIN":
            iscritti = getIscritti(id)
            data['iscritti'] = iscritti
            res['result'] = True
            return res
        res['result'] = True
    except Exception as e:
        res['result'] = True
        res['message'] = str(e)
        print('ERROR', str(e))
    cursor.close()
    conn.close()
    return res


def getIscritti (id) :
    try:
        sql = (""" 
            SELECT u.nome, u.cognome, ci.voto
            FROM  corso_iscritto ci , user u
            WHERE ci.id_corso = ? AND u.id = ci.id_user
        """)
        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        cursor.execute(sql, (id,))

        mapped = []
        for data in cursor.fetchall():
            mapped.append({ 'nome': data[0], 'cognome': data[1], 'voto': data[2] })

        cursor.close()
        conn.close()
        return mapped
    except Exception as e:
        print('ERROR', str(e))
        cursor.close()
        conn.close()
        return []


def getUserCorso (idUser, idCorso) :
    try:
        sql = (""" 
            SELECT id_user, voto
            FROM  corso_iscritto 
            WHERE id_corso = ? AND id_user = ?
        """)
        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        cursor.execute(sql, (idCorso, idUser))
        data = cursor.fetchone()
        res = {}
        if data :
            res['id_user'] = data[0]
            res['voto'] = data[1]
            res['result'] = True
        else :
            res['result'] = False
        cursor.close()
        conn.close()
        return res
    except Exception as e:
        print('ERROR', str(e))
        cursor.close()
        conn.close()
        return {'result':False}


def iscriverti (idCorso, idUser):
    try:
        userCorso = getUserCorso(idUser, idCorso)
        res = {}
        if not userCorso['result']:
            sql = (""" INSERT INTO corso_iscritto (id_corso, id_user) VALUES (?, ?) """)
            conn = sqlite3.connect('palestra.db')
            cursor = conn.cursor()
            cursor.execute(sql, (idCorso,idUser))

            conn.commit()
            cursor.close()
            conn.close()
            res['result'] = True
            res['message'] = "Iscrizione andato bene"
        else :
            res['result'] = False
            res['message'] = "Non ti puoi iscrivere a questo corso"

        return res
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
        cursor.close()
        conn.close()
        res['result'] = False
        res['message'] = str(e)
        return res



def vota(idUser, idCorso, voto):
    try:
        userCorso = getUserCorso(idUser, idCorso)
        res = {}
        if userCorso['result'] and not userCorso['voto'] :
            sql = (""" UPDATE corso_iscritto SET voto = ? WHERE id_user = ? AND id_corso = ? """)
            conn = sqlite3.connect('palestra.db')
            cursor = conn.cursor()
            cursor.execute(sql, (voto,idUser,idCorso))

            conn.commit()
            cursor.close()
            conn.close()
            res['result'] = True
            res['message'] = "Votazione presso in considerazione"
        else:
            res['result'] = False
            res['message'] = "Votazione non è presso in considerazione"
        return res
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
        cursor.close()
        conn.close()
        res['result'] = False
        res['message'] = str(e)
        return res


def getMediaVoto( idCorso, idUser=None):
    try:
        sql = (""" SELECT AVG(voto) FROM corso_iscritto WHERE voto IS NOT NULL AND id_corso = ? """)
        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        cursor.execute(sql, (idCorso,))
        media = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return media
    except Exception as e:
        print('ERROR', str(e))
        cursor.close()
        conn.close()



def getVoti( idCorso):
    try:
        sql = ("""  SELECT u.nome, u.cognome, ci.voto FROM  corso_iscritto ci , user u
                    WHERE ci.id_corso = ? AND u.id = ci.id_user AND ci.voto IS NOT NULL
             """)
        conn = sqlite3.connect('palestra.db')
        cursor = conn.cursor()
        cursor.execute(sql, (idCorso,))
        dati = []
        for data in cursor.fetchall():
            dati.append({'nome': data[0], 'cognome': data[1],'voto': data[2]})

        cursor.close()
        conn.close()
        return dati
    except Exception as e:
        print('ERROR', str(e))
        cursor.close()
        conn.close()
        return []

