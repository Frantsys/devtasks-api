from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import SprintFilter, ProjectFilter
from .models import Sprint, Project
from .serializers import (
    SprintSerializer,
    SprintWriteSerializer,
    ProjectSerializer,
    ProjectWriteSerializer,
)

CACHE_TTL = 60 * 5  # 5 minutos


@extend_schema_view(
    list=extend_schema(
        summary="Listar sprints",
        description="Retorna a lista paginada de sprints. Filtre por `status`, intervalo de datas e busca por `search`.",
        tags=["sprints"],
        parameters=[
            OpenApiParameter("search", description="Busca por título ou descrição", required=False, type=str),
            OpenApiParameter("status", description="Filtrar por status (not_started | in_progress | done)", required=False, type=str),
            OpenApiParameter("start_date_after", description="Data início >= (YYYY-MM-DD)", required=False, type=str),
            OpenApiParameter("start_date_before", description="Data início <= (YYYY-MM-DD)", required=False, type=str),
            OpenApiParameter("end_date_after", description="Data fim >= (YYYY-MM-DD)", required=False, type=str),
            OpenApiParameter("end_date_before", description="Data fim <= (YYYY-MM-DD)", required=False, type=str),
        ],
    ),
    retrieve=extend_schema(summary="Detalhar sprint", tags=["sprints"]),
    create=extend_schema(summary="Criar sprint", tags=["sprints"]),
    update=extend_schema(summary="Atualizar sprint (PUT)", tags=["sprints"]),
    partial_update=extend_schema(summary="Atualizar sprint (PATCH)", tags=["sprints"]),
    destroy=extend_schema(summary="Deletar sprint (soft delete)", tags=["sprints"]),
)
class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.filter(is_deleted=False).prefetch_related("tasks")
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SprintFilter
    search_fields = ["title", "description"]
    ordering_fields = ["title", "status", "start_date", "end_date", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SprintWriteSerializer
        return SprintSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Sprint deletada com sucesso (soft delete)."},
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema_view(
    list=extend_schema(
        summary="Listar projetos",
        description="Retorna a lista paginada de projetos. Filtre por `status` e busca por `search`.",
        tags=["projects"],
        parameters=[
            OpenApiParameter("search", description="Busca por título ou descrição", required=False, type=str),
            OpenApiParameter("status", description="Filtrar por status (paused | active | done | closed)", required=False, type=str),
        ],
    ),
    retrieve=extend_schema(summary="Detalhar projeto", tags=["projects"]),
    create=extend_schema(summary="Criar projeto", tags=["projects"]),
    update=extend_schema(summary="Atualizar projeto (PUT)", tags=["projects"]),
    partial_update=extend_schema(summary="Atualizar projeto (PATCH)", tags=["projects"]),
    destroy=extend_schema(summary="Deletar projeto (soft delete)", tags=["projects"]),
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = (
        Project.objects.filter(is_deleted=False)
        .prefetch_related("sprints")
        .select_related("current_sprint")
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ["title", "description"]
    ordering_fields = ["title", "status", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProjectWriteSerializer
        return ProjectSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Projeto deletado com sucesso (soft delete)."},
            status=status.HTTP_204_NO_CONTENT,
        )
