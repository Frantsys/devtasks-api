from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import TeamFilter, TeamMemberFilter
from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamWriteSerializer, TeamMemberSerializer

CACHE_TTL = 60 * 5  # 5 minutos


@extend_schema_view(
    list=extend_schema(
        summary="Listar equipes",
        description="Retorna a lista paginada de equipes. Suporta busca por `search` e filtro por `sector`.",
        tags=["teams"],
        parameters=[
            OpenApiParameter("search", description="Busca por setor", required=False, type=str),
            OpenApiParameter("sector", description="Filtrar por setor (icontains)", required=False, type=str),
        ],
    ),
    retrieve=extend_schema(summary="Detalhar equipe", tags=["teams"]),
    create=extend_schema(summary="Criar equipe", tags=["teams"]),
    update=extend_schema(summary="Atualizar equipe (PUT)", tags=["teams"]),
    partial_update=extend_schema(summary="Atualizar equipe (PATCH)", tags=["teams"]),
    destroy=extend_schema(summary="Deletar equipe (soft delete)", tags=["teams"]),
)
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.filter(is_deleted=False).prefetch_related("members__user")
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TeamFilter
    search_fields = ["sector"]
    ordering_fields = ["sector", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TeamWriteSerializer
        return TeamSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Equipe deletada com sucesso (soft delete)."},
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema_view(
    list=extend_schema(
        summary="Listar membros de equipes",
        description="Retorna membros. Filtre por `team` (UUID) e/ou `user` (UUID).",
        tags=["team-members"],
        parameters=[
            OpenApiParameter("team", description="UUID da equipe", required=False, type=str),
            OpenApiParameter("user", description="UUID do usuário", required=False, type=str),
            OpenApiParameter("role", description="Filtrar por papel (icontains)", required=False, type=str),
        ],
    ),
    retrieve=extend_schema(summary="Detalhar membro", tags=["team-members"]),
    create=extend_schema(summary="Adicionar membro à equipe", tags=["team-members"]),
    update=extend_schema(summary="Atualizar membro (PUT)", tags=["team-members"]),
    partial_update=extend_schema(summary="Atualizar membro (PATCH)", tags=["team-members"]),
    destroy=extend_schema(summary="Remover membro (soft delete)", tags=["team-members"]),
)
class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.filter(is_deleted=False).select_related("user", "team")
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TeamMemberFilter
    search_fields = ["user__username", "user__email", "role"]
    ordering_fields = ["role", "created_at"]
    ordering = ["-created_at"]

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Membro removido com sucesso (soft delete)."},
            status=status.HTTP_204_NO_CONTENT,
        )
