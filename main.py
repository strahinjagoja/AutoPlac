import json
from tkinter import *
import tkinter
import Automobil
import threading
import time
from datetime import datetime
zahtev=""
primljeno=""
red=0
def Upisi():
    import socket  # Import socket module
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12345  # Reserve a port for your service.
    s.connect((host, port))
    global zahtev
    zahtev="Upis"
    s.send(zahtev.encode())
    global primljeno
    primljeno=s.recv(1024).decode()
    print(primljeno)
    try:
        Auto = Automobil.Automobil(em1.get(), em2.get(), int(em3.get()), int(em4.get())).to_json()
        s.send(Auto.encode())
        primljeno = s.recv(1024).decode()
        print(primljeno)
        Lb1.delete(0, "end")
        Lb1.insert(red, primljeno)
        primljeno = s.recv(1024).decode()
        print(primljeno)
    except:
        print("Greska pri unosu")
    finally:
        s.close()

def Izlistaj():
    import socket  # Import socket module
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12345  # Reserve a port for your service.
    s.connect((host, port))
    global zahtev
    zahtev = "Izlistaj"
    s.send(zahtev.encode())
    global primljeno
    primljeno = s.recv(1024).decode()
    Lb1.delete(0, "end")
    Lb1.insert(red, "Izlistano u datoteku!")
    primljeno = s.recv(1024).decode()
    print(primljeno)
    llisti=json.loads(primljeno)
    fp = open('podaci.txt', 'w')
    zafajl=""
    for lista in llisti:
        for podatak in lista:
            if(podatak==lista[3]):
                zafajl+="- " + str(podatak)+"e\n"
            else:
                zafajl+=str(podatak)+" "
    fp.write(zafajl)
    fp.close()
    s.close()

def Pretvori():
    import socket  # Import socket module
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12345  # Reserve a port for your service.
    s.connect((host, port))
    global zahtev
    zahtev = "Pretvori"
    s.send(zahtev.encode())
    global primljeno
    primljeno = s.recv(1024).decode()
    print(primljeno)
    global red
    Lb1.delete(0, "end")
    Lb1.insert(red, primljeno+":\n")
    red+=1
    primljeno = s.recv(1024).decode()
    podaci=json.loads(primljeno)
    for lista in podaci:
        zaprikaz = ""
        for podatak in lista:
            if (podatak == lista[3]):
                zaprikaz += "- " + str(podatak) + "din"
            else:
                zaprikaz += str(podatak) + " "
        Lb1.insert(red,zaprikaz)
        red+=1
    red=0
    s.close()

def Izracunaj():
    import socket  # Import socket module
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12345  # Reserve a port for your service.
    s.connect((host, port))
    global zahtev
    global primljeno
    zahtev = "Izracunaj"
    s.send(zahtev.encode())
    primljeno=s.recv(1024).decode()
    print(primljeno)
    global red
    Lb1.delete(0, "end")
    Lb1.insert(red, primljeno + ":\n")
    red += 1
    primljeno = s.recv(1024).decode()
    Lb1.insert(red, "Ukupna cena svih automobila koji su trenutno na oglasu je: "+ primljeno + "e")
    red=0
    s.close()

def Filtriraj():
    import socket  # Import socket module
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12345  # Reserve a port for your service.
    s.connect((host, port))
    global zahtev
    zahtev = "Filtriraj"
    s.send(zahtev.encode())
    global primljeno
    primljeno = s.recv(1024).decode()
    global red
    Lb1.delete(0, "end")
    Lb1.insert(red, primljeno + ":\n")
    red += 1
    zahtev=em5.get()
    s.send(zahtev.encode())
    primljeno=s.recv(1024).decode()
    podaci=json.loads(primljeno)
    for lista in podaci:
        zaprikaz = ""
        for podatak in lista:
            if (podatak == lista[3]):
                zaprikaz += "- " + str(podatak) + "e"
            else:
                zaprikaz += str(podatak) + " "
        Lb1.insert(red, zaprikaz)
        red += 1
    red = 0
    s.close()

def Sat():
    while(1):
       L5.config(text=time.ctime(time.time()).split(" ")[3])
       time.sleep(1)


root = tkinter.Tk()
root.geometry("400x700")
LN = Label(root, text="Auto plac")
LN.config(font=30)
LN.place(relx = 0.52, rely=0.015, anchor=N)
L1 = Label(root, text="Marka:")
L1.place(relx = 0.35, rely=0.12, anchor=CENTER)
em1=StringVar()
E1 = Entry(root, textvariable=em1)
E1.place(relx = 0.6, rely=0.12, anchor=CENTER)
L2 = Label(root, text="Model:")
L2.place(relx = 0.35, rely=0.18, anchor=CENTER)
em2=StringVar()
E2 = Entry(root, textvariable=em2)
E2.place(relx = 0.6, rely=0.18, anchor=CENTER)
L3 = Label(root, text="Godiste:")
L3.place(relx = 0.35, rely=0.24, anchor=CENTER)
em3=StringVar()
E3 = Entry(root, textvariable=em3)
E3.place(relx = 0.6, rely=0.24, anchor=CENTER)
L4 = Label(root, text="Cena:")
L4.place(relx = 0.35, rely=0.30, anchor=CENTER)
em4=StringVar()
E4 = Entry(root, textvariable=em4)
E4.place(relx = 0.6, rely=0.30, anchor=CENTER)
B1 = tkinter.Button(root, text ="Upisi u bazu", command = Upisi, width=15)
B1.place(relx = 0.37, rely=0.39, anchor=CENTER)
B2 = tkinter.Button(root, text="Izlistaj u datoteku", command=Izlistaj, width=15)
B2.place(relx = 0.68, rely=0.39,anchor=CENTER)
B3 = tkinter.Button(root, text="Pretvori u dinare", command=Pretvori, width=15)
B3.place(relx = 0.37, rely=0.45,anchor=CENTER)
B4 = tkinter.Button(root, text="Ukupna cena", command=Izracunaj, width=15)
B4.place(relx = 0.68, rely=0.45,anchor=CENTER)
L5 = Label(root, text="Filtriraj po godini:")
L5.place(relx = 0.42, rely=0.51, anchor=CENTER)
em5=StringVar()
E5 = Entry(root, textvariable=em5, width=12)
E5.place(relx = 0.65, rely=0.51, anchor=CENTER)
B5 = tkinter.Button(root, text="Filtriraj", command=Filtriraj)
B5.place(relx = 0.53, rely=0.57, anchor=CENTER)
Lb1 = Listbox(root, selectmode=SINGLE, height=33, width=60)
Lb1.place(relx = 0.5, rely=1, anchor=CENTER)
L5 = Label(root, text="")
L5.place(relx = 0.5, rely=1, anchor=S)
t1 = threading.Thread(target=Sat)
#t1.setDaemon(True)
t1.start()
root.mainloop()

