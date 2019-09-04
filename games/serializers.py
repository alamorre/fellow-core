from rest_framework import serializers
from games.models import Block


class PrivateBlockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Block model
    """
    class Meta(object):
        model = Block
        fields = ['id', 'is_flipped', 'is_flagged', 'game', 'index']


class PublicBlockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Block model
    """
    is_mine = serializers.ReadOnlyField

    class Meta(object):
        model = Block
        fields = '__all__'


def serialize_blocks(game):
    # Run the save scripts to ensure
    game.save()

    # Add private and public blocks to game
    data = []
    for block in Block.objects.filter(game=game):
        if block.is_flipped or block.game.has_lost:
            data.append(PublicBlockSerializer(block, many=False).data)
        else:
            data.append(PrivateBlockSerializer(block, many=False).data)

    # Return the data
    return {
        "id": game.pk,
        "blocks": data,
        "has_won": game.has_won,
        "has_lost": game.has_lost,
        "flags_left": game.flags_left
    }
