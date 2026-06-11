import django_filters
from .models import Task, PriorityChoices, StatusChoices


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=StatusChoices.choices)
    priority = django_filters.ChoiceFilter(choices=PriorityChoices.choices)
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ["status", "priority", "title"]
