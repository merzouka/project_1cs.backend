from django.urls import path
from .views import check_tirage_definition, fetch_winners, participants_tirage, registration,associate_tirage_with_baladiyas,baladiya_names_by_utilisateur
from . import views
urlpatterns = [
    path('registration', registration, name='registration'),
    path('fetch-winners/', fetch_winners, name='fetch_winners'),
    path('baladiya_names_by_utilisateur/', baladiya_names_by_utilisateur, name='baladiya_names_by_utilisateur'),
    path('associate-tirage', associate_tirage_with_baladiyas, name='associate_tirage_with_baladiyas'),
    path('participants_tirage/', participants_tirage, name='participants_tirage'),
    path('check-tirage/', check_tirage_definition, name='check_tirage_definition'),


]
