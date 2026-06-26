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