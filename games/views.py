# Django specific imports
from django.shortcuts import get_object_or_404

# Imports for Rest APIs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# App/DB specific imports
from games.models import Game, Block
from games.serializers import GameSerializer


class Games(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        This method will create a new game from scratch
        :param request: POST
        :return: return 200 for a new game
        """
        # Start a new game
        game = Game.objects.create()

        # For 0 to 99, create a block for this game with i as index
        for i in range(0, 100):
            Block.objects.create(game=game, index=i)

        # Return the new data in a GameSerializer
        serializer = GameSerializer(game, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GameDetails(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, game_id):
        """
        This method will find the message with pk == game_id
        :param request: GET
        :param game_id: Primary Key of the Game obj
        :return: 200 if pk is found and 404 otherwise
        """
        # Retrieve the game with this Primary Key or throw 404
        game = get_object_or_404(Game, pk=game_id)

        # Return the new data in a GameSerializer
        serializer = GameSerializer(game, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)