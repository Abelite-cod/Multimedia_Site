from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_pic = forms.ImageField(required=False)  # this is only for the form input

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]  # remove profile_pic from here

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile_pic = self.cleaned_data.get('profile_pic')
        if profile_pic:
            # Save the uploaded profile pic to the related Profile
            user.profile.profile_pic = profile_pic
            user.profile.save()
        return user
