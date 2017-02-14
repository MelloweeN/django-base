# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from .views import *
import views

urlpatterns = patterns('users.views',
	url(r'^login$', views.logIn, name='login'),
	url(r'^login-ajax$', views.loginAjax, name='login_ajax'),
	url(r'^logout$', views.logOut, name='logout'),

	url(r'^mi-cuenta$', login_required(views.miCuenta), name='mi_cuenta'),
	url(r'^mi-cuenta/editar$', login_required(views.miCuentaEditarAjax), name='mi_cuenta_editar'),

    url(r'^mantenedor/usuarios/lista$', views.mantenedorUsuarioLista, name='mantenedor_usuario_lista'),
)