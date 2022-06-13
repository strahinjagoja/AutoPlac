import datetime
import json
from tkinter import *
import tkinter
import threading
import time
from datetime import datetime
import sqlite3
from functools import reduce
zahtev=""
primljeno=""
slanje=""
red=0
def Dinari(x):
    return x*118
def Pokreni():
    import socket  # Import socket module
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12345  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    while True:
        conn, addr = s.accept()  # Establish connection with client.
        print('Got connection from', addr)
        global zahtev
        global slanje
        global primljeno
        zahtev=conn.recv(1024).decode()
        if(zahtev=="Upis"):
            slanje="Upis u bazu"
            conn.send(slanje.encode())
            global primljeno
            primljeno=conn.recv(1024).decode()
            print(primljeno)
            print(type(primljeno))
            zaupis=json.loads(primljeno)    #Recnik
            print(zaupis)
            print(type(zaupis))
            try:
                connsql = sqlite3.connect('Auto_Plac.db')
                c = connsql.cursor()
                vreme=datetime.now().strftime("%B %d, %Y %I:%M%p")
                c.execute('''INSERT INTO AUTOMOBIL (MARKA, MODEL, GODISTE, CENA, DATUM) VALUES (?, ?, ?, ?, ?)''', (zaupis['marka'], zaupis['model'], zaupis['godiste'], zaupis['cena'], vreme))
                for row in c.execute('SELECT * FROM AUTOMOBIL'):
                    print(row)
                connsql.commit()
                slanje="Uspesno upisani podaci!"
                conn.send(slanje.encode())
                global red
                red += 1
                Lb1.insert(red, "KLIJENT:" + zaupis['marka'] + " " + zaupis['model'] + " " + str(
                    zaupis['godiste']) + " - " + str(zaupis['cena']) + "e")
                red += 1
                Lb1.insert(red, "SERVER: waiting")
            except ValueError:
                slanje="Greska pri upisu!"
                conn.send(slanje.encode())
            finally:
                connsql.close()
                conn.close()


        elif(zahtev=="Izlistaj"):
            slanje = "Izlistaj u datoteku"
            red+=1
            Lb1.insert(red, "KLIJENT: "+ slanje)
            red+=1
            Lb1.insert(red, "SERVER: waiting")
            conn.send(slanje.encode())
            try:
                connsql = sqlite3.connect('Auto_Plac.db')
                c = connsql.cursor()
                c.execute('SELECT MARKA, MODEL, GODISTE, CENA FROM AUTOMOBIL')
                rezultat=c.fetchall()
                slanje=json.dumps(rezultat)
                print(slanje)
                connsql.commit()
                connsql.close()
                conn.send(slanje.encode())
                info="Uspesno uzeti podaci iz baze!"
                print(info)
            except:
                info = "Greska pri konektovanju sa bazom!"
                print(info)
            finally:
                conn.close()

        elif(zahtev=="Pretvori"):
            slanje = "Pretvori u dinare"
            red += 1
            Lb1.insert(red, "KLIJENT: " + slanje)
            red += 1
            Lb1.insert(red, "SERVER: waiting")
            conn.send(slanje.encode())
            connsql = sqlite3.connect('Auto_Plac.db')
            c = connsql.cursor()
            c.execute('SELECT MARKA, MODEL, GODISTE FROM AUTOMOBIL')
            rezultat1 = c.fetchall()
            print(rezultat1)           # Entorka
            rezultat1l=[list(elem) for elem in rezultat1]
            print(rezultat1l)
            c.execute('SELECT CENA FROM AUTOMOBIL')
            rezultat2 = c.fetchall()
            connsql.commit()
            connsql.close()
            print(rezultat2)
            pr1=[x for t in rezultat2 for x in t]
            print(pr1)
            pr2=list(map(Dinari, pr1))
            print(pr2)
            i=0
            for l in rezultat1l:
                l.append(pr2[i+1])
                # i+=1
            slanje=json.dumps(rezultat1l)
            conn.send(slanje.encode())
            conn.close()

        elif(zahtev=="Izracunaj"):
            slanje = "Izracunaj ukupnu cenu svih automobila"
            red += 1
            Lb1.insert(red, "KLIJENT: " + slanje)
            red += 1
            Lb1.insert(red, "SERVER: waiting")
            conn.send(slanje.encode())
            connsql = sqlite3.connect('Auto_Plac.db')
            c = connsql.cursor()
            c.execute('SELECT CENA FROM AUTOMOBIL')
            rezultat = c.fetchall()
            connsql.commit()
            connsql.close()
            cene = [x for t in rezultat for x in t]
            slanje = reduce( (lambda x, y: x + y), cene )
            conn.send(str(slanje).encode())
            print(slanje)
            conn.close()

        elif(zahtev=="Filtriraj"):
            slanje = "Filtriraj po godistu"
            red += 1
            Lb1.insert(red, "KLIJENT: " + slanje)
            red += 1
            Lb1.insert(red, "SERVER: waiting")
            conn.send(slanje.encode())
            primljeno = int(conn.recv(1024).decode())
            print(primljeno)
            connsql = sqlite3.connect('Auto_Plac.db')
            c = connsql.cursor()
            c.execute('SELECT MARKA, MODEL, GODISTE, CENA FROM AUTOMOBIL')
            rezultat1 = c.fetchall()
            print(rezultat1)
            rezultat1l = [list(elem) for elem in rezultat1]
            print(rezultat1l)
            c.execute('SELECT GODISTE FROM AUTOMOBIL')
            rezultat2 = c.fetchall()
            connsql.commit()
            connsql.close()
            pr1 = [x for t in rezultat2 for x in t]
            #pr2=[]
            #for pod in rezultat1l:
                #pr2.append(list( filter((lambda x: x[2] ==primljeno), pod)))
            filt =list(filter(lambda a:int(a[2])==primljeno, rezultat1l))
            #pr2 = list(map(lambda a:a, filt))
            print(filt)
            slanje=json.dumps(filt)
            conn.send(slanje.encode())
tr1=threading.Thread(target=Pokreni)

top = tkinter.Tk()
top.geometry("500x500")
Lb1 = Listbox(top, selectmode=SINGLE, height=100, width=100)
Lb1.pack()
Lb1.insert(red, "SERVER: waiting")
tr1.start()
top.mainloop()