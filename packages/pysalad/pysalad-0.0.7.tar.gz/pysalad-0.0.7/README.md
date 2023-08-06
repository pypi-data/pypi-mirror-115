# pysalad

Ein kleines Tool um über die Kommandozeile auf Salat zuzugreifen

# How-to
### Salatbuchungen von Heute anzeigen
````bash
pysalad --url <URL> --user <Mitarbeiterkürzel> show day
````

### Salatbuchungen von dieser Woche anzeigen
````bash
pysalad --url <URL> --user <Mitarbeiterkürzel> show week
````

### Salatbuchungen von diesem Monat anzeigen
````bash
pysalad --url <URL> --user <Mitarbeiterkürzel> show month
````

### Eigenen Vertrag in Salat anzeigen
````bash
pysalad --url <URL> --user <Mitarbeiterkürzel> show contract
````

### Eigenen Daten anzeigen
````bash
pysalad --url <URL> --user <Mitarbeiterkürzel> show employee
````

### Aufträge auf die man buchen kann
````bash
pysalad --url <URL> --user <Mitarbeiterkürzel> show orders
````

### Neue Buchung erstellen
````bash
pysalad --url <URL> --user <Mitarbeiterkürzel> report <Kommentar> <Dauer> <Auftrag> <Datum>
````

### Einstellungen speichern
````bash
pysalad --url <URL> config save # URL speichern
pysalad --user <Mitarbeiterkürzel> config save # eigenes Mitarbeiterkürzel speichern
pysalad --password <Passwort> config save # eigenes Passwort speichern
pysalad --defaultorder <Text> config save # mein am häufigsten genutzten Unterauftrag speichern
````

Wenn die Einstellungen gespeichert sind, kann man zum Beispiel auf seinen häufigsten Unterauftrag buchen mit:
````bash
pysalad report "verschiedene Dinge" 4.5
````