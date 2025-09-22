# indicators.py
"""
Technical indicators module for Global Yield Optimizer v3.0
"""
import pandas as pd


def calculate_sma(data, period):
    """
    Calcula la media móvil simple (SMA) para un conjunto de datos.
    
    Args:
        data (list): Lista de valores (por ejemplo, tasas de cambio)
        period (int): Período para calcular la media móvil
    
    Returns:
        float: Valor de la media móvil
    """
    if len(data) < period:
        raise ValueError(f"No hay suficientes datos para calcular SMA de período {period}")
    
    return sum(data[-period:]) / period


def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Calcula el MACD (Moving Average Convergence Divergence).
    
    Args:
        data (list): Lista de valores
        fast_period (int): Período para la media móvil rápida
        slow_period (int): Período para la media móvil lenta
        signal_period (int): Período para la línea de señal
    
    Returns:
        tuple: (macd_line, signal_line, histogram)
    """
    # Convertir a pandas Series para facilitar cálculos
    series = pd.Series(data)
    
    # Calcular medias móviles exponenciales
    ema_fast = series.ewm(span=fast_period).mean()
    ema_slow = series.ewm(span=slow_period).mean()
    
    # Calcular línea MACD
    macd_line = ema_fast - ema_slow
    
    # Calcular línea de señal
    signal_line = macd_line.ewm(span=signal_period).mean()
    
    # Calcular histograma
    histogram = macd_line - signal_line
    
    return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]