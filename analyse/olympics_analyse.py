"""
=============================================================
Olympics Fallstudie - Python Datenanalyse
=============================================================
Autor:      Rustam Toschpulotov (Einzelarbeit, DSI-Weiterbildung)
Ziel:       Analyse der Olympia-Daten (1960–2016) zu drei
            Fragestellungen:
              1. Peak-Alter: Judo vs. Boxing
              2. Nationen-Aufstieg über die Jahrzehnte
              3. Körperbau & Medaillenerfolg
Datenquelle: Normalisierte Excel-Tabellen aus pgAdmin-Export
Tools:      Pandas, NumPy, Matplotlib
=============================================================
"""

# ── Bibliotheken importieren ──────────────────────────────────
# pandas  → Daten einlesen, verarbeiten und analysieren
# numpy   → Mathematische Berechnungen (z.B. gewichteter Durchschnitt)
# matplotlib → Visualisierungen und Dashboard erstellen
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Kein Fenster öffnen, direkt als Datei speichern
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────────────────────
# SCHRITT 1: Daten aus Excel-Dateien einlesen
# Jede Excel-Datei hat zwei Sheets: "Daten" und "Analyse"
# Wir lesen immer das Sheet "Daten" ein, da dort die Rohdaten sind
# ─────────────────────────────────────────────────────────────

# Fragestellung 1: Peak-Alter (Judo vs. Boxing)
# Enthält: Sportart, Medaille, Durchschnittsalter, Anzahl Athleten
df_alter = pd.read_excel(
    'Altersanalyse_Judo_Boxing.xlsx',
    sheet_name='Daten'
)

# Fragestellung 2: Nationen-Aufstieg
# Enthält: Land, Medaillen früh (1960-1980), Medaillen spät (1996-2016), Verbesserung
df_nationen = pd.read_excel(
    'Nationen_Aufstieg.xlsx',
    sheet_name='Daten'
)

# Fragestellung 3: Körperbau & Medaillenerfolg
# Enthält: Sportart, Größe mit/ohne Medaille, Gewicht mit/ohne Medaille
df_koerper = pd.read_excel(
    'Koerperbau_Analyse.xlsx',
    sheet_name='Daten'
)

# Kurze Überprüfung: Wurden die Daten korrekt eingelesen?
print("=" * 55)
print("DATEN ERFOLGREICH EINGELESEN")
print("=" * 55)
print(f"Altersanalyse:   {len(df_alter)} Zeilen")
print(f"Nationen:        {len(df_nationen)} Zeilen")
print(f"Körperbau:       {len(df_koerper)} Zeilen")

# ─────────────────────────────────────────────────────────────
# SCHRITT 2: Datenanalyse mit Pandas & NumPy
# Hier berechnen wir zusätzliche Kennzahlen die über die
# reinen SQL-Ergebnisse hinausgehen
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("FRAGESTELLUNG 1: Peak-Alter (Judo vs. Boxing)")
print("=" * 55)

# Gewichteter Durchschnitt des Alters berechnen
# (nicht einfacher Durchschnitt, weil Bronze doppelt so viele
#  Athleten hat wie Gold - das muss berücksichtigt werden)
for sport in ['Boxing', 'Judo']:
    subset = df_alter[df_alter['Sportart'] == sport]
    gewichteter_schnitt = np.average(
        subset['Durchschnittsalter'],
        weights=subset['Anzahl Athleten']  # Gewichtung nach Anzahl
    )
    print(f"{sport}: Gewichtetes Ø Alter = {gewichteter_schnitt:.2f} Jahre")

print("\n" + "=" * 55)
print("FRAGESTELLUNG 2: Nationen-Aufstieg")
print("=" * 55)

# Größten Aufsteiger identifizieren
bester_idx = df_nationen['Verbesserung'].idxmax()
print(f"Größter Aufsteiger: {df_nationen.loc[bester_idx, 'Land']}")
print(f"Verbesserung:       +{df_nationen['Verbesserung'].max()} Medaillen")
print(f"Ø Verbesserung:     +{df_nationen['Verbesserung'].mean():.1f} Medaillen")

# Länder die früher gar keine Medaillen hatten (= Newcomer)
newcomer = df_nationen[df_nationen['Medaillen 1960-1980'] == 0]
print(f"Newcomer (0 Medaillen früher): {', '.join(newcomer['Land'].tolist())}")

print("\n" + "=" * 55)
print("FRAGESTELLUNG 3: Körperbau & Medaillenerfolg")
print("=" * 55)

