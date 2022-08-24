from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.instagram_view, name='instagram_url'),
    path('download/<int:pk>/stories/', views.instagram_download_view, {'stories': True}, name='instagram_download_url'),
    path('download/<int:pk>/', views.instagram_download_view, {'stories': False}, name='instagram_download_url'),
    path('clean-media/', views.clean_media_view, name='clean_media_url'),
]
