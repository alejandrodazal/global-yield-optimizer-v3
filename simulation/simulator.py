# simulator.py
"""
Simulation module for Global Yield Optimizer v3.0
"""
import random
from datetime import datetime, timedelta
from core.portfolio import Portfolio
from core.strategy import get_investment_recommendation, calculate_real_return
from core.indicators import calculate_sma
from data.rate_scraper import scrape_bank_rates, get_best_rate
from data.trm_handler import get_current_trm, get_trm_history
from data.inflation_tracker import get_current_inflation


class YieldSimulator:
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio
        self.current_month = 1
        self.simulation_date = datetime.now()
    
    def run_monthly_simulation(self, rag_agent):
        """
        Ejecuta una simulación mensual del proceso de toma de decisiones de inversión.
        
        Args:
            rag_agent: Agente RAG para consulta de memoria
            
        Returns:
            dict: Resultados de la simulación mensual
        """
        print(f"\n--- Simulación del Mes {self.current_month} ---")
        
        # 1. Obtener datos macroeconómicos actuales
        current_trm = get_current_trm()
        trm_history = get_trm_history(45)
        sma_45 = calculate_sma(trm_history, 45)
        inf_co = get_current_inflation("Colombia")
        
        print(f"TRM actual: {current_trm}")
        print(f"SMA45 TRM: {sma_45:.2f}")
        print(f"Inflación Colombia: {inf_co}%")
        
        # 2. Obtener tasas de bancos
        bank_rates = scrape_bank_rates()
        best_bank, best_rate_co = get_best_rate(bank_rates, "COP")
        print(f"Mejor tasa en COP: {best_rate_co}% ({best_bank})")
        
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
        
        self.portfolio.record_inflation_rate(
            month=self.current_month,
            country="Colombia",
            inflation_rate=inf_co
        )
        
        self.portfolio.record_trm(
            date=self.simulation_date.strftime("%Y-%m-%d"),
            trm_value=current_trm
        )
        
        # 7. Registrar decisión en memoria RAG
        decision_text = f"MES {self.current_month}: {recommendation} porque TRM={'{:.2f}'.format(current_trm)} > SMA45={'{:.2f}'.format(sma_45)} y rentabilidad real={'{:.2f}'.format(investment_result['real_rate'])}%"
        metadata = {
            "month": self.current_month,
            "trm": current_trm,
            "sma45": sma_45,
            "inflation_co": inf_co,
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
                "inflation_co": inf_co,
                "best_rate_co": best_rate_co
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
