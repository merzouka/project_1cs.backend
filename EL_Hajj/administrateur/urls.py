from django.urls import path
from . import views
from .views import associate_winner_vol_hotel

urlpatterns = [
    path('users',views.user_list),
    path('user/privilege',views.role_baladiyet_assignement),
    path("administrateur/add-vole",views.add_vol),
    path("administrateur/add-hotel",views.add_hotel),
    path("administrateur/associate-vol-hotel-hedj",associate_winner_vol_hotel),
    path("administrateur/winners-list",views.winners_list),
    path("administrateur/delete-vol-hotel-association",views.delete_vol_hotel_association),
    path("administrateur/winners-list-vol-hotel",views.winners_hotel_vol),
    path("administrateur/hotels-list",views.list_hotel),
    path("administrateur/voles-list",views.list_vole),
]
