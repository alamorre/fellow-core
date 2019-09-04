# Django specific imports
from django.shortcuts import get_object_or_404

# Imports for Rest APIs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# App/DB specific imports
from games.models import Game, Block
from games.serializers import PrivateBlockSerializer, serialize_blocks

# Helper packages
import random
from games.sweeper import sweeper

# Constant for number of mines (written only once)
from games.constants import NUMBER_OF_MINES, NUMBER_OF_BLOCKS


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

        # Make NUMBER_OF_MINES random mines on the board
        for mine in random.sample(range(1, NUMBER_OF_BLOCKS), NUMBER_OF_MINES):
            block = Block.objects.get(game=game, index=mine)
            block.is_mine = True
            block.save()

        # Return the new data in a GameSerializer
        return Response(serialize_blocks(game), status=status.HTTP_200_OK)


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
        return Response(serialize_blocks(game), status=status.HTTP_200_OK)


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
        game = block.game

        # Update the block and return new game state
        serializer = PrivateBlockSerializer(block, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # If the block is flipped, start the sweep
            block = get_object_or_404(Block, pk=block_id)
            if block.is_flipped:
                sweeper.breadth_first_sweep(block)

                # Set the game to lost if it's a mine
                if block.is_mine:
                    game.has_lost = True
                    game.save()

            # If block is flagged, check if the user won
            if block.is_flagged:
                game.has_won = True                                       # Start assuming True
                for b in Block.objects.filter(game=game, is_mine=True):   # Look for one counter example
                    if not b.is_flagged:                                        # Set to False if found
                        game.has_won = False
                game.save()                                               # Save result

            # Return the new game state
            return Response(serialize_blocks(game), status=status.HTTP_200_OK)

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

        # Make NUMBER_OF_MINES of Flagged mines on the board
        for mine in random.sample(range(1, NUMBER_OF_BLOCKS), NUMBER_OF_MINES):
            block = Block.objects.get(game=game, index=mine)
            block.is_flipped = False
            block.is_flagged = True
            block.is_mine = True
            block.save()

        # Set the game as won
        game.has_won = True
        game.save()

        # Return the new data in a GameSerializer
        return Response(serialize_blocks(game), status=status.HTTP_200_OK)


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

        # Set the game as lost
        game.has_lost = True
        game.save()

        # Return the new data in a GameSerializer
        return Response(serialize_blocks(game), status=status.HTTP_200_OK)


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
