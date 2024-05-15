from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'gemini_app'

urlpatterns = [
   path('chat-Gemini/',views.gemini_view, name='chat-Gemini'),
   path('',views.home_view, name='home'),
   path('register/',views.register_view, name='register'),
   path('login/',views.login_view, name='login'),
   path('logout/',views.logout_view, name='logout'),

]
