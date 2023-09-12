from rest_framework import viewsets
from .serializers import PermissionSerializer,DeviceSerializer,DeviceTypeserializers
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import HttpResponse,HttpRequest,JsonResponse
from app1.models import User,Account,Device,DeviceType,CustomPermission,Parameter
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import random
from django.utils import timezone
from datetime import timedelta
import pandas as pd
from django.shortcuts import get_object_or_404
from datetime import datetime
import os

# Create your views here.


#def get_csrf(request):
#    global csrf_token1
#    csrf_token1=get_token(request)
#    return JsonResponse({"csrf_token":csrf_token1})

@csrf_exempt
def login(request):
    if request.method == 'POST':
       userdata=JSONParser().parse(request)
       phone=userdata.get('mobileno')
       password=userdata.get('password')
       try:
            users=User.objects.get(Mobno=phone)
            if phone == users.Mobno and users.user_type == "general":
                print("yessss")
                if phone == users.Mobno and password != users.password:
                    return JsonResponse("Invalid Password For General User",safe=False)
                elif phone == users.Mobno and password == users.password:
                    return JsonResponse({"Login Successful For General User" : users.Name},safe=False)
            elif phone == users.Mobno and users.user_type == "admin":
                 if phone == users.Mobno and password != users.password:
                     return JsonResponse("Invalid Password For Admin",safe=False)
                 elif phone == users.Mobno and password == users.password:
                     return JsonResponse({"Login Successful For Admin" : users.Name},safe=False)
       except:
            return JsonResponse("Invalid Credentials",safe=False)


@csrf_exempt
def account_create(request):
    if request.method == 'POST':
       account_page = JSONParser().parse(request)
       account_nm=account_page.get('accountname')
       user_mobno=account_page.get('usermobno')
       print(account_nm)
       try:
           if Account.objects.filter(account_name=account_nm).exists():
                return JsonResponse({"error":"Account already exists"})
           else:
            while True:
                 user_instance = User.objects.get(Mobno=user_mobno)
                 accountid=random.randrange(100000000,9999999999999)
                 print(accountid)
                 if not Account.objects.filter(Account_id=accountid).exists():
                     accountsave=Account(account_name=account_nm, Account_id=accountid,user=user_instance)
                     accountsave.save()
                     return JsonResponse({"message":"Account created"})
                 else:
                     pass
               
       except Exception as e:
             return JsonResponse({'error': str(e)}, status=500)
       

           
@csrf_exempt
def user_create(request):
    if request.method=="POST":
       user = JSONParser().parse(request)
       fname=user.get('firstname')
       lname=user.get('lastname')
       email=user.get('email')
       mobno=user.get('mobileno')
       password=user.get('password')
       usertype=user.get('usertype')
       fullname = fname+" "+lname
       try:
            if not User.objects.filter(Mobno=mobno).exists():
                user=User(Name=fullname,Email=email,Mobno=mobno,password=password,user_type=usertype)
                user.save()
                return JsonResponse({"message":"User Created"})
            else:
                return JsonResponse({"message":"User already exists,Report to Admin"})
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

