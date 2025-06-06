from django.urls import path
from .views import pdf_resume_view

# URL patterns for the resume app
urlpatterns = [
    path('<str:username>/<str:action>/', pdf_resume_view, name='pdf_resume'),
]
