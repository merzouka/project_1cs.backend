from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.SerializerMethodField("get_alternate_first_name")
    lastName = serializers.SerializerMethodField("get_alternate_last_name")
    class Meta :
        model = User
        exclude = ["password", "is_email_verified", "code", "last_login", "first_name", "last_name"]
    def get_alternate_first_name(self, obj):
        return obj.first_name

    def get_alternate_last_name(self, obj):
        return obj.last_name
