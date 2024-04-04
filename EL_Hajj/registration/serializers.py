from rest_framework import serializers
from .models import Haaj , Haaja
from django.utils import timezone
from authentication.models import utilisateur 


class HaajSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Haaj
        fields = ['__all__']

    def create(self, validated_data):
        return Haaj.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update Haaj instance with additional data
        instance.first_name_arabic = validated_data.get('first_name_arabic', instance.first_name_arabic)
        instance.last_name_arabic = validated_data.get('last_name_arabic', instance.last_name_arabic)
        instance.mother_name = validated_data.get('mother_name', instance.mother_name)
        instance.father_name = validated_data.get('father_name', instance.father_name)
        instance.NIN = validated_data.get('NIN', instance.NIN)
        instance.card_expiration_date = validated_data.get('card_expiration_date', instance.card_expiration_date)
        instance.passport_id = validated_data.get('passport_id', instance.passport_id)
        instance.passport_expiration_date = validated_data.get('passport_expiration_date', instance.passport_expiration_date)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.personal_picture = validated_data.get('personal_picture', instance.personal_picture)
        instance.save()
        return instance
        
    def validate_card_expiration_date(self, value):
        current_date = timezone.now().date()
        if value < current_date  + timezone.timedelta(days=180):  
            raise serializers.ValidationError("The card expiration date must be at least six months in the future.")
        return value

    def validate_passport_expiration_date(self, value):
        current_date = timezone.now().date()
        if value < current_date + timezone.timedelta(days=180):
            raise serializers.ValidationError("The passport expiration date must be at least six months in the future.")
        return value
    

        
        
        