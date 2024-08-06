# urls for website

from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('app/', views.app, name='app'),
    path('upload/', views.upload_files, name='upload_files'),
    path('list_images/', views.list_images, name='list_images'),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)