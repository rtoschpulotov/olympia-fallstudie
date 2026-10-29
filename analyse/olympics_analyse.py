"""
Olympics Fallstudie - Auswertung und Dashboard
Autor: Rustam T. (Einzelarbeit, DSI-Weiterbildung)

Liest die Ergebnisse meiner SQL-Abfragen (sql/04_analyse.sql) aus dem Ordner
ergebnisse/ und baut daraus das Dashboard.
Starten aus dem Hauptordner:  python analyse/olympics_analyse.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # kein Fenster, nur als Bild speichern
import matplotlib.pyplot as plt

# Pfade relativ zu diesem Skript, dann ist egal von wo ich es starte
ORDNER = Path(__file__).resolve().parent.parent
ERGEBNISSE = ORDNER / "ergebnisse"
BILD = ORDNER / "images" / "Olympics_Dashboard.png"

df_alter = pd.read_csv(ERGEBNISSE / "alter_analyse.csv")
df_mit_ohne = pd.read_csv(ERGEBNISSE / "alter_mit_ohne_medaille.csv")
df_koerper = pd.read_csv(ERGEBNISSE / "koerperbau_analyse.csv")
df_nationen = pd.read_csv(ERGEBNISSE / "nationen_aufstieg.csv")


# --- Frage 1: Peak-Alter ---
print("Peak-Alter (gewichtet nach Anzahl Medaillengewinner):")
for sport in ["Boxing", "Judo"]:
    teil = df_alter[df_alter["sport_name"] == sport]
    # gewichtet, weil es bei Bronze doppelt so viele Medaillen gibt wie bei Gold
    schnitt = np.average(teil["durchschnittsalter"], weights=teil["anzahl"])
    print(f"  {sport}: {schnitt:.1f} Jahre")

# --- Frage 2: Nationen ---
# China und Ukraine waren 1960-1980 nicht als eigenes Team bei Sommerspielen,
# deren "Aufstieg" ist kein fairer Vergleich -> im Diagramm grau
NICHT_VERGLEICHBAR = ["China", "Ukraine"]
vergleichbar = df_nationen[~df_nationen["country_name"].isin(NICHT_VERGLEICHBAR)]
top = vergleichbar.iloc[0]
print(f"Größter Aufstieg (vergleichbare Länder): {top['country_name']} +{top['verbesserung']}")

# --- Frage 3: Körperbau ---
df_koerper["diff_cm"] = (df_koerper["groesse_medaille_cm"] - df_koerper["groesse_ohne_cm"]).round(1)
df_koerper["diff_kg"] = (df_koerper["gewicht_medaille_kg"] - df_koerper["gewicht_ohne_kg"]).round(1)
print(df_koerper[["sport_name", "diff_cm", "diff_kg"]].to_string(index=False))


# ------------------------------------------------------------
# Dashboard
# ------------------------------------------------------------
BLAU, HELLBLAU = "#2E5FA3", "#9DBCE0"
GRUEN, HELLGRUEN = "#1A7A4A", "#93CFA8"
GRAU = "#B5B5B5"

plt.rcParams.update({
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
})

fig = plt.figure(figsize=(16, 20))
fig.suptitle("Olympia-Daten 1960 bis 2016: Judo, Boxen und Nationen",
             fontsize=19, fontweight="bold", y=0.985)


def werte_beschriften(ax, balken, format_="{:.1f}"):
    for b in balken:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(),
                format_.format(b.get_height()), ha="center", va="bottom", fontsize=9)


# 1) Alter je Medaille - Achse ab 0, sonst sehen 0,3 Jahre riesig aus
ax1 = fig.add_subplot(3, 2, 1)
farben = {"Boxing": [BLAU, "#5B86C4", HELLBLAU], "Judo": [GRUEN, "#4FA673", HELLGRUEN]}
beschriftung = df_alter["sport_name"] + "\n" + df_alter["medal"]
balkenfarben = [farben[s][i % 3] for i, s in enumerate(df_alter["sport_name"])]
werte_beschriften(ax1, ax1.bar(beschriftung, df_alter["durchschnittsalter"], color=balkenfarben))
ax1.set_ylim(0, 30)
ax1.set_title("Durchschnittsalter der Medaillengewinner")
ax1.set_ylabel("Jahre")

# 2) mit gegen ohne Medaille
ax2 = fig.add_subplot(3, 2, 2)
x = np.arange(len(df_mit_ohne))
breite = 0.35
b1 = ax2.bar(x - breite / 2, df_mit_ohne["alter_mit_medaille"], breite, color=[BLAU, GRUEN], label="mit Medaille")
b2 = ax2.bar(x + breite / 2, df_mit_ohne["alter_ohne_medaille"], breite, color=[HELLBLAU, HELLGRUEN], label="ohne Medaille")
werte_beschriften(ax2, b1)
werte_beschriften(ax2, b2)
ax2.set_xticks(x, df_mit_ohne["sport_name"])
ax2.set_ylim(0, 30)
ax2.set_title("Alter mit und ohne Medaille")
ax2.set_ylabel("Jahre")
ax2.legend(fontsize=9)

# 3) Nationen
ax3 = fig.add_subplot(3, 2, (3, 4))
sortiert = df_nationen.sort_values("verbesserung")
farben3 = [GRAU if land in NICHT_VERGLEICHBAR else BLAU for land in sortiert["country_name"]]
balken3 = ax3.barh(sortiert["country_name"], sortiert["verbesserung"], color=farben3)
for b, wert in zip(balken3, sortiert["verbesserung"]):
    ax3.text(b.get_width() + 5, b.get_y() + b.get_height() / 2, f"+{wert}", va="center", fontsize=9)
ax3.set_title("Mehr Medaillen 1996-2016 als 1960-1980 (Top 15, Medaillen pro Athlet)")
ax3.set_xlabel("zusätzliche Medaillen")
ax3.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=GRAU)],
           labels=["1960-1980 nicht als eigenes Team dabei, nicht vergleichbar"],
           fontsize=9, loc="lower right")

# 4) + 5) Körpergröße und Gewicht
for pos, (spalte_mit, spalte_ohne, titel, einheit) in zip(
        [5, 6],
        [("groesse_medaille_cm", "groesse_ohne_cm", "Körpergröße mit und ohne Medaille", "cm"),
         ("gewicht_medaille_kg", "gewicht_ohne_kg", "Gewicht mit und ohne Medaille", "kg")]):
    ax = fig.add_subplot(3, 2, pos)
    x = np.arange(len(df_koerper))
    m = ax.bar(x - breite / 2, df_koerper[spalte_mit], breite, color=[BLAU, GRUEN], label="mit Medaille")
    o = ax.bar(x + breite / 2, df_koerper[spalte_ohne], breite, color=[HELLBLAU, HELLGRUEN], label="ohne Medaille")
    werte_beschriften(ax, m)
    werte_beschriften(ax, o)
    ax.set_xticks(x, df_koerper["sport_name"])
    ax.set_ylim(0, df_koerper[[spalte_mit, spalte_ohne]].max().max() * 1.15)
    ax.set_title(titel)
    ax.set_ylabel(einheit)
    ax.legend(fontsize=9)

fig.text(0.5, 0.005,
         "Quelle: Olympia-Datensatz des Data Science Institute, Spiele ab 1960. "
         "Alter 0 (fehlender Wert) herausgefiltert.",
         ha="center", fontsize=9, color="#555555")

plt.tight_layout(rect=[0, 0.015, 1, 0.97])
plt.savefig(BILD, dpi=150, bbox_inches="tight")
plt.close()
print("Dashboard gespeichert:", BILD)
