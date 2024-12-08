from django.urls import path, re_path
from .views import *
from django.shortcuts import redirect
from api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupAPIView.as_view(), name="signup"),
    path('profile/<int:pk>/', ProfileAPIView.as_view(), name = "api_profile"),
    path('posts/', PostListCreateApiView.as_view(), name = "posts_list"),
    path('posts/<int:pk>/', postRetrieveUpdateDestroyAPIView.as_view()),
    path('posts/<int:pk>/like/', LikeAPIView.as_view(), name = "likeview"),
    path('posts/<int:pk>/comments/', CommentListCreateApiView.as_view()),
    path('posts/<int:com_pk>/comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('friend_requests/', friendrequestAPIView.as_view(), name = "request_api"),

]

