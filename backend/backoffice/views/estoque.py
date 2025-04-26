from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.db import transaction
from backend.backoffice.permissions import IsGestor
from backend.backoffice.models.estoque import (
    EstoqueSuprimento,
    Suprimento,
    UnidadeMedida,
    MovimentacaoSuprimento
)
from backend.backoffice.serializers.estoque import (
    EstoqueSuprimeiroSerializer,
    SuprimeiroSerializer,
    UnidadeMedidaSerializer,
    MovimentacaoSuprimentoSerializer
)

'''
ESTOQUE E SUPRIMENTO
- Somente administradores do tipo GESTOR podem criar, editar e excluir dados
- Médicos e pacientes não podem ver essas informações
'''

@extend_schema(tags=['Estoque'])
class EstoqueSuprimentoViewSet(ModelViewSet):
    queryset = EstoqueSuprimento.objects.all()
    serializer_class = EstoqueSuprimeiroSerializer
    permission_classes = [IsAuthenticated, IsGestor]

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Método não permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Método não permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(tags=['Estoque'])
class SuprimentoViewSet(ModelViewSet):
    queryset = Suprimento.objects.all()
    serializer_class = SuprimeiroSerializer
    permission_classes = [IsAuthenticated, IsGestor]


@extend_schema(tags=['Estoque'])
class UnidadeMedidaViewSet(ModelViewSet):
    queryset = UnidadeMedida.objects.all()
    serializer_class = UnidadeMedidaSerializer
    permission_classes = [IsAuthenticated, IsGestor]


@extend_schema(tags=['Estoque'])
class MovimentacaoSuprimentoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = MovimentacaoSuprimento.objects.all()
    serializer_class = MovimentacaoSuprimentoSerializer
    permission_classes = [IsAuthenticated, IsGestor]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        id_suprimento = data['idSuprimento'].idSuprimento
        id_local = data['idLocal'].idLocal
        quantidade = data['quantidade']
        tipo = data['tipoMovimentacao']

        try:
            estoque = EstoqueSuprimento.objects.select_for_update().get(
                idSuprimento=id_suprimento,
                idLocal=id_local
            )
        except EstoqueSuprimento.DoesNotExist:
            return Response(
                {'detail': 'Estoque não encontrado para o suprimento/local informado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if tipo == 'ENTR':
            estoque.quantidadeAtual += quantidade
        elif tipo == 'SAID':
            if estoque.quantidadeAtual < quantidade:
                return Response({'detail': 'Quantidade insuficiente em estoque.'},
                                status=status.HTTP_400_BAD_REQUEST)
            estoque.quantidadeAtual -= quantidade
        elif tipo == 'AJUS':
            estoque.quantidadeAtual = quantidade
        else:
            return Response(
                {'detail': 'Tipo de movimentação inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        estoque.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Método não permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Método não permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response({'detail': 'Método não permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
