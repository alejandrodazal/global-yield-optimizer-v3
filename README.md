# Global Yield Optimizer v3.0

Sistema inteligente de optimización de rendimiento global con memoria RAG y agente de mejora continua.

## 🌟 Características Principales

- **Optimización de Portafolio Internacional**: Maximiza el rendimiento real de tus inversiones en múltiples monedas.
- **Sistema RAG Local**: Memoria de largo plazo basada en ChromaDB y SQLite.
- **Agente Inteligente de Mejora Continua**: Aprende de decisiones pasadas para ofrecer recomendaciones cada vez mejores.
- **Dashboard Web Interactivo**: Visualiza tus inversiones, métricas y decisiones del agente.
- **Simulador Financiero**: Prueba estrategias y evalúa resultados en un entorno controlado.

## 🏗️ Arquitectura

```
/global_yield_optimizer_v3
│
├── /data
│   ├── inflation_tracker.py
│   ├── rate_scraper.py
│   └── trm_handler.py
│
├── /core
│   ├── portfolio.py
│   ├── indicators.py
│   ├── strategy.py
│   └── rag_agent.py
│
├── /simulation
│   └── simulator.py
│
├── /api
│   └── main.py
│
├── /dashboard
│   └── app.py
│
├── /rag_memory
│   ├── chroma_db/
│   └── sqlite_db.db
│
├── /models
│   └── local_llm/
│
└── main.py
```

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone <repositorio>
   cd global_yield_optimizer_v3
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## ▶️ Uso

### Modos de Ejecución

- **Simulación**: Ejecuta una simulación de inversión por 12 meses por defecto
  ```bash
  python main.py --mode simulate --months 12
  ```

- **Dashboard**: Inicia el dashboard web
  ```bash
  python main.py --mode dashboard
  ```
  Luego accede en tu navegador a `http://localhost:8501`

- **Entrenamiento**: Entrena el agente RAG (en desarrollo)
  ```bash
  python main.py --mode train
  ```

## 🤖 Componentes Clave

### 1. Base de Datos Local RAG
- **ChromaDB**: Almacena embeddings de decisiones de inversión pasadas
- **SQLite**: Almacena datos estructurados (inversiones, tasas, inflación, TRM)

### 2. Agente RAG Inteligente
- Recupera decisiones pasadas similares
- Aprende de errores y resultados reales
- Genera recomendaciones mejoradas con ayuda de un LLM local

### 3. Dashboard Web (Streamlit)
- Visualización de inversiones y métricas
- Panel de memoria RAG
- Feedback manual para entrenamiento del agente

## 📈 Flujo de Mejora Continua

1. Registrar decisión en ChromaDB
2. Al final del mes, registrar resultado real
3. Entrenar al agente con nuevos datos
4. Próximo mes: Recomendación aún más afinada

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.