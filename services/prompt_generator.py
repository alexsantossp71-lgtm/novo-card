import requests
import json

class OllamaPromptGenerator:
    def __init__(self, model="llama3.2:3b", url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = url

    def generate_prompts(self, summary_data: dict) -> dict:
        """
        Generates 4 image prompts (general, intro, dev, conc).
        """
        
        # Construct a prompt for the LLM
        prompt_text = f"""
        act as an expert prompt engineer for Generative AI (Stable Diffusion XL).
        
        Based on the news summary below (which is in Portuguese), create 4 high-quality image prompts in ENGLISH.
        
        Target Style: "Graphic Novel illustration by Gibrat"
        
        CRITICAL RULES:
        1. OUTPUT MUST BE IN ENGLISH ONLY.
        2. KEEP PROMPTS CONCISE (Max 25 words each). Avoid filler words.
        3. For public figures (like Lula, Trump), ADD VISUAL TRAITS manually (e.g., "Lula" -> "an older man with white beard and curly gray hair"; "Trump" -> "an older man with blond hair and blue tie"). This is crucial !!
        4. FOCUS on the visual action and setting.
        5. Output MUST be valid JSON.
        
        Summary to visualize:
        1. Intro: {summary_data.get('introduction', '')}
        2. Dev: {summary_data.get('development', '')}
        3. Conc: {summary_data.get('conclusion', '')}
        
        JSON Output Format:
        {{
            "general_summary": "Concise English prompt...",
            "introduction": "Concise English prompt...",
            "development": "Concise English prompt...",
            "conclusion": "Concise English prompt..."
        }}
        """

        payload = {
            "model": self.model,
            "prompt": prompt_text,
            "stream": False,
            "format": "json"
        }

        try:
            response = requests.post(self.url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return json.loads(result['response'])
        except Exception as e:
            print(f"Error generating prompts: {e}")
            return {
                "general_summary": "Error",
                "introduction": "Error",
                "development": "Error",
                "conclusion": "Error"
            }
