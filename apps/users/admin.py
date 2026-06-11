from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "group", "is_active", "is_deleted", "date_joined"]
    list_filter = ["group", "is_active", "is_deleted"]
    search_fields = ["username", "email"]
    ordering = ["-date_joined"]
    fieldsets = tuple(list(UserAdmin.fieldsets) + [
        ("DevTasks", {"fields": ["group", "is_deleted"]}),
    ])
