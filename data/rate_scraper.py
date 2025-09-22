# rate_scraper.py
"""
Rate scraper module for Global Yield Optimizer v3.0
"""
import random  # Para simulación de datos


def scrape_bank_rates():
    """
    Simula el scraping de tasas de interés de bancos.
    En una implementación real, aquí se conectaría a APIs o sitios web de bancos.
    
    Returns:
        dict: Diccionario con tasas de diferentes bancos
    """
    # Tasas simuladas para diferentes bancos en Colombia
    banks = {
        "Bancolombia": {"COP": 10.5, "USD": 2.1},
        "Davivienda": {"COP": 11.2, "USD": 2.3},
        "BBVA": {"COP": 10.8, "USD": 2.0},
        "Banco de Bogotá": {"COP": 11.0, "USD": 2.2}
    }
    
    return banks


def get_best_rate(bank_rates, currency):
    """
    Obtiene la mejor tasa para una moneda específica.
    
    Args:
        bank_rates (dict): Diccionario con tasas de bancos
        currency (str): Moneda ("COP" o "USD")
    
    Returns:
        tuple: (nombre_banco, tasa)
    """
    best_bank = None
    best_rate = 0
    
    for bank, rates in bank_rates.items():
        if currency in rates and rates[currency] > best_rate:
            best_rate = rates[currency]
            best_bank = bank
    
    return best_bank, best_rate