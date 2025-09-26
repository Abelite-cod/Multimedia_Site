from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "profile_pic"]

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile_pic = self.cleaned_data.get('profile_pic')
        if commit and profile_pic:
            # profile should exist thanks to post_save signal
            user.profile.profile_pic = profile_pic
            user.profile.save()
        return user