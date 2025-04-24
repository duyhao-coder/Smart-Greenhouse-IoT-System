from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from mqtt import *
from aiot_lcd1602 import LCD1602
from machine import Pin, SoftI2C
from aiot_dht20 import DHT20
from event_manager import *
from aiot_rgbled import RGBLed
import time

def on_mqtt_message_receive_callback__button2_(th_C3_B4ng_tin):
  global temp_AI, status, temp, AI
  if th_C3_B4ng_tin == '1':
    temp = 1
  if th_C3_B4ng_tin == '0':
    temp = 0

def on_mqtt_message_receive_callback__AI_(temp_AI):
  global th_C3_B4ng_tin, status, temp, AI
  if temp_AI == 'on':
    AI = 1
  if temp_AI == 'off':
    AI = 0

aiot_lcd1602 = LCD1602()

aiot_dht20 = DHT20()

event_manager.reset()

tiny_rgb = RGBLed(pin1.pin, 4)

def on_event_timer_callback_e_u_a_d_U():
  global th_C3_B4ng_tin, temp_AI, status, temp, AI
  mqtt.publish('temperature', (aiot_dht20.dht20_temperature()))
  mqtt.publish('humidity', (aiot_dht20.dht20_humidity()))
  mqtt.publish('soil_moisture', (translate((pin0.read_analog()), 0, 4095, 0, 100)))

event_manager.add_timer_event(15000, on_event_timer_callback_e_u_a_d_U)

if True:
  display.scroll('Hello, World!')
  mqtt.connect_wifi('ACLAB', 'ACLAB2023')
  mqtt.connect_broker(server='io.adafruit.com', port=1883, username='add name', password='add key')
  mqtt.on_receive_message('button2', on_mqtt_message_receive_callback__button2_)
  mqtt.on_receive_message('AI', on_mqtt_message_receive_callback__AI_)
  status = 0
  temp = 5
  AI = 4

while True:
  mqtt.check_message()
  aiot_lcd1602.clear()
  aiot_dht20.read_dht20()
  if button_a.is_pressed():
    status = 0
  if button_b.is_pressed():
    status = 1
  event_manager.run()
  if temp == 1:
    pin6.write_digital((1))
  if temp == 0:
    pin6.write_digital((0))
  if status == 0:
    aiot_lcd1602.move_to(0, 0)
    aiot_lcd1602.putstr('NHIET DO')
    aiot_lcd1602.move_to(0, 1)
    aiot_lcd1602.putstr('DO AM ')
    aiot_lcd1602.move_to(10, 0)
    aiot_lcd1602.putstr((aiot_dht20.dht20_temperature()))
    aiot_lcd1602.move_to(10, 1)
    aiot_lcd1602.putstr((aiot_dht20.dht20_humidity()))
  if status == 1:
    aiot_lcd1602.move_to(0, 0)
    aiot_lcd1602.putstr('MODEL 2')
    aiot_lcd1602.move_to(0, 1)
    aiot_lcd1602.putstr('DO AM DAT')
    aiot_lcd1602.move_to(10, 1)
    aiot_lcd1602.putstr((translate((pin0.read_analog()), 0, 4095, 0, 100)))
  if (aiot_dht20.dht20_temperature()) >= 30:
    tiny_rgb.show(0, hex_to_rgb('#ff0000'))
  if (aiot_dht20.dht20_temperature()) > 20 and (aiot_dht20.dht20_temperature()) < 30:
    tiny_rgb.show(0, hex_to_rgb('#00ff00'))
  if (aiot_dht20.dht20_temperature()) >= 0 and (aiot_dht20.dht20_temperature()) < 20:
    tiny_rgb.show(0, hex_to_rgb('#ffff00'))
  if AI == 1:
    pin6.write_digital((1))
  if AI == 0:
    pin6.write_digital((0))
  time.sleep_ms(1000)
  time.sleep_ms(10)
