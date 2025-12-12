import requests
import json
from abc import ABC, abstractmethod

class BaseSummarizer(ABC):
    @abstractmethod
    def summarize(self, text: str) -> dict:
        """
        Summarizes the text into Introduction, Development, and Conclusion.
        Returns a dict with 'introduction', 'development', 'conclusion'.
        """
        pass

class OllamaSummarizer(BaseSummarizer):
    def __init__(self, model="llama3.2:3b", url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = url

    def summarize(self, text: str) -> dict:
        prompt = f"""
        Você é um assistente especialista em resumir notícias.
        Sua tarefa é ler o texto abaixo e criar um resumo estruturado em 3 partes: Introdução, Desenvolvimento e Conclusão.
        
        Regras RÍGIDAS:
        1. Cada parte deve ter NO MÁXIMO 144 caracteres.
        2. Seja fiel ao texto original.
        3. A saída deve ser APENAS um JSON válido no seguinte formato:
        {{
            "introduction": "Texto da introdução...",
            "development": "Texto do desenvolvimento...",
            "conclusion": "Texto da conclusão...",
            "tiktok_summary": "Resumo de 1 parágrafo engajante para o TikTok aqui. (Pule uma linha) #hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5"
        }}

        Texto da notícia:
        {text[:4000]} 
        """
        # Truncate text to avoid token limits if necessary, though 4000 chars is usually fine.

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }

        try:
            response = requests.post(self.url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return json.loads(result['response'])
        except Exception as e:
            print(f"Error generating summary: {e}")
            return {
                "introduction": "Erro ao gerar resumo.",
                "development": str(e),
                "conclusion": "Verifique se o Ollama está rodando."
            }
