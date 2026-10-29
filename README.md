# Olympia-Fallstudie: Judo, Boxen und Nationen 1960 bis 2016

Fallstudie aus meiner Data-Analyst-Weiterbildung am Data Science Institute (06/2026),
als Einzelarbeit umgesetzt. Auftraggeber im Szenario ist die fiktive Firma SportsStats.
Ziel war es, aus Olympia-Daten Erkenntnisse für zwei Zielgruppen abzuleiten:
Elite-Personal-Trainer und lokale Nachrichtenredaktionen.

## Fragestellungen
1. In welchem Alter erreichen Boxer und Judokas ihren Medaillen-Höhepunkt?
2. Welche Nationen haben sich zwischen 1960 bis 1980 und 1996 bis 2016 am stärksten verbessert?
3. Unterscheiden sich Medaillengewinner im Körperbau von Athleten ohne Medaille?

## Daten
Grundlage ist eine CSV-Datei mit 216.784 Teilnahmen an Olympischen Spielen von
1904 bis 2016, die das Data Science Institute für die Fallstudie bereitgestellt hat.
Ich habe sie auf die Spiele ab 1960 gefiltert (165.978 Teilnahmen) und in fünf
Tabellen normalisiert. Die Daten selbst liegen nicht im Repository.

| Tabelle | Inhalt | Datensätze |
|---|---|---|
| athletes | Stammdaten der Athleten | 87.734 |
| countries | Nationale Olympische Komitees | 222 |
| sports | Sportarten ab 1960 | 36 |
| events | Wettkampfdisziplinen | 375 |
| participations | Faktentabelle, eine Zeile pro Teilnahme | 165.978 |

![ERD](images/ERD_Diagramm.png)

Hinweis zum Modell: `participations` enthält zusätzlich `sport_id`, obwohl die
Sportart über `events` schon eindeutig feststeht. Das spart bei Auswertungen nach
Sportart einen JOIN, ist aber eine Redundanz.

## Vorgehen
- **Datenmodell:** ERD entworfen, Tabellen in PostgreSQL 17 mit Primär- und
  Fremdschlüsseln angelegt. Für Medaillen habe ich einen ENUM-Typ verwendet, damit
  ungültige Werte schon in der Datenbank abgewiesen werden.
- **Import und Validierung:** Import in fester Reihenfolge wegen der Fremdschlüssel,
  danach Prüfung der Zeilenzahlen und der Beziehungen über JOIN-Abfragen.
- **Auswertung:** Kennzahlen per SQL (`sql/04_analyse.sql`), Ergebnisse als CSV in
  `ergebnisse/`, Dashboard mit Python (pandas, NumPy, Matplotlib).

## Ergebnisse
- Boxer gewinnen ihre Medaillen im Schnitt mit 23,4 Jahren, Judokas mit 25,2 Jahren.
- Zwischen Athleten mit und ohne Medaille gibt es beim Alter kaum Unterschiede
  (Boxen 23,4 zu 23,3 Jahre, Judo 25,2 zu 25,4 Jahre).
- Boxer mit Medaille sind im Schnitt 2,0 cm größer und 2,6 kg schwerer als Boxer ohne
  Medaille. Im Judo sind Medaillengewinner 0,5 cm kleiner, aber 1,7 kg schwerer.
  Die Unterschiede sind klein, Gewichtsklassen sind dabei nicht berücksichtigt.
- Die USA steigern sich von 795 auf 1.593 Medaillen, Australien von 197 auf 817.

![Dashboard](images/Olympics_Dashboard.png)

## Grenzen der Analyse
- China (0 auf 705 Medaillen) und die Ukraine (0 auf 188) erscheinen als große
  Aufsteiger. Beide nahmen im frühen Zeitraum aber gar nicht als eigenes Team an
  Sommerspielen teil. Der Vergleich misst bei ihnen also vor allem die Teilnahme.
- Länder sind nach Namen gruppiert. Die Sowjetunion zählt dadurch zu Russland,
  BRD und DDR zu Deutschland.
- Medaillen sind pro Athlet gezählt. Mannschaftssportarten treiben die Zahlen
  dadurch nach oben.
- Größe und Gewicht fehlen in den frühen Jahrzehnten oft. Gewichtsklassen habe ich
  nicht getrennt ausgewertet.

## Herausforderungen
Beim Import blieben die Tabellen zunächst leer, weil die CSV-Dateien mit Semikolon
statt Komma getrennt waren. Die Original-ID konnte nicht Primärschlüssel werden, da
ein Athlet mehrere Wettkämpfe bestreitet. Leere Medaillenfelder passten nicht zum
ENUM-Typ, ich habe sie beim Normalisieren mit `None` gefüllt.

## Überarbeitung (10/2026)
Beim erneuten Prüfen ist mir aufgefallen, dass in den Rohdaten ein fehlendes Alter
als 0 eingetragen ist (1.040 Teilnahmen ab 1960). In der Abgabe sind diese Nullen in
die Durchschnitte eingeflossen. Ich habe alle Auswertungen mit `age > 0` neu
berechnet, die Abfragen in `sql/04_analyse.sql` festgehalten und das Dashboard direkt
aus den Ergebnis-CSVs erzeugt. Dadurch haben sich Alterswerte um 0,1 bis 0,5 Jahre
verschoben, und der vorher gezeigte Altersvorsprung der Medaillengewinner ist
weggefallen. Die Körpermaße weichen durch einheitliches Runden um höchstens 0,1 ab. Die Excel-Zwischenstände aus der Abgabe sind nicht mehr im Repository.

Schlussfolgerungen und Empfehlungen für beide Zielgruppen:
[docs/Schlussfolgerungen_Empfehlungen.pdf](docs/Schlussfolgerungen_Empfehlungen.pdf)

## Selbst ausführen
Das Dashboard lässt sich ohne Datenbank aus den CSVs neu erzeugen:
```
pip install -r requirements.txt
python analyse/olympics_analyse.py
```
Für die SQL-Skripte wird PostgreSQL mit den normalisierten Tabellen gebraucht,
Reihenfolge: `01_create_tables.sql`, `02_import_data.sql`, `03_validierung.sql`,
`04_analyse.sql`.

## Projektstruktur
```
sql/          Tabellen anlegen, Import, Validierung, Auswertungen
analyse/      Python-Skript für Kennzahlen und Dashboard
ergebnisse/   Ergebnisse der SQL-Auswertungen als CSV
images/       ERD und Dashboard
docs/         Schlussfolgerungen und Empfehlungen
```

## Werkzeuge
PostgreSQL 17, pgAdmin, SQL, Python (pandas, NumPy, Matplotlib), Excel in der ersten Auswertung
