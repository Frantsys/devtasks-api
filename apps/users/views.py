from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .filters import UserFilter
from .models import User
from .serializers import UserSerializer, UserReadSerializer

CACHE_TTL = 60 * 5  # 5 minutos


@extend_schema_view(
    list=extend_schema(
        summary="Listar usuários",
        description="Retorna a lista paginada de usuários ativos. Suporta busca por `search` e filtro por `group`.",
        tags=["users"],
        parameters=[
            OpenApiParameter("search", description="Busca por username ou email", required=False, type=str),
            OpenApiParameter("group", description="Filtrar por grupo (funcionario | supervisor)", required=False, type=str),
        ],
    ),
    retrieve=extend_schema(summary="Detalhar usuário", tags=["users"]),
    create=extend_schema(summary="Criar usuário", tags=["users"]),
    update=extend_schema(summary="Atualizar usuário (PUT)", tags=["users"]),
    partial_update=extend_schema(summary="Atualizar usuário (PATCH)", tags=["users"]),
    destroy=extend_schema(summary="Deletar usuário (soft delete)", tags=["users"]),
    me=extend_schema(summary="Dados do usuário autenticado", tags=["users"]),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UserFilter
    search_fields = ["username", "email"]
    ordering_fields = ["username", "email", "created_at", "group"]
    ordering = ["-date_joined"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return UserReadSerializer
        return UserSerializer

    def get_permissions(self):
        # Cadastro de novo usuário é público
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Usuário deletado com sucesso (soft delete)."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserReadSerializer(request.user)
        return Response(serializer.data)
