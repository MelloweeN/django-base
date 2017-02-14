# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import connection

from django.contrib.auth import authenticate, login, logout

from .forms import *

import re
import os
import rut
import json
import string
from django.http import JsonResponse

def getMe(request):
	myId = request.user.id
	yo = usuario.objects.get(id=myId)
	return { "yo":yo,"request": request}

def logIn(request):
	if(request.user.id):
		#print request.user.id
		return HttpResponseRedirect("/")
	else:
		form = LoginForm()
		return render(request,'login.html',{"form": form})

def loginAjax(request):
	mimetype = 'application/json'
	results = []
	name_json = {}

	#Valida RUT
	r = rut.rut(request.POST["rut"])

	if r.isValid() or request.POST["rut"] == '':
		rutUser = string.replace(r.getFormated(), '.', '')
		rutUser = string.replace(rutUser, '-', '')
		rutUser = string.replace(rutUser, ' ', '')
		password = request.POST['password']
		user = authenticate(rut=rutUser, password=password)
		if user is not None:
			if user.is_active:
				name_json['respuesta'] = 'ok'
				login(request, user)

				#Registra el login en loginHistory
				history = loginHistory(usuario = user)
				history.save()
			else:
				name_json['respuesta'] = 'errorActiveUser'
		else:
			name_json['respuesta'] = 'errorUser'

	elif not r.isValid():
		name_json['respuesta'] = 'errorRut'

	results.append(name_json)
	data = json.dumps(results)
	return HttpResponse(data,mimetype)

def logOut(request):
	logout(request)
	return redirect('/login')

def miCuenta(request):
	contextData = getMe(request)

	user = usuario.objects.get(id=request.user.id)
	form = userForm(instance = user)

	contextData.update({
		'form':form
	})
	return render(request,'perfil.html',contextData)

def miCuentaEditarAjax(request):
	mimetype = 'application/json'
	results = []
	name_json = {}
	errores = []
	persona = usuario.objects.get(id=request.user.id)

	if request.is_ajax():
		data = {}
		form = userForm(request.POST, instance = persona)


		if form.is_valid():
			if 'avatar' in request.FILES:
				form.instance.avatar = request.FILES['avatar']
				name_json['avatar'] = 'media/uploads/avatar/'+str(request.FILES['avatar'])

			user = form.save()
			if 'password' in request.POST  and request.POST['password']: #Si viene password y trae datos
				#Encripta y Guarda la contraseña
				usuario.setPassword(user,user.id, user.password)

			name_json['respuesta'] = 'ok'
			name_json['usuario_id'] = user.id
		else:
			name_json['respuesta'] = 'errorForm'
			errores = json.dumps(form.errors)
			name_json['errores'] = form.errors
	else:
		name_json['respuesta'] = 'error'

	results.append(name_json)
	data = json.dumps(results)
	return HttpResponse(data,mimetype)

def mantenedorUsuarioLista(request):
	contextData = getMe(request)
	return render(request,'mantenedores/usuarios/lista.html',contextData)
