from django.urls import path
from .views import fetch_winners, registration,associate_tirage_with_baladiyas,baladiya_ids_by_utilisateur
from . import views
urlpatterns = [
    path('registration', registration, name='registration'),
    path('baladiya-ids/<int:utilisateur_id>', baladiya_ids_by_utilisateur, name='baladiya_ids_by_utilisateur'),
    path('associate-tirage', associate_tirage_with_baladiyas, name='associate_tirage_with_baladiyas'),
    path('fetch-winners/<int:id_utilisateur>/', fetch_winners, name='fetch_winners'),

]
