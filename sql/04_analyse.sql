-- ============================================================
-- Olympics Fallstudie
-- Skript 4: Auswertungen zu den drei Fragestellungen
-- ============================================================
-- Die Abfragen aus der Abgabe hatte ich nicht als Datei gespeichert.
-- Bei der Überarbeitung (10/2026) habe ich sie hier neu aufgeschrieben
-- und die Ergebnisse gegen die Rohdaten geprüft.
--
-- Wichtig: In der Rohdatei steht bei fehlendem Alter eine 0.
-- Deshalb filtere ich überall age > 0, sonst rechnet AVG()
-- diese Athleten als 0 Jahre alt mit und der Schnitt sinkt.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Durchschnittsalter je Medaille, Boxen und Judo
--    -> ergebnisse/alter_analyse.csv
-- ------------------------------------------------------------
SELECT s.sport_name,
       p.medal,
       ROUND(AVG(p.age)::numeric, 1) AS durchschnittsalter,
       COUNT(*)                      AS anzahl
FROM participations p
JOIN sports s ON s.sport_id = p.sport_id
WHERE s.sport_name IN ('Boxing', 'Judo')
  AND p.medal <> 'None'
  AND p.age > 0
GROUP BY s.sport_name, p.medal
ORDER BY s.sport_name, p.medal;


-- ------------------------------------------------------------
-- 2. Alter mit und ohne Medaille
--    -> ergebnisse/alter_mit_ohne_medaille.csv
-- ------------------------------------------------------------
SELECT s.sport_name,
       ROUND(AVG(p.age) FILTER (WHERE p.medal <> 'None')::numeric, 1) AS alter_mit_medaille,
       ROUND(AVG(p.age) FILTER (WHERE p.medal =  'None')::numeric, 1) AS alter_ohne_medaille
FROM participations p
JOIN sports s ON s.sport_id = p.sport_id
WHERE s.sport_name IN ('Boxing', 'Judo')
  AND p.age > 0
GROUP BY s.sport_name
ORDER BY s.sport_name;


-- ------------------------------------------------------------
-- 3. Körpergröße und Gewicht mit und ohne Medaille
--    Fehlende Werte (NULL) lässt AVG() von selbst weg
--    -> ergebnisse/koerperbau_analyse.csv
-- ------------------------------------------------------------
SELECT s.sport_name,
       ROUND(AVG(a.height_cm) FILTER (WHERE p.medal <> 'None')::numeric, 1) AS groesse_medaille_cm,
       ROUND(AVG(a.height_cm) FILTER (WHERE p.medal =  'None')::numeric, 1) AS groesse_ohne_cm,
       ROUND(AVG(a.weight_kg) FILTER (WHERE p.medal <> 'None')::numeric, 1) AS gewicht_medaille_kg,
       ROUND(AVG(a.weight_kg) FILTER (WHERE p.medal =  'None')::numeric, 1) AS gewicht_ohne_kg
FROM participations p
JOIN athletes a ON a.athlete_id = p.athlete_id
JOIN sports   s ON s.sport_id   = p.sport_id
WHERE s.sport_name IN ('Boxing', 'Judo')
GROUP BY s.sport_name
ORDER BY s.sport_name;


-- ------------------------------------------------------------
-- 4. Nationen-Aufstieg: Medaillen 1960-1980 gegen 1996-2016
--    Gezählt wird jede Medaille pro Athlet (Teams zählen mehrfach).
--    Gruppiert nach Ländername, dadurch zählt z.B. die Sowjetunion
--    zu Russland und BRD/DDR zu Deutschland.
--    -> ergebnisse/nationen_aufstieg.csv
-- ------------------------------------------------------------
SELECT c.country_name,
       COUNT(*) FILTER (WHERE p.year BETWEEN 1960 AND 1980) AS medaillen_frueh,
       COUNT(*) FILTER (WHERE p.year BETWEEN 1996 AND 2016) AS medaillen_spaet,
       COUNT(*) FILTER (WHERE p.year BETWEEN 1996 AND 2016)
     - COUNT(*) FILTER (WHERE p.year BETWEEN 1960 AND 1980) AS verbesserung
FROM participations p
JOIN countries c ON c.noc_code = p.noc_code
WHERE p.medal <> 'None'
GROUP BY c.country_name
ORDER BY verbesserung DESC
LIMIT 15;
