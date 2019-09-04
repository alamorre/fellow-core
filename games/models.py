from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Global constants
from games.constants import NUMBER_OF_BLOCKS


class Game(models.Model):
    # Is this game part of an automation test
    is_test = models.BooleanField(default=False)

    # Progress of the game
    has_lost = models.BooleanField(default=False)
    has_won = models.BooleanField(default=False)
    flags_left = models.PositiveIntegerField(default=0)

    # Display string as game pk
    def __str__(self):
        return str(self.pk)


class Block(models.Model):
    # Every block is associated to a game
    game = models.ForeignKey(Game, related_name='blocks', on_delete=models.CASCADE)

    # Where is the block (position 0 to 99)
    index = models.PositiveIntegerField()

    # Is the block a mine, flipped or flagged
    is_mine = models.BooleanField(default=False)
    is_flipped = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)

    # Count the nearby mines
    nearby_mines = models.PositiveIntegerField(default=0)

    # Order in ascending index
    ordering = ('index',)

    # Display string as an index belonging to a game's pk
    def __str__(self):
        return str(self.game.pk) + ' - ' + str(self.index)


def update_flags_left(game):
    """
    This method returns the number of flags from the number of needed flags
    :param game: Game Obj
    :return: Flags left - int
    """
    mine_blocks = Block.objects.filter(game=game, is_mine=True)
    flag_blocks = Block.objects.filter(game=game, is_flagged=True, is_flipped=False)
    return len(mine_blocks) - len(flag_blocks)


@receiver(post_save, sender=Game)
def post_save_game_method(sender, instance, created, **kwargs):
    """
    This method will create all the blocks for the flag and update the number of flags left
    :param sender: Game Class
    :param instance: Game Obj
    :param created: Was this Obj just created
    :return: void
    """
    # If created, create 100 blocks
    if created:
        for i in range(0, NUMBER_OF_BLOCKS):
            Block.objects.create(game=instance, index=i)

    # Update the number of flags left
    if instance.flags_left is not update_flags_left(instance):
        instance.flags_left = update_flags_left(instance)
        instance.save()


@receiver(post_save, sender=Block)
def post_save_block_method(sender, instance, created, **kwargs):
    """
    This method takes a newly saves block and updates the number of neighbouring mines
    :param sender: Block Class
    :param instance: Block Obj
    :param created: is this block newly created - boolean
    :return: void
    """
    # Update the number of neighbouring mines if different
    from games.sweeper import count_nearby_mines
    if not created and instance.nearby_mines is not count_nearby_mines(instance):
        instance.nearby_mines = count_nearby_mines(instance)
        instance.save()
