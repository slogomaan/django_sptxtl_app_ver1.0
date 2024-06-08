from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transcribe/', views.transcribe_audio_view, name='transcribe_audio'),
    path('send_email/', views.send_email, name='send_email'),
]
