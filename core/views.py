from random import randint
from .forms import PostForm, CommentForm, UsernameChangeForm, imageupdateform,CustomUserCreationForm,profileform
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Like, Profile,FriendRequest, Room, Message, OTP
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib import messages
from core.otpfunctions import send_otp
from django.db.models import Q
from django.views import View

class landingview(View):
    def get(self, request, *args, **kwargs):
        return render(request,"guest_profile.html",)

     ### ------------!!!!<<<*****>>>!!!!----------------###

class loginView(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        context = {
            "form":form
        }
        return render(request, "login.html", context)
     
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("feed")
        else:
            messages.error(request, "Invalid username or password.")
            form = AuthenticationForm()
            context = {
            "form":form
                }
            return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect("login")

    ### ------------!!!!<<<*****>>>!!!!----------------###

class signupview(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        context = {
            "form":form
        }
        return render(request, "signup.html", context)
    
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            form = CustomUserCreationForm()
            context = {
                "form":form
                }
            return redirect("signup")

    ### ------------!!!!<<<*****>>>!!!!----------------###        

class feedview(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        posts=Post.objects.all().order_by("-created_at")
        form = PostForm()
        context =  {
            "posts":posts,
            "form":form
        }
        return render(request, "feed.html", context)
    
    ### ------------!!!!<<<*****>>>!!!!----------------###

class post_createview(View):

    def get(self, request, *args, **kwargs):
        form = PostForm()
        context = {
            "form":form
        }
        return render(request, "post_create.html", context)
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid:
            new_post = form.save(commit = False)
            new_post.author = request.user
            new_post.save()
            return redirect("feed")
        else:
            messages.error(request, "Invalid username or password.")
            form = PostForm()
            context = {
                 "form":form
                  }
            return render(request, "post_create.html", context) 

    ### ------------!!!!<<<*****>>>!!!!----------------###

class posteditview(LoginRequiredMixin, UserPassesTestMixin, View):
     
    def get(self,request, pk , *args, **kwargs):
        post = Post.objects.get(id=pk)
        form = PostForm(instance=post)
        context = {
            "form":form
        }
        return render(request, "post_edit.html", context)
    
    def post(self,request,pk,*args, **kwargs):
        instance = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=instance)
        if form.is_valid:
            edited_post = form.save(commit=False)
            edited_post.author = request.user
            edited_post.save()
            return redirect("feed")
        else:
            messages.error(request, "Something went wrong.")
            form = PostForm(request.POST)
            context = {
                 "form":form
                  }
            return render(request, "post_edit.html", context) 
        
    def test_func(self):
        pk = self.kwargs['pk']
        post = Post.objects.get(id=pk)
        return self.request.user == post.author

    ### ------------!!!!<<<*****>>>!!!!----------------###

class post_deleteview(LoginRequiredMixin, UserPassesTestMixin,View):
    def get(self,request,pk,*args,**kwargs):
        post = Post.objects.get(id=pk)
        post.delete()
        return redirect("feed")
    
    def test_func(self):
        pk = self.kwargs['pk']
        post = Post.objects.get(id=pk)
        return self.request.user == post.author

    ### ------------!!!!<<<*****>>>!!!!----------------###

class addcommentview(LoginRequiredMixin,View):
    def get(self,request,pk,*args, **kwargs):
        post = Post.objects.get(id=pk)
        form = CommentForm()
        context = {
            "form":form,
            "post":post
        }
        return render(request, "comment_create.html", context)
    
    def post(self,request,pk,*args, **kwargs):
        post = Post.objects.get(id=pk)
        form =  CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            return redirect("feed")
        else:
            messages.error(request, "somenthing went wrong")
            form = CommentForm()
            context = {
                 "form":form
                  }
            return render(request, "comment_create.html", context) 

    ### ------------!!!!<<<*****>>>!!!!----------------###

class comment_deleteview(View):
    def get(self,request,pk,*args, **kwargs):
        comment = Comment.objects.get(id=pk)
        comment.delete()
        return redirect("feed")
    
    def test_func(self):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(id=pk)
        return self.request.user == comment.user
    
    ### ------------!!!!<<<*****>>>!!!!----------------###

class likeview(View):
    def get(self, request, pk , *args, **kwargs):
        post = Post.objects.get(id=pk)
        Like.objects.get_or_create(
            post=post,
            user=request.user
        )
        return redirect("feed")

    ### ------------!!!!<<<*****>>>!!!!----------------###

class profileview(LoginRequiredMixin,View):
    def get(self,request,pk,*args, **kwargs):
        profile = Profile.objects.get(id=pk)
        posts = Post.objects.filter(author =request.user)
        likes = Like.objects.filter(user = request.user)
        form = PasswordChangeForm(user = request.user)
        is_follower = profile.followers.filter(id=request.user.id).exists()
        is_friend =  profile.friends.filter(id=request.user.id).exists()
        is_request = FriendRequest.objects.filter(from_profile=request.user.profile, to_profile=profile).exists()
        context = {
            "profile":profile,
            "posts":posts,
            "likes": likes,
            "form": form,
            "is_follower":is_follower,
            "is_friend":is_friend,
            "is_request":is_request
        }
        return render(request,"user_profile.html", context)
    
    def post(self,request,pk,*args, **kwargs):
        profile = Profile.objects.get(id=pk)
        last_name = request.POST.get('last_name')
        first_name =  request.POST.get('first_name')
        birth_date =  request.POST.get('birthday')
        phone =  request.POST.get('phone')
        bio =  request.POST.get('bio')
        email = request.POST.get('email')
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        form = profileform(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"data saved successfuly")
            return HttpResponseRedirect(reverse_lazy("profile", kwargs={"pk": pk}))
        messages.error(request,"something went wrong")
        return HttpResponseRedirect(reverse_lazy("profile", kwargs={"pk": pk}))

    ### ------------!!!!<<<*****>>>!!!!----------------###

class changeusernameview(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form =  UsernameChangeForm(instance=request.user)
        context = {
            "form":form
        }
        return render(request, "change_username.html", context)
    def post(self,request,*args, **kwargs):
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid:
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your username has been updated.')
            return redirect("profile")
        else:
            form =  UsernameChangeForm(instance=request.user)
            context = {
                "form":form
            }
            return render(request, "change_username.html", context)
        
    ### ------------!!!!<<<*****>>>!!!!----------------###

class searchuserview(View):
    def get(self,request,*args, **kwargs):
        return redirect("feed")
    
    def post(self,request,*args, **kwargs):
        search = request.POST.get('q')
        users = User.objects.filter(
            Q(username__icontains = search)|
            Q(first_name__icontains = search)|
            Q(last_name__icontains = search)
        )
        context = {
            "users":users,
            "search":search
        }
        return render(request,"search_users.html", context)
    
    ### ------------!!!!<<<*****>>>!!!!----------------###

class changeimageview(LoginRequiredMixin,View):
    def get(self,request,pk,*args, **kwargs):
        profile = Profile.objects.get(id=pk)
        form = imageupdateform(instance=profile)
        context = {
            "form":form
        }
        return render(request, "change_image.html", context)
    
    def post(self,request,*args, **kwargs):
        profile = request.user.profile
        form =  imageupdateform(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy("profile", kwargs={"pk": request.user.id}))
        return self.render_to_response({'form': form})   

    ### ------------!!!!<<<*****>>>!!!!----------------###

class deleteimage(LoginRequiredMixin,View):
    def get(self,request,pk,*args, **kwargs):
        profile =Profile.objects.get(id=pk)
        profile.image = 'images/default.png'
        profile.save()
        return HttpResponseRedirect(reverse_lazy("profile", kwargs={"pk": request.user.id}))

    ### ------------!!!!<<<*****>>>!!!!----------------###

class change_passwordview(LoginRequiredMixin,View):

    def post(self,request,*args, **kwargs):
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()  # Save the new password
            update_session_auth_hash(request, user)  # Prevent the user from being logged out
            return redirect('profile')
        else:
            messages.error(request,"Something went Wrong Password not changed")
            return redirect("profile")    
        
      ### ------------!!!!<<<*****>>>!!!!----------------###

class follow_view(View):
    def get(self, request,pk,*args, **kwargs):
        profile_to_follow = Profile.objects.get(id=pk)
        profile_following =  Profile.objects.get(user = request.user)
        profile_to_follow.followers.add(profile_following)
        profile_following.following.add(profile_to_follow)
        return redirect(reverse('profile', kwargs={'pk': pk}))

     ### ------------!!!!<<<*****>>>!!!!----------------###

class unfollow_view(View):
    def get(self, request,pk, *args, **kwargs):
        profile_to_unfollow = Profile.objects.get(id=pk)
        profile_unfollowing = Profile.objects.get(user = request.user)
        profile_to_unfollow.followers.remove(profile_unfollowing)
        profile_unfollowing.following.remove(profile_to_unfollow)
        return redirect(reverse('profile', kwargs={'pk': pk}))

class show_requests_view(View):
    def get(self,request,*args, **kwargs):
        profile = Profile.objects.get(user = request.user)
        all_request_sent = profile.sent_requests.all()
        all_request_recieved = profile.received_requests.all()
        context = {
            "all_request_sent":all_request_sent,
            "all_request_recieved":all_request_recieved
        }
        return render(request, "friend_request.html", context)

class send_request_view(View):
    def get(self,request,pk,*args, **kwargs):
        receiver_profile = Profile.objects.get(id=pk)
        sender_profile = Profile.objects.get(user = request.user)
        FriendRequest.objects.create(
             from_profile = sender_profile,
             to_profile = receiver_profile
        )
        return HttpResponseRedirect(reverse_lazy('profile', kwargs={"pk":pk}))

class delete_request_view(View):
    def get(self,request,pk,*args, **kwargs):
        receiver_profile = Profile.objects.get(id=pk)
        sender_profile = Profile.objects.get(user = request.user)
        print(receiver_profile)
        print(sender_profile)
        object_delete = get_object_or_404(FriendRequest, to_profile=sender_profile, from_profile=receiver_profile)
        object_delete.delete()
        return HttpResponseRedirect(reverse_lazy('profile', kwargs={"pk":pk}))

class  addfriend_view(View):
    def post(self, request,pk,*args, **kwargs):
        profile_to= Profile.objects.get(id=pk)
        profile_by = Profile.objects.get(user=request.user)
        profile_by.friends.add(profile_to)
        object_delete = get_object_or_404(FriendRequest, to_profile=profile_by, from_profile=profile_to)
        object_delete.delete()
        return redirect(reverse('profile', kwargs={'pk': pk}))
    
class  unfriend_view(View):
    def get(self, request,pk,*args, **kwargs):
        profile= Profile.objects.get(id=pk)
        profile_unfriend = Profile.objects.get(user = request.user)
        profile_unfriend.friends.remove(profile)
        return redirect(reverse('profile', kwargs={'pk': pk}))

class friendlist_view(View):
    def get(self,request,*args, **kwargs):
        profile = Profile.objects.get(user=request.user.id)
        friends = profile.friends.all()
        context = {
            "friends":friends 
        }
        return render(request, "friends.html",context)

class chatview(View):    
    def get(self, request, *args, **kwargs):
        profile =Profile.objects.get(user=request.user)
        rooms = Room.objects.filter(participants = profile )  # Fetch all room instances
        if rooms:
            chat_rooms = []
            for room in rooms:
                current_user = request.user
                other_participant = room.participants.exclude(id=current_user.id).first()
                chat_rooms.append({
                    "room": room,
                    "username": other_participant.user.username,
                    "image": other_participant.image.url 
                })           
                context = {
                    "chat_rooms": chat_rooms  
                }
            return render(request, "chat_list.html", context)
        else:
            return render(request,"chat_list.html")
              
class createroom_view(View):
    def get(self,request,pk,*args, **kwargs):
        profile1 = Profile.objects.get(id=pk)
        profile2 = Profile.objects.get(user=request.user)
        room = Room.objects.filter(participants=profile1).filter(participants=profile2).first()
        if room:
            return redirect(reverse('chatroom', kwargs={'pk': room.id}))
        else:
            newroom= Room.objects.create()
            newroom.participants.add(profile1,profile2)
            newroom.save() 
            return redirect(reverse('chatroom', kwargs={'pk': newroom.id}))

class chat_room(View):
    def get(self,request,pk,*args, **kwargs):
        room = Room.objects.get(id=pk)
        messages = room.messages.all()
        context = {
            "room":room,
            "messages":messages,
            "current_user":request.user
        }
        return render(request, "chat_room.html", context)

class get_otp_detail(View):
    def get(self,request,*args, **kwargs):
        return render(request, "otp_detail.html")
    
    def post(self,request,*args, **kwargs):
        number = request.POST.get("phone")
        username = request.POST.get("username")
        user = User.objects.get(username=username)
        if user.exists():
            if user.profile.phone == number:
                otp = randint(10000,99999)
                OTP.objects.update_or_create(
                    number=number,
                    defaults={"otp": otp, "created_at": now()},
                    )
                status = send_otp(number,otp)
                if status:
                    return redirect("verify_otp")
                else:
                    messages.error(request,"otp not sent try again")
                    return redirect("otp_detail")
            else:
                messages.error(request,"number is incorrect")
                return redirect("otp_detail")       
        messages.error(request,"user does not exits")
        return redirect("otp_detail")
class otp_verifyview(View):
    def get(self,request,*args, **kwargs):    
        return render(request,"otp.html")