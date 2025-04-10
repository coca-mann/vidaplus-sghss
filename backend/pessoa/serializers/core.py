from rest_framework import serializers
from backend.pessoa.models.core import Administrador, Pessoa


class AdministradorSerializer(serializers.ModelSerializer):


    class Meta:
        model = Administrador
        fields = '__all__'


class PessoaSerializer(serializers.ModelSerializer):


    class Meta:
        model = Pessoa
        fields = '__all__'
