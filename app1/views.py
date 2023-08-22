from rest_framework import viewsets
# from django.contrib.auth.models import Permission
from .serializers import PermissionSerializer
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import HttpResponse,HttpRequest,JsonResponse
from app1.models import User,Account,Device,DeviceType,CustomPermission
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import random
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .serializers import Accountserializers
from django.db import transaction

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
            print(users.Mobno)
            print(users.password)
            print(users.user_type)
            if phone == users.Mobno and users.user_type == "general":
                print("yessss")
                if phone == users.Mobno and password != users.password:
                    return JsonResponse("Invalid Password For General User",safe=False)
                elif phone == users.Mobno and password == users.password:
                    return JsonResponse("Login Successful For General User",safe=False)
            elif phone == users.Mobno and users.user_type == "admin":
                 if phone == users.Mobno and password != users.password:
                     return JsonResponse("Invalid Password For Admin",safe=False)
                 elif phone == users.Mobno and password == users.password:
                     return JsonResponse("Login Successful For Admin",safe=False)
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
       name=user.get('name')
       email=user.get('email')
       mobno=user.get('mobileno')
       password=user.get('password')
       usertype=user.get('usertype')
       try:
            if not User.objects.filter(Mobno=mobno).exists():
                user=User(Name=name,Email=email,Mobno=mobno,password=password,user_type=usertype)
                user.save()
                return JsonResponse({"message":"User Created"})
            else:
                return JsonResponse({"message":"User alredy exist,Report to Admin"})
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
def account_view(request):
    try:
        if request.method == 'GET':
            accounts=JSONParser().parse(request)
            mobile_no=accounts.get('mobileno')
            list=Account.objects.filter(user=mobile_no)
            final_list = [list.account_name for list in list]
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
def device_view(request):
    if request.method=="GET":
        device=JSONParser().parse(request)
        account_id=device.get('accountid')
    try:
        device_list=Device.objects.filter(account=account_id)
        final_list=[list.device_name for list in device_list]
        if final_list:
            return JsonResponse({"result":final_list})
        else:
            return JsonResponse({'error': 'Device does not exists'}, status=400)
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def permission_save(request):
    if request.method=="POST":
        device=JSONParser().parse(request)
        usercreate = device.get('usercreate')
        useredit = device.get('useredit')
        userdelete = device.get('userdelete')
        user = device.get('username')
        user1 = User.objects.get(Mobno=user)
        datasave=CustomPermission(user_create=usercreate,user_edit=useredit,user_delete=userdelete,user=user1)
        datasave.save()
        print("save")
        return JsonResponse({"message":"saved"})



