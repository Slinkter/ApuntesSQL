-- 🎬 CineVerse: Base de datos relacional para practicar SQL (MySQL)
-- Incluye creación de tablas, inserción de datos y consultas explicadas paso a paso.

-- ------------------------------------------------------
-- 1️⃣ CREACIÓN DE BASE DE DATOS Y TABLAS
-- ------------------------------------------------------
CREATE DATABASE cineverse;
USE cineverse;

-- Tabla de películas
CREATE TABLE movies (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  genre VARCHAR(100),
  release_year INT,
  director_id INT UNSIGNED,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de directores
CREATE TABLE directors (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  country VARCHAR(100)
);

-- Tabla de actores
CREATE TABLE actors (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  birth_year INT
);

-- Tabla intermedia que relaciona películas y actores
CREATE TABLE castings (
  movie_id INT UNSIGNED,
  actor_id INT UNSIGNED,
  role_name VARCHAR(255),
  PRIMARY KEY (movie_id, actor_id),
  FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
  FOREIGN KEY (actor_id) REFERENCES actors(id) ON DELETE CASCADE
);

-- Tabla de reseñas de usuarios
CREATE TABLE reviews (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  movie_id INT UNSIGNED NOT NULL,
  user_name VARCHAR(100) NOT NULL,
  rating DECIMAL(2,1) CHECK (rating BETWEEN 0 AND 10),
  comment TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);

-- ------------------------------------------------------
-- 2️⃣ INSERCIÓN DE DATOS DE EJEMPLO
-- ------------------------------------------------------
INSERT INTO directors (name, country) VALUES
('Christopher Nolan', 'UK'),
('Greta Gerwig', 'USA'),
('Hayao Miyazaki', 'Japan');

INSERT INTO movies (title, genre, release_year, director_id) VALUES
('Inception', 'Sci-Fi', 2010, 1),
('Barbie', 'Comedy', 2023, 2),
('Spirited Away', 'Fantasy', 2001, 3),
('Interstellar', 'Sci-Fi', 2014, 1);

INSERT INTO actors (name, birth_year) VALUES
('Leonardo DiCaprio', 1974),
('Margot Robbie', 1990),
('Matthew McConaughey', 1969),
('Chiwetel Ejiofor', 1977),
('Rumi Hiiragi', 1987);

INSERT INTO castings (movie_id, actor_id, role_name) VALUES
(1, 1, 'Cobb'),
(2, 2, 'Barbie'),
(4, 3, 'Cooper'),
(3, 5, 'Chihiro');

INSERT INTO reviews (movie_id, user_name, rating, comment) VALUES
(1, 'Sofia', 9.0, 'Excelente trama y efectos visuales.'),
(1, 'Carlos', 8.5, 'Muy buena pero un poco confusa.'),
(2, 'Lucía', 7.8, 'Divertida y original.'),
(3, 'Pedro', 9.5, 'Una obra maestra del cine japonés.'),
(4, 'Ana', 9.2, 'Ciencia ficción con corazón.');

-- ------------------------------------------------------
-- 3️⃣ CONSULTAS DE PRÁCTICA CON EXPLICACIONES
-- ------------------------------------------------------

-- 🧩 CONSULTA 1: Listar todas las películas con su director
SELECT m.title, m.genre, d.name AS director
FROM movies m
JOIN directors d ON m.director_id = d.id;
-- 👉 Ejemplo básico de INNER JOIN para combinar dos tablas relacionadas.

-- 🧩 CONSULTA 2: Mostrar las películas con el promedio de puntuación
SELECT m.title, ROUND(AVG(r.rating), 2) AS promedio_rating
FROM movies m
JOIN reviews r ON m.id = r.movie_id
GROUP BY m.title
ORDER BY promedio_rating DESC;
-- 👉 Usa GROUP BY para agrupar reseñas por película y AVG() para calcular el promedio.
-- 👉 ORDER BY DESC para ver primero las películas con mejor puntaje.

-- 🧩 CONSULTA 3: Cantidad de películas por género
SELECT genre, COUNT(*) AS total_peliculas
FROM movies
GROUP BY genre
ORDER BY total_peliculas DESC;
-- 👉 Ejemplo clásico de agregación: cuenta cuántas películas hay por género.

-- 🧩 CONSULTA 4: Mostrar actores y las películas donde participaron
SELECT a.name AS actor, m.title AS pelicula
FROM actors a
JOIN castings c ON a.id = c.actor_id
JOIN movies m ON c.movie_id = m.id
ORDER BY actor;
-- 👉 Combina tres tablas con JOIN para listar relaciones muchos-a-muchos.

-- 🧩 CONSULTA 5: Películas con más de una reseña
SELECT m.title, COUNT(r.id) AS cantidad_reseñas
FROM movies m
JOIN reviews r ON m.id = r.movie_id
GROUP BY m.title
HAVING COUNT(r.id) > 1;
-- 👉 Usa HAVING (no WHERE) para filtrar sobre resultados agregados.

-- 🧩 CONSULTA 6: Top 3 películas más valoradas
SELECT m.title, ROUND(AVG(r.rating), 2) AS promedio
FROM movies m
JOIN reviews r ON m.id = r.movie_id
GROUP BY m.title
ORDER BY promedio DESC
LIMIT 3;
-- 👉 Combina GROUP BY, ORDER BY y LIMIT para crear un ranking de películas.