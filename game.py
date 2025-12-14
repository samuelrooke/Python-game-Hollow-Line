import json
import random
import textwrap
DANGER = "\033[91m"   
WARNING = "\033[93m"  
GREEN = "\033[92m"
RESET = "\033[0m"

with open("rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)
    items = rooms.get("items", {})


# globaali 

inventory = []
currentRoom = "sisaantulokaytava"
drifter_room = "kiskokuoppa"

flare_active = False
flare_timer = 0
ending = None

fear = 0                          # 0-10, kun 10 => hermoromahdus
drifter_met_with_flare = False

score = 0
max_score = 366
visited_rooms = set()

danger_distance = 0
fear_tick = 0

def wrap(text):
    if not text:
        return ""
    return "\n".join(textwrap.wrap(text, width=80))


# ohje

def instructions():
    print("""
          
M""MMMMM""MM          dP dP                        M""MMMMMMMM oo                   
M  MMMMM  MM          88 88                        M  MMMMMMMM                      
M         `M .d8888b. 88 88 .d8888b. dP  dP  dP    M  MMMMMMMM dP 88d888b. .d8888b. 
M  MMMMM  MM 88'  `88 88 88 88'  `88 88  88  88    M  MMMMMMMM 88 88'  `88 88ooood8 
M  MMMMM  MM 88.  .88 88 88 88.  .88 88.88b.88'    M  MMMMMMMM 88 88    88 88.  ... 
M  MMMMM  MM `88888P' dP dP `88888P' 8888P Y8P     M         M dP dP    dP `88888P' 
MMMMMMMMMMMM                                       MMMMMMMMMMM                      
                                                                                    
""")
    print("""
Tervetuloa Hollow Lineen.

Olet herännyt hylätyllä metroalueella, kaukana pinnasta.
Käytävät jatkuvat pimeään ja jokin liikkuu linjoilla hitaasti.

Lue huolellisesti kaikki teksti, saatat muuten missata jotain! 

KOMENNOT (kirjoita pienillä kirjaimilla):

    mene pohjoinen / etelä / itä / länsi
    ota <esine>         - poimi esine
    pudota <esine>      - pudota esine lattialle

    katsele             - näytä huoneen kuvaus
    tutki               - etsi piilossa olevia asioita
    lue                 - lue muistiinpanot, jos niitä on

    mukana              - näytä, mitä kannat
    lopeta              - lopeta peli
    help                - tulosta ohjesivu ja vinkit
          
    käytä <esine>       - Pelissä on esineitä jonka käyttö on selviytymisen kannalta tärkeitä. esim. Soihtu. 
""")


# tila

def status():
    huone = rooms[currentRoom]
    print("------------------")
    print(f"Sijainti: {huone['name']}")
    if inventory:
        print("Mukanasi: " + ", ".join(inventory))
    else:
        print("Mukanasi: ei mitään")
    print(f"Pelko: {fear}/10")
    print("-------------------")
    print(f"Pisteet: {score}")


def show_room():
    room = rooms[currentRoom]

    print()
    print(room["name"])
    print(wrap(room["description"]))

    item = room.get("item")
    if item:
        print("----------------")
        print(f"Lattialla on esine: {item}.")

    exits = ", ".join(room["exits"].keys())
    print("----------------")
    print(f"Poistumistiet: {exits}")

# kontekstuaalinen vihje

    if currentRoom == "ruosteinen_portti" and "poltin" in inventory:
        print()
        print("Ruosteinen portti näyttää haurastuneelta.")
        print("Kannat mukanasi työkalua, jonka kuumuus voisi tehdä tähän aukon.")
    
    if currentRoom == "signaaliarkisto" and "siru" in inventory and "vanha_kortti" in inventory:
        print()
        print("Huoneen reunassa huomaat lattialla raitoja,")
        print("kuin jokin raskas olisi liikkunut saranoilla.")
        print("Lähempänä paljastuu konsoli, jossa vilkkuu punainen valo.")
        print("Kädessäsi oleva vanha kortti ja siru tuntuu loksahtavan yhteen ja haluat kokeille käyttää konsolia.")




# tunnelmalinjat

ambient_lines = [
    "Kaukaa tunnelista kuuluu metallin hidas raapaisu.",
    "Kylmä veto kulkee ohitsesi, kuin linjalla olisi yhä elämää.",
    "Vesipisara tipahtaa pimeyteen ja ääni kantaa pitkälle.",
    "Vanha putki värähtää, kuin jokin nojaisi siihen toiselta puolelta.",
    "Valosi välähtää oudosti ja palautuu takaisin.",
    "Jokin kolisee etäämmällä… sitten hiljenee kuin se olisi pysähtynyt kuuntelemaan."
]

def ambient():
    if random.random() < 0.25:
        print(random.choice(ambient_lines))


# satunnaiset tapahtumat

def power_failure():
    global fear
    if random.random() < 0.05:
        print("Taskulamppusi lakkaa toimimasta, sinua pelottaa.")
        fear = min(fear + 1, 10)


def drifter_hint():
    room = rooms[currentRoom]
    exits = room["exits"].values()

    if drifter_room in exits:
        print("Naapuritunnelissa varjot värähtävät. Jokin liikkuu siellä hiljaa.")


# vihollisen (drifterin) logiikka

def move_drifter():
    global drifter_room
    exits = list(rooms[drifter_room]["exits"].values())

    if not exits:
        return

    if flare_active:
        filtered = [r for r in exits if r != currentRoom]
        if filtered:
            exits = filtered

    drifter_room = random.choice(exits)


def drifter_encounter():
    """
    Palauttaa True jos peli päättyy kohtaamiseen (kuolema tai vapautus),
    muuten False.
    """
    global drifter_met_with_flare, score

    if currentRoom != drifter_room:
        return False

    print("Edessäsi kohoaa pitkä, vääristyneen näköinen hahmo. Se peittää tunnelin kulun ja seisoo liikkumatta pimeää vasten.")

    if "soihtu" in inventory and flare_active:
        if not drifter_met_with_flare:
            print("Hehkuva soihtu pakottaa hahmon perääntymään. Se taittuu varjoihin ja vetäytyy kauemmas.")
            drifter_met_with_flare = True
            score += 15
            move_drifter()
            return False
        else:
            print("Soihtu leimahtaa jälleen kirkkaana. Tällä kertaa hahmo ei väisty.")
            print("Valo leikkaa sen lävitse, kunnes mitään kiinteää ei enää ole.")
            print("Pöly hiipii ilmaan ja metro vaikenee ympärilläsi.")
            print("Se, mikä vaelsi näillä linjoilla, ei enää palaa.")
            score += 30
            print(f"Pisteet: {score}")
            return True
    else:
        print("Yrität tavoittaa turvaa, jota ei ole enää lähettyvillä.")
        print("Jääkylmä läsnäolo sulkeutuu ympärilläsi ja tunneli nielee sinut.")
        print(" SINÄ KUOLIT - PELI PÄÄTTYY")
        print(f"Pisteet: {score}")
        return True




# pelin päälooppi

def main():
    global currentRoom, flare_active, flare_timer, fear, score, visited_rooms
    global danger_distance, fear_tick, ending


    # merkitään aloitushuone käydyksi
    visited_rooms.add(currentRoom)

    instructions()
    show_room()
    status()






    while True:

        # drifterin etäisyys tarkistus

        drifter_exits = rooms[drifter_room]["exits"].values()

        if drifter_room == currentRoom:
            danger_distance = 2
        elif currentRoom in drifter_exits:
            danger_distance = 1
        else:
            danger_distance = 0


        # viereinen huone -> varoitus + pelko
        if danger_distance == 1:
            print(WARNING + "Kylmä väre käy pitkin selkääsi – jokin on aivan seinän takana..." + RESET)
            if not flare_active:
                fear_tick += 1
                if fear_tick >= 3:
                    fear = min(fear + 1, 10)
                    fear_tick = 0

        # sama huone -> yksi vuoro aikaa
        if danger_distance == 2 and not flare_active:
            print(DANGER + "Pimeys paksuuntuu ympärilläsi. Drifter on HUONEESSA!" + RESET)
            print(WARNING + "Sinulla on YKSI vuoro aikaa karata tai käyttää soihtua!" + RESET)

            user = input("> ").strip().lower()

            if user == "käytä soihtu" and "soihtu" in inventory:
                flare_active = True
                flare_timer = 4
                print("Soihtu välähtää kirkkaasti.")
                print("Hahmo reagoi välittömästi lämpöön ja vetäytyy pimeyteen.")
                print("Saat hetkeksi tilaa hengittää.")

                move_drifter()
                continue  # siirry seuraavaan vuoroon

            else:
                # jos yrität liikkua -> jos huoneessa on poistumistie, annetaan pelaajan paeta
                parts = user.split(" ", 1)

                if parts[0] == "mene" and len(parts) > 1:
                    direction = parts[1]
                    if direction in rooms[currentRoom]["exits"]:
                        # pako onnistuu
                        currentRoom = rooms[currentRoom]["exits"][direction]
                        print("Juokset paniikissa pois huoneesta!")
                        show_room()
                        status()
                        continue

                # jos ei paennut -> kuolee
                if drifter_encounter():
                    break

        ambient()
        drifter_hint()
        power_failure()




        if flare_active:
            flare_timer -= 1
            if flare_timer <= 0:
                flare_active = False
                print("Soihtu hiipuu ja sammuu.")
                print("Lämpö katoaa ja varjot palaavat lähemmäs.")

# pelko saavuttaa maksimin ja peli loppuu
        if fear >= 10:
            print("Hermosi pettävät. Juokset vailla suuntaa, kunnes käytäväverkosto nielaisee sinut.")
            print(f"HÄVISIT - Pisteet: {score}")
            break

        move = input("> ").strip().lower().split(" ", 1)

        if not move[0]:
            continue

        action = move[0]
        arg = move[1] if len(move) > 1 else None

        room = rooms[currentRoom]

        # liikkuminen
        if action == "mene":
            if not arg:
                # näytä selkeästi mihin suuntiin voi mennä
                print("Voit mennä suuntiin: " + ", ".join(room["exits"].keys()))
            elif arg in room["exits"]:
                if "one_way" in room and arg in room["one_way"]:
                    print("Tähän suuntaan pääsee, mutta samaa reittiä ei voi palata.")
                currentRoom = room["exits"][arg]

                # pisteitä uudesta huoneesta
                if currentRoom not in visited_rooms:
                    visited_rooms.add(currentRoom)
                    score += 10

                show_room()
                status()
            else:
                print("Siihen suuntaan ei pääse.")

        # esineen ottaminen
        elif action == "ota":
            if not arg:
                print("Mitä haluat ottaa?")
            else:
                room_item = room.get("item")
                if room_item is None:
                    print("Täällä ei ole mitään otettavaa.")
                elif arg == room_item:
                    print(f"Nostat esineen '{arg}' mukaasi.")
                    inventory.append(arg)
                    room["item"] = None
                    score += 5  # esineen löytämisestä pisteitä
                else:
                    print(f"Et näe täällä esinettä nimeltä '{arg}'.")

        # esineen pudottaminen
        elif action == "pudota":
            if not arg:
                print("Mitä haluat pudottaa?")
            elif arg not in inventory:
                print(f"Sinulla ei ole esinettä nimeltä '{arg}'.")
            else:
                room_item = room.get("item")
                if room_item is not None:
                    print("Lattialla on jo yksi esine. Et halua sotkea enempää.")
                else:
                    inventory.remove(arg)
                    room["item"] = arg
                    print(f"Pudotat esineen '{arg}' lattialle.")

        # esineen käyttäminen
        elif action == "käytä":

            if arg == "soihtu":
                if "soihtu" in inventory:
                    flare_active = True
                    flare_timer = 4
                    inventory.remove("soihtu")

                    print("Soihtu leimahtaa rajuun valoon ja kuumuuteen.")
                    print("Lämpö ja valo pakottavat pimeyden loitolle.")
                    print("Hetken kuluttua soihtu palaa loppuun eikä siitä ole enää apua.")
                else:
                    print("Sinulla ei ole soihtua.")

            elif arg == "poltin":
                if "poltin" not in inventory:
                    print("Sinulla ei ole poltinta.")
                elif currentRoom != "ruosteinen_portti":
                    print("Tätä ei voi käyttää täällä.")
                else:
                    print("Sytytät polttimen. Metalli alkaa hehkua ja antaa periksi.")
                    ending = "ruosteportti"


            elif arg == "konsoli":
                if "vanha_kortti" not in inventory or "siru" not in inventory:
                    print("Sinulta puuttuu jotain, jotta konsoli toimisi.")
                elif currentRoom != "signaaliarkisto":
                    print("Täällä ei ole mitään konsolia.")
                else:
                    print("Konsoli herää henkiin. Syvällä rakenteissa lukot vapautuvat.")
                    ending = "arkisto"


            else:
                print("Et voi käyttää sitä.")


        elif action in ("help", "ohje", "apu"):
            print("""
            KOMENNOT:
            mene <suunta>        liiku huoneesta toiseen
            ota <esine>         poimi esine mukaasi
            pudota <esine>      jätä esine huoneeseen
            käytä <esine>       käytä esinettä tilanteen mukaan
            tutki               etsi piilossa olevia asioita
            lue                 lue huoneen muistiinpanot tai esineitä
            katsele             näytä huoneen kuvaus uudelleen
            mukana              näytä inventaario
            lopeta              lopeta peli

            VINKKEJÄ:
            - Kaikilla esineillä ei ole käyttöä heti
            - Ympäristö antaa vihjeitä esineiden käytöstä
            - Valo ja lämpö vaikuttavat Drifteriin
            - Jos jokin tuntuu reagoivan esineeseen, kokeile käyttää sitä
            """)

        # tutkiminen
        elif action == "tutki":
            if "secret" in room:
                print("Tutkit ympäristöä tarkemmin.")
                print(wrap(room["secret"]))
                hidden = room.get("hidden_item")
                if hidden:
                    print(f"Löydät esineen: {hidden}.")
                    inventory.append(hidden)
                    room["hidden_item"] = None
                    score += 8  # salaisen esineen löytämisestä enemmän pisteitä
            else:
                print("Tutkit aluetta, mutta et löydä mitään uutta.")

        elif action == "lue":
            if arg:
                if arg in inventory and arg in items:
                    print(wrap(items[arg]["text"]))
                else:
                    print("Et voi lukea sitä.")
            elif "notes" in room:
                print(wrap(room["notes"]))
            else:
                print("Täällä ei ole mitään luettavaa.")



        # huoneen kuvaus
        elif action in ("katsele", "katso"):
            show_room()
            status()

        # inventaario
        elif action in ("mukana", "inv", "i", "inventaario"):
            if inventory:
                print("Mukanasi on: " + ", ".join(inventory))
            else:
                print("Et kanna mitään mukanasi.")

        # pelin lopetus
        elif action in ("lopeta", "poistu", "quit", "exit"):
            print("Istahdat pölyn ja hiljaisuuden keskelle ja annat tunneleiden pitää tarinasi.")
            print(f"Pisteet: {score}")
            break

        else:
            print("Tunneli ei tunnu ymmärtävän sitä, mitä yrität sanoa.")

        # drifter liikkuu vuoron lopuksi
        move_drifter()


        # loppuratkaisun tarkistus
        if ending == "ruosteportti":
            score += 50

            print("\n------------------------------")
            print("Loppu: Pako ruosteportin kautta")
            print("------------------------------\n")

            print("Metalli antaa lopulta periksi.")
            print("Portaikko johtaa ylös, pois hylätyiltä linjoilta.")
            print("Metro jää taaksesi.")

            print(GREEN + "\nSINÄ VOITIT" + RESET)
            print(f"Pisteet: {score} / {max_score}")
            print("------------------------------\n")
            break

        elif ending == "arkisto":
            score += 50

            print("\n------------------------------")
            print("Loppu: Salainen ovi Arkistossa")
            print("------------------------------\n")

            print("Huoltotie vie sinut pois metron syvyyksistä.")
            print("Drifter ei enää seuraa.")

            print(GREEN + "\nSINÄ VOITIT" + RESET)
            print(f"Pisteet: {score} / {max_score}")
            print("------------------------------\n")
            break



if __name__ == "__main__":
    main()
