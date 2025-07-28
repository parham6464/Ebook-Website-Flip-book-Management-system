from mimetypes import init
from django import forms 
from allauth.account.forms import LoginForm
from django.contrib.auth.forms import UserCreationForm , UserChangeForm 
from django.contrib.auth.forms import AuthenticationForm
from typing import Any
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from .models import Magazines
from django.forms import ModelForm, HiddenInput



class NewMagazineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewMagazineForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = HiddenInput()

    class Meta:
        model= Magazines
        fields = ('title_name' , 'title_picture' ,'pdf' , 'user' ,'tozihat' , 'category' , 'tags' , 'nashrie' , 'saheb_emtiaz' , 'modir_masol' , 'sar_dabir')



# class NewMagazineForm1(forms.Form):
#     title_name = forms.CharField(max_length=250 , label='موضوع مجله')
#     title_picture = forms.ImageField(label='عکس مجله')
#     pdf = forms.FileField(label='فایل پی دی اف')
    
