
from django.contrib import admin
from app1 import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from app1.tests import uid
# router = DefaultRouter()
# router.register(r'permissions', views.PermissionViewSet)
# a = uid()

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('registration/',views.registration),
    path('register_view/<int:mobno>/',views.register_view),
    path('login/',views.login),
    path('account_view/<int:mobno>/',views.account_view),
    path('device_create/',views.device_create),
    path('device_edit/',views.device_edit),
    path('device_delete/',views.device_delete),
    path('device_view/<int:account_id>/',views.device_view),
    path('user/',views.user_create),
    path('account/',views.account_create),
    path('user_view/<mobno>/',views.user_view),
    path('user_edit/',views.user_edit),
    path('user_delete/',views.user_delete),
    path('account_edit/',views.account_edit),
    path('account_delete/',views.account_delete),
    path('datefilter/<int:device_id>/<int:user_given_day>/',views.datefilter),
    path('custom_datefilter/<int:device_id>/<from_date>/<to_date>/',views.custom_datefilter),
    path('fixedexcel/<int:device_id>/<str:data_type>/<int:user_given_day>/',views.fixed_date_data_download),
    path('customexcel/<int:device_id>/<str:data_type>/<from_date>/<to_date>/',views.custom_date_data_download),
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
    path('email_send/<mobno>/',views.email_send),
    path('email_verification/',views.forgot_password_email_verification),
    path('password_sent/<user_email>/',views.forgot_password_sent_to_user),
    path('token_verification/',views.token_verification),
    path('thermal_img/<mobno>/<int:user_given_day>/',views.thermal_actual_image),
    path('ocr/',views.ocr),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#imp for what you want to achieve.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)