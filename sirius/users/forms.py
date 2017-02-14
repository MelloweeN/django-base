# -*- coding: utf-8 -*-
from django import forms
#from django.forms import *
from models import *

class LoginForm(forms.Form):
	rut = forms.CharField(label="Rut", max_length=12)
	password = forms.CharField(label="Password", max_length=50,
		widget = forms.TextInput(attrs = {'type':'password'}))

class userForm(forms.ModelForm):

	nombres =  forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'readonly':'True'}))
	apellidoPaterno =  forms.CharField(label="Apellido Paterno", widget=forms.TextInput(attrs={'readonly':'True'}))
	apellidoMaterno =  forms.CharField(label="Apellido Materno", widget=forms.TextInput(attrs={'readonly':'True'}))
	password =  forms.CharField(required=False, widget=forms.PasswordInput())
	email =  forms.EmailField(widget=forms.TextInput(attrs={'readonly':'True'}))

	class Meta:
		model = usuario
		fields=["nombres","apellidoPaterno","apellidoMaterno","email","password"]
