-- ============================================================
-- Olympics Fallstudie
-- Skript 3: Validierung nach dem Import
-- ============================================================

-- ------------------------------------------------------------
-- 1. Zeilenanzahl aller Tabellen prüfen
-- Erwartete Ergebnisse:
--   athletes      = 87.734
--   countries     = 222
--   sports        = 36
--   events        = 375
--   participations = 165.978
-- ------------------------------------------------------------
SELECT 'athletes'       AS tabelle, COUNT(*) AS anzahl FROM athletes
UNION ALL
SELECT 'countries',     COUNT(*) FROM countries
UNION ALL
SELECT 'sports',        COUNT(*) FROM sports
UNION ALL
SELECT 'events',        COUNT(*) FROM events
UNION ALL
SELECT 'participations',COUNT(*) FROM participations;

-- ------------------------------------------------------------
-- 2. JOIN-Test: Athleten mit ihren Medaillen
-- Prüft ob die Beziehung zwischen participations und athletes funktioniert
-- ------------------------------------------------------------
SELECT a.name, p.year, p.medal
FROM participations p
JOIN athletes a ON a.athlete_id = p.athlete_id
WHERE p.medal != 'None'
LIMIT 10;

-- ------------------------------------------------------------
-- 3. JOIN-Test: Top 10 Länder nach Teilnahmen
-- Prüft ob die Beziehung zwischen participations und countries funktioniert
-- ------------------------------------------------------------
SELECT c.country_name, COUNT(*) AS teilnahmen
FROM participations p
JOIN countries c ON c.noc_code = p.noc_code
GROUP BY c.country_name
ORDER BY teilnahmen DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 4. JOIN-Test: Events mit Sportart und Teilnahmenanzahl
-- Prüft ob die Beziehungen über alle Tabellen hinweg funktionieren
-- ------------------------------------------------------------
SELECT e.event_name, s.sport_name, COUNT(*) AS teilnahmen
FROM participations p
JOIN events e  ON e.event_id  = p.event_id
JOIN sports s  ON s.sport_id  = e.sport_id
GROUP BY e.event_name, s.sport_name
ORDER BY teilnahmen DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 5. Medaillenverteilung prüfen
-- Zeigt wie viele Gold, Silber, Bronze und None vergeben wurden
-- ------------------------------------------------------------
SELECT medal, COUNT(*) AS anzahl
FROM participations
GROUP BY medal
ORDER BY anzahl DESC;
