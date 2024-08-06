from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import os

UPLOAD_FOLDER = 'uploads'

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def app(request):
    return render(request, 'app.html')

def create_user_media_folder(request):
    # get user
    user = request.user  
    # create user media folder
    media_folder = os.path.join(UPLOAD_FOLDER, user.username)  
    os.makedirs(media_folder, exist_ok=True)
    return media_folder

@csrf_exempt
def upload_files(request):
    USER_MEDIA_FOLDER = create_user_media_folder(request)
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        # Delete files in the folder
        for file in os.listdir(USER_MEDIA_FOLDER):
            os.remove(os.path.join(USER_MEDIA_FOLDER, file))
        # Save files to the folder
        for file in files:
            with open(os.path.join(USER_MEDIA_FOLDER, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        files_count = len(os.listdir(USER_MEDIA_FOLDER))
        print(files_count)
        return JsonResponse({'message': 'Files successfully uploaded', "files_count":files_count}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def list_images(request):
    user = request.user
    user_media_folder = os.path.join(UPLOAD_FOLDER, user.username)
    if request.method == 'GET':
        images = os.listdir(os.path.join(user_media_folder))
        image_urls = [os.path.join(user_media_folder, image) for image in images]
        return JsonResponse({'images': image_urls}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)
