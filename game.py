import json
import random

# ------------- DATAN LATAUS -------------

with open("rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

# ------------- GLOBAALI TILA -------------

inventory = []                  # pelaajan kantamat esineet (nimet merkkijonoina)
currentRoom = "entrance_shaft"  # aloitushuoneen tunniste

drifter_room = "rail_pit"       # Drifterin aloitussijainti
flare_active = False
flare_timer = 0

fear = 0                        # 0–10, kun 10 => hermoromahdus
drifter_met_with_flare = False  # vaikuttaa loppukohtaukseen


# ------------- KÄYTTÖOHJE -------------

def instructions():
    print(r"""
 ██░ ██  ▒█████   ██▓     ██▓     ▒█████   █     █░    ██▓     ██▓ ███▄    █ ▓█████ 
▓██░ ██▒▒██▒  ██▒▓██▒    ▓██▒    ▒██▒  ██▒▓█░ █ ░█░   ▓██▒    ▓██▒ ██ ▀█   █ ▓█   ▀ 
▒██▀▀██░▒██░  ██▒▒██░    ▒██░    ▒██░  ██▒▒█░ █ ░█    ▒██░    ▒██▒▓██  ▀█ ██▒▒███   
░▓█ ░██ ▒██   ██░▒██░    ▒██░    ▒██   ██░░█░ █ ░█    ▒██░    ░██░▓██▒  ▐▌██▒▒▓█  ▄ 
░▓█▒░██▓░ ████▓▒░░██████▒░██████▒░ ████▓▒░░░██▒██▓    ░██████▒░██░▒██░   ▓██░░▒████▒
 ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒░▓  ░░ ▒░▓  ░░ ▒░▒░▒░ ░ ▓░▒ ▒     ░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░
 ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░ ▒  ░░ ░ ▒  ░  ░ ▒ ▒░   ▒ ░ ░     ░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░ ░ ░  ░
 ░  ░░ ░░ ░ ░ ▒    ░ ░     ░ ░   ░ ░ ░ ▒    ░   ░       ░ ░    ▒ ░   ░   ░ ░    ░   
 ░  ░  ░    ░ ░      ░  ░    ░  ░    ░ ░      ░           ░  ░ ░           ░    ░  ░
""")
    print("""
Tervetuloa Hollow Lineen.

Olet herännyt hylätyllä metroalueella, kaukana pinnasta. 
Käytävät jatkuvat pimeään ja jokin liikkuu linjoilla hitaasti.

KOMENNOT (kirjoita pienillä kirjaimilla):

    mene pohjoinen / etelä / itä / länsi
    ota <esine>         - poimi esine
    pudota <esine>      - pudota esine lattialle

    katsele             - näytä huoneen kuvaus
    tutki               - etsi piilossa olevia asioita
    lue                 - lue muistiinpanot, jos niitä on

    mukana              - näytä, mitä kannat
    lopeta              - lopeta peli

    käytä soihtu        - käyttää soihtua (jos sinulla on se)

Liiku varoen, kuuntele ääniä ja käytä valoa viisaasti.
""")


# ------------- TILAN NÄYTTÖ -------------

def status():
    huone = rooms[currentRoom]
    print("------------------")
    print(f"Sijainti: {huone['name']}")
    if inventory:
        print("Mukanasi: " + ", ".join(inventory))
    else:
        print("Mukanasi: ei mitään")
    print(f"Pelko: {fear}/10")


def show_room():
    room = rooms[currentRoom]

    print()
    print(room["name"])
    print(room["description"])

    item = room.get("item")
    if item:
        print(f"Lattialla on esine: {item}.")

    exits = ", ".join(room["exits"].keys())
    print(f"Poistumistiet: {exits}")
    print()


# ------------- TUNNELMALINJAT -------------

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


# ------------- SATUNNAISET TAPAHTUMAT -------------

def power_failure():
    global fear
    if random.random() < 0.10:
        print("Pimeys tuntuu tihenevän ympärilläsi. Selkäpiitäsi karmii.")
        fear = min(fear + 1, 10)


def drifter_hint():
    room = rooms[currentRoom]
    exits = room["exits"].values()

    if drifter_room in exits:
        print("Naapuritunnelissa varjot värähtävät. Jokin liikkuu siellä hiljaa.")


# ------------- DRIFTERIN LOGIIKKA -------------

def move_drifter():
    global drifter_room
    exits = list(rooms[drifter_room]["exits"].values())

    if not exits:
        return

    # Kun soihtu palaa, Drifter yrittää välttää pelaajan huonetta
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
    global drifter_met_with_flare
    if currentRoom != drifter_room:
        return False

    print("Edessäsi kohoaa pitkä, vääristyneen näköinen hahmo. Se peittää tunnelin kulun ja seisoo liikkumatta pimeää vasten.")

    if "soihtu" in inventory and flare_active:
        if not drifter_met_with_flare:
            print("Hehkuva soihtu pakottaa hahmon perääntymään. Se taittuu varjoihin ja vetäytyy kauemmas.")
            drifter_met_with_flare = True
            move_drifter()
            return False
        else:
            print("Soihtu leimahtaa jälleen kirkkaana. Tällä kertaa hahmo ei väisty.")
            print("Valo leikkaa sen lävitse, kunnes mitään kiinteää ei enää ole.")
            print("Pöly hiipii ilmaan ja metro vaikenee ympärilläsi.")
            print("Se, mikä vaelsi näillä linjoilla, ei enää palaa.")
            return True
    else:
        print("Yrität tavoittaa turvaa, jota ei ole enää lähettyvillä.")
        print("Jääkylmä läsnäolo sulkeutuu ympärilläsi ja tunneli nielee sinut.")
        print(" SINÄ KUOLIT – PELI PÄÄTTYY")
        return True


# ------------- PELIN PÄÄKOODI -------------

def main():
    global currentRoom, flare_active, flare_timer, fear

    instructions()
    show_room()
    status()

    while True:
        ambient()
        drifter_hint()
        power_failure()

        # Pelko kasvaa, jos Drifter on viereisessä huoneessa eikä soihtua käytetä
        if drifter_room in rooms[currentRoom]["exits"].values() and not flare_active:
            fear = min(fear + 1, 10)

        if flare_active:
            flare_timer -= 1
            if flare_timer <= 0:
                flare_active = False
                print("Soihtu hiipuu ja sammuu. Varjot tihenevät ympärilläsi.")

        if fear >= 10:
            print("Hermosi pettävät. Juokset vailla suuntaa, kunnes käytäväverkosto nielaisee sinut.")
            break

        move = input("> ").strip().lower().split(" ", 1)

        if not move[0]:
            continue

        action = move[0]
        arg = move[1] if len(move) > 1 else None

        room = rooms[currentRoom]

        # --- liikkuminen ---
        if action == "mene":
            if not arg:
                print("Mihin suuntaan haluat mennä?")
            elif arg in room["exits"]:
                if "one_way" in room and arg in room["one_way"]:
                    print("Tähän suuntaan pääsee, mutta samaa reittiä ei voi palata.")
                currentRoom = room["exits"][arg]
                show_room()
                status()
            else:
                print("Siihen suuntaan ei pääse.")

        # --- esineen ottaminen ---
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
                else:
                    print(f"Et näe täällä esinettä nimeltä '{arg}'.")

        # --- esineen pudottaminen ---
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

        # --- esineen käyttäminen ---
        elif action == "käytä":
            if arg == "soihtu":
                if "soihtu" in inventory:
                    flare_active = True
                    flare_timer = 6
                    print("Soihtu leimahtaa rajuun valoon ja kuumuuteen. Varjot vetäytyvät hetkeksi kauemmas.")
                else:
                    print("Sinulla ei ole soihtua.")
            else:
                print("Mitä haluat käyttää?")

        # --- tutkiminen (piilojutut) ---
        elif action == "tutki":
            if "secret" in room:
                print("Tutkit ympäristöä tarkemmin.")
                print(room["secret"])
                hidden = room.get("hidden_item")
                if hidden:
                    print(f"Löydät esineen: {hidden}.")
                    inventory.append(hidden)
                    room["hidden_item"] = None
            else:
                print("Tutkit aluetta, mutta et löydä mitään uutta.")

        # --- muistiinpanot / tekstit ---
        elif action == "lue":
            if "notes" in room:
                print(room["notes"])
            else:
                print("Täällä ei ole mitään luettavaa.")

        # --- huoneen kuvaus ---
        elif action in ("katsele", "katso"):
            show_room()
            status()

        # --- inventaario ---
        elif action in ("mukana", "inv", "i", "inventaario"):
            if inventory:
                print("Mukanasi on: " + ", ".join(inventory))
            else:
                print("Et kanna mitään mukanasi.")

        # --- pelin lopetus ---
        elif action in ("lopeta", "poistu", "quit", "exit"):
            print("Istahdat pölyn ja hiljaisuuden keskelle ja annat tunneleiden pitää tarinasi.")
            break

        else:
            print("Tunneli ei tunnu ymmärtävän sitä, mitä yrität sanoa.")

        # --- Drifter liikkuu vuoron lopuksi ---
        move_drifter()
        if drifter_encounter():
            break

        # --- mahdolliset loppuratkaisut ---

        # Ruosteportin pako polttimen kanssa
        if currentRoom == "rust_gate" and "poltin" in inventory:
            print("Käytät poltinta ja leikkaat puhki Ruosteportin paksun metallin.")
            print("Portaikko nousee ylös purevaan kylmään ilmaan.")
            print("Astut vanhojen linjojen yläpuolelle kalpean taivaan alle.")
            print("Olet löytänyt tien ulos.")
            print(" SINÄ VOITIT")
            break

        # Signaaliarkiston loppu sirun ja vanhan kortin kanssa
        if currentRoom == "signal_archive" and "vanha_kortti" in inventory and "siru" in inventory:
            print("Asetat sirun haljenneeseen konsoliin ja pyyhkäiset vanhan kortin lukijan ohi.")
            print("Syvällä allasi lukot vapautuvat raskaalla, matalalla äänellä.")
            print("Piilossa ollut huoltoputki avautuu ja lähtee nousemaan ylemmäs.")
            print("Pitkän nousun jälkeen saavut tyhjälle valvomolle, joka katsoo yhä kaupungin ylle.")
            print("Jätät metron taaksesi.")
            print(" SINÄ VOITIT")
            break


if __name__ == "__main__":
    main()
