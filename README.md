<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/7e1585a2-3eea-44ec-980c-7e0d3e7a6842" />

# Hollow Line

Hollow Line on komentorivipohjainen selviytymisteemainen tekstiseikkailupeli, joka sijoittuu hylättyyn metrojärjestelmään syvälle maan alle. Pelaaja herää yksin kylmässä ja pimeässä ympäristössä ilman tietoa siitä, miten on päätynyt sinne. Tunnelit ovat täynnä ruostetta, pölyä ja hylättyjä rakenteita, ja jossain käytävien välissä jokin yhä liikkuu.

Peliä pelataan kokonaan tekstikomennoilla. Pelaaja tutkii huoneita, lukee muistiinpanoja, kerää esineitä ja liikkuu metroalueen eri osissa etsiessään ulospääsyä. Pelimaailma on rakenteeltaan kiinteä, mutta reagoi pelaajan tekoihin, ja huolellinen tutkiminen palkitaan.

Metroverkostossa vaeltaa vihamielinen olento nimeltä **Drifter**. Se ei jahtaa pelaajaa suoraan, mutta sen läheisyys kasvattaa uhkaa ja pelkoa ajan myötä. Liiallinen altistuminen johtaa häviöön. Valo ja lämpö voivat torjua Drifterin hetkellisesti, mutta käytettävät välineet ovat rajallisia ja niiden käyttö vaatii harkintaa.

## Pelin tavoitteet

Pelin päätavoitteena on löytää keino paeta metrosta. Tämä voidaan saavuttaa kahdella eri tavalla:
- käyttämällä lämpöön perustuvaa työkalua oikeassa paikassa
- yhdistämällä tietyt esineet ja aktivoimalla vanha konsoli syvemmällä metroalueella

Pelin aikana pelaaja kerää pisteitä tutkimisesta, esineiden löytämisestä ja selviytymisestä. Pisteet eivät vaikuta suoraan lopputulokseen, mutta ne kertovat, kuinka paljon pelimaailmaa tuli nähtyä.

## Ominaisuudet

- Komentorivipohjainen tekstiseikkailu
- Laaja, käsin suunniteltu pelimaailma
- Satunnaisesti liikkuva vihollinen
- Pelko- ja pistemekaniikka
- Useampi mahdollinen loppuratkaisu
- Sisällön ja pelilogiikan erottaminen JSON-rakenteella

## Pelaaminen

Peli käynnistetään Pythonilla komentoriviltä. Pelaaja syöttää yksinkertaisia yhden tai kahden sanan komentoja, kuten:
- mene itä
- ota soihtu
- käytä poltin
- tutki
- katsele


Peli jatkuu, kunnes pelaaja joko pakenee metrosta tai menettää pelin.

## Huomio

Hollow Line on tunnelmallinen ja pelottava peli, jossa uhka rakentuu hitaasti. Mikään ei tapahdu nopeasti, mutta virheet kasaantuvat. Pelaajaa kannustetaan lukemaan ympäristöä tarkasti ja tekemään päätökset harkiten.
