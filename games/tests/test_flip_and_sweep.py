from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.utils import json

from games.views import BlockDetails
from games.models import Game, Block


class BlockPatchTestCase(APITestCase):
    """
    This Test Case is for editing blocks
    """

    def setUp(self):
        """
        In set up, create a game and make the last block a mine
        """
        self.game = Game.objects.create()
        self.first_block = Block.objects.get(game=self.game, index=0)
        self.last_block = Block.objects.get(game=self.game, index=99)
        self.last_block.is_mine = True
        self.last_block.save()

    def tearDown(self):
        """
        For tear down, delete all games
        """
        Game.objects.all().delete()
        Block.objects.all().delete()

    def test_flip_block_and_sweep_whole_board(self):
        # Flip the first block
        url = '/games/blocks/' + str(self.first_block.pk) + '/'
        factory = APIRequestFactory()
        view = BlockDetails.as_view()
        request = factory.patch(url, data=json.dumps({'is_flipped': True}), content_type='application/json')
        response = view(request, block_id=self.first_block.pk)

        # Assert the response was okay
        self.assertEqual(response.status_code, 200)

        # Assert the first block is PUBLIC (i.e. has mine data)
        block = response.data.get('blocks')[0]
        self.assertFalse(block.get('is_mine'))

        # Assert a middle block is PUBLIC (i.e. has mine data)
        block = response.data.get('blocks')[50]
        self.assertFalse(block.get('is_mine'))

        # Assert the second last block is PUBLIC (i.e. has mine data)
        block = response.data.get('blocks')[98]
        self.assertFalse(block.get('is_mine'))

        # Assert the last block is PRIVATE (i.e. no mine data)
        block = response.data.get('blocks')[99]
        self.assertFalse(hasattr(block, 'is_mine'))

    def test_bad_block_patch(self):
        # Send a bad block patch
        url = '/games/blocks/' + str(self.first_block.pk) + '/'
        factory = APIRequestFactory()
        view = BlockDetails.as_view()
        request = factory.patch(url, data=json.dumps({'is_flipped': 100}), content_type='application/json')
        response = view(request, block_id=self.first_block.pk)

        # Assert the response was BAD REQUEST and nothing changed
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Block.objects.get(game=self.game, index=0), self.first_block)

