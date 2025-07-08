# viewer/urls.py
from django.urls import path
from . import views  # Le '.' signifie 'depuis le dossier actuel'

urlpatterns = [
    # Cette ligne dit : "Pour une URL vide (la racine),
    # exécute la fonction 'news_list' qui se trouve dans 'views.py'".
    path('', views.news_list, name='news_list'),
]