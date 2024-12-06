from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.permissions import *
from core.models import Post
from core.serializer import *
from .permissions import *
from rest_framework.views import APIView
from rest_framework.response import Response
from core.forms import CustomUserCreationForm
from rest_framework import status

class PostListCreateApiView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class   = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)


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

class SignupAPIView(APIView):
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(data=request.data)
        if form.is_valid():
            form.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

