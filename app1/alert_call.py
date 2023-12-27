import psycopg2
from django.core.mail import send_mail
from django.db import connection
def alert(device_id):
    conn = connection.cursor()  
    print(device_id)
    conn.execute(f'select param_type,param_value from app1_parameter where "device_id"={device_id} order by id desc limit 50;') 
    data = conn.fetchall()
    # print(data)
    Sensor1=[]
    Sensor2=[]
    Sensor3=[]
    Sensor4=[]
    
    for i in data:
        a = [m for m in i]
        if a[0]=='Sensor1':
            Sensor1.append(a[1])
        if a[0]=='Sensor2':
            Sensor2.append(a[1])
        if a[0]=='Sensor3':
            Sensor3.append(a[1])
        if a[0]=='Sensor4':
            Sensor4.append(a[1])
    # print(Sensor1,Sensor2,Sensor3,Sensor4)
    if  Sensor1 and Sensor2 and Sensor3 and Sensor4:
        print("data is  there")
    else:
        import datetime
        print("data is not there")
        # from twilio.rest import Client
        # account_sid = "ACc6e3e4c321caf63ea5bb6950c3557733"
        # auth_token = "bbf3e6c3d3e9c3b62d952ac30350f1b1"
        # client = Client(account_sid, auth_token)
        # call = client.calls.create(
        #   url="http://demo.twilio.com/docs/voice.xml",
        #   to="+918249970090",
        #   from_="+15343445060"
        # )
        # print(call.sid)
        body = f"Hi Admin,\nThis massage is regarding your device {device_id}. This device fails at {datetime.datetime.now()}"
        subject = "Alert Message"
        send_mail(
            subject,
            body,
            'care.bariflolabs@gmail.com',
            ["gaurab.bariflo@outlook.com"],
            fail_silently=False,    
            )
        print("email sent")