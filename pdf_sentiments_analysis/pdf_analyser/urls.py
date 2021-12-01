"""
urls module for pdf anaylser app
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.file_upload, name='upload_pdf')
]
