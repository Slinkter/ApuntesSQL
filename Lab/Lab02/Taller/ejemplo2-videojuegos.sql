-- 🎮 GameHub: Base de datos relacional para practicar SQL (MySQL)
-- Incluye creación de tablas, inserción de datos y consultas explicadas paso a paso.

-- ------------------------------------------------------
-- 1️⃣ CREACIÓN DE BASE DE DATOS Y TABLAS
-- ------------------------------------------------------
CREATE DATABASE gamehub;
USE gamehub;

-- Tabla de plataformas (consolas o sistemas)
CREATE TABLE platforms (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  manufacturer VARCHAR(100),
  release_year INT
);

-- Tabla de videojuegos
CREATE TABLE games (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  genre VARCHAR(100),
  release_year INT,
  platform_id INT UNSIGNED,
  FOREIGN KEY (platform_id) REFERENCES platforms(id) ON DELETE SET NULL
);

-- Tabla de usuarios
CREATE TABLE users (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  country VARCHAR(100),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de sesiones de juego
CREATE TABLE sessions (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNSIGNED NOT NULL,
  game_id INT UNSIGNED NOT NULL,
  hours_played DECIMAL(5,1) NOT NULL,
  session_date DATE DEFAULT (CURRENT_DATE),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
);

-- ------------------------------------------------------
-- 2️⃣ INSERCIÓN DE DATOS DE EJEMPLO
-- ------------------------------------------------------
INSERT INTO platforms (name, manufacturer, release_year) VALUES
('PlayStation 5', 'Sony', 2020),
('Xbox Series X', 'Microsoft', 2020),
('Nintendo Switch', 'Nintendo', 2017),
('PC', 'Various', 2000);

INSERT INTO games (title, genre, release_year, platform_id) VALUES
('The Last of Us Part II', 'Action', 2020, 1),
('Halo Infinite', 'Shooter', 2021, 2),
('Zelda: Breath of the Wild', 'Adventure', 2017, 3),
('Cyberpunk 2077', 'RPG', 2020, 4),
('Fortnite', 'Battle Royale', 2017, 4);

INSERT INTO users (username, country) VALUES
('GamerMax', 'Argentina'),
('LunaPlayz', 'Chile'),
('ProTaku', 'México'),
('ShadowFox', 'España');

INSERT INTO sessions (user_id, game_id, hours_played, session_date) VALUES
(1, 1, 15.5, '2024-06-10'),
(1, 4, 8.0, '2024-06-12'),
(2, 3, 22.3, '2024-06-09'),
(2, 5, 5.0, '2024-06-11'),
(3, 2, 12.5, '2024-06-08'),
(3, 5, 30.0, '2024-06-13'),
(4, 3, 5.5, '2024-06-14'),
(4, 5, 40.0, '2024-06-15');

-- ------------------------------------------------------
-- 3️⃣ CONSULTAS DE PRÁCTICA CON EXPLICACIONES
-- ------------------------------------------------------

-- 🧩 CONSULTA 1: Listar todos los videojuegos con su plataforma
SELECT g.title, g.genre, p.name AS plataforma
FROM games g
JOIN platforms p ON g.platform_id = p.id;
-- 👉 INNER JOIN básico entre juegos y plataformas.

-- 🧩 CONSULTA 2: Total de horas jugadas por usuario
SELECT u.username, SUM(s.hours_played) AS total_horas
FROM users u
JOIN sessions s ON u.id = s.user_id
GROUP BY u.username
ORDER BY total_horas DESC;
-- 👉 Usa GROUP BY + SUM() para sumar horas por usuario.
-- 👉 ORDER BY DESC muestra el top de jugadores más activos.

-- 🧩 CONSULTA 3: Total de horas jugadas por videojuego
SELECT g.title, ROUND(SUM(s.hours_played), 1) AS total_horas
FROM games g
JOIN sessions s ON g.id = s.game_id
GROUP BY g.title
ORDER BY total_horas DESC;
-- 👉 Similar al anterior, pero agrupando por juego.

-- 🧩 CONSULTA 4: Promedio de horas jugadas por sesión y juego
SELECT g.title, ROUND(AVG(s.hours_played), 2) AS promedio_horas
FROM games g
JOIN sessions s ON g.id = s.game_id
GROUP BY g.title
ORDER BY promedio_horas DESC;
-- 👉 Usa AVG() para calcular promedios de tiempo por sesión.

-- 🧩 CONSULTA 5: Usuarios que jugaron más de un juego
SELECT u.username, COUNT(DISTINCT s.game_id) AS juegos_distintos
FROM users u
JOIN sessions s ON u.id = s.user_id
GROUP BY u.username
HAVING COUNT(DISTINCT s.game_id) > 1;
-- 👉 HAVING filtra resultados agregados: solo usuarios con más de un juego distinto.

-- 🧩 CONSULTA 6: Ranking de los 3 juegos más jugados
SELECT g.title, ROUND(SUM(s.hours_played), 1) AS total_horas
FROM games g
JOIN sessions s ON g.id = s.game_id
GROUP BY g.title
ORDER BY total_horas DESC
LIMIT 3;
-- 👉 Combina GROUP BY, ORDER BY y LIMIT para mostrar el top 3.

-- 🧩 CONSULTA 7: Mostrar qué usuarios jugaron en cada plataforma
SELECT DISTINCT u.username, p.name AS plataforma
FROM users u
JOIN sessions s ON u.id = s.user_id
JOIN games g ON s.game_id = g.id
JOIN platforms p ON g.platform_id = p.id
ORDER BY u.username, plataforma;
-- 👉 Ejemplo de varios JOINs encadenados, mostrando la relación indirecta entre usuario y plataforma.