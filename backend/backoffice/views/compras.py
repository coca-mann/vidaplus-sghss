from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, inline_serializer, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from backend.backoffice.models.compras import (
    Fornecedor,
    ItemPedidoCompra,
    PedidoCompra,
    STATUS_PEDIDO
)
from backend.backoffice.serializers.compras import (
    FornecedorSerializer,
    ItemPedidoSerializer,
    PedidoCompraSerializer
)
from backend.backoffice.permissions import IsAdminOrManager

'''
FORNECEDOR E PEDIDO COMPRA
- Somente administradores do tipo DIRFINAN, DIRGERAL, DIRADMIN e GESTOR podem ver, editar e excluir dados.
- Pacientes e médicos não pode ver essas informações
'''
@extend_schema(tags=['Fornecedores'])
@extend_schema_view(
    list=extend_schema(
        summary="Listar fornecedores",
        description="Lista todos os fornecedores cadastrados."
    ),
    retrieve=extend_schema(
        summary="Detalhar fornecedor",
        description="Recupera os detalhes de um fornecedor específico."
    ),
    create=extend_schema(
        summary="Criar fornecedor",
        description="Cadastra um novo fornecedor."
    ),
    update=extend_schema(
        summary="Atualizar fornecedor",
        description="Atualiza todos os dados de um fornecedor existente."
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de fornecedor",
        description="Atualiza parcialmente os dados de um fornecedor."
    ),
    destroy=extend_schema(
        summary="Remover fornecedor",
        description="Remove um fornecedor do sistema."
    ),
)
class FornecedorViewSet(ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def perform_create(self, serializer):
        serializer.save()

    @extend_schema(
            description="Retorna apenas fornecedores marcados como ativos no sistema.",
            summary="Listar fornecedores ativos",
            responses={200, FornecedorSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        fornecedores = self.get_queryset().filter(ativo=True)
        page = self.paginate_queryset(fornecedores)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(fornecedores, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Compras'])
@extend_schema_view(
    list=extend_schema(
        summary="Listar itens de pedido",
        description="Lista todos os itens de pedido cadastrados."
    ),
    retrieve=extend_schema(
        summary="Detalhar item de pedido",
        description="Recupera os detalhes de um item de pedido específico."
    ),
    create=extend_schema(
        summary="Criar item de pedido",
        description="Adiciona um novo item a um pedido de compra."
    ),
    update=extend_schema(
        summary="Atualizar item de pedido",
        description="Atualiza todos os dados de um item de pedido existente."
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de item de pedido",
        description="Atualiza parcialmente os dados de um item de pedido."
    ),
    destroy=extend_schema(
        summary="Remover item de pedido",
        description="Remove um item de pedido do sistema."
    ),
)
class ItemPedidoViewSet(ModelViewSet):
    queryset = ItemPedidoCompra.objects.all()
    serializer_class = ItemPedidoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def perform_create(self, serializer):
        item = serializer.save()
        self._atualizar_valor_total_pedido(item.idPedido)

    def perform_update(self, serializer):
        item = serializer.save()
        self._atualizar_valor_total_pedido(item.idPedido)

    def perform_destroy(self, instance):
        pedido = instance.idPedido
        instance.delete()
        self._atualizar_valor_total_pedido(pedido)

    def _atualizar_valor_total_pedido(self, pedido):
        itens = ItemPedidoCompra.objects.filter(idPedido=pedido)
        total = sum(item.valorUnitario * item.quantidade for item in itens)
        pedido.valorTotal = total
        pedido.save()

    @extend_schema(
            summary="Listar itens por pedido",
            description="Retorna todos os itens associados a um pedido específico.",
            request=inline_serializer(
                name="PedidoIdRequest",
                fields={
                    'idPedido': serializers.IntegerField(help_text="ID do pedido para filtrar itens")
                }
            ),
            responses={
                200: ItemPedidoSerializer(many=True),
                400: OpenApiResponse(description="Erro: ID do pedido não fornecido")
            },
            examples=[
                OpenApiExample(
                    name="Exemplo de requisição",
                    value={"idPedido": 1},
                    request_only=True,
                    summary="Dados para filtro de itens por pedido"
                )
            ]
    )
    @action(detail=False, methods=['get'])
    def por_pedido(self, request):
        idPedido = request.data.get('idPedido')
        if not idPedido:
            return Response(
                {'detail': 'É necessário informar a chave idPedido no corpo da requisição.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        itens = self.get_queryset().filter(idPedido=idPedido)
        serializer = self.get_serializer(itens, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Compras'])
@extend_schema_view(
    list=extend_schema(
        summary="Listar pedidos de compra",
        description="Lista todos os pedidos de compra cadastrados."
    ),
    retrieve=extend_schema(
        summary="Detalhar pedido de compra",
        description="Recupera os detalhes de um pedido de compra específico."
    ),
    create=extend_schema(
        summary="Criar pedido de compra",
        description="Cadastra um novo pedido de compra."
    ),
    update=extend_schema(
        summary="Atualizar pedido de compra",
        description="Atualiza todos os dados de um pedido de compra existente."
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de pedido de compra",
        description="Atualiza parcialmente os dados de um pedido de compra."
    ),
    destroy=extend_schema(
        summary="Remover pedido de compra",
        description="Remove um pedido de compra do sistema."
    ),
)
class PedidoCompraViewSet(ModelViewSet):
    queryset = PedidoCompra.objects.all()
    serializer_class = PedidoCompraSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def perform_create(self, serializer):
        serializer.save()

    @extend_schema(
        summary="Alterar status do pedido",
        description="Atualiza o status de um pedido de compra",
        request=inline_serializer(
            name='AlterarStatusRequest',
            fields={
                'status': serializers.ChoiceField(
                    choices=STATUS_PEDIDO,
                    help_text="Novo status para o pedido"
                )
            }
        ),
        responses={
            200: PedidoCompraSerializer,
            400: OpenApiResponse(description="Erro: Status inválido")
        },
        examples=[
            OpenApiExample(
                name="Exemplo de alteração de status",
                value={"status": "ENVI"},
                request_only=True,
                summary="Alterar para status 'Enviado'"
            )
        ]
    )
    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        pedido = self.get_object()
        novo_status = request.data.get('status')

        if not novo_status or novo_status not in dict(STATUS_PEDIDO).keys():
            return Response(
                {'error': 'Status inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pedido.status = novo_status
        pedido.save()

        serializer = self.get_serializer(pedido)
        return Response(serializer.data)

    @extend_schema(
        summary="Listar itens do pedido",
        description="Retorna todos os itens associados a um pedido específico",
        responses={200: ItemPedidoSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def itens(self, request, pk=None):
        pedido = self.get_object()
        itens =ItemPedidoCompra.objects.filter(idPedido=pedido)

        serializer = ItemPedidoSerializer(itens, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Filtrar pedidos por status",
        description="Retorna pedidos com um status específico",
        parameters=[
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Status do pedido (ABER, ENVI, RECE, CANC)",
                required=True,
                enum=[status[0] for status in STATUS_PEDIDO]
            )
        ],
        responses={
            200: PedidoCompraSerializer(many=True),
            400: OpenApiResponse(description="Erro: Status não fornecido")
        }
    )
    @action(detail=False, methods=['get'])
    def por_status(self, request):
        status_pedido = request.data.get('status')

        if not status_pedido:
            return Response(
                {'error': 'É necessário informar o status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pedidos = self.get_queryset().filter(status=status_pedido)
        page = self.paginate_queryset(pedidos)
        if page is None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(pedidos, many=True)
        return Response(serializer.data)
