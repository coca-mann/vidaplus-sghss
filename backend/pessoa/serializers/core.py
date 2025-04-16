from rest_framework import serializers
from backend.pessoa.models.core import Administrador


class AdministradorSerializer(serializers.ModelSerializer):


    class Meta:
        model = Administrador
        fields = '__all__'
