# Imports to support REST APIs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from games.models import Game, Block
from games.serializers import GameSerializer


class Games(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        This method will create a new game from scratch
        :param request: POST
        :return: return 201 for a new game
        """
        # Start a new game
        game = Game.objects.create()

        # For 0 to 99, create a block for this game with i as index
        for i in range(0, 100):
            block = Block.objects.create(game=game, index=i)
            print(str(block.game.pk))
            print(str(block.index))

        # Return the new data in a GameSerializer
        serializer = GameSerializer(game, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
