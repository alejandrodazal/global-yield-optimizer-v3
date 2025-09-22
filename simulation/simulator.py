# simulator.py
"""
Simulation module for Global Yield Optimizer v3.0
"""
import random
from datetime import datetime, timedelta
from core.portfolio import Portfolio
from core.strategy import get_investment_recommendation, calculate_real_return
from core.indicators import calculate_sma
from data.rate_scraper import scrape_bank_rates, get_best_rate, fetch_banrep_indicator
from data.trm_handler import get_current_trm, get_trm_history, fetch_trm_from_banrep
from data.inflation_tracker import get_current_inflation, fetch_colombian_inflation_from_banrep
from data.financial_data_provider import get_financial_data, get_best_investments
from data.cdt_scraper import get_cdt_rates, get_best_cdt_rate
from data.etf_scraper import get_etf_rates, get_best_etf_rate


class YieldSimulator:
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio
        self.current_month = 1
        self.simulation_date = datetime.now()
        # Países relevantes para el portafolio global
        self.relevant_countries = ["Colombia", "USA", "Panama"]
    
    def run_monthly_simulation(self, rag_agent):
        """
        Ejecuta una simulación mensual del proceso de toma de decisiones de inversión.
        
        Args:
            rag_agent: Agente RAG para consulta de memoria
            
        Returns:
            dict: Resultados de la simulación mensual
        """
        print(f"\n--- Simulación del Mes {self.current_month} ---")
        
        # 1. Obtener datos financieros completos
        financial_data = get_financial_data()
        best_investments = get_best_investments()
        
        current_trm = financial_data["trm"]
        trm_history = get_trm_history(45)
        sma_45 = calculate_sma(trm_history, 45)
        inflation_data = financial_data["inflation_rates"]
        
        inf_co = inflation_data["Colombia"]
        
        print(f"TRM actual: {current_trm}")
        print(f"SMA45 TRM: {sma_45:.2f}")
        print(f"Inflación Colombia: {inf_co}%")
        print(f"Inflación EE.UU.: {inflation_data['USA']}%")
        print(f"Inflación Panamá: {inflation_data['Panama']}%")
        
        # Mostrar mejores opciones de inversión
        print("\nMejores opciones de inversión:")
        for country in self.relevant_countries:
            best_cdt = best_investments[country]["best_cdt"]
            best_etf = best_investments[country]["best_etf"]
            print(f"{country}:")
            print(f"  Mejor CDT: {best_cdt['bank']} - {best_cdt['rate']}%")
            print(f"  Mejor ETF: {best_etf['symbol']} - {best_etf['details']['rate']}%")
        
        # 2. Obtener tasas de bancos (método existente para compatibilidad)
        bank_rates = scrape_bank_rates()
        best_bank, best_rate_co = get_best_rate(bank_rates, "COP")
        print(f"\nMejor tasa en COP (bancos): {best_rate_co}% ({best_bank})")
        
        # 3. Obtener recomendación de inversión usando el agente RAG
        recommendation = get_investment_recommendation(
            current_trm, sma_45, inf_co, best_rate_co, 
            self.current_month, rag_agent
        )
        print(f"Recomendación: {recommendation}")
        
        # 4. Simular ejecución de la inversión
        investment_result = self._execute_investment(best_bank, best_rate_co, inf_co)
        print(f"Inversión ejecutada: {investment_result}")
        
        # 5. Registrar en portfolio
        self.portfolio.record_investment(
            month=self.current_month,
            amount=investment_result['amount'],
            currency=investment_result['currency'],
            instrument=investment_result['instrument'],
            nominal_rate=investment_result['nominal_rate'],
            real_rate=investment_result['real_rate'],
            start_date=investment_result['start_date'],
            end_date=investment_result['end_date']
        )
        
        # 6. Registrar datos en base de datos
        for bank, rates in bank_rates.items():
            self.portfolio.record_bank_rate(
                month=self.current_month,
                bank=bank,
                currency="COP",
                nominal_rate=rates["COP"]
            )
            self.portfolio.record_bank_rate(
                month=self.current_month,
                bank=bank,
                currency="USD",
                nominal_rate=rates["USD"]
            )
        
        # Registrar inflación de países relevantes
        for country, inflation_rate in inflation_data.items():
            self.portfolio.record_inflation_rate(
                month=self.current_month,
                country=country,
                inflation_rate=inflation_rate
            )
        
        self.portfolio.record_trm(
            date=self.simulation_date.strftime("%Y-%m-%d"),
            trm_value=current_trm
        )
        
        # Registrar tasas de CDTs
        cdt_rates = financial_data["cdt_rates"]
        for country, banks in cdt_rates.items():
            for bank, rate in banks.items():
                self.portfolio.record_bank_rate(
                    month=self.current_month,
                    bank=f"{country}:{bank}",
                    currency="COP" if country == "Colombia" else "USD",
                    nominal_rate=rate
                )
        
        # Registrar tasas de ETFs
        etf_rates = financial_data["etf_rates"]
        for country, etfs in etf_rates.items():
            for symbol, details in etfs.items():
                self.portfolio.record_bank_rate(
                    month=self.current_month,
                    bank=f"{country}:ETF:{symbol}",
                    currency=details["currency"],
                    nominal_rate=details["rate"]
                )
        
        # 7. Registrar decisión en memoria RAG
        decision_text = f"MES {self.current_month}: {recommendation} porque TRM={'{:.2f}'.format(current_trm)} > SMA45={'{:.2f}'.format(sma_45)} y rentabilidad real={'{:.2f}'.format(investment_result['real_rate'])}%"
        metadata = {
            "month": self.current_month,
            "trm": current_trm,
            "sma45": sma_45,
            "inflation_co": inf_co,
            "inflation_usa": inflation_data["USA"],
            "inflation_panama": inflation_data["Panama"],
            "nominal_rate": best_rate_co,
            "real_rate": investment_result['real_rate'],
            "bank": best_bank
        }
        rag_agent.store_decision(decision_text, metadata)
        
        # 8. Avanzar al siguiente mes
        self.current_month += 1
        self.simulation_date += timedelta(days=30)
        
        return {
            "month": self.current_month - 1,
            "recommendation": recommendation,
            "investment": investment_result,
            "macro_data": {
                "trm": current_trm,
                "sma45": sma_45,
                "inflation_data": inflation_data,
                "best_rate_co": best_rate_co,
                "best_investments": best_investments
            }
        }
    
    def _execute_investment(self, bank, nominal_rate, inflation):
        """
        Simula la ejecución de una inversión.
        
        Args:
            bank (str): Nombre del banco
            nominal_rate (float): Tasa nominal
            inflation (float): Tasa de inflación
            
        Returns:
            dict: Detalles de la inversión ejecutada
        """
        # Simular detalles de la inversión
        amount = round(random.uniform(1000000, 5000000), 2)  # Entre 1M y 5M COP
        currency = "COP"
        instrument = f"CDT {bank}"
        real_rate = calculate_real_return(nominal_rate, inflation)
        start_date = self.simulation_date.strftime("%Y-%m-%d")
        end_date = (self.simulation_date + timedelta(days=30)).strftime("%Y-%m-%d")
        
        return {
            "amount": amount,
            "currency": currency,
            "instrument": instrument,
            "nominal_rate": nominal_rate,
            "real_rate": real_rate,
            "start_date": start_date,
            "end_date": end_date
        }
    
    def fetch_real_data(self):
        """
        Obtiene datos reales del Banco de la República para la simulación.
        
        Returns:
            dict: Datos reales obtenidos
        """
        try:
            # Obtener TRM real
            trm_data = fetch_trm_from_banrep()
            
            # Obtener inflación real
            inflation_data = fetch_colombian_inflation_from_banrep()
            
            # Obtener otras tasas de interés
            ti_data = fetch_banrep_indicator("TI")  # Tasa de Intervención
            
            return {
                "trm": trm_data,
                "inflation": inflation_data,
                "interest_rate": ti_data
            }
        except Exception as e:
            print(f"Error al obtener datos reales: {e}")
            return None
