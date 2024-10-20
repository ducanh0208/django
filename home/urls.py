from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ChangePasswordView
from users.views import ResetPasswordView

urlpatterns = [
   path('', views.index),
   path('contact/', views.contact, name='contact'),
   path('register/', views.register, name="register"),
   path('login/',auth_views.LoginView.as_view(template_name="pages/login.html"), name="login"),
   path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
   path('change_password/', ChangePasswordView.as_view(), name='change_password'),
   path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
   path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
   path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]

