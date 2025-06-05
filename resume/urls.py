from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<str:username>/<str:action>/', views.pdf_resume_view, name='resume_pdf'),
]