from rest_framework import serializers
from .models import Haaj 
from django.utils import timezone
from authentication.models import utilisateur

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = utilisateur
        fields = ['first_name', 'last_name', 'emailUtilisateur', 'dateOfBirth', 'province', 'city', 'gender']
        read_only_fields = fields

class HaajSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    personal_picture = serializers.ImageField(max_length=None, use_url=True)

    def validate_card_expiration_date(self, value):
        if value < timezone.now() + timezone.timedelta(days=180):  
            raise serializers.ValidationError("The card expiration date must be at least six months in the future.")
        return value

    def validate_passport_expiration_date(self, value):
        if value < timezone.now() + timezone.timedelta(days=180):
            raise serializers.ValidationError("The passport expiration date must be at least six months in the future.")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = utilisateur.objects.create(**user_data)
        haaj = Haaj.objects.create(user=user, **validated_data)
        return haaj

    class Meta:
        model = Haaj
        fields = '__all__'