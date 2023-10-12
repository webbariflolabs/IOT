
from django.contrib import admin
from app1 import views
from django.urls import path, include

# router = DefaultRouter()
# router.register(r'permissions', views.PermissionViewSet)


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('registration/',views.registration),
    path('login/',views.login),
    path('account_view/<int:mobno>/',views.account_view),
    path('device_create/',views.device_create),
    path('device_edit/',views.device_edit),
    path('device_delete/',views.device_delete),
    path('device_view/<int:account_id>/',views.device_view),
    path('user/',views.user_create),
    path('account/',views.account_create),
    path('permission/<int:user_id>/',views.permission_save),
    path('user_view/<arg>/',views.user_view),
    path('user_edit/',views.user_edit),
    path('user_delete/',views.user_delete),
    path('account_edit/',views.account_edit),
    path('account_delete/',views.account_delete),
    path('datefilter/<int:device_id>/<int:user_given_day>/',views.datefilter),
    path('custom_datefilter/<int:device_id>/<from_date>/<to_date>/',views.custom_datefilter),
    path('fixedexcel/<int:device_id>/<str:data_type>/<int:user_given_day>/',views.fixed_date_data_download),
    path('customexcel/<int:device_id>/<str:data_type>/<from_date>/<to_date>/',views.download_excel),
    path('devicetype_create/',views.devicetype_create),
    path('devicetype_edit/',views.devicetype_edit),
    path('devicetype_view/',views.devicetype_view),
    path('devicetype_delete/',views.devicetype_delete),
    path('mqtt/',views.mqtt),
    path('on_off_control/',views.on_off_controls),
    path('slider_control/',views.slider_controls),
    path('graph_control/',views.graph_controls),
    path('controls_view/<str:type_name>/<int:type_ver>/',views.controls_view),
    path('control_delete/',views.control_delete),
    path('on_off_control_edit/',views.on_off_control_edit),
    path('slider_control_edit/',views.slider_control_edit),
    path('graph_control_edit/',views.graph_control_edit),
    
]
