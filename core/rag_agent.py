# rag_agent.py
"""
RAG Investment Agent for Global Yield Optimizer v3.0
"""
from chromadb import Client
from sentence_transformers import SentenceTransformer


class RAGInvestmentAgent:
    def __init__(self, chroma_client, model_name='all-MiniLM-L6-v2'):
        self.chroma = chroma_client
        self.encoder = SentenceTransformer(model_name)
        self.collection = self.chroma.get_or_create_collection("investment_memories")

    def store_decision(self, decision_text, metadata):
        # Convierte el texto de la decisión en un embedding y lo almacena
        embedding = self.encoder.encode(decision_text).tolist()
        self.collection.add(
            embeddings=[embedding],
            documents=[decision_text],
            metadatas=[metadata],
            ids=[f"decision_{metadata['month']}"]
        )

    def retrieve_similar_decisions(self, current_context_text, top_k=5):
        # Busca decisiones pasadas similares en la base vectorial
        query_embedding = self.encoder.encode(current_context_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results['documents'], results['metadatas']

    def generate_improved_strategy(self, current_context, similar_decisions):
        # Usa un LLM local (Ollama, Llama.cpp) o API para generar una recomendación mejorada
        # Basada en el contexto actual + decisiones pasadas similares
        prompt = f"""
        Eres un asesor financiero experto. Basado en el contexto actual y decisiones pasadas similares, 
        genera una recomendación de inversión mejorada.

        Contexto actual: {current_context}
        Decisiones pasadas similares: {similar_decisions}

        Recomendación mejorada:
        """
        # Aquí integrarías un LLM local (ej: Ollama con Llama 3) o una API
        improved_recommendation = call_local_llm(prompt)
        return improved_recommendation


def call_local_llm(prompt):
    # Placeholder para la integración con un LLM local
    # En una implementación real, aquí conectarías con Ollama, Llama.cpp, etc.
    return "Recomendación generada por LLM local"