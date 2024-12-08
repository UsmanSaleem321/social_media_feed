from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class PostSerializer(ModelSerializer):
    author = serializers.CharField(source = 'author.username', read_only=True)
    class Meta:
        model = Post
        fields = ['content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content','user','post','created_at','updated_at']
        read_only_fields = ['user','post']

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'birth_date', 'phone', 'followers', 'image','friends']

class FriendRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['from_profile', 'to_profile','created_at']


   