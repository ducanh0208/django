from django import forms
import re
from users.models import CustomUser  # Make sure to import your CustomUser model

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 == password2:
            return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Tài khoản đã tồn tại")
        return username

    def save(self):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        return user

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
class UploadFileForm(forms.Form):
    file = forms.FileField()