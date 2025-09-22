# financial_data_provider.py
"""
Financial data provider module for Global Yield Optimizer v3.0
"""
from typing import Dict, List, Tuple
from .cdt_scraper import get_cdt_rates, get_best_cdt_rate
from .etf_scraper import get_etf_rates, get_best_etf_rate
from .inflation_tracker import get_current_inflation
from .trm_handler import get_current_trm
from .rate_scraper import scrape_bank_rates


class FinancialDataProvider:
    """Proveedor unificado de datos financieros para el Global Yield Optimizer."""
    
    def __init__(self):
        """Inicializa el proveedor de datos financieros."""
        self.countries = ["Colombia", "USA", "Panama"]
    
    def get_all_cdt_rates(self) -> Dict[str, Dict[str, float]]:
        """
        Obtiene tasas de CDTs de todos los países relevantes.
        
        Returns:
            Dict[str, Dict[str, float]]: Tasas de CDTs por país
        """
        cdt_rates = {}
        for country in self.countries:
            cdt_rates[country] = get_cdt_rates(country)
        return cdt_rates
    
    def get_all_etf_rates(self) -> Dict[str, Dict[str, Dict]]:
        """
        Obtiene tasas de ETFs de todos los países relevantes.
        
        Returns:
            Dict[str, Dict[str, Dict]]: Tasas de ETFs por país
        """
        etf_rates = {}
        for country in self.countries:
            etf_rates[country] = get_etf_rates(country)
        return etf_rates
    
    def get_all_inflation_rates(self) -> Dict[str, float]:
        """
        Obtiene tasas de inflación de todos los países relevantes.
        
        Returns:
            Dict[str, float]: Tasas de inflación por país
        """
        inflation_rates = {}
        for country in self.countries:
            inflation_rates[country] = get_current_inflation(country)
        return inflation_rates
    
    def get_best_investment_options(self) -> Dict[str, Dict]:
        """
        Obtiene las mejores opciones de inversión por país.
        
        Returns:
            Dict[str, Dict]: Mejores opciones de inversión por país
        """
        best_options = {}
        
        # Obtener mejores CDTs
        for country in self.countries:
            best_cdt_bank, best_cdt_rate = get_best_cdt_rate(country)
            best_etf_symbol, best_etf_details = get_best_etf_rate(country)
            
            best_options[country] = {
                "best_cdt": {
                    "bank": best_cdt_bank,
                    "rate": best_cdt_rate
                },
                "best_etf": {
                    "symbol": best_etf_symbol,
                    "details": best_etf_details
                }
            }
        
        return best_options
    
    def get_macro_data(self) -> Dict[str, any]:
        """
        Obtiene todos los datos macroeconómicos relevantes.
        
        Returns:
            Dict[str, any]: Datos macroeconómicos
        """
        return {
            "trm": get_current_trm(),
            "inflation_rates": self.get_all_inflation_rates(),
            "cdt_rates": self.get_all_cdt_rates(),
            "etf_rates": self.get_all_etf_rates(),
            "best_investment_options": self.get_best_investment_options()
        }


# Funciones de conveniencia
def get_financial_data() -> Dict[str, any]:
    """
    Obtiene todos los datos financieros relevantes.
    
    Returns:
        Dict[str, any]: Datos financieros
    """
    provider = FinancialDataProvider()
    return provider.get_macro_data()


def get_best_investments() -> Dict[str, Dict]:
    """
    Obtiene las mejores opciones de inversión de todos los países.
    
    Returns:
        Dict[str, Dict]: Mejores opciones de inversión por país
    """
    provider = FinancialDataProvider()
    return provider.get_best_investment_options()