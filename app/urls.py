from django.contrib import admin
from django.urls import path, include
from app.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', home, name='home_page'),
    path('predict_text',predict_text, name='predict'),
    path('audio_detect/', detect_cb_audio, name='audio-detection'),
    path('video_detect/', detect_cb_video, name='video-detect'),
]