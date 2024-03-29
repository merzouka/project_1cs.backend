from rest_framework import serializers
from .models import CustomUser,utilisateur,role


class UtilisateurSerializer(serializers.ModelSerializer):
    firstName = serializers.SerializerMethodField("get_alternate_first_name")
    lastName = serializers.SerializerMethodField("get_alternate_last_name")
    class Meta :
        model = utilisateur
        fields = '__all__'
    def get_alternate_first_name(self, obj):
        return obj.first_name

    def get_alternate_last_name(self, obj):
        return obj.last_name
    
    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = role
        fields = '__all__'
        

class CustomUserSerializer(serializers.ModelSerializer):
    id_role = serializers.PrimaryKeyRelatedField(queryset=role.objects.all(), many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_email_verified', 'code', 'id_role']

    def create(self, validated_data):
        id_role_data = validated_data.pop('id_role')
        user = CustomUser.objects.create(**validated_data)
        for role in id_role_data:
            user.id_role.add(role)
        return user
        

        


