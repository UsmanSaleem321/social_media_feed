from django.urls import path, re_path
from .views import *
from django.shortcuts import redirect
from core import views

urlpatterns = [
    path('', landingview.as_view(), name="landing"),
    path('login/', loginView.as_view(), name="login"),
    path("Forgetpassword/", get_otp_detail.as_view(), name="otp_detail"),
    path('signup/', signupview.as_view(), name="signup"),
    path("logout/", views.logout_view, name = "logout" ),
    path('feed/', feedview.as_view(), name="feed"),
    path("create/", post_createview.as_view(), name = "create"),
    path("delete/<int:pk>", post_deleteview.as_view(), name = "delete"),
    path("create_comment/<int:pk>",addcommentview.as_view(), name = "create_comment" ),
    path("delete_comment/<int:pk>",comment_deleteview.as_view(), name = "delete_comment" ),
    path("like/<int:pk>" , likeview.as_view(), name="like"),
    path("edit/<int:pk>", posteditview.as_view(), name = "edit"),
    path("profile/<int:pk>", profileview.as_view(), name="profile"),
    path("change_username/",changeusernameview.as_view(), name="change_username"),
    path("find_user/",searchuserview.as_view(), name = "find_user"  ),
    path("change_image/<int:pk>", changeimageview.as_view(), name = "changeimage" ),
    path("delete_image/<int:pk>", deleteimage.as_view(), name = "deleteimage" ),
    path("change_password/", change_passwordview.as_view(), name = "change_password" ),
    path("follower/<int:pk>", follow_view.as_view(), name= "follow"),
    path("unfollow/<int:pk>", unfollow_view.as_view(), name="unfollow"),
    path("show_request/",show_requests_view.as_view(), name = "show_request"),
    path("addfriend/<int:pk>", addfriend_view.as_view(), name= "addfriend"),
    path("unfriend/<int:pk>", unfriend_view.as_view(), name="unfriend"),
    path("friendrequestsend/<int:pk>",send_request_view.as_view(), name = "sendrequest"),
    path("deleterequestsent/<int:pk>" ,delete_request_view.as_view(), name="delete_request" ),
    path("friends/", friendlist_view.as_view(), name= "friends"),
    path("create_room/<int:pk>", createroom_view.as_view(), name = "create_room"),
    path("chats/",chatview.as_view(), name = "chats"),
    path("chats/<int:pk>", chat_room.as_view(), name = "chatroom")
]


