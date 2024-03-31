from django.contrib import admin
from .models import Haaj


@admin.register(Haaj)
class HaajAdmin(admin.ModelAdmin):
    list_display = [ 'first_name_arabic', 'last_name_arabic', 'NIN']  
    search_fields = [ 'first_name_arabic', 'last_name_arabic', 'NIN']  
