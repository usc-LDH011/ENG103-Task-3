from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=17, trigger=4, max_distance = 2)
try:

  while True:
     dis = sensor.distance * 100
     print('Distance: {:.2f} cm'.format(dis))

     sleep(0.3)

except KeyboardInterrupt:
      pass