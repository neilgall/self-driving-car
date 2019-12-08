import RPi.GPIO as gpio
import sys
import time

gpio.setmode(gpio.BCM)

while True:
  print ">",
  words = sys.stdin.readline().strip().split()
  try:
    if words[0] == 'x':
        break
    elif words[0] == 'out':
        gpio.setup(int(words[1]), gpio.OUT)
        print int(words[1]), "out"
    elif words[0] == 'in':
        gpio.setup(int(words[1]), gpio.IN)
        print int(words[1]), "in"
    elif words[0] == 'w':
        gpio.output(int(words[1]), int(words[2]))
        print "w", int(words[1]), int(words[2])
    elif words[0] == 'r':
        print "r", int(words[1]), gpio.input(int(words[1]))
  except:
    print "unknown command"

gpio.cleanup()

