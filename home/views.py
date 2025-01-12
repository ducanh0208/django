from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .form import RegistrationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import pandas as pd
from blog.models import Post
from .form import UploadFileForm
import csv
from datetime import datetime

# Create your views here.
def index(request):
   return render(request, 'pages/home.html')
def contact(request):
   return render(request, 'pages/contact.html')
def excel_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            try:
                # Đọc file Excel
                df = pd.read_excel(excel_file)

                # Lặp qua từng hàng để lưu dữ liệu vào database
                for _, row in df.iterrows():
                    date_value = row['date']
                    if isinstance(date_value, str):
                        date_value = datetime.strptime(date_value, '%Y-%m-%d')  # Adjust the format as necessary

                    image_value = row.get('image', '')
                    if isinstance(image_value, float):
                        image_value = str(image_value)  # Convert to string if it's a float

                    post = Post.objects.create(
                        title=row['title'],
                        body=row['body'],
                        date=date_value,
                        author=request.user
                    )
                    print(f"success import {post}")
                return render(request, 'pages/excel.html', {'form': form})
            
            except Exception as e:
                return render(request, 'pages/excel.html', {'form': form, 'error': str(e)})

    else:
        form = UploadFileForm()  # Tạo
        
    return render(request, 'pages/excel.html', {'form': form})


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

def import_excel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            try:
                # Đọc file Excel
                df = pd.read_excel(excel_file)

                # Lặp qua từng hàng để lưu dữ liệu vào database
                for _, row in df.iterrows():
                    Post.objects.create(
                        title=row['title'],
                        body=row['body'],
                        date=row['date'],
                        image=row.get('image', '')
                    )
                return redirect('success')
            
            except Exception as e:
                return render(request, 'import.html', {'form': form, 'error': str(e)})

    else:
        form = UploadFileForm()

    return render(request, 'import.html', {'form': form})
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Post.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Price', 'Stock', 'Description'])

    Post = Post.objects.all().values_list('name', 'price', 'stock', 'description')
    for Post in Post:
        writer.writerow(Post)

    return response
def export_excel(request):
    Post = Post.objects.all().values()
    df = pd.DataFrame(Post)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Post.xlsx"'

    df.to_excel(response, index=False, engine='openpyxl')

    return response