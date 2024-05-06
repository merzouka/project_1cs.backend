from django.urls import path
from .views import check_tirage_definition, fetch_winners, participants_tirage, registration,associate_tirage_with_baladiyas,baladiya_names_by_utilisateur, tirage_fini
from . import views
urlpatterns = [
    path('registration', registration, name='registration'),
    path('fetch-winners/<int:id_utilisateur>/', fetch_winners, name='fetch_winners'),
    path('baladiya_names_by_utilisateur/<int:utilisateur_id>/', baladiya_names_by_utilisateur, name='baladiya_names_by_utilisateur'),
    path('associate-tirage', associate_tirage_with_baladiyas, name='associate_tirage_with_baladiyas'),
    path('participants_tirage/<int:utilisateur_id>/', participants_tirage, name='participants_tirage'),
    path('check-tirage/<int:utilisateur_id>/', check_tirage_definition, name='check_tirage_definition'),
    path('tirage_fini/<int:utilisateur_id>/', tirage_fini, name='tirage_fini'),


]
