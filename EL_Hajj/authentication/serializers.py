from rest_framework import serializers
from .models import user


class userSerializer(serializers.ModelSerializer):
    class Meta :
        model = user
        fields = ['email','password','dateOfBirth','gender','phone','first_name','last_name','city','province','role','is_email_verified']
