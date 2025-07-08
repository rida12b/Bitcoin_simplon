
from django.shortcuts import render
import requests # La bibliothèque pour faire des appels HTTP

# L'adresse de notre API FastAPI.
# Pour l'instant, on la met en dur. On suppose qu'elle tourne sur le port 8000.
API_BASE_URL = "http://127.0.0.1:8001"

def news_list(request):
    """
    Cette vue récupère toutes les données de l'API FastAPI
    pour les afficher sur un tableau de bord.
    """
    # Dictionnaire pour stocker toutes nos données
    context = {
        'news_list': [],
        'price_history': [],
        'price_analysis': "Analyse non disponible.",
        'error_message': None
    }

    try:
        # --- 1. Récupérer les nouvelles ---
        news_response = requests.get(f"{API_BASE_URL}/latest-news?limit=5")
        news_response.raise_for_status()
        context['news_list'] = news_response.json()

        # --- 2. Récupérer l'historique des prix ---
        history_response = requests.get(f"{API_BASE_URL}/price-history?limit=24")
        history_response.raise_for_status()
        context['price_history'] = history_response.json()

        # --- 3. Récupérer l'analyse de l'IA ---
        analysis_response = requests.get(f"{API_BASE_URL}/price-analysis")
        analysis_response.raise_for_status()
        # La réponse est un dictionnaire {"analysis": "..."}
        context['price_analysis'] = analysis_response.json().get('analysis', "Format d'analyse inattendu.")

    except requests.exceptions.RequestException as e:
        # Si un seul des appels échoue, on affiche un message d'erreur global
        context['error_message'] = f"Erreur de connexion à l'API : {e}"

    # On "rend" le template HTML en lui passant toutes les données
    return render(request, 'viewer/news_list.html', context)