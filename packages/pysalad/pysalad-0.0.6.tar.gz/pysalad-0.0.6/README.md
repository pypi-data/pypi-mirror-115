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

### Misc
Um weniger tippen zu müssen Funktion in `.bashrc`, `.zshrc` o.ä. hinzufügen (funktioniert nur in Verbindung mit obrigem symlink):
```bash
function salat() {
  url="URL" # Salat URL hier einsetzen
  abbrev="abc" # mein Kuerzel hier einsetzen
  order=${3:-blabla} # mein haeufigsten Unterauftrag hier einsetzen
  echo "$(pysalad --url ${url}--user ${abbrev} report $1 $2 ${order})"
}

# Usage:
# ohne Angabe eines Unterauftrags wird auf den im Skript eingetragenen gebucht
salat ticket123 3.0
# oder mit Anfabe eines Unterauftrags (gestalten):
salat HBT-Tag 2.0 gestalten
```
