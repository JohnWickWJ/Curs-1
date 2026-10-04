PARAMETRI={"senzor": ("temperatura", "umiditate"), "pompa": ("debit",), "ventilator": ("turatie",), "iluminat": ("intensitate",)}
CONSUM={"senzor": 2, "pompa": 150, "ventilator": 80, "iluminat": 200}
LIMITE={"temperatura": (-10, 60), "umiditate": (0, 100), "debit": (0, 20), "turatie": (0, 1500), "intensitate": (0, 100),}
sistem={}

def inregistreaza(id, tip, nume, stare, parametri):
    sistem[id]={"tip": tip, "nume": nume, "stare": stare, "parametri": parametri}
    return "Echipament adaugat"

def eroare(mesaj):
    print("Eroare:", mesaj)
    print("Echipamentul nu s-a adaugat")

def e_numar(text):
    return text.replace(".", "", 1).isdigit()

def adauga_echipament():
    id=input("ID: ")
    if not id.isdigit():
        eroare("ID-ul trebuie sa contina doar cifre")
        return
    if id in sistem:
        eroare("ID deja folosit")
        return
    tip=input("Tip ("+"senzor/pompa/ventilator/iluminat"+"): ")
    if tip not in PARAMETRI:
        eroare("tip necunoscut")
        return
    nume=input("Nume: ")
    stare=input("Stare (pornit/oprit): ")
    if stare not in ("pornit", "oprit"):
        eroare("stare invalida")
        return
    parametri={}
    for p in PARAMETRI[tip]:
        minim, maxim=LIMITE[p]
        text=input(p+" ("+str(minim)+" - "+str(maxim)+"): ")
        if not e_numar(text):
            eroare("valoarea trebuie sa fie numar")
            return
        valoare=float(text)
        if valoare<minim or valoare>maxim:
            eroare("valoare in afara limitelor")
            return
        parametri[p]=valoare
    print(inregistreaza(id, tip, nume, stare, parametri))

def afiseaza(id):
    e=sistem[id]
    if e["stare"]=="pornit":
        print(id, "|", e["nume"], "|", e["tip"], "|", e["stare"], "|", e["parametri"])
    else:
        print(id, "|", e["nume"], "|", e["tip"], "|", e["stare"])

def listeaza():
    for id in sistem:
        afiseaza(id)

def citeste(id):
    if id not in sistem:
        return None
    return sistem[id]

def comanda(id, actiune, param="", valoare=0.0):
    e=citeste(id)
    if e is None:
        return "Eroare: echipament inexistent"
    if actiune=="porneste":
        if e["stare"]=="pornit":
            return "Echipamentul este deja pornit"
        else:
            e["stare"]="pornit"
    elif actiune=="opreste":
        if e["stare"]=="oprit":
            return "Echipamentul este deja oprit"
        else:
            e["stare"]="oprit"
    elif actiune=="seteaza":
        if param not in e["parametri"]:
            return "Eroare: parametru invalid pentru acest tip"
        minim, maxim=LIMITE[param]
        if valoare<minim or valoare>maxim:
            return "Eroare: valoare in afara limitelor"
        e["parametri"][param]=valoare
    else:
        return "Eroare: actiune necunoscuta"
    return "Comanda executata"

def trimite_comanda():
    id=input("ID: ")
    e=citeste(id)
    if e is None:
        print("Eroare: echipament inexistent")
        return
    actiune=input("Actiune (porneste/opreste/seteaza): ")
    if actiune not in ("porneste", "opreste", "seteaza"):
        print("Eroare: actiune necunoscuta")
        return
    if actiune!="seteaza":
        print(comanda(id, actiune))
        return
    param=input("Parametru ("+", ".join(e["parametri"])+"): ")
    if param not in e["parametri"]:
        print("Eroare: parametru invalid pentru acest tip")
        return
    text=input("Valoare: ")
    if not e_numar(text):
        print("Eroare: valoarea trebuie sa fie numar")
        return
    print(comanda(id, actiune, param, float(text)))

def agregare():
    active=0
    consum=0
    temperaturi=[]
    for e in sistem.values():
        if e["stare"]=="pornit":
            active+=1
            consum+=CONSUM[e["tip"]]
            if e["tip"]=="senzor":
                temperaturi.append(e["parametri"]["temperatura"])
    print("Total echipamente:", len(sistem))
    print("Echipamente active:", active)
    print("Consum total (W):", consum)
    if len(temperaturi)>0:
        print("Temperatura medie:", round(sum(temperaturi)/len(temperaturi), 1))
    else:
        print("Temperatura medie: niciun senzor pornit")

def date_test():
    inregistreaza("1", "senzor", "Senzor nord", "pornit", {"temperatura": 26.5, "umiditate": 60.0})
    inregistreaza("2", "senzor", "Senzor sud", "pornit", {"temperatura": 23.0, "umiditate": 55.0})
    inregistreaza("3", "pompa", "Pompa irigatie", "oprit", {"debit": 5.0})
    inregistreaza("4", "ventilator", "Ventilator acoperis", "pornit", {"turatie": 900.0})
    inregistreaza("5", "iluminat", "Lumini crestere", "oprit", {"intensitate": 50.0})

def meniu():
    while True:
        print("\n   MENIU   ")
        print("\n 0.Iesire\n 1.Inregistrare\n 2.Listare\n 3.Comanda\n 4.Citire\n 5.Agregare\n")
        opt=input("Alege: ")
        match opt:
            case "0":
                print("La revedere")
            case "1":
                adauga_echipament()
            case "2":
                listeaza()
            case "3":
                trimite_comanda()
            case "4":
                id=input("ID: ")
                if citeste(id) is None:
                    print("Eroare: echipament inexistent")
                else:
                    afiseaza(id)
            case "5":
                agregare()
            case _:
                print("Optiune invalida")
        if opt=="0":
            break

date_test()
meniu()