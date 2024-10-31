# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class PostForm(forms.ModelForm):
     content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            "rows":"3",
            "placeholder":"say something"
        }))
     class Meta:
        model = Post
        fields = ['content']
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class imageupdateform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class profileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','location','phone','profession','birth_date']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
