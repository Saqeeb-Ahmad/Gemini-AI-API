from audioop import reverse
from base64 import b64encode
from django.shortcuts import redirect, render
from django.urls import reverse
from .utils import configure_api
import google.generativeai as genai
from PIL import Image
import io

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm



def gemini_view(request):
    configure_api()
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        image_file = request.FILES.get('image')
        print(image_file)

        if image_file:
            image = Image.open(image_file)
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content([prompt, image], stream=True)
            response.resolve()
            generated_text = response.text
        else:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            generated_text = response.text
    else:
        generated_text = None

    context = {'generated_text': generated_text}
    return render(request, 'gemini_app/chat-Gemini.html', context)

def home_view(request):
    return render(request,'gemini_app/home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('gemini_app:login'))
    else:
        form = CustomUserCreationForm()

    return render(request, 'gemini_app/register.html', {'form':form} )
    
def login_view(request):
    return redirect(request, 'gemini_app/login.html')