# Unterschied zwischen Medaillengewinnern und Nicht-Gewinnern berechnen
# Positive Zahl = Medaillengewinner sind größer/schwerer
df_koerper['Größen-Unterschied (cm)'] = (
    df_koerper['Größe mit Medaille (cm)'] -
    df_koerper['Größe ohne Medaille (cm)']
).round(1)

df_koerper['Gewichts-Unterschied (kg)'] = (
    df_koerper['Gewicht mit Medaille (kg)'] -
    df_koerper['Gewicht ohne Medaille (kg)']
).round(1)

print(df_koerper[['Sportart',
                   'Größen-Unterschied (cm)',
                   'Gewichts-Unterschied (kg)']].to_string(index=False))

# ─────────────────────────────────────────────────────────────
# SCHRITT 3: Dashboard erstellen mit Matplotlib
# 5 Diagramme in einem Layout - alle 3 Fragestellungen
# ─────────────────────────────────────────────────────────────

# Farbpalette definieren - konsistent durch alle Diagramme
BLAU      = "#2E5FA3"   # Boxing Hauptfarbe
HELLBLAU  = "#7BA7D4"   # Boxing Nebenfarbe
GRUEN     = "#1A7A4A"   # Judo Hauptfarbe
HELLGRUEN = "#6DBF8A"   # Judo Nebenfarbe
ROT       = "#E8523A"   # Ausreißer / Hervorhebung
GRAU      = "#F5F5F5"   # Hintergrundfarbe
DUNKEL    = "#2C2C2C"   # Textfarbe

# Globale Einstellungen für alle Diagramme
plt.rcParams.update({
    'font.family':       'DejaVu Sans',
    'axes.spines.top':   False,   # Rahmen oben ausblenden
    'axes.spines.right': False,   # Rahmen rechts ausblenden
    'axes.facecolor':    GRAU,    # Hintergrundfarbe der Diagramme
    'figure.facecolor':  'white', # Hintergrundfarbe des gesamten Dashboards
    'axes.titlesize':    13,
    'axes.titleweight':  'bold',
    'axes.labelsize':    11,
})

# Dashboard-Grundgerüst erstellen
# 3 Zeilen, 2 Spalten - insgesamt 5 Diagramme
fig = plt.figure(figsize=(18, 22))
fig.suptitle(
    "Olympics Datenanalyse - Judo & Boxing (1960–2016)",
    fontsize=20, fontweight='bold', color=DUNKEL, y=0.98
)

# ── Diagramm 1: Alter nach Medaillentyp ──────────────────────
# Zeigt wie alt Athleten im Schnitt waren als sie Gold/Silver/Bronze gewannen
ax1 = fig.add_subplot(3, 2, 1)

# Farben je nach Sportart zuweisen
farben1 = [BLAU, HELLBLAU, "#A8C4E0",   # Boxing: dunkel → hell
           GRUEN, HELLGRUEN, "#A8D4B8"]  # Judo:   dunkel → hell

labels1 = df_alter['Sportart'] + "\n" + df_alter['Medaille']
bars1   = ax1.bar(labels1, df_alter['Durchschnittsalter'],
                  color=farben1, edgecolor='white', linewidth=1.5, width=0.6)

# Werte über den Balken anzeigen
for bar, val in zip(bars1, df_alter['Durchschnittsalter']):
    ax1.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.05,
             f'{val}', ha='center', va='bottom',
             fontsize=10, fontweight='bold', color=DUNKEL)

ax1.set_ylim(20, 27)
ax1.set_title("Ø Alter der Medaillengewinner")
ax1.set_ylabel("Alter (Jahre)")

# Legende für Farbzuordnung
boxing_p = mpatches.Patch(color=BLAU,  label='Boxing (~23 J.)')
judo_p   = mpatches.Patch(color=GRUEN, label='Judo (~25 J.)')
ax1.legend(handles=[boxing_p, judo_p], fontsize=9)

# ── Diagramm 2: Alter mit vs. ohne Medaille ──────────────────
# Vergleich: Sind Medaillengewinner älter als Nicht-Gewinner?
ax2 = fig.add_subplot(3, 2, 2)

kat2   = ["Boxing\nmit Medaille", "Boxing\nohne Medaille",
          "Judo\nmit Medaille",   "Judo\nohne Medaille"]
werte2 = [23.3, 22.8, 25.2, 25.1]
farb2  = [BLAU, HELLBLAU, GRUEN, HELLGRUEN]

bars2 = ax2.bar(kat2, werte2, color=farb2,
                edgecolor='white', linewidth=1.5, width=0.6)
