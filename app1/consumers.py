import asyncio
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
import json
from app1.management.commands.mqtt_listener import Command
class MySyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']  # Extract user_id from the URL
        await self.accept()

        while True:
            data = await self.get_data()  # No need to pass user_id here
            await self.send(data)

            await asyncio.sleep(60)

    @sync_to_async
    def get_data(self):
        data = {
        "ORP": None,
        "DO": None,
        "Ph": None,
        "CPU_TEMPERATURE": None,
        "Current": None,
        "voltage": None
    }
        obj =Parameter.objects.filter(device_id=self.user_id)
        if not obj:
            # return JsonResponse({"error": "No user found with the given ID"})
            print("No user found with the given ID")

        current_time = datetime.now().strftime("%H:%M")
        for user in obj:
        
            user_time_str = user.time.strftime("%H:%M")
            seven_minutes_ago = timezone.localtime(timezone.now()) - timezone.timedelta(minutes=7)

            
            print("Current Time:", current_time)
            print("User Time:", user_time_str)
            print("minute : ",seven_minutes_ago)

            while current_time:
                orp_obj = Parameter.objects.filter(device_id=self.user_id, param_type="ORP",time__gte=seven_minutes_ago)
                do_obj = Parameter.objects.filter(device_id=self.user_id, param_type="DO",time__gte=seven_minutes_ago)
                ph_obj = Parameter.objects.filter(device_id=self.user_id, param_type="Ph",time__gte=seven_minutes_ago)
                cpu_obj = Parameter.objects.filter(device_id=self.user_id, param_type="CPU_TEMPERATURE",time__gte=seven_minutes_ago)
                curr_obj = Parameter.objects.filter(device_id=self.user_id, param_type="Current",time__gte=seven_minutes_ago)
                volt_obj = Parameter.objects.filter(device_id=self.user_id, param_type="voltage",time__gte=seven_minutes_ago)

                if orp_obj:
                    data["ORP"] = [i.param_value for i in orp_obj]
                if do_obj:
                    data["DO"] = [i.param_value for i in do_obj]
                if ph_obj:
                    data["Ph"] = [i.param_value for i in ph_obj]      
                if cpu_obj:
                    data["CPU_TEMPERATURE"] = [i.param_value for i in cpu_obj]
                if curr_obj:
                    data["Current"] = [i.param_value for i in curr_obj]
                if volt_obj:
                    data["voltage"] = [i.param_value for i in volt_obj]

                data_json = json.dumps(data)

                if data_json:
                    return data_json
            return ''

    @sync_to_async
    def websocket_disconnect(self, message):
        return super().websocket_disconnect(message)
