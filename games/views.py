# Imports to support REST APIs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


class Games(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        This method will create a new game from scratch
        :param request: POST
        :return: return 201 for a new game
        """
        return Response({"message": "New game buddy!"}, status=status.HTTP_200_OK)
