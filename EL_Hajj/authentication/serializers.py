from rest_framework import serializers
from .models import elHadj


class elHadjSerializer(serializers.ModelSerializer):
    class Meta :
        model = elHadj
        fields = '__all__'
    