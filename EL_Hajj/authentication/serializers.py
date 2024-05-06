from rest_framework import serializers
from .models import user


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = [ 'email', 'password', 'last_login', 'is_email_verified', 'code', 'first_name', 'last_name', 'phone', 'dateOfBirth','province', 'gender', 'nombreInscription', 'role', 'winner', 'winning_date', 'personal_picture']
