from django.urls import path
from . import views
from .views import associate_winner_vol_hotel

urlpatterns = [
    path('administrateur/list',views.user_list),
    path('administrateur/search-user/<str:email>',views.search_user),
    path('administrateur/assigne-role-baladiyet',views.role_baladiyet_assignement),
    path("administrateur/search-role-wilaya",views.users_role_wilaya),
    path("administrateur/delete-assignement",views.delete_baladiya_role_assignement),
    path("administrateur/add-vole",views.add_vol),
    path("administrateur/add-hotel",views.add_hotel),
    path("administrateur/associate-vol-hotel-hedj",associate_winner_vol_hotel),
    path("administrateur/responsable_users",views.responsable_users),
    path("administrateur/winners-list",views.winners_list),
    path("administrateur/delete-vol-hotel-association",views.delete_vol_hotel_association),
    path("administrateur/winners-list-vol-hotel",views.winners_hotel_vol),
    path("administrateur/hotels-list",views.list_hotel),
    path("administrateur/voles-list",views.list_vole),
]
