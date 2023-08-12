from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import HttpResponse,HttpRequest,JsonResponse
from .models import User,Account
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import random
from .serializers import Accountserializers
# Create your views here.


#def get_csrf(request):
#    global csrf_token1
#    csrf_token1=get_token(request)
#    return JsonResponse({"csrf_token":csrf_token1})

@csrf_exempt
def login(request):
    if request.method == 'POST':
       userdata=JSONParser().parse(request)
       #csrf_token=request.headers.get('X-CSRFToken')
       #if csrf_token != csrf_token1:
       #   return JsonResponse({'error': 'Invalid CSRF token'}, status=403)
       phone=userdata.get('mobileno')
       password=userdata.get('password')
       try:
            users=User.objects.get(Mobno=phone)
            print(users.user_type)
            if phone == users.Mobno and users.user_type == "general":
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
       

def account_create(request):
    if request.method == 'POST':
       account_page = JSONParser().parse(request)
       account_name=account_page.get('accountname')
       accountid=account_page.get('id')
       try:
           accounts=Account.objects.get(account_name=account_name)
           if not accounts.DoesNotExist:
              accountnumber=accounts.Account_id
           else:
              accountnumber1=random.randrange(100000,999999)
              if accountnumber1 == accountnumber:
                  pass
              else :
                  pass                  
       except Exception as e:
         pass
       
@csrf_exempt
def admin_account_view(request):
    if request.method == 'GET':
       accounts=Account.objects.all()
       accountdata=Accountserializers(accounts,many=True)
       return JsonResponse(accountdata.data,safe=False)
    
@csrf_exempt
def general_account_view(request):
    if request.method == 'POST':
       accounts=JSONParser().parse(request)
       user_id=accounts.get('user_id')
       accountslist=Account.objects.filter(user_id=user_id)
       accountdata=Accountserializers(accountslist,many=True)
       return JsonResponse(accountdata.data,safe=False)

def device_create():
    pass
def device_edit():
    pass
def device_delete():
    pass      