import os
from dotenv import load_dotenv
import google.generativeai as genai  # Adapter selon la lib utilisée

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_text(prompt):
    # Exemple d'appel à Gemini (adapter selon la doc officielle)
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    prompt = "Analyse le prix du Bitcoin sur les dernières 24h."
    print(analyze_text(prompt))