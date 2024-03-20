from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login_user,name='login'),
    path('register',views.register),
    path('verification-email', views.send_verification_email),
    path("reset-password-email", views.send_reset_password_email),
    path("reset-password", views.reset_password),
    path('logout',views.logout_user,name='logout'),
    path("", views.default),
]
