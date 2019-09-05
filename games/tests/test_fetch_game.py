from rest_framework.test import APITestCase, APIRequestFactory

from games.views import Games, GameDetails
from games.models import Game, Block

from games.constants import NUMBER_OF_MINES, NUMBER_OF_BLOCKS


class GamePostTestCase(APITestCase):
    """
    This Test Case is for Posting a new Game
    """

    def setUp(self):
        pass

    def tearDown(self):
        """
        For tear down, delete all games and blocks
        """
        Game.objects.all().delete()
        Block.objects.all().delete()

    def test_post_and_fetch_game_for_correct_data(self):
        # Assert there are no games and blocks
        self.assertEqual(len(Game.objects.all()), 0)
        self.assertEqual(len(Block.objects.all()), 0)

        # Post a new Game
        url = '/games/'
        factory = APIRequestFactory()
        view = Games.as_view()
        request = factory.post(url, content_type='application/json')
        response = view(request)

        # Post a new Game
        url = '/games/' + str(response.data.get('id')) + '/'
        factory = APIRequestFactory()
        view = GameDetails.as_view()
        request = factory.get(url, content_type='application/json')
        response = view(request, game_id=response.data.get('id'))

        # Assert the response was okay
        self.assertEqual(response.status_code, 200)

        # Assert a new game with NUMBER_OF_BLOCKS blocks was made
        self.assertEqual(len(Game.objects.all()), 1)
        self.assertEqual(len(Block.objects.all()), NUMBER_OF_BLOCKS)

        # Assert there are NUMBER_OF_MINES mines in the game
        game = Game.objects.first()
        self.assertEqual(len(Block.objects.filter(game=game, is_mine=True)), NUMBER_OF_MINES)

        # Assert the blocks are PRIVATE (i.e. no mine data)
        first_block = response.data.get('blocks')[0]
        self.assertFalse(hasattr(first_block, 'is_mine'))

        # Assert the game is not over
        self.assertFalse(response.data.get('is_test'))
        self.assertFalse(response.data.get('has_won'))
        self.assertFalse(response.data.get('has_lost'))
        self.assertEqual(response.data.get('flags_left'), NUMBER_OF_MINES)
