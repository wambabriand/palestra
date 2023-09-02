import  sqlite3

def initDb ():

    print("Debut initialisation")
    conn = sqlite3.connect('palestra.db')
    cursor = conn.cursor()
    sql = ("""CREATE TABLE IF NOT EXISTS user 
    ( 
        id INTEGER NOT NULL PRIMARY KEY,
	    nome TEXT NOT NULL,
	    cognome TEXT NOT NULL,
	    email TEXT NOT NULL UNIQUE,
	    ruolo TEXT NOT NULL ,
	    password TEXT NOT NULL ,
	    dataDeactivazione DATE
    ) """)
    cursor.execute(sql)

    sql = ("""CREATE TABLE IF NOT EXISTS corso ( 
            id INTEGER NOT NULL PRIMARY KEY,
    	    titolo TEXT NOT NULL,
    	    descrizione TEXT NOT NULL,
    	    istruttore TEXT NOT NULL UNIQUE,
    	    startTime DATE NOT NULL ,
    	    endTime DATE NOT NULL
        ) """)
    cursor.execute(sql)


    sql = ("""CREATE TABLE IF NOT EXISTS corso_iscritto ( 
            id_user INTEGER NOT NULL,
            id_corso INTEGER NOT NULL,
            voto INTEGER,
            CONSTRAINT key_c_i PRIMARY KEY (id_user, id_corso)  
        ) """)
    cursor.execute(sql)

    # delete dtable
    sql = ("""DROP TABLE corso_iscritto""")
    #cursor.execute(sql)

    cursor.close()
    conn.close()

    print("Debut initialisation")
    return