# Django specific imports
from django.shortcuts import get_object_or_404

# Imports for Rest APIs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# App/DB specific imports
from games.models import Game, Block
from games.serializers import GameSerializer, BlockSerializer

# Helper packages
import random
from games.sweeper import sweeper

# Constant for number of mines (written only once)
NUMBER_OF_BLOCKS = 100
NUMBER_OF_MINES = 12


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
        for i in range(0, NUMBER_OF_BLOCKS):
            Block.objects.create(game=game, index=i)

        # Make NUMBER_OF_MINES random mines on the board
        for mine in random.sample(range(1, NUMBER_OF_BLOCKS), NUMBER_OF_MINES):
            block = Block.objects.get(game=game, index=mine)
            block.is_mine = True
            block.save()

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


class BlockDetails(APIView):
    permission_classes = (permissions.AllowAny,)

    def patch(self, request, block_id):
        """
        This method will update block data and return the new game state
        :param request: PATCH
        :param block_id: Primary key of the block
        :return: 200 if block is updated, 400 or 404 otherwise
        """
        block = get_object_or_404(Block, pk=block_id)

        # Update the block and return new game state
        serializer = BlockSerializer(block, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # If the block is flipped, start the sweep
            block = get_object_or_404(Block, pk=block_id)
            if block.is_flipped:
                sweeper.breadth_first_sweep(block)

            # Return the new game state
            serializer = GameSerializer(block.game, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If 400 errors, let the user be aware of them
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WinnerGame(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        This method will create a return a won game
        :param request: POST
        :return: 200 with game data
        """
        # Create a new game
        game = Game.objects.create(is_test=True)

        # Create NUMBER_OF_BLOCKS new blocks
        for i in range(0, NUMBER_OF_BLOCKS):
            Block.objects.create(game=game, index=i, is_flipped=True)

        # Make NUMBER_OF_MINES of Flagged mines on the board
        for mine in random.sample(range(1, NUMBER_OF_BLOCKS), NUMBER_OF_MINES):
            block = Block.objects.get(game=game, index=mine)
            block.is_flipped = False
            block.is_flagged = True
            block.is_mine = True
            block.save()

        # Return the new data in a GameSerializer
        serializer = GameSerializer(game, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoserGame(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        This method will create a return a won game
        :param request: POST
        :return: 200 with game data
        """
        # Create a new game
        game = Game.objects.create(is_test=True)

        # Create NUMBER_OF_BLOCKS new blocks
        for i in range(0, NUMBER_OF_BLOCKS):
            Block.objects.create(game=game, index=i)

        # Make NUMBER_OF_MINES of mines on the board and flip them
        for mine in random.sample(range(1, NUMBER_OF_BLOCKS), NUMBER_OF_MINES):
            block = Block.objects.get(game=game, index=mine)
            block.is_flipped = True
            block.is_mine = True
            block.save()

        # Free block 99 for a hard coded test
        block = Block.objects.get(game=game, index=99)
        block.is_flipped = False
        block.save()

        # Return the new data in a GameSerializer
        serializer = GameSerializer(game, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CleanTests(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        This method will delete all games that are tests
        :param request: POST
        :return: 200 with message
        """
        Game.objects.filter(is_test=True).delete()
        return Response({'message': 'Test games deleted!'}, status=status.HTTP_200_OK)
