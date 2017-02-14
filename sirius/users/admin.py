# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import usuario,loginHistory
from django import forms
import rut


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = usuario
        fields = ('nombres', 'apellidoPaterno', 'apellidoMaterno', 'rut', 'email', 'password','groups','is_staff')

    def clean(self):
        userRut = rut.rut(self.cleaned_data["rut"])
       	if not userRut.isValid():
			raise forms.ValidationError("RUT no es válido")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        #Consulto si la password enviada por formulario es la mista que esta registrada
        #Si es distinta la encripto y guardo
        userPasswd = self.cleaned_data["password"]
        try:
            passwd = usuario.objects.get(rut=self.cleaned_data["rut"])
            passwd = passwd.password

            if userPasswd != passwd:
                user.set_password(userPasswd)
                user.save()
        except usuario.DoesNotExist:
            user.save()
            user.set_password(userPasswd)
        return user

@admin.register(usuario)
class UserAdmin(admin.ModelAdmin):
	form = UserCreationForm
	list_display = ('nombres', 'apellidoPaterno', 'apellidoMaterno', 'rut', 'email','is_staff')
	search_fields = ('nombres', 'apellidoPaterno', 'apellidoMaterno', 'rut', 'email')
	list_filter = ('groups',)

@admin.register(loginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):

	list_display = ('usuario', 'login')
