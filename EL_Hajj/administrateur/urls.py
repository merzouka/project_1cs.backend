from django.urls import path
from . import views

urlpatterns = [
    path('administrateur/list',views.user_list),
    path('administrateur/search-user/<str:email>',views.search_user),
    path('administrateur/assigne-role-baladiyet/',views.role_baladiyet_assignement),
    path("administrateur/search-by-role-baladiya-wilaya",views.users_by_role_wilaya_baladiya),
    path("administrateur/delete-assignement/<int:user_id>",views.delete_baladiya_role_assignement)
]
