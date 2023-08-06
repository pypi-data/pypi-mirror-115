[<img src="https://img.shields.io/pypi/v/pysalad">](https://pypi.org/project/pysalad/)
<img src="https://img.shields.io/badge/python-3.9-blue">
<img src="https://img.shields.io/badge/license-MIT-green">

# pysalad🥗🐍     

Ein kleines Tool um über die Kommandozeile auf den [HBT](https://www.hbt.de)-Salat zuzugreifen



# How-to

## Install
````bash
pip install pysalad
````

### Salatbuchungen von Heute anzeigen
````bash
pysalad show day
````

### Salatbuchungen von dieser Woche anzeigen
````bash
pysalad show week
````

### Salatbuchungen von diesem Monat anzeigen
````bash
pysalad show month
````

### Eigenen Vertrag in Salat anzeigen
````bash
pysalad show contract
````

### Eigenen Daten anzeigen
````bash
pysalad show employee
````

### Aufträge auf die man buchen kann
````bash
pysalad show orders
````

### Neue Buchung erstellen
````bash
pysalad report <Kommentar> <Dauer> <Auftrag> <Datum>
````

### Benachrichtigungen
````bash
pysalad --nsilence <Minuten zwischen Benachrichtigungen> \
        --nthreshold <Minuten bei fehlender Buchung bis Benachrichtigung angezeigt wird> \
        remind me
````

### Einstellungen speichern
````bash
pysalad --url <URL> config save # URL speichern
pysalad --user <Mitarbeiterkürzel> config save # eigenes Mitarbeiterkürzel speichern
pysalad --password <Passwort> config save # eigenes Passwort speichern
pysalad --order <Text> config save # mein am häufigsten genutzten Unterauftrag speichern
````

Wenn die Einstellungen gespeichert sind, kann man zum Beispiel auf seinen häufigsten Unterauftrag buchen mit:
````bash
pysalad report "verschiedene Dinge" 4.5
````
