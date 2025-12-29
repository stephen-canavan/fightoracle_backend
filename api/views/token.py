from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


class TokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        refresh_token = data.get("refresh", None)

        if refresh_token:
            import os
            secure_cookie = os.getenv("SECURE_COOKIE", "False").lower() == "true"
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=secure_cookie,
                samesite="Lax",
            )
        del data["refresh"]

        return response


class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token", None)

        if refresh_token is None:
            return Response(
                {"detail": "Refresh token not found in cookies"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["refresh_token"] = refresh_token
        response = super().post(request, *args, **kwargs)

        return response
