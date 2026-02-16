<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/7e1585a2-3eea-44ec-980c-7e0d3e7a6842" />

# Hollow Line

Hollow Line on komentorivipohjainen selviytymisteemainen tekstiseikkailupeli, joka sijoittuu hylättyyn metrojärjestelmään syvälle maan alle. Pelaaja herää kylmässä ja pimeässä ympäristössä ilman tietoa siitä, miten on päätynyt sinne. Tunnelit ovat täynnä ruostetta, pölyä ja hylättyjä rakenteita. Metroverkostossa liikkuu olento nimeltä **Drifter**, joka lisää jatkuvaa uhkaa.

Peli toteutetaan Pythonilla ja sitä pelataan kokonaan tekstikomennoilla.

## Pelin tavoite

Pelaajan tavoitteena on paeta metrojärjestelmästä. Tämä voidaan saavuttaa kahdella eri tavalla:

1.  **Käyttämällä lämpöön perustuvaa työkalua** oikeassa paikassa.
2.  **Keräämällä tietyt esineet** ja aktivoimalla vanha järjestelmä syvemmällä metroalueella.

Pelaaja kerää pisteitä tutkimisesta, esineiden löytämisestä ja selviytymisestä. Pisteet mittaavat etenemistä, mutta eivät estä pelin läpäisyä.

## Ominaisuudet

* Komentorivipohjainen tekstiseikkailu
* Yli 20 käsin suunniteltua sijaintia
* Useita kerättäviä esineitä
* Satunnaisesti liikkuva vihollinen
* Pelko- ja pistemekaniikka
* Useampi mahdollinen loppuratkaisu
* Pelimaailma tallennettu JSON-rakenteeseen

## Vaatimukset

* Python 3.x

Tarkista Python-versio:

    python --version

## Tiedostot

Projektikansiossa tulee olla seuraavat tiedostot:

* `game.py`: Sisältää pelilogiikan.
* `Rooms.json`: Sisältää pelimaailman rakenteen, huoneet ja esineet.

## Pelin käynnistäminen

Siirry komentorivillä projektikansioon ja suorita:

**Windows:**

    py game.py

**macOS / Linux:**

    python3 game.py

Jos käynnistys onnistuu, peli näyttää ohjeet ja aloitushuoneen kuvauksen.

## Komennot

Peli hyväksyy yhden tai kahden sanan komentoja.

Esimerkkejä:

    mene itä
    mene pohjoinen
    ota soihtu
    pudota köysi
    käytä soihtu
    tutki
    katsele
    lue
    mukana
    lopeta

Jos komento ei ole tunnistettu, peli ilmoittaa siitä.

## Pelimekaniikka

* **Drifter** liikkuu jokaisen vuoron jälkeen.
* Jos se on viereisessä huoneessa, **pelko** kasvaa.
* Jos se on samassa huoneessa ilman aktiivista lämpölähdettä, pelaajalla on yksi vuoro aikaa paeta tai käyttää soihtua.
* Pelko kasvaa liiallisesta altistumisesta ja peli päättyy, jos mittari täyttyy.
* Soihtu antaa väliaikaista suojaa.
* Tietyt esineet mahdollistavat pelin lopullisen ratkaisemisen.

## Walkthrough (lyhyt ratkaisuohje)

**Yksi mahdollinen ratkaisutapa:**

1.  Tutki metroverkostoa järjestelmällisesti.
2.  Hanki soihtu **Syvä rata** -alueelta.
3.  Hanki poltin **Huoltohallista** tutkimalla piilotettu alue.
4.  Saavuta ruosteinen portti.
5.  Käytä poltinta avataksesi reitin ulos.

**Vaihtoehtoinen ratkaisu:**

1.  Kerää siru ja vanha kortti.
2.  Saavuta **Signaaliarkisto**.
3.  Aktivoi järjestelmä yhdistämällä esineet.

## Tekniset tiedot

* Pelimaailma tallennetaan sanakirja- ja listarakenteisiin.
* Huoneet, esineet ja poistumistiet määritellään JSON-tiedostossa.
* Komentotulkki käsittelee yhden tai kahden sanan syötteitä.
* Pistemäärä ja pelkomittari tallennetaan globaaliin pelitilaan.
* Vihollisen liike perustuu satunnaisuuteen.

## Huomio

Hollow Line on tunnelmallinen ja pelottava peli, jossa uhka rakentuu hitaasti. Mikään ei tapahdu nopeasti, mutta virheet kasaantuvat. Pelaajaa kannustetaan lukemaan ympäristöä tarkasti ja tekemään päätökset harkiten.
