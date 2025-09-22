# app.py
"""
Dashboard for Global Yield Optimizer v3.0
"""
import streamlit as st
import pandas as pd
from core.portfolio import Portfolio


def main():
    st.set_page_config(page_title="Global Yield Optimizer v3.0", layout="wide")
    st.title("🌍 Global Yield Optimizer v3.0")
    
    # Inicializar portfolio
    portfolio = Portfolio()
    
    # Sidebar
    st.sidebar.header("Navegación")
    page = st.sidebar.radio("Ir a:", [
        "Dashboard Principal", 
        "Historial de Inversiones", 
        "Memoria RAG",
        "Simulación"
    ])
    
    if page == "Dashboard Principal":
        show_dashboard(portfolio)
    elif page == "Historial de Inversiones":
        show_investment_history(portfolio)
    elif page == "Memoria RAG":
        show_rag_memory()
    elif page == "Simulación":
        show_simulation()


def show_dashboard(portfolio):
    st.header("📊 Dashboard Principal")
    
    # Mostrar últimas inversiones
    st.subheader("Últimas Inversiones")
    investments = portfolio.get_historical_investments()
    
    if investments:
        # Convertir a DataFrame para mejor visualización
        df = pd.DataFrame(investments, columns=[
            "ID", "Mes", "Monto", "Moneda", "Instrumento", 
            "Tasa Nominal", "Tasa Real", "Fecha Inicio", "Fecha Fin", "Estado"
        ])
        st.dataframe(df.tail(10))
    else:
        st.info("No hay inversiones registradas aún.")
    
    # Mostrar métricas clave
    st.subheader(" Métricas Clave")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Invertido", "$10.5M", "+$1.2M")
    with col2:
        st.metric("Rentabilidad Promedio", "4.2%", "+0.3%")
    with col3:
        st.metric("Inversiones Activas", "8", "2")


def show_investment_history(portfolio):
    st.header("🕒 Historial de Inversiones")
    
    investments = portfolio.get_historical_investments()
    
    if investments:
        # Convertir a DataFrame para mejor visualización
        df = pd.DataFrame(investments, columns=[
            "ID", "Mes", "Monto", "Moneda", "Instrumento", 
            "Tasa Nominal", "Tasa Real", "Fecha Inicio", "Fecha Fin", "Estado"
        ])
        st.dataframe(df)
        
        # Filtros
        st.subheader("Filtros")
        month_filter = st.selectbox("Filtrar por mes:", ["Todos"] + sorted(df["Mes"].unique()))
        
        if month_filter != "Todos":
            df = df[df["Mes"] == month_filter]
            st.dataframe(df)
    else:
        st.info("No hay inversiones registradas aún.")


def show_rag_memory():
    st.header("📚 Memoria RAG")
    st.info("En una implementación completa, aquí se mostrarían las decisiones pasadas recuperadas por el sistema RAG.")
    
    # Ejemplo de decisiones pasadas (simuladas)
    sample_decisions = [
        "MES 12: Invertí en CDT Davivienda 9.8% porque TRM > SMA45 y rentabilidad real 5.16%",
        "MES 11: Mantuve liquidez en USD porque TRM < SMA45 y la mejor tasa en COP era solo 4.2%",
        "MES 10: Invertí en CDT Bancolombia 10.5% con rentabilidad real 6.3% gracias a TRM favorable",
        "MES 9: Invertí en HYSA USA 2.4% pero podría haber obtenido mejor tasa esperando 15 días"
    ]
    
    for i, decision in enumerate(sample_decisions, 1):
        st.write(f"{i}. {decision}")


def show_simulation():
    st.header("🔄 Simulación")
    st.info("En una implementación completa, aquí se ejecutaría el simulador mensual.")
    
    if st.button("Ejecutar Simulación del Mes"):
        st.success("Simulación ejecutada correctamente. Ver resultados en el dashboard principal.")


if __name__ == "__main__":
    main()