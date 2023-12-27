# import octoprint.plugin
# import os
# class TemperatureLoggerPlugin(octoprint.plugin.EventHandlerPlugin):
#     def on_event(self, event, payload):
#         if event == "TemperatureReceived":
#             for key, value in payload.items():
#                 if key.startswith("tool0"):
#                     temperature_data = {
#                         "tool": key,
#                         "actual": value["actual"],
#                         "target": value["target"]
#                     }
#                     self._log_temperature(temperature_data)

#     def _log_temperature(self, data):
#         path = "/home/pi/OctoPrint/"
#         file_name = 'testing.txt'
#         file_path = os.path.join(path, file_name)
#         with open(file_path, "a") as file:
#             file.write(str(data) + "\n")
#         self._logger.info(f"Temperature data written: {data}")

# __plugin_name__ = "Temperature Logger"
# __plugin_version__ = "1.0.0"
# __plugin_description__ = "Logs temperature information to a file"
# __plugin_pythoncompat__ = ">=3.7,<4"
# __plugin_implementation__ = TemperatureLoggerPlugin()