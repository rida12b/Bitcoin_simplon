import pytest
from unittest.mock import patch, MagicMock
from scripts.llm_analyzer import analyze_text

# Objectif : Tester notre fonction `analyze_text` SANS appeler l'API Google Gemini.
# On utilise un "patch" pour intercepter et simuler l'appel à la bibliothèque genai.

@patch('scripts.llm_analyzer.genai.GenerativeModel')
def test_analyze_text_with_mock(mock_generative_model):
    """
    Vérifie que notre fonction `analyze_text` appelle bien le modèle
    et retourne le texte de la réponse simulée.
    """
    # --- 1. Préparation (Arrange) ---
    # On définit ce que la réponse simulée (le "mock") doit retourner.
    fake_response_text = "Ceci est une analyse simulée réussie."
    
    # On configure notre objet simulé pour qu'il se comporte comme le vrai objet genai
    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.return_value.text = fake_response_text
    mock_generative_model.return_value = mock_model_instance

    prompt_test = "Ceci est un prompt de test."

    # --- 2. Action (Act) ---
    # On appelle notre fonction. Le @patch va intercepter l'appel à genai.
    result = analyze_text(prompt_test)

    # --- 3. Vérification (Assert) ---
    # On vérifie que le modèle simulé a bien été appelé avec notre prompt.
    mock_model_instance.generate_content.assert_called_once_with(prompt_test)
    
    # On vérifie que le résultat de notre fonction est bien celui qu'on a simulé.
    assert result == fake_response_text
    print("\n✅ Test de `analyze_text` avec mock réussi !")