for bar, val in zip(bars2, werte2):
    ax2.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.05,
             f'{val}', ha='center', va='bottom',
             fontsize=10, fontweight='bold', color=DUNKEL)

ax2.set_ylim(20, 27)
ax2.set_title("Ø Alter: Mit vs. Ohne Medaille")
ax2.set_ylabel("Alter (Jahre)")

# ── Diagramm 3: Nationen-Aufstieg (horizontales Balkendiagramm) ──
# Horizontale Darstellung weil Ländernamen lang sind
ax3 = fig.add_subplot(3, 2, (3, 4))  # Diagramm über beide Spalten

# Daten aufsteigend sortieren für bessere Lesbarkeit
df_sort = df_nationen.sort_values('Verbesserung')

# Ausreißer (China, USA, Australia) rot markieren - Rest blau
farb3 = [ROT if v >= 400 else BLAU for v in df_sort['Verbesserung']]

bars3 = ax3.barh(df_sort['Land'], df_sort['Verbesserung'],
                 color=farb3, edgecolor='white', linewidth=1, height=0.65)

# Werte rechts neben den Balken anzeigen
for bar, val in zip(bars3, df_sort['Verbesserung']):
    ax3.text(bar.get_width() + 5,
             bar.get_y() + bar.get_height() / 2,
             f'+{val}', va='center', fontsize=9,
             fontweight='bold', color=DUNKEL)

ax3.set_title("Medaillen-Verbesserung: 1960–1980 vs. 1996–2016 (Top 15 Nationen)")
ax3.set_xlabel("Anzahl zusätzlicher Medaillen")

# Trennlinie bei 400 um Ausreißer visuell hervorzuheben
ax3.axvline(x=400, color=ROT, linestyle='--',
            alpha=0.5, linewidth=1.5, label='Ausreißer-Grenze (400+)')
ax3.legend(fontsize=9)

# ── Diagramm 4: Körpergröße Vergleich ────────────────────────
ax4 = fig.add_subplot(3, 2, 5)

x     = np.arange(2)   # Positionen für Boxing und Judo
width = 0.35           # Balkenbreite

# Zwei Balkengruppen: mit Medaille und ohne Medaille
b1 = ax4.bar(x - width / 2,
             df_koerper['Größe mit Medaille (cm)'],
             width, label='Mit Medaille',
             color=[BLAU, GRUEN], edgecolor='white')
b2 = ax4.bar(x + width / 2,
             df_koerper['Größe ohne Medaille (cm)'],
             width, label='Ohne Medaille',
             color=[HELLBLAU, HELLGRUEN], edgecolor='white')

# Werte über Balken anzeigen
for gruppe in [b1, b2]:
    for bar in gruppe:
        ax4.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.1,
                 f'{bar.get_height()}',
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

ax4.set_xticks(x)
ax4.set_xticklabels(["Boxing", "Judo"])
ax4.set_ylim(168, 178)  # Engerer Bereich um Unterschiede besser sichtbar zu machen
ax4.set_title("Körpergröße: Mit vs. Ohne Medaille (cm)")
ax4.set_ylabel("Größe (cm)")
ax4.legend(fontsize=9)

# ── Diagramm 5: Gewicht Vergleich ────────────────────────────
ax5 = fig.add_subplot(3, 2, 6)

b3 = ax5.bar(x - width / 2,
             df_koerper['Gewicht mit Medaille (kg)'],
             width, label='Mit Medaille',
             color=[BLAU, GRUEN], edgecolor='white')
b4 = ax5.bar(x + width / 2,
             df_koerper['Gewicht ohne Medaille (kg)'],
             width, label='Ohne Medaille',
             color=[HELLBLAU, HELLGRUEN], edgecolor='white')

for gruppe in [b3, b4]:
    for bar in gruppe:
        ax5.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.1,
                 f'{bar.get_height()}',
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

ax5.set_xticks(x)
ax5.set_xticklabels(["Boxing", "Judo"])
ax5.set_ylim(58, 86)
ax5.set_title("Gewicht: Mit vs. Ohne Medaille (kg)")
ax5.set_ylabel("Gewicht (kg)")
ax5.legend(fontsize=9)

# ─────────────────────────────────────────────────────────────
# SCHRITT 4: Dashboard speichern
# dpi=150 sorgt für gute Qualität ohne zu große Dateigröße
# bbox_inches='tight' schneidet leere Ränder ab
# ─────────────────────────────────────────────────────────────
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('Olympics_Dashboard.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nDashboard gespeichert als: Olympics_Dashboard.png")
print("Analyse abgeschlossen!")
