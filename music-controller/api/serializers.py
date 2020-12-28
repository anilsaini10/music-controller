from rest_framework import serializers
from .models import Room

class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model =Room 
        fields= ('id', 'code', 'host', 'guest_can_pause', 'vote_to_skip','created_at')
        # fields= ('__all__')



class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model= Room
        fields = ('guest_can_pause', 'vote_to_skip')

class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[])
    class Meta:
        model= Room
        fields = ('guest_can_pause', 'vote_to_skip', 'code')
