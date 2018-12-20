--
-- Drop tables
-- turn off FK checks temporarily to eliminate drop order issues
--
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS movie, genre, gender, cast, movie_cast, movie_genre;
SET FOREIGN_KEY_CHECKS=1;

import release_date as a string

--
-- gender
--
CREATE TABLE IF NOT EXISTS gender
  (
    gender_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    gender_name VARCHAR(45) NOT NULL,
    PRIMARY KEY (gender_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO gender (gender_name) VALUES
  ('Unspecified'), ('Female'), ('Male');   

--
-- genre
--
CREATE TABLE IF NOT EXISTS genre
  (
    genre_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    genre_name VARCHAR(45) NOT NULL,
    PRIMARY KEY (genre_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO genre (genre_name) VALUES
  ('Action'), ('Adventure'), ('Fantasy'), ('Animation'), ('Science Fiction'), ('Drama'), ('Thriller'), ('Family'), ('Comedy'), ('History'), 
  ('War'), ('Western'), ('Romance'), ('Crime'), ('Mystery'), ('Horror'), ('Documentary'), ('Music'), ('TV Movie'), ('Foreign');   

--
-- cast_temp
--

CREATE TEMPORARY TABLE cast_temp
  (
    cast_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    cast_name VARCHAR(45) NOT NULL,
    gender_id INTEGER NULL,
    identifier INTEGER NULL,
    PRIMARY KEY (cast_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/cast.csv'
INTO TABLE cast_temp
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (gender_id, identifier, cast_name)
  SET gender_id = IF(gender_id = '', NULL, gender_id),
  identifier = IF(identifier = '', NULL, identifier),
  cast_name = IF(cast_name = '', NULL, cast_name);

--
-- cast
--

SET FOREIGN_KEY_CHECKS=0;
CREATE TABLE IF NOT EXISTS cast
  (
    cast_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    cast_name VARCHAR(45) NOT NULL,
    gender_id INTEGER NULL,
    PRIMARY KEY (cast_id),
    FOREIGN KEY (gender_id) REFERENCES gender(gender_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO cast (cast_name, gender_id)
SELECT ct.cast_name, ct.gender_id FROM cast_temp ct ORDER BY ct.cast_id;
SET FOREIGN_KEY_CHECKS=1;

--
-- movie_temp
--
CREATE TEMPORARY TABLE movie_temp
  (
    movie_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    genres VARCHAR(255) NULL,
    budget INTEGER NULL,
    homepage VARCHAR(255) NULL,
    tmdb_id INTEGER NOT NULL,
    original_language VARCHAR(255) NULL,
    original_title VARCHAR(255) NULL,
    overview TEXT NULL,
    popularity VARCHAR(255) NULL,
    release_date CHAR(6) NULL,
    revenue BIGINT NULL,
    runtime INTEGER NULL,
    tagline VARCHAR(255) NULL,
    title VARCHAR(255) NULL,
    vote_average VARCHAR(255) NULL,
    vote_count INTEGER NULL,
    PRIMARY KEY (movie_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movie.csv'
INTO TABLE movie_temp
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (budget, genres, homepage, original_language, original_title, overview, popularity, @release_date, 
  revenue, runtime, @dummy, tagline, title, vote_average, vote_count, tmdb_id)
  
  SET budget = IF(budget = '', NULL, budget),
  genres = IF(genres = '', NULL,  genres),
  homepage = IF(homepage = '', NULL, homepage),
  original_language = IF(original_language = '', NULL, original_language),
  original_title = IF(original_title = '', NULL,  original_title),
  overview = IF(overview = '', NULL, overview),
  popularity = IF(popularity = '', NULL, popularity),
  release_date = IF(release_date = '', NULL,  release_date),
  revenue = IF(revenue = '', NULL, revenue),
  runtime = IF(runtime = '', NULL, runtime),
  tagline = IF(tagline = '', NULL, tagline),
  title = IF(title = '', NULL, title),
  vote_average = IF(vote_average = '', NULL, vote_average),
  vote_count = IF(tagline = '', NULL, vote_count);


--
-- movie
--

CREATE TABLE IF NOT EXISTS movie
  (
    movie_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    budget INTEGER NULL,
    homepage VARCHAR(255) NULL,
    tmdb_id INTEGER NULL,
    original_language VARCHAR(255) NULL,
    original_title VARCHAR(255) NULL,
    overview TEXT NULL,
    popularity DECIMAL(12,6) NULL,
    -- release_date DATE NULL,
    revenue BIGINT NULL,
    runtime INTEGER NULL,
    tagline VARCHAR(255) NULL,
    title VARCHAR(255) NULL,
    vote_average DECIMAL(10, 1) NULL,
    vote_count INTEGER NULL,
    PRIMARY KEY (movie_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO movie(budget, homepage, original_language, original_title, overview, popularity, 
  revenue, runtime, tagline, title, vote_average, vote_count, tmdb_id)
SELECT mt.budget, mt.homepage, mt.original_language, mt.original_title, mt.overview, CAST(mt.popularity AS DECIMAL(12, 6)) AS popularity,
       mt.revenue, mt.runtime, mt.tagline, mt.title, CAST(mt.vote_average AS DECIMAL(10, 1)) AS vote_average, mt.vote_count, mt.tmdb_id 
       FROM movie_temp mt ORDER BY mt.movie_id;

--
-- movie_genre
--

CREATE TABLE IF NOT EXISTS movie_genre
  (
    movie_genre_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
    ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Create temporary numbers table that will be used to split out comma-delimited lists of genres.
CREATE TEMPORARY TABLE numbers
  (
    num INTEGER NOT NULL UNIQUE,
    PRIMARY KEY (num)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO numbers (num) VALUES
  (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15), (16), (17), (18), (19), (20);

-- Create temporary table to store split out genres.
CREATE TEMPORARY TABLE multi_genre
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    movie_id INTEGER NOT NULL,
    genre_name VARCHAR(45) NOT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- This query splits the genres and inserts them into the target temp table.
INSERT IGNORE INTO multi_genre(movie_id, genre_name)
SELECT mt.movie_id,
       SUBSTRING_INDEX(SUBSTRING_INDEX(mt.genres, ',', numbers.num), ',', -1)
       AS genre_name
  FROM numbers
       INNER JOIN movie_temp mt
               ON CHAR_LENGTH(mt.genres) -
                  CHAR_LENGTH(REPLACE(mt.genres, ',', ''))
                  >= numbers.num - 1
 ORDER BY mt.movie_id, numbers.num;

 -- Insert movie linked to multiple genres in junction table.
INSERT IGNORE INTO movie_genre(movie_id, genre_id)
SELECT m.movie_id,
       g.genre_id
  FROM multi_genre mg
       LEFT JOIN movie m
              ON mg.movie_id = m.movie_id
       LEFT JOIN genre g
              ON mg.genre_name = g.genre_name
 ORDER BY mg.id;

--
-- movie_cast
--

CREATE TEMPORARY TABLE movie_cast_temp
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    tmdb_id INTEGER NOT NULL,
    actor_id INTEGER NOT NULL,
    characters VARCHAR(300) NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movie_cast.csv'
INTO TABLE movie_cast_temp
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (characters, actor_id, tmdb_id)
  SET characters = IF(characters = '', NULL, characters),
  actor_id = IF(actor_id = '', NULL, actor_id),
  tmdb_id = IF(tmdb_id = '', NULL, tmdb_id);

CREATE TABLE IF NOT EXISTS movie_cast
  (
    movie_cast_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    movie_id INTEGER NOT NULL,
    cast_id INTEGER NOT NULL,
    characters VARCHAR(300) NULL,
    PRIMARY KEY (movie_cast_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO movie_cast(movie_id, cast_id, characters)
SELECT m.movie_id,
       c.cast_id,
       mct.characters
  FROM movie_cast_temp mct
       LEFT JOIN movie m
              ON mct.tmdb_id = m.tmdb_id
       LEFT JOIN cast_temp ct
              ON mct.actor_id = ct.identifier
       LEFT JOIN cast c 
              ON ct.cast_name = c.cast_name
 ORDER BY mct.id;

DROP TEMPORARY TABLE cast_temp, movie_temp, numbers, multi_genre, movie_cast_temp;