# main.py
"""
Main entry point for Global Yield Optimizer v3.0
"""
import argparse
from core.portfolio import Portfolio
from core.rag_agent import RAGInvestmentAgent
from simulation.simulator import YieldSimulator
from chromadb import Client


def main():
    parser = argparse.ArgumentParser(description="Global Yield Optimizer v3.0")
    parser.add_argument(
        "--mode", 
        choices=["simulate", "dashboard", "train"], 
        default="simulate",
        help="Modo de ejecución: simulate, dashboard, o train"
    )
    parser.add_argument(
        "--months", 
        type=int, 
        default=12,
        help="Número de meses para simular (solo en modo simulate)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "simulate":
        run_simulation(args.months)
    elif args.mode == "dashboard":
        run_dashboard()
    elif args.mode == "train":
        run_training()


def run_simulation(months=12):
    """Ejecuta la simulación por un número especificado de meses."""
    print("🚀 Iniciando Global Yield Optimizer v3.0 - Modo Simulación")
    
    # Inicializar componentes
    portfolio = Portfolio()
    chroma_client = Client()
    rag_agent = RAGInvestmentAgent(chroma_client)
    simulator = YieldSimulator(portfolio)
    
    # Ejecutar simulación mensual
    for _ in range(months):
        simulator.run_monthly_simulation(rag_agent)
    
    print(f"✅ Simulación completada por {months} meses")


def run_dashboard():
    """Inicia el dashboard web."""
    print("🌐 Iniciando dashboard web...")
    print("Ejecuta: streamlit run dashboard/app.py")


def run_training():
    """Ejecuta el entrenamiento del agente RAG."""
    print("🤖 Iniciando entrenamiento del agente RAG...")
    # En una implementación completa, aquí se entrenaría el agente
    # con datos históricos y feedback


if __name__ == "__main__":
    main()