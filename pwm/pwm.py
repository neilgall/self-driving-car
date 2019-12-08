import pigpio
import time

RIGHT_FORWARD = 17
RIGHT_BACKWARD = 22
LEFT_FORWARD = 23
LEFT_BACKWARD = 24
MIN_SPEED = 25
MAX_SPEED = 125

def init(io):
  for pin in [RIGHT_FORWARD, RIGHT_BACKWARD, LEFT_FORWARD, LEFT_BACKWARD]:
    io.set_PWM_range(pin, MAX_SPEED)
    io.set_PWM_frequency(pin, 25)
    io.set_PWM_dutycycle(pin, 0)

def stop(io):
  for pin in [RIGHT_FORWARD, RIGHT_BACKWARD, LEFT_FORWARD, LEFT_BACKWARD]:
    io.set_PWM_dutycycle(pin, 0)

def run(io):
  direction=0
  try: 
    while True:
      stop(io)

      fwd = LEFT_FORWARD if direction else LEFT_BACKWARD
      bwd = RIGHT_BACKWARD if direction else RIGHT_FORWARD

      for dc in range(MIN_SPEED, MAX_SPEED, 5):
        print(direction,dc)
        io.set_PWM_dutycycle(fwd, dc)
        io.set_PWM_dutycycle(bwd, dc)
        time.sleep(0.5)

      for dc in range(MAX_SPEED, MIN_SPEED, -5):
        print(direction,dc)
        io.set_PWM_dutycycle(fwd, dc)
        io.set_PWM_dutycycle(bwd, dc)
        time.sleep(0.5)

      stop(io)
      time.sleep(0.5)

      direction = 1-direction

  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
  io = pigpio.pi()
  run(io)
  stop(io)
  io.stop()

