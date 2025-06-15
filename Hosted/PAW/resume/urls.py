# File: resume/urls.py

from django.urls import path
from . import views

# URL patterns for the resume app
urlpatterns = [
    path('<str:username>/<str:action>/', views.pdf_resume_view, name='pdf_resume'),
    
]