# app.py
"""
Dashboard for Global Yield Optimizer v3.0
"""
import streamlit as st
import pandas as pd
from core.portfolio import Portfolio
from data.financial_data_provider import get_financial_data, get_best_investments


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
        "Simulación",
        "Datos Financieros"
    ])
    
    if page == "Dashboard Principal":
        show_dashboard(portfolio)
    elif page == "Historial de Inversiones":
        show_investment_history(portfolio)
    elif page == "Memoria RAG":
        show_rag_memory()
    elif page == "Simulación":
        show_simulation()
    elif page == "Datos Financieros":
        show_financial_data()


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
    
    # Mostrar inflación de países relevantes
    st.subheader("Inflación por País")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Colombia", "3.2%", "↓0.1%")
    with col2:
        st.metric("EE.UU.", "2.8%", "↑0.2%")
    with col3:
        st.metric("Panamá", "2.5%", "0.0%")


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


def show_financial_data():
    st.header("💰 Datos Financieros")
    
    # Obtener datos financieros
    financial_data = get_financial_data()
    best_investments = get_best_investments()
    
    # Mostrar TRM
    st.subheader("Tasa de Cambio (TRM)")
    st.metric("TRM Actual", f"${financial_data['trm']:,.2f} COP/USD")
    
    # Mostrar inflación por país
    st.subheader("Inflación por País")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Colombia", f"{financial_data['inflation_rates']['Colombia']}%")
    with col2:
        st.metric("EE.UU.", f"{financial_data['inflation_rates']['USA']}%")
    with col3:
        st.metric("Panamá", f"{financial_data['inflation_rates']['Panama']}%")
    
    # Mostrar mejores inversiones
    st.subheader("Mejores Opciones de Inversión")
    
    for country in ["Colombia", "USA", "Panama"]:
        st.write(f"**{country}**")
        col1, col2 = st.columns(2)
        
        with col1:
            best_cdt = best_investments[country]["best_cdt"]
            st.write(f"CDT: {best_cdt['bank']} - {best_cdt['rate']}%")
        
        with col2:
            best_etf = best_investments[country]["best_etf"]
            st.write(f"ETF: {best_etf['symbol']} - {best_etf['details']['rate']}%")
        
        st.markdown("---")


if __name__ == "__main__":
    main()