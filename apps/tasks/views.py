from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import TaskFilter
from .models import Task
from .serializers import TaskSerializer

CACHE_TTL = 60 * 5  # 5 minutos


@extend_schema_view(
    list=extend_schema(
        summary="Listar tarefas",
        description=(
            "Retorna a lista paginada de tarefas ativas. "
            "Suporta busca por `search` e filtros por `status` e `priority`."
        ),
        tags=["tasks"],
        parameters=[
            OpenApiParameter("search", description="Busca por título ou descrição", required=False, type=str),
            OpenApiParameter("status", description="Filtrar por status (not_started | in_progress | done)", required=False, type=str),
            OpenApiParameter("priority", description="Filtrar por prioridade (low | medium | high)", required=False, type=str),
        ],
    ),
    retrieve=extend_schema(summary="Detalhar tarefa", tags=["tasks"]),
    create=extend_schema(summary="Criar tarefa", tags=["tasks"]),
    update=extend_schema(summary="Atualizar tarefa (PUT)", tags=["tasks"]),
    partial_update=extend_schema(summary="Atualizar tarefa (PATCH)", tags=["tasks"]),
    destroy=extend_schema(summary="Deletar tarefa (soft delete)", tags=["tasks"]),
)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["title", "priority", "status", "created_at"]
    ordering = ["-created_at"]

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Tarefa deletada com sucesso (soft delete)."},
            status=status.HTTP_204_NO_CONTENT,
        )
