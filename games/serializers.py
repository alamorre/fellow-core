from rest_framework import serializers
from games.models import Game, Block


class BlockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Block model
    """
    class Meta(object):
        model = Block
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Game model and related blocks
    """
    id = serializers.ReadOnlyField
    blocks = BlockSerializer(many=True)

    class Meta(object):
        model = Game
        fields = '__all__'
