import django_filters
from .models import Team, TeamMember


class TeamFilter(django_filters.FilterSet):
    sector = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Team
        fields = ["sector"]


class TeamMemberFilter(django_filters.FilterSet):
    team = django_filters.UUIDFilter(field_name="team__id")
    user = django_filters.UUIDFilter(field_name="user__id")
    role = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = TeamMember
        fields = ["team", "user", "role"]
