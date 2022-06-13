import sqlite3
conn = sqlite3.connect('Auto_Plac.db')
c = conn.cursor()
c.execute('''CREATE TABLE Automobil(ID INTEGER PRIMARY KEY NOT NULL, MARKA TEXT NOT NULL, MODEL TEXT NOT NULL, GODISTE INTEGER NOT NULL, CENA INTEGER, DATUM DATETIME NOT NULL)''')
conn.commit()
conn.close()