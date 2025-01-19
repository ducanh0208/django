from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .form import RegistrationForm, UploadFileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import pandas as pd
from blog.models import Post
import csv
from datetime import datetime


def index(request):
    return render(request, 'pages/home.html')

def contact(request):
    return render(request, 'pages/contact.html')

def excel_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            image_file = request.FILES.get('image')  # Optional image file uploaded manually

            try:
                # Read Excel file
                df = pd.read_excel(excel_file)

                # Iterate through each row and save data to the database
                for _, row in df.iterrows():
                    date_value = row['date']
                    if isinstance(date_value, str):
                        date_value = datetime.strptime(date_value, '%Y-%m-%d')  # Adjust format if needed

                    # Prepare image for import
                    image_url = row['image']  # Assuming 'image' column holds image URL or file path
                    
                    post = Post.objects.create(
                        title=row['title'],
                        body=row['body'],
                        date=date_value,
                        author=request.user
                    )

                    # If there is an image URL or path, download the image and save it
                    if image_url:
                        try:
                            # If it's a URL, download the image
                            if image_url.startswith('http'):
                                response = requests.get(image_url)
                                if response.status_code == 200:
                                    image_name = image_url.split("/")[-1]
                                    post.image.save(image_name, ContentFile(response.content))
                            else:
                                # If it's a file path, save it (ensure the path is correct)
                                post.image = image_file  # Save the uploaded image (if any)
                        except Exception as e:
                            print(f"Error saving image for post {post.id}: {str(e)}")
                    
                    post.save()  # Save the post after adding the image
                    print(f"Successfully imported {post}")

                return render(request, 'pages/excel.html', {'form': form})

            except Exception as e:
                return render(request, 'pages/excel.html', {'form': form, 'error': str(e)})

    else:
        form = UploadFileForm()

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

                df = pd.read_excel(excel_file)

         
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

    posts = Post.objects.all().values_list('name', 'price', 'stock', 'description')
    for post in posts:
        writer.writerow(post)

    return response

def export_excel(request):
    posts = Post.objects.all().values()
    df = pd.DataFrame(posts)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Post.xlsx"'

    df.to_excel(response, index=False, engine='openpyxl')

    return response
