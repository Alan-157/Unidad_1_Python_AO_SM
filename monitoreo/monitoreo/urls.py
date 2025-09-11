"""
URL configuration for monitoreo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from dispositivos.views import dashboard,inicio,register,device_list,device_detail,measurement_list,alert_summary

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='dispositivos/login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='dispositivos/logout.html'), name='logout'), 
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='dispositivos/password_reset.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='dispositivos/password_reset_done.html'
    ), name='password_reset_done'),
    path('', inicio, name='inicio'),  # vista pública
    path('panel/', dashboard, name='dashboard'),  # dashboard protegido
    path('devices/', device_list, name='device_list'),
    path('devices/<int:device_id>/', device_detail, name='device_detail'),
    path('measurements/', measurement_list, name='measurement_list'),
    path('alerts/summary/', alert_summary, name='alert_summary'),
]

