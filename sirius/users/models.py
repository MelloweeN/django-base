# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from datetime import datetime
from datetime import timedelta

import rut
from .valida_extension import *

class UserManager(BaseUserManager, models.Manager):
	def _create_user(self,email,password,is_staff,is_superuser,**extra_fields):
		email = self.normalize_email(email)
		if not email:
			raise ValueError('El email debe ser obligatorio')
		user = self.model(email = email, is_active = True, is_staff = is_staff, is_superuser = is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_user(self, email, password = None, **extra_fields):
		return self._create_user(email,password,False,False,**extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, password, True, True, **extra_fields)

class usuario(AbstractBaseUser,PermissionsMixin):
	CHOICES_CUENTA = ((1,"Si"),(0,"No"))
	username = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nombre de Usuario")
	rut = models.CharField(max_length=9, unique=True, blank=False, null=False, verbose_name="RUT")
	#dni = models.CharField(max_length=50, blank=True, null=True, verbose_name="DNI Extranjero")
	nombres = models.CharField(max_length=255, blank=False, null=False, verbose_name="Nombre")
	apellidoPaterno = models.CharField(max_length=50, blank=False, null=False, verbose_name="Apellido Paterno")
	apellidoMaterno = models.CharField(max_length=50, blank=False, null=False, verbose_name="Apellido Materno")
	#fechaNacimiento = models.DateField(blank=False, null=False, verbose_name="Fecha de Nacimiento")
	email = models.EmailField(unique=True, max_length=255, verbose_name="Email")
	#telefono = models.CharField(max_length=50, blank=True, null=True,verbose_name="Teléfono")
	#nacionalidad = models.CharField(default="Chilena", max_length=50, blank=False, null=False, verbose_name="Nacionalidad")
	#direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
	#numero = models.CharField(max_length=30, blank=True, null=True, verbose_name="Número")
	#departamento = models.CharField(max_length=50, blank=True, null=True, verbose_name="Departamento")
	#pais = models.CharField(default='(+56)', max_length=10, blank=True, null=True)
	#region = models.ForeignKey(provincia, blank=True, null=True, related_name="usuario_region", verbose_name="Región")
	#ciudad = models.ForeignKey(provincia, blank=True, null=True, related_name="usuario_ciudad")
	#comuna = models.ForeignKey(provincia, blank=True, null=True, related_name="usuario_comuna")
	avatar = models.ImageField(upload_to='uploads/avatar/',max_length=500, blank=True, null=True, validators=[valid_extension_image], verbose_name="Avatar")
	created_at = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False,auto_now=True)
	is_active = models.IntegerField(default=1,choices = CHOICES_CUENTA,verbose_name="Está Activo")
	is_staff = models.BooleanField(default=False,verbose_name="Pertenece al Staff de Administradores")

	#Llama y utiliza el manager antes creado
	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['nombres','apellidoPaterno','apellidoMaterno','rut'] #lista de campos requeridos

	def get_rut(self):
		r = rut.rut(self.rut)
		return r.getFormated()

	def get_short_name(self):
		return self.nombres

	def get_full_name(self):
		return "%s %s %s" % (self.nombres, self.apellidoPaterno, self.apellidoMaterno)

	def setPassword(self, userId, password):
		u = usuario.objects.get(id=userId)
		u.set_password(password)
		u.save()
		return "OK"

	def __unicode__(self):
		return "%s %s %s" % (self.nombres, self.apellidoPaterno, self.apellidoMaterno)
	class Meta:
		verbose_name_plural = "Usuarios"

class loginHistory(models.Model):
	usuario = models.ForeignKey(usuario, blank=False, null=False, verbose_name="Usuario")
	login = models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name="Logueado el")

	class Meta:
		verbose_name_plural = "Historial de Login"
