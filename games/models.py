from django.db import models


class Game(models.Model):
    # Is this game part of an automation test
    is_test = models.BooleanField(default=False)


class Block(models.Model):
    # Every block is associated to a game
    game = models.ForeignKey(Game, related_name='blocks', on_delete=models.CASCADE)

    # Where is the block (position 0 to 99)
    index = models.PositiveIntegerField()

    # Is the block a mine, flipped or flagged
    is_mine = models.BooleanField(default=False)
    is_flipped = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)

    def __str__(self):
        return str(self.game.pk) + ' - ' + str(self.index)
