import django_filters
from .models import User, GroupChoices


class UserFilter(django_filters.FilterSet):
    group = django_filters.ChoiceFilter(choices=GroupChoices.choices)
    is_active = django_filters.BooleanFilter()
    email = django_filters.CharFilter(lookup_expr="icontains")
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ["group", "is_active", "email", "username"]
