"""
URL configuration for IOT_Dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app1 import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'permissions', views.PermissionViewSet)


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('account_view/',views.account_view),
    path('device_create/',views.device_create),
    path('device_edit/',views.device_edit),
    path('device_delete/',views.device_delete),
    path('device_view/',views.device_view),
    path('user/',views.user_create),
    path('account/',views.account_create),
    path('permission/',views.permission_save),
    path('user_view/',views.user_view),
    path('user_edit/',views.user_edit),
    path('user_delete/',views.user_delete),
    path('account_edit/',views.account_edit),
]
