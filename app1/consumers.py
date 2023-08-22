import asyncio
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
import time
from django.http import JsonResponse

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
        device_id = Device.objects.filter(device_id=self.user_id)
        print(device_id)
        if not device_id:
            return JsonResponse({"error": "No user found with the given ID"})

        current_time = time.strftime("%H:%M:%S", time.localtime())

        for user in device_id:
            user_time = user.time.strftime("%H:%M:%S")
            user_roll = user.roll
            user_name = user.name
            

            print("Current Time:", current_time)
            print("User Time:", user_time)

        if current_time == user_time:
            print("Times match for user:", user)
            return f'{user_roll,user_name}'

        return ''

    @sync_to_async
    def websocket_disconnect(self, message):
        return super().websocket_disconnect(message)
