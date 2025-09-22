# strategy.py
"""
Investment strategy module for Global Yield Optimizer v3.0
"""
from .rag_agent import RAGInvestmentAgent


def get_investment_recommendation(current_trm, sma_45, inf_co, best_rate_co, month, rag_agent: RAGInvestmentAgent):
    """
    Genera una recomendación de inversión basada en indicadores actuales y memoria RAG.
    
    Args:
        current_trm (float): Tipo de cambio actual (TRM)
        sma_45 (float): Media móvil de 45 días de la TRM
        inf_co (float): Tasa de inflación en Colombia
        best_rate_co (float): Mejor tasa de interés en Colombia
        month (int): Mes actual
        rag_agent (RAGInvestmentAgent): Agente RAG para consulta de memoria
    
    Returns:
        str: Recomendación de inversión
    """
    # Contexto actual
    current_context = f"TRM: {current_trm}, SMA45: {sma_45}, Inflación CO: {inf_co}, Mejor tasa CO: {best_rate_co}"
    
    # Recuperar decisiones pasadas similares
    similar_docs, metadatas = rag_agent.retrieve_similar_decisions(current_context)
    
    # Si hay decisiones pasadas con buen resultado, ajusta la recomendación
    if similar_docs:
        improved_rec = rag_agent.generate_improved_strategy(current_context, similar_docs)
        return improved_rec
    else:
        # Regla simple por defecto si no hay memoria suficiente
        if current_trm > sma_45 * 1.025:  # Si TRM está 2.5% sobre su media
            return f"Recomendación: Invertir en instrumentos en COP con mejor tasa ({best_rate_co}%)"
        else:
            return "Recomendación: Mantener liquidez en USD hasta mejores condiciones"


def calculate_real_return(nominal_rate, inflation):
    """
    Calcula la rentabilidad real de una inversión.
    
    Args:
        nominal_rate (float): Tasa nominal de interés
        inflation (float): Tasa de inflación
    
    Returns:
        float: Rentabilidad real
    """
    return ((1 + nominal_rate/100) / (1 + inflation/100) - 1) * 100