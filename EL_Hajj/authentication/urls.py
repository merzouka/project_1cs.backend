from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login_user,name='login'),
    path('signup',views.register),
    path('email',views.email_existance_verification),
    path('activate-user/<uidb64>/<token>',
         views.activate_user, name='activate'),
    path('logout',views.logout_user,name='logout')
]
