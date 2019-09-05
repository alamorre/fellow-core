from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.utils import json

from games.views import BlockDetails
from games.models import Game, Block


class WinGameTestCase(APITestCase):
    """
    This Test Case is for winning the game
    """

    def setUp(self):
        """
        In set up, create a game and make the last block a mine
        """
        self.game = Game.objects.create()
        self.last_block = Block.objects.get(game=self.game, index=99)
        self.last_block.is_mine = True
        self.last_block.save()

    def tearDown(self):
        """
        For tear down, delete all games
        """
        Game.objects.all().delete()
        Block.objects.all().delete()

    def test_flag_last_block_to_win(self):
        # Flag the only mine
        url = '/games/blocks/' + str(self.last_block.pk) + '/'
        factory = APIRequestFactory()
        view = BlockDetails.as_view()
        request = factory.patch(url, data=json.dumps({'is_flagged': True}), content_type='application/json')
        response = view(request, block_id=self.last_block.pk)

        # Assert the response was okay
        self.assertEqual(response.status_code, 200)

        # Assert the game has been won
        self.assertTrue(response.data.get('has_won'))

