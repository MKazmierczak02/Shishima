from rest_framework import serializers


class ManageGameSerializer(serializers.Serializer):
    method = serializers.CharField(help_text="Method to manage the game: start or stop")
    game_id = serializers.IntegerField(required=False, help_text="The id of the game you wish to stop")


class MoveGameSerializer(serializers.Serializer):
    move_from = serializers.IntegerField(help_text="Move from index")
    move_to = serializers.IntegerField(help_text="Move to index")
