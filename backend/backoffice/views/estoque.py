from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
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
@extend_schema_view(
    list=extend_schema(
        summary="Listar estoque de suprimentos",
        description="Lista todos os registros de estoque de suprimentos por local e suprimento."
    ),
    retrieve=extend_schema(
        summary="Detalhar estoque de suprimento",
        description="Recupera os detalhes de um registro de estoque de suprimento específico."
    ),
    create=extend_schema(
        summary="Criar estoque de suprimento",
        description="Registra um novo estoque de suprimento para um local."
    ),
    destroy=extend_schema(
        summary="Remover estoque de suprimento",
        description="Remove um registro de estoque de suprimento do sistema."
    ),
)
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
@extend_schema_view(
    list=extend_schema(
        summary="Listar suprimentos",
        description="Lista todos os suprimentos cadastrados no sistema."
    ),
    retrieve=extend_schema(
        summary="Detalhar suprimento",
        description="Recupera os detalhes de um suprimento específico."
    ),
    create=extend_schema(
        summary="Criar suprimento",
        description="Cadastra um novo suprimento no sistema."
    ),
    update=extend_schema(
        summary="Atualizar suprimento",
        description="Atualiza todos os dados de um suprimento existente."
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de suprimento",
        description="Atualiza parcialmente os dados de um suprimento."
    ),
    destroy=extend_schema(
        summary="Remover suprimento",
        description="Remove um suprimento do sistema."
    ),
)
class SuprimentoViewSet(ModelViewSet):
    queryset = Suprimento.objects.all()
    serializer_class = SuprimeiroSerializer
    permission_classes = [IsAuthenticated, IsGestor]


@extend_schema(tags=['Estoque'])
@extend_schema_view(
    list=extend_schema(
        summary="Listar unidades de medida",
        description="Lista todas as unidades de medida cadastradas."
    ),
    retrieve=extend_schema(
        summary="Detalhar unidade de medida",
        description="Recupera os detalhes de uma unidade de medida específica."
    ),
    create=extend_schema(
        summary="Criar unidade de medida",
        description="Cadastra uma nova unidade de medida."
    ),
    update=extend_schema(
        summary="Atualizar unidade de medida",
        description="Atualiza todos os dados de uma unidade de medida existente."
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de unidade de medida",
        description="Atualiza parcialmente os dados de uma unidade de medida."
    ),
    destroy=extend_schema(
        summary="Remover unidade de medida",
        description="Remove uma unidade de medida do sistema."
    ),
)
class UnidadeMedidaViewSet(ModelViewSet):
    queryset = UnidadeMedida.objects.all()
    serializer_class = UnidadeMedidaSerializer
    permission_classes = [IsAuthenticated, IsGestor]


@extend_schema(tags=['Estoque'])
@extend_schema_view(
    list=extend_schema(
        summary="Listar movimentações de suprimento",
        description="Lista todas as movimentações de suprimento registradas no sistema."
    ),
    retrieve=extend_schema(
        summary="Detalhar movimentação de suprimento",
        description="Recupera os detalhes de uma movimentação de suprimento específica."
    ),
    create=extend_schema(
        summary="Registrar movimentação de suprimento",
        description="Registra uma nova movimentação (entrada, saída ou ajuste) de suprimento em um estoque."
    ),
    destroy=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
)
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
