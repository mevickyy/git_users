from rest_framework import serializers
from search.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'username',
                  'location',
                  'followers',
                  'repos',
                  'created',
                  'type',
                  'avatar',
                  'score')
