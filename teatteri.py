import json

with open("./teatteri.json", "r+") as teatteri:
    global data
    data = json.load(teatteri)

cmd = ["init"]
paivat = {
    "Ma":"1",
    "Ti":"2",
    "Ke":"3",
    "To":"4",
    "Pe":"5",
    "Maanantai":"1",
    "Tiistai":"2",
    "Keskiviikko":"3",
    "Torstai":"4",
    "Perjantai":"5"
}
paivatnum = {
    "1":"Maanantai",
    "2":"Tiistai",
    "3":"Keskiviikko",
    "4":"Torstai",
    "5":"Perjantai"
}
kirjautunut = None
yllapitaja = False

def rewritejson(data):
    jsonfile = open("./teatteri.json", "w")
    jsonfile.write(json.dumps(data, indent=4))
    jsonfile.close()

def suorita(komento, parametri=None):
    if((commands[komento]["admin"] and yllapitaja) or (commands[komento]["admin"]==False)):
        if parametri == None:
            commands[komento]["func"]()
        else:
            commands[komento]["func"](parametri)
    else:
        print("Sinulla ei ole tarvittavia oikeuksia tämän komennon suorittamiseen.")

def apua(entry=None):
    if (entry != None):
        print(entry+" : "+commands[entry]["desc"])
    else:
        for command in commands:
            print(command+" : "+commands[command]["desc"])

def tietoa():
    print("Slikin elokuvateatterissa on neljä salia, joissa on 60-100 paikkaa.")
    print("Aukioloaikamme ovat 10.00-23.00 Ma-Pe.")
    print("Me Slikillä näytämme vain alle kolmen tunnin elokuvia, elokuvat alkavat tasatunnein.")
    print("Teatterin saleissa voit nauttia Slikin mahtavista herkuista ja huikeista elokuvista.")
    print("Toivomme että viihdyt kanssamme!")

def parse_naytos_id(naytos_id):
    return {"sali":naytos_id[0:2],"paiva":paivatnum[str(naytos_id[2])],"aika":naytos_id[3:5],"viikko":naytos_id[5:8]}
    
def luo_naytos():
    sali = input("Valitse sali (A1-2, B1, C1): ")
    paiva = input("Valitse päivä (Ma-Pe): ")
    paiva = paivat[paiva]
    aika = input("Valitse alkamisaika(10, 13, 16 tai 19): ")
    viikko = input("Valitse viikko(1-52): ")
    nimi = input("Elokuvan nimi: ")
    if viikko in data["naytokset"][sali][paiva][aika]:
        muutos = input("Tällä ajankohdalla on jo näytös. Haluatko muuttaa tämän näytöksen(1=tosi/0=epätosi): ")
        if bool(int(muutos)):
            data["naytokset"][sali][paiva][aika][viikko]={"nimi":nimi, "katsojat":[]}
            if nimi in data["elokuvat"]:
                naytos_id = str(sali+paiva+aika+viikko)
                if naytos_id not in data["elokuvat"][nimi]["naytokset"]:
                    data["elokuvat"][nimi]["naytokset"].append(naytos_id)
            rewritejson(data)
            print("Näytös luotu.")
        else:
            print("Näytöksen luominen peruuttu.")
    else:
        data["naytokset"][sali][paiva][aika][viikko]={"nimi":nimi, "katsojat":[]}
        if nimi in data["elokuvat"]:
                naytos_id = str(sali+paiva+aika+viikko)
                if naytos_id not in data["elokuvat"][nimi]["naytokset"]:
                    data["elokuvat"][nimi]["naytokset"].append(naytos_id)
        rewritejson(data)
        print("Näytös luotu.")

def poista_naytos():
    sali = input("Valitse sali (A1-2, B1, C1): ")
    paiva = input("Valitse päivä (Ma-Pe): ")
    paiva = paivat[paiva]
    aika = input("Valitse alkamisaika(10, 13, 16 tai 19): ")
    viikko = input("Valitse viikko(1-52): ")
    try:
        nimi = data["naytokset"][sali][paiva][aika][viikko]["nimi"]
        print(nimi)
        data["naytokset"][sali][paiva][aika].pop(viikko)
        if nimi in data["elokuvat"]:
            naytos_id = str(sali+paiva+aika+viikko)
            if naytos_id in data["elokuvat"][nimi]["naytokset"]:
                data["elokuvat"][nimi]["naytokset"].remove(naytos_id)
        rewritejson(data)
        print("Näytös poistettu.")
    except:
        print("Näytöstä ei voitu poistaa, se ei ole olemassa tai parametrit olivat väärät.")
    
