from django.urls import path
from . import views 
from .views import DrawRegistrationView


urlpatterns = [
    path('draw-registration/', DrawRegistrationView.as_view(), name='draw_registration'),
]