from rest_framework import serializers
from backend.local.models import Local


class LocalSerializer(serializers.ModelSerializer):


    class Meta:
        model = Local
        fields = '__all__'
