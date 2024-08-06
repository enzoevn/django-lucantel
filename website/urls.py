# urls for website

from django.urls import path, include
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('app/', views.app, name='app'),
]