from rest_framework.serializers import ModelSerializer
from .models import *

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content','user','post','created_at','updated_at']
        read_only_fields = ['user','post']


   