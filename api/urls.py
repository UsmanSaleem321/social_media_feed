from django.urls import path, re_path
from .views import *
from django.shortcuts import redirect
from api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', PostListCreateApiView.as_view(), name = "posts_list"),
    path('posts/<int:pk>/', postRetrieveUpdateDestroyAPIView.as_view()),
    path('posts/<int:pk>/comments/', CommentListCreateApiView.as_view()),
    path('posts/<int:com_pk>/comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view()),

]

