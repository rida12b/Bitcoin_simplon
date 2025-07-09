from django.shortcuts import render
import requests
import logging  # ## AJOUT ##

# ## AJOUT ## : Initialisation du logger pour ce module.
# C'est une bonne pratique de nommer le logger avec __name__.
logger = logging.getLogger(__name__)

# L'adresse de notre API FastAPI.
API_BASE_URL = "http://127.0.0.1:8001"

def news_list(request):
    """
    Cette vue récupère toutes les données de l'API FastAPI
    pour les afficher sur un tableau de bord.
    """
    # ## AJOUT ## : Log de la requête entrante.
    logger.info(f"Requête reçue pour le tableau de bord depuis l'IP : {request.META.get('REMOTE_ADDR')}")

    context = {
        'news_list': [],
        'price_history': [],
        'price_analysis': "Analyse non disponible.",
        'error_message': None
    }

    try:
        # --- 1. Récupérer les nouvelles ---
        news_url = f"{API_BASE_URL}/latest-news?limit=5"
        logger.info(f"Début de l'appel API vers : {news_url}") # ## AJOUT ##
        news_response = requests.get(news_url, timeout=5) # Ajout d'un timeout
        news_response.raise_for_status()
        context['news_list'] = news_response.json()
        logger.info(f"Succès : {len(context['news_list'])} actualités récupérées.") # ## AJOUT ##

        # --- 2. Récupérer l'historique des prix ---
        history_url = f"{API_BASE_URL}/price-history?limit=24"
        logger.info(f"Début de l'appel API vers : {history_url}") # ## AJOUT ##
        history_response = requests.get(history_url, timeout=5)
        history_response.raise_for_status()
        context['price_history'] = history_response.json()
        logger.info(f"Succès : {len(context['price_history'])} points d'historique récupérés.") # ## AJOUT ##

        # --- 3. Récupérer l'analyse de l'IA ---
        analysis_url = f"{API_BASE_URL}/price-analysis"
        logger.info(f"Début de l'appel API vers : {analysis_url}") # ## AJOUT ##
        analysis_response = requests.get(analysis_url, timeout=15) # Timeout plus long pour l'IA
        analysis_response.raise_for_status()
        context['price_analysis'] = analysis_response.json().get('analysis', "Format d'analyse inattendu.")
        logger.info("Succès : Analyse de l'IA récupérée.") # ## AJOUT ##

    except requests.exceptions.RequestException as e:
        # Si un seul des appels échoue, on affiche un message d'erreur global
        error_message = f"Erreur de communication avec l'API backend : {e}"
        logger.error(error_message, exc_info=True) # ## AJOUT ## : exc_info=True ajoute la stack trace
        context['error_message'] = "Le service d'analyse est actuellement indisponible. Veuillez réessayer plus tard."

    # On "rend" le template HTML en lui passant toutes les données
    return render(request, 'viewer/news_list.html', context)