def listaa_naytokset():
    sali = input("Minkä salin näytökset haluat nähdä: ")
    naytokset = data["naytokset"][sali]
    print("Salin",sali,"näytökset:")
    for paiva in naytokset:
        try:
            for naytos in naytokset[paiva]:
                for viikko in naytokset[paiva][naytos]:
                    print("     Viikko",viikko,".",paivatnum[paiva],"klo:",naytos,":",naytokset[paiva][naytos][viikko]["nimi"])
        except:
            continue

def elokuva_naytokset():
    nimi = input("Minkä elokuvan tiedot haluat: ")
    try:
        print(f"{nimi}:\n       näytökset:")
        for naytos in data["elokuvat"][nimi]["naytokset"]:
            tieto = parse_naytos_id(naytos)
            print(f"              Viikko {tieto['viikko']}. {tieto['paiva']} klo. {tieto['aika']}, salissa {tieto['sali']}")
            print(f"                   Näytös id: {naytos}")
    except:
        print("Elokuvaa ei löydetty, se ei ole olemassa tai sillä ei ole näytöksiä.")
            
def salit():
    salit = data["naytokset"]
    print("Salit:")
    for sali in salit:
        print("     ",sali,":\n          koko:",data["naytokset"][sali]["koko"])

def luo_elokuva():
    nimi = input("Elokuvan nimi: ")
    kesto = input("Elokuvan kesto minuutteina: ")
    aikuisille = input("Onko elokuva aikuisille?(1=tosi/0=epätosi): ")
    kuvaus = input("Elokuvan kuvaus: ")
    data["elokuvat"][nimi] = {"kesto":int(kesto),"aikuisille":bool(int(aikuisille)), "kuvaus":kuvaus, "naytokset":[]}
    rewritejson(data)
    print(f"Elokuva '{nimi}' luotu.")
    
def poista_elokuva():
    nimi = input("Elokuvan nimi: ")
    data["elokuvat"].pop(nimi)
    rewritejson(data)
    print(f"Elokuva '{nimi}' poistettu.")

def listaa_elokuvat():
    elokuvat = data["elokuvat"]
    for elokuva in elokuvat:
        print(elokuva, ":\n     elokuvan pituus: ", data["elokuvat"][elokuva]["kesto"], "minuuttia \n     K18: ", data["elokuvat"][elokuva]["aikuisille"],"\n     kuvaus:",data["elokuvat"][elokuva]["kuvaus"],"\n     näytökset:",data["elokuvat"][elokuva]["naytokset"])

def luo_varaus():
    asiakas_id = kirjautunut
    if asiakas_id == data['setup']['admin_log']:
        asiakas_id = input("Syötä asiakastunnus kenelle varaus tehdään: ")
    naytos_id = input("Näytöksen id: ")
    naytos = parse_naytos_id(naytos_id)
    if asiakas_id not in data["naytokset"][naytos["sali"]][paivat[naytos["paiva"]]][naytos["aika"]][naytos["viikko"]]["katsojat"] and len(data["naytokset"][naytos["sali"]][paivat[naytos["paiva"]]][naytos["aika"]][naytos["viikko"]]["katsojat"]) < data["naytokset"][naytos["sali"]]["koko"]:
        data["naytokset"][naytos["sali"]][paivat[naytos["paiva"]]][naytos["aika"]][naytos["viikko"]]["katsojat"].append(asiakas_id)
        rewritejson(data)
        print(f"Näytos {naytos_id}, varattu asiakkaalle {asiakas_id}.")
    else:
        print(f"Varaus näytökseen {naytos_id} on jo olemassa asiakkaalle {asiakas_id} tai sali on täynnä.")

