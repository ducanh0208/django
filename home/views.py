from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .form import RegistrationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

# Create your views here.
def index(request):
   return render(request, 'pages/home.html')
def contact(request):
   return render(request, 'pages/contact.html')
def error(request, exception):
    return render(request, 'pages/error.html', {'message': exception})
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'pages/register.html', {'form': form})
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'change_password.html'
