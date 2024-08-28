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

from django.contrib.auth.decorators import login_required
# from .models import CustomUser


@login_required(login_url='gemini_app:login')
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

from django.contrib import messages

def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('gemini_app:chat-Gemini'))

    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, 'gemini_app/register.html', {'form': form})
        
        if len(password1) < 8 or len(password2) < 8:
            messages.error(request, "Password is too short")
            return render(request, 'gemini_app/register.html', {'form': form})
        
        if form.is_valid():

            form.save()
            messages.success(request, 'Account has been successfully created')
            return redirect('gemini_app:login')
    context = {'form': form,}
    # 'first_name':first_name, 'last_name':last_name
    return render(request, 'gemini_app/register.html',context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('gemini_app:chat-Gemini'))

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            first_name = user.first_name
            last_name = user.last_name
            return redirect(reverse('gemini_app:chat-Gemini'))
        else:
            messages.info(request, 'username or password is invalid')
    return render(request, 'gemini_app/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse('gemini_app:home'))
        
    return redirect(reverse('gemini_app:login'))
          