def poista_varaus():
    asiakas_id = kirjautunut
    if asiakas_id == data['setup']['admin_log']:
        asiakas_id = input("Syötä asiakastunnus: ")
    naytos_id = input("Näytöksen id: ")
    naytos = parse_naytos_id(naytos_id)
    if asiakas_id in data["naytokset"][naytos["sali"]][paivat[naytos["paiva"]]][naytos["aika"]][naytos["viikko"]]["katsojat"]:
        data["naytokset"][naytos["sali"]][paivat[naytos["paiva"]]][naytos["aika"]][naytos["viikko"]]["katsojat"].remove(asiakas_id)
        rewritejson(data)
        print(f"Varaus näytökseen {naytos_id} poistettu asiakkaalta {asiakas_id}.")
    else:
        print(f"Asiakkaalla {asiakas_id} ei ole varausta näytökseen {naytos_id}.")

def init():
    global kirjautunut, yllapitaja
    yllapitaja = False
    kirjautunut = None
    while (kirjautunut == data["setup"]["admin_log"] and yllapitaja == False) or kirjautunut == None:
        kirjautunut = input(f"Kirjaudu sisään. Anna käyttäjätunnus(nimi/{data['setup']['admin_log']}): ")
        if kirjautunut == data["setup"]["admin_log"]:
            passcode = input("Anna ylläpidon salasana: ")
            if passcode == data["setup"]["admin_pass"]:
                yllapitaja = True
            else:
                print("Väärä salasana! Kirjaudu uudelleen.")

    print(f"Tervetuloa Slikin elokuvateatteriin {kirjautunut}! Jos tarvitset apua, syötä 'apua' komentoriviin.")

commands = {
    "apua": {
        "func": apua,
        "desc":"Listaa komennot tai kertoo komennon toiminnoista. Kertoo haluamasi komennon toiminnasta, kun syötät komennon nimen 'apua' perään.",
        "admin": False
        },
    "salit": {
        "func": salit,
        "desc":"Kertoo perustietoja elokuvateatterin saleista.",
        "admin": False
        },
    "tietoa": {
        "func": tietoa,
        "desc":"Kertoo elokuvateatterin perustietoja.",
        "admin": False
        },
    "luo_naytos": {
        "func": luo_naytos,
        "desc": "Luo uuden elokuva näytöksen haluamaasi saliin ja aikaan.",
        "admin": True
    },
    "poista_naytos": {
        "func": poista_naytos,
        "desc": "Poistaa näytöksen antamasi id:n mukaisesti.",
        "admin": True
    },
    "listaa_naytokset": {
        "func": listaa_naytokset,
        "desc": "Listaa näytökset valitsemallasi salilla.",
        "admin": False
    },
    "luo_varaus": {
        "func": luo_varaus,
        "desc": "Varaa paikan elokuva näytökseen antamasi näytös id:n mukaisesti asiakkaalle.",
        "admin": False
    },
    "poista_varaus": {
        "func": poista_varaus,
        "desc": "Poistaa varauksen näytöksen ja asiakkaan id:n mukaisesti.",
        "admin": False
    },
    "luo_elokuva": {
        "func": luo_elokuva,
        "desc": "Luo elokuvan antamiesi tietojen mukaisesti elokuva listaan.",
        "admin": True
    },
    "poista_elokuva": {
        "func": poista_elokuva,
        "desc": "Poistaa elokuvan antamiesi tietojen mukaisesti elokuva listasta.",
        "admin": True
    },
    "listaa_elokuvat": {
        "func": listaa_elokuvat,
        "desc": "Listaa kaikki tarjolla olevat elokuvat.",
        "admin": False
    },
    "elokuva_naytokset": {
        "func": elokuva_naytokset,
        "desc": "Listaa elokuvan tarjolla olevat näytökset.",
        "admin": False
    },
    "lopeta": {
        "func": "",
        "desc": "Lopettaa ohjelman, hei hei.",
        "admin": False
    },
    "init": {
        "func": init,
        "desc": "Alustaa ohjelman.",
        "admin": False
    }
    
}

while cmd[0] != "lopeta":
    print()
    #print(time.time())
    #week = datetime.datetime.utcnow().isocalendar()[1]
    #print(week)
    try:
        if len(cmd) > 1:
            suorita(cmd[0],cmd[1])
        else:
            suorita(cmd[0])
    except:
        print("Tuntematon komento.")
    cmd = input("Syötä komento: ").split()

print("Kiitos asioinnista, tervetuloa uudelleen!")