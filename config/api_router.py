from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet
from apps.teams.views import TeamViewSet, TeamMemberViewSet
from apps.tasks.views import TaskViewSet
from apps.projects.views import SprintViewSet, ProjectViewSet

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"team-members", TeamMemberViewSet, basename="team-member")
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"sprints", SprintViewSet, basename="sprint")
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("auth/", include("apps.users.auth_urls")),
    path("", include(router.urls)),
]
