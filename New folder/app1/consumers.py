import asyncio
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
import json

class MySyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']  # Extract user_id from the URL
        await self.accept()

        while True:
            data = await self.get_data()  # No need to pass user_id here
            await self.send(data)

            await asyncio.sleep(1)

    @sync_to_async
    def get_data(self):
        data = {
        "ORP": None,
        "DO": None,
        "Ph": None,
        "CPU_TEMPERATURE": None,
        "Current": None,
        "voltage": None,
    }
        obj =Parameter.objects.filter(device_id=self.user_id)
        print(obj)
        if not obj:
            # return JsonResponse({"error": "No user found with the given ID"})
            print("No user found with the given ID")

        current_time = datetime.now().strftime("%H:%M:%S")
        for user in obj:
            # user_time = timezone.localtime(user.Time)
            user_time_str = user.time.strftime("%H:%M:%S")


            print("Current Time:", current_time)
            print("User Time:", user_time_str)

            while current_time == user_time_str:
                orp_obj = Parameter.objects.filter(device_id=self.user_id, param_type="ORP",time=current_time).last()
                do_obj = Parameter.objects.filter(device_id=self.user_id, param_type="DO",time=current_time).last()
                ph_obj = Parameter.objects.filter(device_id=self.user_id, param_type="Ph",time=current_time).last()
                cpu_obj = Parameter.objects.filter(device_id=self.user_id, param_type="CPU_TEMPERATURE",time=current_time).last()
                curr_obj = Parameter.objects.filter(device_id=self.user_id, param_type="Current",time=current_time).last()
                volt_obj = Parameter.objects.filter(device_id=self.user_id, param_type="voltage",time=current_time).last()

                if orp_obj:
                    data["ORP"] = orp_obj.param_value
                if do_obj:
                    data["DO"] = do_obj.param_value
                if ph_obj:
                    data["Ph"] = ph_obj.param_value
                if cpu_obj:
                    data["CPU_TEMPERATURE"] = cpu_obj.param_value
                if curr_obj:
                    data["Current"] = curr_obj.param_value
                if volt_obj:
                    data["voltage"] = volt_obj.param_value

                data_json = json.dumps(data)

                if data_json:
                    return data_json
        return ''

    @sync_to_async
    def websocket_disconnect(self, message):
        return super().websocket_disconnect(message)
