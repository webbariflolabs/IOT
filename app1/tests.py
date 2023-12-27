a= 10
b = 20
from datetime import datetime,timedelta
import time

delta1 = datetime.now() + timedelta(minutes=1)
delta2 = [delta1.strftime("%H:%M")]
timing = []
while input():
    cur2 = datetime.now().strftime("%H:%M")
    print(cur2)
    print(delta2)
    print(a+b)
    time.sleep(1)

    if cur2==delta2[0]:
        delta3 = datetime.now() + timedelta(minutes=1)
        delta4 = delta3.strftime("%H:%M")
        while True:
            cur4 = datetime.now().strftime("%H:%M")
            print(cur4)
            print(delta4)
            print(a+50)
            time.sleep(1)
            if cur4==delta4:
                delta5 = datetime.now()+timedelta(minutes=1)
                delta6 = delta5.strftime("%H:%M")
                delta2[0]=delta6
                break