from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.permissions import *
from core.models import Post
from core.serializer import *
from .permissions import *

class PostListCreateApiView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class   = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

    
    def get_queryset(self):
        posts = Post.objects.filter(author = self.request.user)
        return posts

class postRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner]

class CommentListCreateApiView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, id=pk)
        serializer.save(
            post=post,
            user = self.request.user
            )

    def get_queryset(self):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, id=pk)
        comments = Comment.objects.filter(post=post)
        return comments

class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        com_pk = self.kwargs['com_pk']
        post = get_object_or_404(Post, id=com_pk)
        comments = Comment.objects.filter(post=post, id=pk)
        return comments

