# portfolio.py
"""
Portfolio management module for Global Yield Optimizer v3.0
"""
import sqlite3
from datetime import datetime


class Portfolio:
    def __init__(self, db_path="rag_memory/sqlite_db.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Inicializa la base de datos SQLite para el portfolio."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Crear tabla de inversiones si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month INTEGER,
                amount REAL,
                currency TEXT,
                instrument TEXT,
                nominal_rate REAL,
                real_rate REAL,
                start_date TEXT,
                end_date TEXT,
                status TEXT
            )
        ''')
        
        # Crear tabla de tasas mensuales por banco
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bank_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month INTEGER,
                bank TEXT,
                currency TEXT,
                nominal_rate REAL
            )
        ''')
        
        # Crear tabla de inflación mensual por país
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inflation_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month INTEGER,
                country TEXT,
                inflation_rate REAL
            )
        ''')
        
        # Crear tabla de TRM diaria/histórica
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trm_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                trm_value REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_investment(self, month, amount, currency, instrument, nominal_rate, real_rate, start_date, end_date):
        """Registra una inversión en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO investments 
            (month, amount, currency, instrument, nominal_rate, real_rate, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (month, amount, currency, instrument, nominal_rate, real_rate, start_date, end_date, 'active'))
        
        conn.commit()
        conn.close()
    
    def update_investment_result(self, investment_id, real_return, status='completed'):
        """Actualiza el resultado real de una inversión."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE investments 
            SET real_rate = ?, status = ?
            WHERE id = ?
        ''', (real_return, status, investment_id))
        
        conn.commit()
        conn.close()
    
    def get_historical_investments(self, month=None):
        """Obtiene inversiones históricas, opcionalmente filtradas por mes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if month:
            cursor.execute('SELECT * FROM investments WHERE month = ?', (month,))
        else:
            cursor.execute('SELECT * FROM investments')
            
        investments = cursor.fetchall()
        conn.close()
        return investments
    
    def record_bank_rate(self, month, bank, currency, nominal_rate):
        """Registra la tasa de un banco para un mes específico."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bank_rates (month, bank, currency, nominal_rate)
            VALUES (?, ?, ?, ?)
        ''', (month, bank, currency, nominal_rate))
        
        conn.commit()
        conn.close()
    
    def record_inflation_rate(self, month, country, inflation_rate):
        """Registra la tasa de inflación de un país para un mes específico."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO inflation_rates (month, country, inflation_rate)
            VALUES (?, ?, ?)
        ''', (month, country, inflation_rate))
        
        conn.commit()
        conn.close()
    
    def record_trm(self, date, trm_value):
        """Registra el valor de la TRM para una fecha específica."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trm_history (date, trm_value)
            VALUES (?, ?)
        ''', (date, trm_value))
        
        conn.commit()
        conn.close()