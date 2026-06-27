
SELECT version() AS "Server Info";

-- rpta :
-- PostgreSQL 16.14 on x86_64-pc-linux-musl,
--                     compiled by gcc (Alpine 15.2.0) 15.2.0,
--                                                         64-bit

SELECT current_database() AS "Base_de_Datos_Activa";

-- rpta :
-- northwind


SELECT current_user AS "Usuario_Conectado";
-- rpta:
-- slinkter

SELECT inet_server_addr() AS "IP_del_Servidor_Remoto";





SELECT category_id,
       category_name,
       description,
       picture
FROM public.categories
LIMIT 1000;

SHOW tables;


SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;


SELECT *
FROM categories;