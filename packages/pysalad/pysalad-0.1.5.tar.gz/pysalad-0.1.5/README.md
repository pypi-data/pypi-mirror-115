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

### Salatbuchungen eines Tages anzeigen
````bash
pysalad show day # alle Buchungen von Heute zeigen
pysalad show yesterday # alle Buchungen von Gestern zeigen
pysalad show tomorrow # alle Buchungen von Morgen zeigen
pysalad show day 2021-01-01 # alle Buchungen vom ersten Januar zeigen
````

### Salatbuchungen einer Woche anzeigen
````bash
pysalad show week # alle Buchungen der aktuellen Woche zeigen
pysalad show week 2021-01-01 # alle Buchungen der ersten Januar Woche zeigen
````

### Salatbuchungen eines Monats anzeigen
````bash
pysalad show month # alle Buchungen des aktuellen Monats zeigen
pysalad show month 2021-01-01 # alle Buchungen für Januar 2021 zeigen
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
pysalad report <Kommentar> <Dauer> <Auftrag> # Arbeitszeit für Heute buchen
pysalad report <Kommentar> <Dauer> <Auftrag> <Datum> # Arbeitszeit an einem bestimmten Tag buchen
````

### Einstellungen speichern
````bash
pysalad --url <URL> config save # URL speichern
pysalad --user <Mitarbeiterkürzel> config save # eigenes Mitarbeiterkürzel speichern
pysalad --password <Passwort> config save # eigenes Passwort speichern
pysalad --order <Text> config save # mein am häufigsten genutzten Unterauftrag speichern
````

### Einstellungen anzeigen
````bash
pysalad config show
````

Wenn die Einstellungen gespeichert sind, kann man zum Beispiel auf seinen häufigsten Unterauftrag buchen mit:
````bash
pysalad report <Kommentar> <Dauer>
````
