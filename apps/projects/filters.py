import django_filters
from .models import Sprint, Project, SprintStatusChoices, ProjectStatusChoices


class SprintFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=SprintStatusChoices.choices)
    title = django_filters.CharFilter(lookup_expr="icontains")
    start_date_after = django_filters.DateFilter(field_name="start_date", lookup_expr="gte")
    start_date_before = django_filters.DateFilter(field_name="start_date", lookup_expr="lte")
    end_date_after = django_filters.DateFilter(field_name="end_date", lookup_expr="gte")
    end_date_before = django_filters.DateFilter(field_name="end_date", lookup_expr="lte")

    class Meta:
        model = Sprint
        fields = ["status", "title", "start_date_after", "start_date_before", "end_date_after", "end_date_before"]


class ProjectFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=ProjectStatusChoices.choices)
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Project
        fields = ["status", "title"]
