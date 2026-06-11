from django.contrib import admin
from .models import Team, TeamMember


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0
    fields = ["user", "role", "is_deleted"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["sector", "is_deleted", "created_at"]
    list_filter = ["is_deleted"]
    search_fields = ["sector"]
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["user", "team", "role", "is_deleted", "created_at"]
    list_filter = ["is_deleted", "team"]
    search_fields = ["user__username", "user__email", "role"]
