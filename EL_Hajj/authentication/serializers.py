from rest_framework import serializers
from .models import user,role



class userSerializer(serializers.ModelSerializer):
    class Meta :
        model = user
        fields = ['email','password','dateOfBirth','gender','phone','first_name','last_name','city','province']
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = role
        fields = '__all__'
        

