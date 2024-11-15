from django.urls import path
from . import views
from .views import upload_pdf

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('display_extracted_text/', views.display_extracted_text, name='display_extracted_text'),
   path('api/extract_pdf_text/', views.extract_pdf_text_api, name='extract_pdf_text_api'),  # New API endpoint
]