from rest_framework import viewsets
from .serializers import *
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import HttpResponse,HttpRequest,JsonResponse
from app1.models import *
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import random
from django.utils import timezone
from datetime import timedelta
import pandas as pd
from django.shortcuts import get_object_or_404
from datetime import datetime
from paho.mqtt.client import Client
import json
from django.core.mail import send_mail
from rest_framework.decorators import api_view
import psycopg2 
from django.conf import settings  
from rest_framework.decorators import parser_classes
from django.db import connection
# Create your views here.


#def get_csrf(request):
#    global csrf_token1
#    csrf_token1=get_token(request)
#    return JsonResponse({"csrf_token":csrf_token1})
@csrf_exempt
def token_verification(request):
    if request.method == 'POST':
        jsondata = JSONParser().parse(request)
        category = jsondata.get('category')
        token = jsondata.get('token')

        try:
            if category == 'aquaUser':
                data = User.objects.get(token=token)
                return JsonResponse({'message': 'Authenticated successfully.',"username":data.Name,"mobile_no":data.Mobno})
            else:
                data = AdminUser.objects.get(token=token)
                return JsonResponse({'message': 'Authenticated successfully.',"username":data.Name,"mobile_no":data.Mobno})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        regd_instance=JSONParser().parse(request)
        firstname=regd_instance.get('firstname')
        lastname=regd_instance.get('lastname')
        email=regd_instance.get('email')
        mobno=regd_instance.get('mobno')
        adhaar=regd_instance.get('adhaar')
        accountname=regd_instance.get('accountname')
        devicedetails=regd_instance.get('devicedetails')
        user_cat=regd_instance.get('user_cat')
        fullname=firstname+" "+lastname
        instance=Registration.objects.filter(Mobno=mobno)
        
        try:
            if not instance.exists():
                datas = Registration(Name=fullname,Email=email,Mobno=mobno,Adhaar=adhaar,account_name=accountname,device_details=devicedetails,user_category=user_cat)
                datas.save()
                return JsonResponse({"massage":"Registration Successfull"})
            else:
                return JsonResponse({"massage":"User Mobile number already registered, Report to Admin"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

@csrf_exempt        
def login(request):
    if request.method == 'POST':
        userdata=JSONParser().parse(request)
        phone=userdata.get('mobileno')
        password=userdata.get('password')
    #    try:
        if type(phone)==int:
            if User.objects.filter(Mobno=phone).exists():
                users = User.objects.get(Mobno=phone)
                if phone == users.Mobno and str(users.user_category) == "3d" and password == users.password:
                    return JsonResponse({'message':"Login Successfull For 3D User",'username':users.Name,'mobno':users.Mobno})
                elif phone == users.Mobno and str(users.user_category) == "water" and password == users.password:
                    return JsonResponse({'message':"Login Successfull For waterbody User",'username':users.Name,'mobno':users.Mobno})
                elif phone == users.Mobno and str(users.user_category) == "aqua" and password == users.password:
                    return JsonResponse({'message':"Login Successfull For aqua User",'username':users.Name,'mobno':users.Mobno})
                else:  
                    return JsonResponse({'error':"Invalid credential for General user"})
            if AdminUser.objects.filter(Mobno=phone).exists():
                admin = AdminUser.objects.get(Mobno=phone)
                if phone == admin.Mobno and str(admin.user_category) == "3d" and password == admin.password:
                    return JsonResponse({'message':"Login Successfull For 3D Admin",'username':admin.Name,'mobno':admin.Mobno})
                elif phone == admin.Mobno and str(admin.user_category) == "water" and password == admin.password:
                    return JsonResponse({'message':"Login Successfull For waterbody Admin",'username':admin.Name,'mobno':admin.Mobno})
                elif phone == admin.Mobno and str(admin.user_category) == "aqua" and password == admin.password:
                    return JsonResponse({'message':"Login Successfull For aqua Admin",'username':admin.Name,'mobno':admin.Mobno})
                else:  
                    return JsonResponse({'error':"Invalid credential for Admin user"})
        if type(phone)==str:
            if User.objects.filter(Email=phone).exists():
                users=User.objects.get(Email=phone)
                if phone == users.Email and str(users.user_category) == "3d" and password == users.password:
                    return JsonResponse({'message':"Login Successfull For 3D User",'username':users.Name,'mobno':users.Mobno})
                elif phone == users.Email and str(users.user_category) == "water" and password == users.password:
                    return JsonResponse({'message':"Login Successfull For waterbody User",'username':users.Name,'mobno':users.Mobno})
                elif phone == users.Email and str(users.user_category) == "aqua" and password == users.password:
                    return JsonResponse({'message':"Login Successfull For aqua User",'username':users.Name,'mobno':users.Mobno})
                else:  
                    return JsonResponse({'error':"Invalid credential for general user"})
            if SuperAdmin.objects.filter(Username=phone).exists():
                admin = SuperAdmin.objects.get(Username=phone)
                if phone == admin.Username and password == admin.Password:
                    return JsonResponse({'message':"Login Successfull For  SuperAdmin",'username':admin.Username,'password':admin.Password})
                else:  
                    return JsonResponse({'error':"Invalid credential for SuperAdmin user"})
            if AdminUser.objects.filter(Email=phone).exists():
                admin = AdminUser.objects.get(Email=phone)
                print(admin.user_img)
                if phone == admin.Email and str(admin.user_category) == "3d" and password == admin.password:
                    return JsonResponse({'message':"Login Successfull For 3D Admin",'username':admin.Name,'mobno':admin.Mobno})
                elif phone == admin.Email and str(admin.user_category) == "water" and password == admin.password:
                    return JsonResponse({'message':"Login Successfull For waterbody Admin",'username':admin.Name,'mobno':admin.Mobno})
                elif phone == admin.Email and str(admin.user_category) == "aqua" and password == admin.password:
                    return JsonResponse({'message':"Login Successfull For aqua Admin",'mobno':admin.Mobno,'username':admin.Name})
                else:  
                    return JsonResponse({'error':"Invalid credential for Admin user"})
            else:  
                return JsonResponse({'error':"Invalid credential for Admin user"})
    #    except:
    #         return JsonResponse("Invalid Credentials",safe=False)


@csrf_exempt
def account_create(request):
    if request.method == 'POST':
        account_page = JSONParser().parse(request)
        account_nm=account_page.get('accountname')
        user_mobno=account_page.get('usermobno')
        lat = account_page.get('lat')
        long = account_page.get('long')
        address = account_page.get('address')
        print(account_nm)
    #    try:
        if Account.objects.filter(account_name=account_nm,user=user_mobno).exists():
            return JsonResponse({"error":"Account already exists"})
        else:
            while True:
                user_instance = User.objects.get(Mobno=user_mobno)
                accountid=random.randrange(100000000,9999999999999)
                print(accountid)
                if not Account.objects.filter(Account_id=accountid).exists():
                    location = Point(float(lat),float(long))
                    accountsave=Account(account_name=account_nm, Account_id=accountid,user=user_instance,location=location,area=address)
                    accountsave.save()
                    return JsonResponse({"message":"Account created","accountid":accountid},safe=False)
                else:
                    pass
                
    #    except Exception as e:
    #          return JsonResponse({'error': str(e)}, status=500)
       

@api_view(['POST'])          
@csrf_exempt
def user_create(request):
    if request.method=="POST":
    #    user = JSONParser().parse(request)
       mobno=request.data['mobileno']
       password=request.data['password']
       user_pic=request.data['user_pic']
       user_docs=request.data['user_docs']

       try: 
            token = get_token(request)
            user_instance = Registration.objects.get(Mobno=mobno)
            user_category_instance = AdminUser.objects.get(user_category=user_instance.user_category)
            if not User.objects.filter(Mobno=mobno).exists():
                user=User(Name=user_instance.Name,Email=user_instance.Email,Mobno=mobno,password=password,Adhaar=user_instance.Adhaar,user_pic=user_pic,user_docs=user_docs,user_category=user_category_instance,token=token)
                user.save()
                param = {
                    'host':'20.244.37.91',
                    'database':'logindb',
                    'user':'bariflolabs',
                    'password':'bariflo2024'
                    }
                conn = psycopg2.connect(**param)
                print("connected")
                cur = conn.cursor() 
                cur.execute('INSERT INTO public.myapp_user("Name", "Email", "Mobno", "password", "Adhaar", "token", "user_category") VALUES (%s, %s, %s, %s, %s, %s, %s);', (f'{user_instance.Name}', f'{user_instance.Email}', f'{user_instance.Mobno}', f'{password}', f'{user_instance.Adhaar}', f'{token}', f'{user_category_instance}'))
                conn.commit()
                return JsonResponse({"message":"User Created"})
            else:
                return JsonResponse({"message":"User already exists,Report to Admin"})
       except Exception as e:
             return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def register_view(request,mobno):
    try:
        if request.method == 'GET':
            ins = AdminUser.objects.get(Mobno=mobno)
            print(ins)
            data=Registration.objects.filter(user_category=ins)
            print(data)
            final_list = [(data.Name,data.Mobno,data.Email,data.params,data.Adhaar,data.user_category) for data in data]
            return JsonResponse({"items":final_list})
        else:
            pass
    except Exception as e:  
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def user_view(request,mobno):
    try:
        if request.method == 'GET':
            ins = AdminUser.objects.get(Mobno=mobno)
            list=User.objects.filter(user_category=ins)
            final_list1 = [(list.Name,list.Mobno,list.Email) for list in list]
            return JsonResponse({"items":final_list1})
        else:
            pass
    except Exception as e:  
            return JsonResponse({'error': str(e)}, status=500)
       
@csrf_exempt
def account_edit(request):
    if request.method=='POST':
        account=JSONParser().parse(request)
        account_id=account.get('accountid')
        newname=account.get('newaccountname')
        try:
            accountid=Account.objects.get(Account_id=account_id)
            accountid.account_name=newname
            accountid.save()
            return JsonResponse({"message":"Account successfully updated"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
@csrf_exempt
def account_delete(request):
    if request.method=='POST':
        account=JSONParser().parse(request)
        accountid=account.get('accountid')
        print(accountid)
        try:
            get_accountdata=Account.objects.get(Account_id=accountid)
            print(get_accountdata)
            get_accountdata.delete()
            return JsonResponse({"message":"Account deleted successfully"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

from django.http import JsonResponse

from django.http import JsonResponse

@csrf_exempt
def account_view(request, mobno):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=mobno)
        final_list = []

        for account in accounts:
            dvc_data = Device.objects.filter(account=account.Account_id)
            device_ids = len([dvc.device_id for dvc in dvc_data])

            account_details = [
                account.account_name,
                account.Account_id,
                account.location.x,
                account.location.y,
                account.area
            ]

            if device_ids:
                account_details.append(device_ids)
            else:
                account_details.append(0)
            final_list.append(account_details)

        return JsonResponse({"items": final_list})


@csrf_exempt
def user_edit(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_mob = user_data.get('mobileno')
        new_user_name = user_data.get('newusername')
        new_user_email = user_data.get('newuseremail')
        usertype = user_data.get('usertype')
        try:
            user = User.objects.get(Mobno=user_mob)
            user.Name = new_user_name
            user.Email = new_user_email
            user.user_type = usertype
            user.save()
            return JsonResponse({'message': 'User updated successfully'}, status=200)
              
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
def user_delete(request):
    if request.method=='POST':
        user=JSONParser().parse(request)
        user_mob=user.get('mobileno')
        try:
            param = {
                    'host':'20.244.37.91',
                    'database':'logindb',
                    'user':'bariflolabs',
                    'password':'bariflo2024'
                    }
            conn = psycopg2.connect(**param)
            print("connected")
            cur = conn.cursor() 
            cur.execute(f'DELETE FROM public.myapp_user WHERE "Mobno"={user_mob};')
            conn.commit()
            user=User.objects.get(Mobno=user_mob)
            user.delete()
            return JsonResponse({"message":"User deleted successfully"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def device_create(request):
    if request.method == 'POST':
        device_data = JSONParser().parse(request)
        device_nm = device_data.get('devicename')
        device_tp_name = device_data.get('devicetype')
        accountid = device_data.get('accountid')
        
        try:
            account = Account.objects.get(Account_id=accountid)
            device_type_instance = DeviceType.objects.get(Name=device_tp_name)
            
            if Device.objects.filter(device_name=device_nm, account=account).exists():
                return JsonResponse({'error': 'Device name already exists for this account'}, status=400)
            
            while True:        
                random_id = random.randrange(10000000000000,999999999999999)
                print(random_id)
                if not Device.objects.filter(device_id=random_id).exists():
                    # params = {'host':'20.244.48.88','database':'iotdb','user':'bariflolabs','password':'bariflo123'}
                    # conn = connection.cursor()  
                    # print('Connected to the PostgreSQL database in device creation part...') 
                    # cur = conn.cursor() 
                    # conn.execute(f'CREATE TABLE device_{random_id}(device BIGINT NOT NULL,param_type VARCHAR NOT NULL,param_value INTEGER NOT NULL,date DATE NOT NULL,time TIME NOT NULL);')
                    # cur.close() 
                    # conn.commit() 
                    new_device = Device(device_name=device_nm, device_type=device_type_instance, account=account, device_id=random_id)
                    new_device.save()
                    return JsonResponse({'message':'Device created successfully'}, status=201)
                else:
                    pass
                
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
def device_edit(request):
    if request.method == 'POST':
        device_data = JSONParser().parse(request)
        device_id = device_data.get('deviceid')
        new_device_name = device_data.get('newdevicename')
        new_device_type_name = device_data.get('newdevicetype')

        try:
            device = Device.objects.get(device_id=device_id)
            
            device_type_instance, _ = DeviceType.objects.get_or_create(Name=new_device_type_name, defaults={'version': 1})
            
            device.device_name = new_device_name
            device.device_type = device_type_instance
            device.save()
            
            return JsonResponse({'message': 'Device updated successfully'}, status=200)
        except Device.DoesNotExist:
            return JsonResponse({'error': 'Device does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def device_delete(request):
    if request.method == 'POST':
        device_data = JSONParser().parse(request)
        device_id = device_data.get('deviceid')

        try:
            device = Device.objects.get(device_id=device_id)
            device.delete()
            return JsonResponse({'message': 'Device deleted successfully'}, status=200)
        except Device.DoesNotExist:
            return JsonResponse({'error': 'Device does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt 
def device_view(request,account_id):
    try:
        if request.method=="GET":
            device_list=Device.objects.filter(account=account_id)
            device_type_list = [(device.device_id,device.device_name,(device.device_type.Name),(device.device_type.version)) for device in device_list]
            return JsonResponse({"result": device_type_list})    
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def datefilter(request,device_id,user_given_day):
    if request.method=="GET":
        diff_time = timezone.now()-timedelta(days=user_given_day)   
        str_diff_time = diff_time.strftime("%Y-%m-%d") 
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM public.device_{device_id} WHERE date >= '{str_diff_time}';")
        data_list = cur.fetchall()
        paramtype = []
        time_set = []
        dataset =[]
        [paramtype.append(typ[1]) for typ in data_list if typ[1] not in paramtype]
        [time_set.append(typ[4]) for typ in data_list if typ[4] not in time_set]
        i=0
        while i < len(paramtype):
            b = [typ[2] for typ in data_list if typ[1]==paramtype[i]]
            dataset.append({paramtype[i]:b})
            i=i+1
    # data={}

    return JsonResponse((dataset,time_set),safe=False)
                

@csrf_exempt
def custom_datefilter(request,device_id,from_date,to_date):    #  Date format must be (YYYY-MM-DD)
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM public.device_{device_id} WHERE date BETWEEN '{from_date}' and '{to_date}';")
        data = cursor.fetchall()
        from collections import deque
        paramtype = deque([])
        time_set = []
        dataset =[]
        [paramtype.append(typ[1]) for typ in data if typ[1] not in paramtype]
        [time_set.append(typ[4]) for typ in data if typ[4] not in time_set]
        # print(d)
        i=0
        while i < len(paramtype):
            b = [typ[2] for typ in data if typ[1]==paramtype[i]]
            dataset.append({paramtype[i]:b})
            i=i+1
        return JsonResponse((dataset,time_set),safe=False)

            


@csrf_exempt
def custom_date_data_download(request,device_id,data_type,from_date,to_date):
    if request.method == "GET":
        records = Data.objects.filter(date__range=(from_date, to_date),device=device_id,param_type=data_type)
        data = [record.param_value for record in records]
        date = [record.date.strftime("%Y-%m-%d") for record in records]
        time = [record.time.strftime("%H:%M:%S") for record in records]
        
        dict_data = {
            "Device_id":id,
            "Values" : data,
            "Time" : time,
            "Date" : date,
        }
        final_result = pd.DataFrame(dict_data)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=f"{data_type}_data.csv"'

        final_result.to_csv(response, index=False)

        return response
    

@csrf_exempt
def fixed_date_data_download(request,device_id,user_given_day,data_type):
    if request.method == "GET":
        diff_time=timezone.now()-timedelta(days=user_given_day)

        result = Data.objects.filter(date__gte=diff_time,device=device_id,param_type=data_type)
        data = [dt.param_value for dt in result]
        id = [dt.device.device_id for dt in result]
        # data_time = [dt.device.date for dt in result]

        dict_data={
            "Device_id":id,
            "Data":data,

            } 
        final_result = pd.DataFrame(dict_data)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=f"{data_type}_data.csv"'

        final_result.to_csv(response, index=False)

        return response
           
            
@csrf_exempt
def devicetype_create(request):
    if request.method=="POST":
        devicetype=JSONParser().parse(request)
        typename=devicetype.get('typename')
        typeversion=devicetype.get('typeversion')
        try:
            if not DeviceType.objects.filter(Name=typename, version=typeversion).exists():
                data_save = DeviceType(Name=typename,version=typeversion)
                data_save.save()
                return JsonResponse({"message":"Devicetype Created"})
            else:
                return JsonResponse({"message":"Devicetype already exists"})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
def devicetype_edit(request):
    if request.method == "POST":
        devicetype=JSONParser().parse(request)
        old_device_type_name=devicetype.get('olddevicetypename')
        old_device_type_version=devicetype.get('olddevicetypeversion')
        new_typename=devicetype.get('newtypename')
        new_typeversion=devicetype.get('newtypeversion')
        print(new_typename)
        try:
            instance = DeviceType.objects.get(Name=old_device_type_name,version=old_device_type_version)
            print("instancee",instance)
            instance.Name = new_typename
            instance.version = new_typeversion
            if not DeviceType.objects.filter(Name=new_typename,version=new_typeversion).exists():
                instance.save()
                return JsonResponse({"message":"Saved"})
            else:
                return JsonResponse({"message":"Devicetype already exists,Rename it"})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 

@csrf_exempt
def devicetype_view(request):
    if request.method=="GET":
        devicetype = DeviceType.objects.all()
        result = [(i.Name,i.version) for i in devicetype]
        return JsonResponse({"results":result})
    
@csrf_exempt
def devicetype_delete(request):
    if request.method=="POST":
        devicetype=JSONParser().parse(request)
        devicetype_name=devicetype.get('devicetypename')
        devicetype_version=devicetype.get('devicetypeversion')
        device_dlt = DeviceType.objects.filter(Name=devicetype_name,version=devicetype_version)
        device_dlt.delete()
        return JsonResponse({"message":"Devicetype deleted"})

@csrf_exempt
def on_off_controls(request):
    cntrl_data1 ={
        "button":{
            "display_name":None,
            "virtual_pin":None,
            "allow_user":None,
            }
        }
    if request.method == 'POST':
        instance = JSONParser().parse(request)
        type_name = instance.get('type_name')
        type_ver = instance.get('type_ver')
        btn_dis = instance.get('btn_dis_name') if instance.get('btn_dis_name') else None
        btn_pin = instance.get('btn_pin') if instance.get('btn_pin') else None
        alw_usr = instance.get('alw_usr') if instance.get('alw_usr') else None

        instance = DeviceType.objects.get(Name=type_name,version=type_ver)
        if instance.controls == None:
            cntrl_data1['button']['display_name']=btn_dis
            cntrl_data1['button']['virtual_pin']=btn_pin
            cntrl_data1['button']['allow_user']=alw_usr
            print("instancccccccccccccccccccccccccccccce")
            # instance.delete()
            lis = []
            lis.append(cntrl_data1)
            instance.controls= lis
            instance.save()
            return JsonResponse({"message":"PIN assigned with a value in ON/OFF button"})

        key_list = []
        a = instance.controls
        if a:
            for dictionary in a:
                for key in dictionary.keys():
                    key_list.append(key)
            if 'button' not in key_list:
                cntrl_data1['button']['display_name']=btn_dis
                cntrl_data1['button']['virtual_pin']=btn_pin
                cntrl_data1['button']['allow_user']=alw_usr
                lis = instance.controls
                lis.append(cntrl_data1)
                instance.controls = lis
                instance.save()
                return JsonResponse({"message":"PIN assigned with a value in ON/OFF button"})
            elif 'button' in key_list: 
                vir_pin_list = []
                obj = instance.controls
                for dictionary in obj:
                    if 'button' in dictionary and 'virtual_pin' in dictionary['button']:
                        values = dictionary['button']['virtual_pin']
                        vir_pin_list.append(values)
                if btn_pin not in vir_pin_list:
                    cntrl_data1['button']['display_name']=btn_dis
                    cntrl_data1['button']['virtual_pin']=btn_pin
                    cntrl_data1['button']['allow_user']=alw_usr
                    lis = instance.controls
                    lis.append(cntrl_data1)
                    instance.controls = lis
                    instance.save()
                    return JsonResponse({"message":"PIN assigned with a value in ON/OFF button"})
                else:
                    return JsonResponse({"error":"PIN already assigned with a value in ON/OFF button"})
            else:
                return JsonResponse({"error":"PIN already assigned with a value in ON/OFF button"})

@csrf_exempt
def slider_controls(request):
    cntrl_data2 ={
        "slider":{
            "display_name":None,
            "virtual_pin":None,
            "min":None,
            "max":None,
            "step_value":None,
            "allow_user":None
            }
    }
    if request.method == 'POST':
        instance = JSONParser().parse(request)
        type_name = instance.get('type_name')
        type_ver = instance.get('type_ver')
        slider_dis = instance.get('slider_dis_name') if instance.get('slider_dis_name') else None
        slider_pin = instance.get('slider_pin') if instance.get('slider_pin') else None
        slider_min = instance.get('slider_min') if instance.get('slider_min') else None
        slider_max = instance.get('slider_max') if instance.get('slider_max') else None
        slider_step_value = instance.get('slider_step_value') if instance.get('slider_step_value') else None
        slider_allow_user = instance.get('slider_allow_user') if instance.get('slider_allow_user') else None
        instance = DeviceType.objects.get(Name=type_name,version=type_ver)
        a = instance.controls
        print(slider_pin)

        if a == None:
            cntrl_data2['slider']['display_name']=slider_dis
            cntrl_data2['slider']['virtual_pin']=slider_pin
            cntrl_data2['slider']['min']=slider_min
            cntrl_data2['slider']['max']=slider_max
            cntrl_data2['slider']['step_value']=slider_step_value
            cntrl_data2['slider']['allow_user']=slider_allow_user
            # instance.delete()
            lis = []
            lis.append(cntrl_data2)
            instance.controls= lis
            instance.save()
            return JsonResponse({"message":"PIN assigned with a value in slider"})

        if a:
            avlbl_lst = []
            for i in a:
                for key in i.keys():
                    avlbl_lst.append(key)
            if 'slider' not in avlbl_lst:
                cntrl_data2['slider']['display_name']=slider_dis
                cntrl_data2['slider']['virtual_pin']=slider_pin
                cntrl_data2['slider']['min']=slider_min
                cntrl_data2['slider']['max']=slider_max
                cntrl_data2['slider']['step_value']=slider_step_value
                cntrl_data2['slider']['allow_user']=slider_allow_user
                lis = a
                lis.append(cntrl_data2)
                instance.controls= lis
                instance.save()
                return JsonResponse({"message":"PIN assigned with a value in slider"})

            elif 'slider' in avlbl_lst:
                obj = instance.controls
                vir_pin = []
                for dictionary in obj:
                    if 'slider' in dictionary and 'virtual_pin' in dictionary['slider']:
                        values = dictionary['slider']['virtual_pin']
                        vir_pin.append(values)
                if slider_pin not in vir_pin:
                    cntrl_data2['slider']['display_name']=slider_dis
                    cntrl_data2['slider']['virtual_pin']=slider_pin
                    cntrl_data2['slider']['min']=slider_min
                    cntrl_data2['slider']['max']=slider_max
                    cntrl_data2['slider']['step_value']=slider_step_value
                    cntrl_data2['slider']['allow_user']=slider_allow_user
                    lis = a
                    lis.append(cntrl_data2)
                    instance.controls= lis
                    instance.save()
                    return JsonResponse({"message":"PIN assigned with a value in slider"})
                else:
                    return JsonResponse({"message":"PIN already assigned with a value in slider"})
            else:
                return JsonResponse({"error":"PIN already assigned with a in slider"})

@csrf_exempt
def graph_controls(request):
    cntrl_data3 ={
        "graph":{
            "display_name":None,
            # "params":[{"graph_label":None,"graph_color":None}],
            "params":None,
            "allow_user":None,
            "x":None,
            "y":None
        }
    }
    if request.method == 'POST':
        instance = JSONParser().parse(request)
        type_name = instance.get('type_name')
        type_ver = instance.get('type_ver')
        graph_dis = instance.get('graph_dis_name') if instance.get('graph_dis_name') else None
        params = instance.get('params') if instance.get('params') else None
        # graph_color = instance.get('graph_color') if instance.get('graph_color') else None
        alw_usr = instance.get('graph_allow_user') if instance.get('graph_allow_user') else None
        x = instance.get('x') if instance.get('x') else None
        y = instance.get('y') if instance.get('y') else None
        instance = DeviceType.objects.get(Name=type_name,version=type_ver)
        a = instance.controls

        if a == None:
            cntrl_data3['graph']['display_name']=graph_dis
            cntrl_data3['graph']['params']=params
            cntrl_data3['graph']['allow_user']=alw_usr
            cntrl_data3['graph']['x']=x
            cntrl_data3['graph']['y']=y
            # instance.delete()
            lis = []
            lis.append(cntrl_data3)
            instance.controls= lis
            instance.save()
            return JsonResponse({"message":"New Line graph created"})
        elif a:
            avlbl_lst = []
            for i in a:
                for key in i.keys():
                    avlbl_lst.append(key) 
            if 'graph' not in avlbl_lst:
                cntrl_data3['graph']['display_name']=graph_dis
                cntrl_data3['graph']['params']=params
                cntrl_data3['graph']['allow_user']=alw_usr
                cntrl_data3['graph']['x']=x
                cntrl_data3['graph']['y']=y
                lis = a
                lis.append(cntrl_data3)
                instance.controls = lis
                instance.save()
                return JsonResponse({"message":"New Line graph created"})
            elif 'graph' in avlbl_lst:
                disp_list = []
                for dictionary in a:
                    if 'graph' in dictionary and 'display_name' in dictionary['graph']:
                        values = dictionary['graph']['display_name']
                        disp_list.append(values)
                if graph_dis not in disp_list:
                    cntrl_data3['graph']['display_name']=graph_dis
                    cntrl_data3['graph']['params']=params
                    cntrl_data3['graph']['allow_user']=alw_usr
                    cntrl_data3['graph']['x']=x
                    cntrl_data3['graph']['y']=y
                    lis = a
                    lis.append(cntrl_data3)
                    instance.controls = lis
                    instance.save()
                    return JsonResponse({"message":"New Line graph created"})
            else:
                return JsonResponse({"message":"Line graph label already assigned"})
        else:
            return JsonResponse({"error":"Line graph label already assigned"})

@csrf_exempt
def controls_view(request,type_name,type_ver):
    if request.method == 'GET':
        instance = DeviceType.objects.get(Name=type_name,version=type_ver)
        a = instance.controls
        return JsonResponse(a,safe=False)


@csrf_exempt
def control_delete(request):
    if request.method == 'POST':
        delete_instance = JSONParser().parse(request)
        type_name = delete_instance.get('type_name')
        type_ver = delete_instance.get('type_ver')
        display_name = delete_instance.get('display_name')
        virtual_pin = delete_instance.get('virtual_pin')
        instance = DeviceType.objects.get(Name=type_name,version=type_ver)
        a = instance.controls
        lists = []
        for dict_list in a:
            lists.append(dict_list)
        for dict in lists:
            if 'button' in dict and 'display_name' in dict['button']:
                if 'button' in dict and 'virtual_pin' in dict['button']:
                    values1 = dict['button']['display_name']
                    values2 = dict['button']['virtual_pin']
                if display_name == values1 and virtual_pin == values2:
                    lists.remove(dict)
                    if len(lists) >= 1:
                        instance.controls = lists
                        instance.save()
                        return JsonResponse({"message":"Removed"})
                    else:
                        instance.controls = None
                        instance.save()
                        return JsonResponse({"message":"Removed"})
            if 'slider' in dict and 'display_name' in dict['slider']:
                if 'slider' in dict and 'virtual_pin' in dict['slider']:
                    values1 = dict['slider']['display_name']
                    values2 = dict['slider']['virtual_pin']
                if display_name == values1 and virtual_pin == values2:
                    lists.remove(dict)
                    if len(lists) >= 1:
                        instance.controls = lists
                        instance.save()
                        return JsonResponse({"message":"Removed"})
                    else:
                        instance.controls = None
                        instance.save()
                        return JsonResponse({"message":"Removed"})
            if 'graph' in dict and 'display_name' in dict['graph']:
                if 'graph' in dict and 'params' in dict['graph']:
                    values1 = dict['graph']['display_name']
                    values2 = dict['graph']['params']
                if display_name == values1 and virtual_pin == values2:
                    lists.remove(dict)
                    if len(lists) >= 1:
                        instance.controls = lists
                        instance.save()
                        return JsonResponse({"message":"Removed"})
                    else:
                        instance.controls = None
                        instance.save()
                        return JsonResponse({"message":"Removed"})
            


@csrf_exempt
def on_off_control_edit(request):
    if request.method == 'POST':
        edit_instance = JSONParser().parse(request)
        type_name = edit_instance.get('type_name')
        type_ver = edit_instance.get('type_ver')
        control_key = edit_instance.get('control_key')
        old_name = edit_instance.get('old_dis_name')
        old_vpin = edit_instance.get('old_vpin')
        new_name = edit_instance.get('new_dis_name')
        new_vpin = edit_instance.get('new_vpin')
        new_alwusr = edit_instance.get('new_alwusr')
        instance = DeviceType.objects.get(Name=type_name,version=type_ver)
        a = instance.controls
        
        for dictionary in a:
            if control_key in dictionary and 'display_name' in dictionary[control_key]:
                if control_key in dictionary and 'virtual_pin' in dictionary[control_key]:
                    value1 = dictionary[control_key]['display_name']
                    value2 = dictionary[control_key]['virtual_pin']
                    print(value1,value2)
                    if (value1==old_name and value2==old_vpin):
                        update_dict = {"button":{"display_name":new_name,"virtual_pin":new_vpin,"allow_user":new_alwusr}}
                        if update_dict not in a:
                            dictionary.update(update_dict)
                            instance.save()
                            return JsonResponse({"message":"control updated"})
                        else:
                            return JsonResponse({"message":"pin already in use"})
                    else:
                        pass

@csrf_exempt
def slider_control_edit(request):
    if request.method == 'POST':
        edit_instance = JSONParser().parse(request)
        type_name = edit_instance.get('type_name')
        type_ver = edit_instance.get('type_ver')
        control_key = edit_instance.get('control_key')
        old_name = edit_instance.get('old_dis_name')
        old_vpin = edit_instance.get('old_vpin')
        new_name = edit_instance.get('new_dis_name')
        new_vpin = edit_instance.get('new_vpin')
        new_min = edit_instance.get('new_min')
        new_max = edit_instance.get('new_max')
        new_step_value = edit_instance.get('new_step_value')
        new_alwusr = edit_instance.get('new_alwusr')
        instance = DeviceType.objects.get(Name=type_name,version=type_ver)
        a = instance.controls

        for dictionary in a:
            if control_key in dictionary and 'display_name' in dictionary[control_key]:
                if control_key in dictionary and 'virtual_pin' in dictionary[control_key]:
                    value1 = dictionary[control_key]['display_name']
                    value2 = dictionary[control_key]['virtual_pin']
                    print(value1,value2)
                    if (value1==old_name and value2==old_vpin):
                        update_dict = {"slider":{"display_name":new_name,"virtual_pin":new_vpin,"min":new_min,"max":new_max,"step_value":new_step_value,"allow_user":new_alwusr}}
                        if update_dict not in a:
                            dictionary.update(update_dict)
                            instance.save()
                            return JsonResponse({"message":"control updated"})
                        else:
                            return JsonResponse({"message":"pin already in use"})
                    else:
                        pass

@csrf_exempt
def graph_control_edit(request):
    if request.method == 'POST':
        edit_instance = JSONParser().parse(request)
        type_name = edit_instance.get('type_name')
        type_ver = edit_instance.get('type_ver')
        control_key = edit_instance.get('control_key')
        old_name = edit_instance.get('old_dis_name')
        new_name = edit_instance.get('new_dis_name')
        new_params = edit_instance.get('new_params')
        new_alwusr = edit_instance.get('new_alwusr')
        new_x = edit_instance.get('new_x')
        new_y = edit_instance.get('new_y')
        instance = DeviceType.objects.get(Name=type_name, version=type_ver)
        a = instance.controls
        
        for i in a:
            print("iii",i)
            for key in i:
                print("key",key)
                if control_key == key and i[control_key]['display_name'] == old_name:
                    print(i)
                    update_dict = {
                        "graph": {
                            "display_name": new_name,
                            "params": new_params,
                            "x": new_x,
                            "y": new_y,
                            "allow_user": new_alwusr
                        }
                    }
                    i.update(update_dict)
                    instance.save()
                    return JsonResponse({"message": "Updated"})
                else:
                    pass


@csrf_exempt
def email_send(request,mobno):
    if request.method == 'GET':
        regd_data = Registration.objects.filter(Mobno=mobno)
        user_data = User.objects.filter(Mobno=mobno)
        for i in regd_data:
            name = i.Name
            username = i.Mobno
            params = i.params
            usr_cat = i.user_category
            usr_email = i.Email
            # dvc_dtls = eval(i.device_details)
            data =[]
            for i in params:
                data.append(params[i])
            device = f"{data[1][0]['value']} Device {data[1][0]['count']}nos."

        for n in user_data:
            password=n.password

        body = f"Hi {name},\nWelcome to Bariflolabs Pvt. Ltd.\n\nNow you are a {usr_cat} user in Bariflolabs\njust below your all details are there. Please check it out.\n\nUsername : {username}\nPassword : {password}\nAccount Name : {data[0]}\nDevice details : {device}\n\n\nThanks and Regards\nM/S Bariflolabs Pvt. Ltd,Bhubaneswar"
        print(body)
        subject = "Succesfully Registered"
        send_mail(
            subject,
            body,
            "care.bariflolabs@gmail.com",
            [f"{usr_email}"],
            fail_silently=False,    
            )
        regd_data.delete()
        return JsonResponse({"message":"Email sent to the user successfully"},safe=False)

@csrf_exempt
def mqtt(request):
    if request.method == "POST":
        obj = JSONParser().parse(request)
        device_id = obj.get('deviceid')
        account_id = obj.get('accountid')
        v_pin = obj.get('virtualpin')
        value = obj.get('value')
        data = {
            "device_id":device_id,
            "account_id":account_id,
            "v_pin":v_pin,
            "value":value
        }
        mqtt = Client()
        mqtt.username_pw_set('BarifloLabs','Bfl@123')
        mqtt.connect('4.240.114.7',1883)
        mqtt.publish('',data)

@csrf_exempt
def forgot_password_email_verification(request):
    if request.method == 'POST':
        parse = JSONParser().parse(request)
        user_email = parse.get('email')
        data = User.objects.filter(Email=user_email)
        if data.exists():
            for i in data:
                pass
            otp = random.randrange(10000,99999)

            body = f"Hi {i.Name}, You have requested for forgot password\n\nThis is your OTP for user verifications\n\n\n {otp}\n\n\nThank you for being a part of Bariflolabs Pvt. Ltd ..."
            subject = "Request for Forgot Password"
            send_mail(
                subject,
                body,
                "care.bariflolabs@gmail.com",
                [f"{user_email}"],
                fail_silently=False,    
                )
            return JsonResponse({"message":"email verified! and otp sent to the user","otp":otp})
        else:
            return JsonResponse({"error":"entered email incorrect"})
        
@csrf_exempt
def forgot_password_sent_to_user(request,user_email):
    if request.method == 'GET':
        data = User.objects.get(Email=user_email)
        body = f"Hi {data.Name}, You have requested for forgot password before so, This is your User Password for user login\n\n{data.password}\n\n\nThank you for being a part of Bariflolabs Pvt. Ltd...."
        subject = "User login password"
        send_mail(
            subject,
            body,
            "care.bariflolabs@gmail.com",
            [f"{user_email}"],
            fail_silently=False,    
            )
        return JsonResponse({"message":"password sent to the user"})
    else:
        return JsonResponse({"error":"entered otp incorrect"})
    
@csrf_exempt
def thermal_actual_image(request,mobno,user_given_day):
    if request.method == 'GET':
        # instance = JSONParser().parse(request)
        diff_time = timezone.now()-timedelta(days=(user_given_day)) 
        str_diff_time = diff_time.strftime("%Y-%m-%d") 
        try:
            data = Thermal_Actual_Image.objects.filter(user=mobno,date__gte = str_diff_time).order_by('-id')[:2]
            a = [f"http://20.244.51.20/media/{i.image.name}" for i in data]
            return JsonResponse({"message":(a)})
        except:
            return JsonResponse({"eror":"AN ERROR OCCURED"},status=400)

from app1.ocr import testing 
@csrf_exempt
def ocr_process(request):
    if request.method == 'POST':
        instance = JSONParser().parse(request)
        mobno = instance.get('mobno')
        img_name = instance.get('imgname')
        try:
            processed_data = testing(mobno,img_name)
            return JsonResponse({"message": processed_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@api_view(['POST'])
@csrf_exempt
def ocr(request):
    if request.method == 'POST':
        img = request.data['image']
        mobno = request.data['mobno']
        user_data = User.objects.get(Mobno=mobno)
        data = OcrImage(image=img,user=user_data,name=user_data.Name)
        data.save()
        return JsonResponse({"message": "Image Uploaded"})

@csrf_exempt
def admin_side_ocr_view(request):
    if request.method == 'GET':
        try:
            data = OcrImage.objects.all()
            result = []
            for item in data:
                result.append([item.image.name, item.name, item.user.Mobno])
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
            
@csrf_exempt
def userside_graph_view(request,mobno):
    if request.method == 'GET':
        try:
            data_user = User.objects.get(Mobno=mobno)
            data_accnt = Account.objects.filter(user=data_user)
            final_data = {}
            for i in data_accnt:
                data_device = Device.objects.filter(account=(i.Account_id))
                print(data_device)
                for i in data_device:
                    data = {i.device_id : i.sensors}
                    final_data.update(data)
            return JsonResponse((final_data),safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def userside_device_view(request,mobno):
    if request.method == 'GET':
        try:
            data_user = User.objects.get(Mobno=mobno)
            data_accnt = Account.objects.filter(user=data_user)
            list_data = []
            for i in data_accnt:
                data = Device.objects.filter(account=(i.Account_id))
                for i in data:
                    device_type = DeviceType.objects.filter(Name=i.device_type)
                    for types in device_type:
                        final_output = [i.device_name,i.device_id,types.controls[0]['button']['virtual_pin']]
                        list_data.append(final_output)
            return JsonResponse((list_data),safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
def test(request,mobno):
    if request.method == 'GET':
        
        return JsonResponse({"msg"})     
