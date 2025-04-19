from http import HTTPMethod

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .auth import generate_token
from .serializers import UserLoginSerializer


@api_view([HTTPMethod.POST])
def jwt_login(req: Request):
    try:
        data = UserLoginSerializer(data=req.data)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        assert (user := authenticate(
            username=data.validated_data["username"],
            password=data.validated_data["password"],
        ))
        token = generate_token(user)

        return Response({"Token": token})
    except Exception:
        return Response(status=status.HTTP_403_FORBIDDEN)