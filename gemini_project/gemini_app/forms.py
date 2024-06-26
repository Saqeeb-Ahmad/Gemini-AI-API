from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User
from django.forms import ModelForm

# from .models import CustomUser
 
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
