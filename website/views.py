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
    list_datasets(request)
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
    user_media_folder = create_user_media_folder(request)
    if request.method == 'POST':        
        dataset = request.POST.get('dataset')
        dataset_folder = os.path.join(user_media_folder, dataset)
        files = request.FILES.getlist('images')
        print(files)
        if files is None or len(files) == 0:
            return JsonResponse({'error': 'No files found in the request'}, status=400)
        # Delete files in the folder
        for file in os.listdir(dataset_folder):
            os.remove(os.path.join(dataset_folder, file))
        # Save files to the folder
        for file in files:
            with open(os.path.join(dataset_folder, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        files_count = len(os.listdir(dataset_folder))
        return JsonResponse({'message': 'Files successfully uploaded', "files_count":files_count}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def list_images(request):
    user_media_folder = create_user_media_folder(request)
    if request.method == 'GET' and 'dataset' in request.GET:  
        dataset = request.GET.get('dataset')
        if not dataset:
            return JsonResponse({'error': 'Dataset is required'}, status=400)
        print(dataset)
        dataset_folder = os.path.join(user_media_folder, dataset) 
        print(dataset_folder)  
        images = os.listdir(os.path.join(dataset_folder))
        image_urls = [os.path.join(dataset_folder, image) for image in images]
        print(image_urls)
        return JsonResponse({'images': image_urls[:5]}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def create_dataset(request):
    if request.method == 'POST':
        user = request.user
        dataset_name = request.POST.get('dataset_name')
        if not dataset_name:
            return JsonResponse({'error': 'Dataset name is required'}, status=400)
        
        user_media_folder = os.path.join(UPLOAD_FOLDER, user.username)
        dataset_folder = os.path.join(user_media_folder, dataset_name)
        
        if not os.path.exists(dataset_folder):
            os.makedirs(dataset_folder)
            return JsonResponse({'message': 'Dataset created successfully'}, status=201)
        else:
            return JsonResponse({'error': 'Dataset already exists'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def delete_dataset(request):
    if request.method == 'GET':
        user = request.user
        dataset_name = request.GET.get('dataset')
        print(dataset_name)
        if not dataset_name:
            return JsonResponse({'error': 'Dataset name is required'}, status=400)
        
        user_media_folder = os.path.join(UPLOAD_FOLDER, user.username)
        dataset_folder = os.path.join(user_media_folder, dataset_name)
        
        if not os.path.exists(dataset_folder):            
            return JsonResponse({'error': 'No dataset selected'}, status=400)
        else:
            os.rmdir(dataset_folder)
            return JsonResponse({'message': 'Dataset deleted successfully'}, status=200)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def list_datasets(request):
    if request.method == 'GET':
        user = request.user
        user_media_folder = os.path.join(UPLOAD_FOLDER, user.username)
        
        if not os.path.exists(user_media_folder):
            return JsonResponse({'datasets': []}, status=200)
        
        datasets = [d for d in os.listdir(user_media_folder) if os.path.isdir(os.path.join(user_media_folder, d))]
        return JsonResponse({'datasets': datasets}, status=200)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)  
