-- ============================================================
-- Olympics Fallstudie
-- Skript 2: Datenimport via COPY
-- ============================================================
-- WICHTIG: Reihenfolge strikt einhalten!
-- Tabellen mit Fremdschluessel muessen nach den
-- referenzierten Tabellen importiert werden.
--
-- Reihenfolge:
-- 1. sports       (keine Abhaengigkeiten)
-- 2. countries    (keine Abhaengigkeiten)
-- 3. athletes     (keine Abhaengigkeiten)
-- 4. events       (benoetigt: sports)
-- 5. participations (benoetigt: alle anderen)
-- ============================================================

-- Dateipfad anpassen falls noetig:
-- C:\Program Files\PostgreSQL\17\data\import\

-- ------------------------------------------------------------
-- 1. sports importieren
-- ------------------------------------------------------------
COPY sports(sport_id, sport_name)
FROM 'C:\Program Files\PostgreSQL\17\data\import\sports.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');

-- ------------------------------------------------------------
-- 2. countries importieren
-- ------------------------------------------------------------
COPY countries(noc_code, country_name)
FROM 'C:\Program Files\PostgreSQL\17\data\import\countries.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');

-- ------------------------------------------------------------
-- 3. athletes importieren
-- ------------------------------------------------------------
COPY athletes(athlete_id, name, sex, height_cm, weight_kg)
FROM 'C:\Program Files\PostgreSQL\17\data\import\athletes.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');

-- ------------------------------------------------------------
-- 4. events importieren (benoetigt sports)
-- ------------------------------------------------------------
COPY events(event_id, event_name, sport_id)
FROM 'C:\Program Files\PostgreSQL\17\data\import\events.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');

-- ------------------------------------------------------------
-- 5. participations importieren (benoetigt alle anderen)
-- ------------------------------------------------------------
COPY participations(participation_id, athlete_id, noc_code,
                    sport_id, event_id, year, age, medal)
FROM 'C:\Program Files\PostgreSQL\17\data\import\participations.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');
