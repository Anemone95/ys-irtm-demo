#!/usr/bin/env python3
"""Example of a the most simple usage of a Switch instance.

The SimpleSwitch is an OptimisticSwitch that will appear on Home Assistant
and offers bidirectional control:

 - Home Assistant can set the state and the callback code is called
   (as shown below in method `callback`)
 - Changes to the switch state (as shown in the `toggle` method) are published
   to MQTT and thus updated on Home Assistant.
"""

from ham import MqttManager
from ham.light import Light 
from time import sleep
import os
from typing import Optional
import json
import my_light

MQTT_USERNAME = os.environ["MQTT_USERNAME"]
MQTT_PASSWORD = os.environ["MQTT_PASSWORD"]
MQTT_HOST = "127.0.0.1"

class SimpleLight(Light):
    name = "Bed Light2"
    short_id = "bed_light"
    brightness_scale = 100
    optimistic = False
    color_mode = True
    brightness = True
    qos = 0.1
    lock = False

    _state: bool = False
    _color_temp: int = 153
    config_fields = ["schema", "optimistic", "color_mode", "brightness", "brightness_scale", "qos"]
    
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: bool):
        self._state = value
        self.publish_mqtt_message(bytes(json.dumps({"state": "ON" if value else "OFF"}), "utf-8"), "main")

    @property
    def color_temp(self):
        return self._color_temp

    @color_temp.setter
    def color_temp(self, value: int):
        self._color_temp = value
        self.publish_mqtt_message(bytes(json.dumps({"state": value}), "utf-8"), "brightness/state")


    def get_config(self):
        config = super().get_config()
        config["supported_color_modes"] = ["color_temp"]
        config["state_topic"] = f'~/{ self.short_id }/main'
        config["brightness_state_topic"] = f'~/{ self.short_id }/brightness/state'
        return config

    def callback(self, *, state: bool, brightness: Optional[int] = None, color_temp: Optional[int] = None):
        print(f"!!state: {state}, brightness: {brightness}, color_temp: {color_temp}")
        if self.lock:
            self.state = self.state;
            return
        # To prevent ir haven't finish the previous one and start the next one
        self.lock=True
        if brightness is None and color_temp is None:
            if state == "ON" and self.state == False:
                self.state = True
                my_light.switch()
            elif state == "OFF" and self.state == True:
                self.state = False
                my_light.switch()
        elif brightness is not None:
            print("Set Darkest")
            if brightness>90:
                my_light.bb()
                sleep(4)
            elif brightness<10:
                my_light.dd()
                sleep(4)
            else:
                my_light.dd()
                sleep(4)
                my_light.brighter(int(brightness/100.0*10))
                print("Set Brighter",int(brightness/100.0*10))
                my_light.brighter(int(brightness/100.0*10))
                self.state = True
                print("Done")
                sleep(int(brightness/100.0*10)*0.2)
        elif self.state == True and color_temp is not None:
            my_light.switch()
            sleep(0.4)
            my_light.switch()
            
        sleep(0.4)
        self.lock=False



    def init(self):
        self.state = False
        self.color_temp=500

if __name__ == "__main__":
    light = SimpleLight()
    manager = MqttManager(MQTT_HOST, username=MQTT_USERNAME, password=MQTT_PASSWORD)
    manager.add_thing(light)
    manager.start()
    sleep(0.3)
    light.init()