@csrf_exempt
def account_view(request,mobno):
    try:
        if request.method == 'GET':
            list=Account.objects.filter(user=mobno)
            final_list = [(list.account_name,list.Account_id) for list in list]
            if final_list:
                return JsonResponse({"items":final_list})
            else:
                return JsonResponse({'error': 'Account does not exist'}, status=400)
        else:
            return JsonResponse({'error': 'Account does not exist'}, status=400)
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def user_view(request):
    try:
        if request.method == 'GET':
            list=User.objects.all()
            final_list1 = [(list.Name,list.Mobno,list.user_type) for list in list]
            return JsonResponse({"items":final_list1})
        else:
            pass
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    

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
                    new_device = Device(device_name=device_nm, device_type=device_type_instance, account=account, device_id=random_id)
                    new_device.save()
                    return JsonResponse({'message': 'Device created successfully'}, status=201)
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
            device_type_list = [(device.device_id,device.device_name,(device.device_type.Name)) for device in device_list]
            return JsonResponse({"result": device_type_list})    
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def permission_save(request,user_id):
    if request.method=="POST":
        device=JSONParser().parse(request)
        usercreate = device.get('usercreate')
        useredit = device.get('useredit')
        userdelete = device.get('userdelete')
        userview = device.get('userview')
        accountcreate = device.get('accountcreate')
        accountedit = device.get('accountedit')
        accountdelete = device.get('accountdelete')
        accountview = device.get('accountview')
        devicecreate = device.get('devicecreate')
        deviceedit = device.get('deviceedit')
        devicedelete = device.get('devicedelete')
        deviceview = device.get('deviceview')
        deviceinstruction = device.get('deviceinstruction')
        setting = device.get('setting')
        print(setting)
        if CustomPermission.objects.filter(user=user_id).exists():
            user_dlt = CustomPermission.objects.filter(user=user_id)
            user_dlt.delete()
            print("yes available")
            CustomPermission.objects.filter(user=user_id)
            userid = User.objects.get(Mobno=user_id)
            datasave=CustomPermission(user=userid,User_create=usercreate,User_edit=useredit,User_delete=userdelete,User_views=userview,Account_create=accountcreate,Account_edit=accountedit,Account_delete=accountdelete,Account_views=accountview,Device_create=devicecreate,Device_edit=deviceedit,Device_delete=devicedelete,Device_views=deviceview,Device_instruction=deviceinstruction,Setting=setting)
            datasave.save()
            return JsonResponse({"message":"saved"})
        else:
            userid = User.objects.get(Mobno=user_id)
            datasave=CustomPermission(user=userid,User_create=usercreate,User_edit=useredit,User_delete=userdelete,User_views=userview,Account_create=accountcreate,Account_edit=accountedit,Account_delete=accountdelete,Account_views=accountview,Device_create=devicecreate,Device_edit=deviceedit,Device_delete=devicedelete,Device_views=deviceview,Device_instruction=deviceinstruction,Setting=setting)
            datasave.save()
            return JsonResponse({"message":"saved"})

    elif request.method=="GET":
        user = get_object_or_404(User, Mobno=user_id)
        permission = CustomPermission.objects.get(user=user)

        response_data = {
            'user_create' : permission.User_create,
            'user_edit' : permission.User_edit,
            'user_delete' : permission.User_delete,
            'user_view' : permission.User_views,
            'account_create' : permission.Account_create,
            'account_edit' : permission.Account_edit,
            'account_delete' : permission.Account_delete,
            'account_view' : permission.Account_views,
            'device_create' : permission.Device_create,
            'device_edit' : permission.Device_edit,
            'device_delete' : permission.Device_delete,
            'device_view' : permission.Device_views,
            'deviceinstruction' : permission.Device_instruction,
            'settings' : permission.Setting,
        }
        return JsonResponse({"message":response_data})
    
@csrf_exempt
def datefilter(request,device_id):
    data={
        'data':None,
        }
    if request.method=="GET":
        user_instance=JSONParser().parse(request)
        user_given_day=user_instance.get('day')
        data_type=user_instance.get('data_type')
        diff_time = timezone.now()-timedelta(days=user_given_day)    

        result = Parameter.objects.filter(date__gte=diff_time,device=device_id,param_type=data_type)
        obj = [dt.param_value for dt in result]
        data['data']=obj
        
        return JsonResponse({"message":data})
            

@csrf_exempt
def custom_datefilter(request,device_id):
    data={
        'data':None,
        }
    if request.method == "GET":
        user_instance = JSONParser().parse(request)
        start_date = user_instance.get('from')
        end_date = user_instance.get('to')
        data_type = user_instance.get('data_type')

        records = Parameter.objects.filter(date__range=(start_date, end_date),device=device_id,param_type=data_type)
        obj = [record.param_value for record in records]
        
        data['data'] = obj
           
        return JsonResponse({"message":data})
            


@csrf_exempt
def download_excel(request,device_id):
    if request.method == "GET":
        data = JSONParser().parse(request)
        start_date = data.get('from')
        end_date = data.get('to')
        data_type = data.get('data_type')

        records = Parameter.objects.filter(date__range=(start_date, end_date),device=device_id,param_type=data_type)

        id = [record.device.device_id for record in records]
        data = [record.param_value for record in records]
        
        dict_data = {
            "Device_id":id,
            "Data" : data
        }
        final_result = pd.DataFrame(dict_data)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=f"{data_type}_data.csv"'

        final_result.to_csv(response, index=False)

        return response
    

@csrf_exempt
def fixed_date_data_download(request,device_id):
    if request.method == "GET":
        data = JSONParser().parse(request)
        day = data.get('day')
        data_type = data.get('data_type')
        diff_time=timezone.now()-timedelta(days=day)

        result = Parameter.objects.filter(date__gte=diff_time,device=device_id,param_type=data_type)
        data = [dt.param_value for dt in result]
        id = [dt.device.device_id for dt in result]

        dict_data={
            "Device_id":id,
            "Data":data
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



















