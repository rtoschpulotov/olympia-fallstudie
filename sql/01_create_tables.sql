-- ============================================================
-- Olympics Fallstudie
-- Skript 1: Datenbankstruktur erstellen
-- ============================================================

-- ENUM-Typ fuer Medaillen definieren
-- Verhindert ungueltige Eingaben und ist effizienter als CHECK-Constraints
CREATE TYPE medal_enum AS ENUM ('Gold', 'Silver', 'Bronze', 'None');

-- ------------------------------------------------------------
-- Tabelle: athletes
-- Stammdaten der Athleten
-- ------------------------------------------------------------
CREATE TABLE athletes (
    athlete_id  INT PRIMARY KEY,
    name        VARCHAR(200),
    sex         CHAR(1),
    height_cm   FLOAT,
    weight_kg   FLOAT
);

-- ------------------------------------------------------------
-- Tabelle: countries
-- Nationale Olympische Komitees (NOC)
-- noc_code als PK, da dieser in den Olympia-Daten
-- der eindeutige Identifier ist
-- ------------------------------------------------------------
CREATE TABLE countries (
    noc_code     CHAR(3) PRIMARY KEY,
    country_name VARCHAR(100)
);

-- ------------------------------------------------------------
-- Tabelle: sports
-- Die 36 Sportarten ab dem Jahr 1960
-- ------------------------------------------------------------
CREATE TABLE sports (
    sport_id    INT PRIMARY KEY,
    sport_name  VARCHAR(100)
);

-- ------------------------------------------------------------
-- Tabelle: events
-- Einzelne Wettkampfdisziplinen, jeweils einer Sportart zugeordnet
-- ------------------------------------------------------------
CREATE TABLE events (
    event_id    INT PRIMARY KEY,
    event_name  VARCHAR(200),
    sport_id    INT REFERENCES sports(sport_id)
);

-- ------------------------------------------------------------
-- Tabelle: participations
-- Faktentabelle - verbindet alle Entitaeten
-- Jede Zeile = ein Athlet bei einem Event in einem Jahr
-- ------------------------------------------------------------
CREATE TABLE participations (
    participation_id INT PRIMARY KEY,
    athlete_id       INT REFERENCES athletes(athlete_id),
    noc_code         CHAR(3) REFERENCES countries(noc_code),
    sport_id         INT REFERENCES sports(sport_id),
    event_id         INT REFERENCES events(event_id),
    year             INT,
    age              INT,
    medal            medal_enum
);
