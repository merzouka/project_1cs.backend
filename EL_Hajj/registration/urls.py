from django.urls import path
from .views import fetch_winners, registration,associate_tirage_with_baladiyas,baladiya_names_by_utilisateur
from . import views
urlpatterns = [
    path('registration', registration, name='registration'),
    path('fetch-winners/<int:id_utilisateur>/', fetch_winners, name='fetch_winners'),
    path('baladiya_names_by_utilisateur/<int:utilisateur_id>/', baladiya_names_by_utilisateur, name='baladiya_names_by_utilisateur'),
    path('associate-tirage', associate_tirage_with_baladiyas, name='associate_tirage_with_baladiyas'),
    

]
