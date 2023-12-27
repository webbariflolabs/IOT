import asyncio
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
import json
# from mqtt_listener import Command

class MySyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']  # Extract user_id from the URL
        await self.accept()

        while True:
            data = await self.get_data()  # No need to pass user_id here
            await self.send(json.dumps(data))

            await asyncio.sleep(10)

    @sync_to_async
    def get_data(self):
        import app1.psycopg_file as psy
        
        data = psy.connect(f"'{self.user_id}'")
        # print(data)

        return data
        # return ''

    @sync_to_async
    def websocket_disconnect(self, message):
        return super().websocket_disconnect(message)
    


























    
    #     from .models import Parameter
    #     data = {
    #     "ORP": None,
    #     "DO": None,
    #     "Ph": None,
    #     "CPU_TEMPERATURE": None,
    #     "Current": None,
    #     "voltage": None,
    #     "Time" : None,
    # }
    #     obj =Parameter.objects.filter(device_id=self.user_id)
    #     if not obj:

    #         print("No user found with the given ID")

    #     current_time = datetime.now().strftime("%H:%M:%S")
    #     current_date = datetime.now().date()
    #     for user in obj:
        
    #         user_time_str = user.time.strftime("%H:%M:%S")
    #         sixty_minutes_ago = timezone.localtime(timezone.now()) - timezone.timedelta(seconds=50)

            
    #         print("Current Time:", current_time) 
    #         print("User Time:", user_time_str)
    #         print("minute : ",sixty_minutes_ago)

    #         while user_time_str:
    #             orp_obj = Parameter.objects.filter(device_id=self.user_id, param_type="ORP",time__gte=sixty_minutes_ago,date=current_date)
    #             do_obj = Parameter.objects.filter(device_id=self.user_id, param_type="DO",time__gte=sixty_minutes_ago,date=current_date)
    #             ph_obj = Parameter.objects.filter(device_id=self.user_id, param_type="Ph",time__gte=sixty_minutes_ago,date=current_date)
    #             cpu_obj = Parameter.objects.filter(device_id=self.user_id, param_type="CPU_TEMPERATURE",time__gte=sixty_minutes_ago,date=current_date)
    #             curr_obj = Parameter.objects.filter(device_id=self.user_id, param_type="Current",time__gte=sixty_minutes_ago,date=current_date)
    #             volt_obj = Parameter.objects.filter(device_id=self.user_id, param_type="voltage",time__gte=sixty_minutes_ago,date=current_date)
    #             time_obj = Parameter.objects.filter(device_id=self.user_id,time__gte=sixty_minutes_ago,date=current_date)
                

    #             if orp_obj:
    #                 data["ORP"] = [i.param_value for i in orp_obj]
    #             if do_obj:
    #                 data["DO"] = [i.param_value for i in do_obj]
    #             if ph_obj:
    #                 data["Ph"] = [i.param_value for i in ph_obj]      
    #             if cpu_obj:
    #                 data["CPU_TEMPERATURE"] = [i.param_value for i in cpu_obj]
    #             if curr_obj:
    #                 data["Current"] = [i.param_value for i in curr_obj]
    #             if volt_obj:
    #                 data["voltage"] = [i.param_value for i in volt_obj]
    #             if time_obj:
    #                 a = []
    #                 for i in time_obj:
    #                     if (i.time.strftime('%H:%M:%S')) not in a:
    #                         a.append(i.time.strftime('%H:%M:%S'))
    #                         data["Time"] = a