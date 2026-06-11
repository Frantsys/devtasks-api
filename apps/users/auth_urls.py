from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        summary="Obter token JWT",
        description=(
            "Autentica com **email** e **password** e retorna um par de tokens JWT "
            "(access + refresh). Use o `access` token no header "
            "`Authorization: Bearer <token>` para acessar os demais endpoints."
        ),
        tags=["auth"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @extend_schema(
        summary="Renovar token JWT",
        description=(
            "Recebe o `refresh` token e retorna um novo `access` token. "
            "O refresh token tem validade configurável via `REFRESH_TOKEN_LIFETIME_DAYS`."
        ),
        tags=["auth"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


urlpatterns = [
    path("token/", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
]
