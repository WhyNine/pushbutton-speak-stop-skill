# Copyright Simon Waller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from mycroft import MycroftSkill
from mycroft.messagebus.message import Message
from mycroft.util.log import getLogger

import RPi.GPIO as GPIO
import time

LOGGER = getLogger(__name__)

longpress_threshold = 2

class PushButtonSkill(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)

    def init_gpio(self):
        self.gpio_initialised = False
        try:
            GPIO.setwarnings(False)
            GPIO.remove_event_detect(self.button_pin)
            if self.button_polarity == 0:                                      # active low
                GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.add_event_detect(self.button_pin, GPIO.FALLING)
                LOGGER.info(f"Set GPIO pin {self.button_pin} as input with pull up")
            else:                                                              # active high
                GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.add_event_detect(self.button_pin, GPIO.RISING)
                LOGGER.info(f"Set GPIO pin {self.button_pin} as input with pull down")
            GPIO.setup(self.led_pin, GPIO.OUT)
            GPIO.output(self.led_pin, 1 - self.led_polarity)
        except:
            LOGGER.warning("Can't initialize GPIO - skill will not load")
            self.speak_dialog("error.initialize")
            return
        self.gpio_initialised = True
        self.pressed = False
        self.schedule_repeating_event(self.check_button, None, 0.1, 'ButtonStatus')


    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.get_settings()
        if self.button_pin is None:
            return
        self.init_gpio()
        self.add_event("mycroft.audio.service.stop", self.audio_stopped)
        self.add_event("mycroft.audio.service.play", self.audio_started)

    def audio_stopped(self, message)
        LOGGER.info("Audio stopped detected")
        if (self.gpio_initialised)
            GPIO.output(self.led_pin, 1 - self.led_polarity)

    def audio_started(self, message)
        LOGGER.info("Audio started detected")
        if (self.gpio_initialised)
            GPIO.output(self.led_pin, self.led_polarity)

    def check_button(self):
        if self.pressed:
            if GPIO.input(self.button_pin) != self.button_polarity:
                self.pressed = False
                self.pressed_time = time.time() - self.pressed_time
                if self.pressed_time < longpress_threshold:
                    self.bus.emit(Message("mycroft.mic.listen"))
                else:
                    self.bus.emit(Message("mycroft.stop"))
        else:
            if GPIO.event_detected(self.button_pin):
                self.pressed = True
                self.pressed_time = time.time()
                LOGGER.debug("Detected pushbutton interrupt")

    def on_settings_changed(self):
        self.get_settings()
        self.pressed = False
        self.init_gpio()
        
    def get_settings(self):
        self.led_pin = int(self.settings.get('led_pin'))
        self.led_polarity = int(self.settings.get('led_polarity', 1))
        self.button_pin = int(self.settings.get('button_pin'))
        self.button_polarity = int(self.settings.get('button_polarity', 0))
        LOGGER.info(f"Button GPIO pin = {self.button_pin}, polarity = {self.button_polarity}")
        if (self.button_pin is None) or (self.button_pin < 0) or (self.button_pin > 27):
            LOGGER.info("Invalid button GPIO pin number")
            self.button_pin = None
        LOGGER.info(f"LED GPIO pin = {self.led_pin}, polarity = {self.led_polarity}")
        if (self.led_pin is None) or (self.led_pin < 0) or (self.led_pin > 27):
            LOGGER.info("Invalid LED GPIO pin number")
            self.led_pin = None


def create_skill():
    return PushButtonSkill()
