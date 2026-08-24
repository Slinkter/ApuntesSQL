WITH dias AS (
    SELECT
        generate_series(
            '1997-01-01'::date,
            '1997-01-31'::date,
            '1 day'::interval
        )::date AS fecha
)
SELECT
    fecha,
    TO_CHAR(fecha, 'Day') AS dia_semana,
    CASE
        WHEN EXTRACT(ISODOW FROM fecha) BETWEEN 1 AND 5 THEN 'Laboral'
        ELSE 'Fin de semana'
    END AS tipo_dia
FROM dias
ORDER BY fecha
LIMIT 12;