# -*- coding: utf-8 -*-
"""
Script para convertir archivos SQL de MySQL a PostgreSQL
Actualiza nombres de tablas/columnas a snake_case y funciones específicas
"""

import re

def convert_mysql_to_postgres(content):
    """Convierte sintaxis MySQL a PostgreSQL"""
    
    # Tabla y columna: PascalCase -> snake_case
    replacements = {
        # Tablas
        r'\bCustomers\b': 'customers',
        r'\bOrders\b': 'orders',
        r'\bOrderDetails\b': 'order_details',
        r'\bProducts\b': 'products',
        r'\bCategories\b': 'categories',
        r'\bSuppliers\b': 'suppliers',
        r'\bEmployees\b': 'employees',
        r'\bShippers\b': 'shippers',
        
        # Columnas comunes
        r'\bCustomerID\b': 'customer_id',
        r'\bOrderID\b': 'order_id',
        r'\bProductID\b': 'product_id',
        r'\bCategoryID\b': 'category_id',
        r'\bSupplierID\b': 'supplier_id',
        r'\bEmployeeID\b': 'employee_id',
        r'\bShipperID\b': 'shipper_id',
        r'\bContactName\b': 'contact_name',
        r'\bCompanyName\b': 'company_name',
        r'\bProductName\b': 'product_name',
        r'\bCategoryName\b': 'category_name',
        r'\bUnitPrice\b': 'unit_price',
        r'\bUnitsInStock\b': 'units_in_stock',
        r'\bOrderDate\b': 'order_date',
        r'\bShipVia\b': 'ship_via',
        r'\bFirstName\b': 'first_name',
        r'\bLastName\b': 'last_name',
        r'\bReportsTo\b': 'reports_to',
        r'\bShipCountry\b': 'ship_country',
        r'\bQuantity\b': 'quantity',
        r'\bCountry\b': 'country',
        r'\bCity\b': 'city',
        
        # Alias comunes en CamelCase
        r'\bEmployeeName\b': 'employee_name',
        r'\bTotalSales\b': 'total_sales',
        r'\bNumberOfOrders\b': 'number_of_orders',
        r'\bLifetimeValue\b': 'lifetime_value',
        r'\bAvgDaysBetweenOrders\b': 'avg_days_between_orders',
        r'\bDaysSinceFirstOrder\b': 'days_since_first_order',
        r'\bGrowthPercentage\b': 'growth_percentage',
        r'\bAvgProductsPerOrder\b': 'avg_products_per_order',
        r'\bPercentageOfTotal\b': 'percentage_of_total',
        r'\bMonthsSinceFirstOrder\b': 'months_since_first_order',
        r'\bRetainedCustomers\b': 'retained_customers',
        r'\bCohortMonth\b': 'cohort_month',
        r'\bOrderMonth\b': 'order_month',
        r'\bSaleMonth\b': 'sale_month',
        r'\bSaleYear\b': 'sale_year',
        r'\bMonthlyTotal\b': 'monthly_total',
        r'\bPreviousMonthTotal\b': 'previous_month_total',
        r'\bTotalSpent\b': 'total_spent',
        r'\bSpendingDecile\b': 'spending_decile',
        r'\bSalesRank\b': 'sales_rank',
        r'\bPopularityRank\b': 'popularity_rank',
        r'\bProductCount\b': 'product_count',
        r'\bTotalSale\b': 'total_sale',
        r'\bMovingAvg3Days\b': 'moving_avg_3_days',
        r'\bPreviousOrderDate\b': 'previous_order_date',
        r'\bNextOrderDate\b': 'next_order_date',
        r'\bPreviousOrderTotal\b': 'previous_order_total',
        r'\bOrderTotal\b': 'order_total',
        r'\bAvgCategoryPrice\b': 'avg_category_price',
        r'\bCumulativeTotal\b': 'cumulative_total',
        r'\bTotalProducts\b': 'total_products',
        r'\bOrderCounts\b': 'order_counts',
        r'\bFirstDate\b': 'first_date',
        r'\bQuarterlySales\b': 'quarterly_sales',
        r'\bGrandTotal\b': 'grand_total',
        r'\bProductTotal\b': 'product_total',
        r'\bAvgProfitMargin\b': 'avg_profit_margin',
        r'\bFrequency\b': 'frequency',
    }
    
    # Aplicar reemplazos de nombres
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
    
    # Funciones MySQL -> PostgreSQL
    # DATE_FORMAT -> TO_CHAR
    content = re.sub(r"DATE_FORMAT\(([^,]+),\s*'%Y-%m'\)", r"TO_CHAR(\1, 'YYYY-MM')", content)
    
    # YEAR() -> EXTRACT(YEAR FROM ...)
    content = re.sub(r'\bYEAR\(([^)]+)\)', r'EXTRACT(YEAR FROM \1)', content)
    
    # MONTH() -> EXTRACT(MONTH FROM ...)
    content = re.sub(r'\bMONTH\(([^)]+)\)', r'EXTRACT(MONTH FROM \1)', content)
    
    # QUARTER() -> EXTRACT(QUARTER FROM ...)
    content = re.sub(r'\bQUARTER\(([^)]+)\)', r'EXTRACT(QUARTER FROM \1)', content)
    
    # CONCAT(a, ' ', b) -> a || ' ' || b
    def replace_concat(match):
        args = match.group(1)
        # Simple split por comas (no perfecto pero funciona para casos comunes)
        parts = [p.strip() for p in args.split(',')]
        return ' || '.join(parts)
    
    content = re.sub(r"CONCAT\(([^)]+)\)", replace_concat, content)
    
    # DATEDIFF(a, b) -> (a - b)
    content = re.sub(r'DATEDIFF\(([^,]+),\s*([^)]+)\)', r'(\1 - \2)', content)
    
    # DATE_SUB(date, INTERVAL n MONTH) -> (date - INTERVAL 'n months')
    content = re.sub(r"DATE_SUB\(([^,]+),\s*INTERVAL\s+(\d+)\s+MONTH\)", r"(\1 - INTERVAL '\2 months')", content)
    
    # TIMESTAMPDIFF -> AGE/EXTRACT (más complejo, hacemos una versión simplificada)
    content = re.sub(
        r"TIMESTAMPDIFF\(MONTH,\s*STR_TO_DATE\(([^,]+),\s*'%Y-%m'\),\s*STR_TO_DATE\(([^,]+),\s*'%Y-%m'\)\)",
        r"EXTRACT(YEAR FROM AGE(TO_DATE(\2, 'YYYY-MM'), TO_DATE(\1, 'YYYY-MM'))) * 12 + EXTRACT(MONTH FROM AGE(TO_DATE(\2, 'YYYY-MM'), TO_DATE(\1, 'YYYY-MM')))",
        content
    )
    
    # Nombres de CTE en CamelCase -> snake_case
    cte_names = {
        'EmployeeHierarchy': 'employee_hierarchy',
        'DailySales': 'daily_sales',
        'CustomerFirstOrder': 'customer_first_order',
        'MonthlyOrders': 'monthly_orders',
        'CohortRetention': 'cohort_retention',
        'EmployeeSales': 'employee_sales',
        'ProductSales': 'product_sales',
        'TotalSales': 'total_sales',
        'CustomerSpending': 'customer_spending',
        'RankedSpending': 'ranked_spending',
        'ProductPopularity': 'product_popularity',
        'FirstOrderDate': 'first_order_date',
        'MonthlySales': 'monthly_sales',
        'RankedSales': 'ranked_sales',
        'SalesWithLag': 'sales_with_lag',
        'ProductsPerOrder': 'products_per_order',
        'OrderedOrders': 'ordered_orders',
        'CountryProductSales': 'country_product_sales',
        'ChaiOrders': 'chai_orders',
        'LondonCustomers': 'london_customers',
        'CustomerSales': 'customer_sales',
        'ProductCategorySales': 'product_category_sales',
    }
    
    for old_name, new_name in cte_names.items():
        content = re.sub(r'\b' + old_name + r'\b', new_name, content)
    
    # Agregar NULLIF para evitar división por cero
    content = re.sub(r'/ ([a-z_]+\.[a-z_]+)', r'/ NULLIF(\1, 0)', content)
    
    return content

def main():
    """Función principal"""
    file_path = r"c:\Users\LJCR\Documents\GitHub\ApuntesSQL\PostgresSQL\3.avanzado.md"
    
    print(f"Leyendo {file_path}...")
    
    # Leer archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Convirtiendo a PostgreSQL...")
    
    # Convertir
    converted = convert_mysql_to_postgres(content)
    
    # Actualizar título
    converted = converted.replace(
        '# SQL Avanzado: Consultas de Alta Complejidad y Análisis de Datos',
        '# SQL Avanzado con PostgreSQL: Consultas de Alta Complejidad y Análisis de Datos'
    )
    
    # Actualizar descripción
    converted = converted.replace(
        'Esta sección aborda escenarios complejos que requieren un profundo conocimiento de SQL para resolver problemas de negocio, realizar análisis de datos avanzados y optimizar el rendimiento.',
        'Esta sección aborda escenarios complejos que requieren un profundo conocimiento de SQL para resolver problemas de negocio, realizar análisis de datos avanzados y optimizar el rendimiento usando **PostgreSQL** y la base de datos **Northwind**.'
    )
    
    # Guardar
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print(f"[OK] Archivo actualizado: {file_path}")
    print("Conversión completada!")

if __name__ == "__main__":
    main()
