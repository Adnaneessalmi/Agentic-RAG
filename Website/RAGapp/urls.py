from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name="overview"),
    path('chat/', views.chat, name="chat"),
]
