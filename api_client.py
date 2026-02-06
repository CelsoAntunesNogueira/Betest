from config import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL
import json
import requests

def enviar_para_groq(prompt):
        """Envia o prompt para a API do Groq"""
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 2048,
            "top_p": 1
        }
        
        try:
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"Erro {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"Erro ao conectar: {str(e)}"
    
def formatar_json( texto):
    """Tenta formatar o texto como JSON"""
    try:
        # Tenta encontrar JSON no texto
        inicio = texto.find('{')
        fim = texto.rfind('}') + 1
        if inicio != -1 and fim > inicio:
            json_str = texto[inicio:fim]
            obj = json.loads(json_str)
            return json.dumps(obj, indent=2, ensure_ascii=False)
        return texto
    except:
        return texto
