from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('sex_choice',)
        fields = UserCreationForm.Meta.fields + ('age',)
        fields = UserCreationForm.Meta.fields + ('sex',)
        fields = UserCreationForm.Meta.fields + ('address',)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields