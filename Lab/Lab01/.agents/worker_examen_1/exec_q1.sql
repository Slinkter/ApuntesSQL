SELECT
    company_name,
    contact_name,
    contact_title,
    country
FROM customers
WHERE country IN ('UK', 'Germany', 'France', 'Spain', 'Italy')
ORDER BY country, company_name;