import pigpio
import queue
import threading
import time

RIGHT_FORWARD = 17
RIGHT_BACKWARD = 22
LEFT_FORWARD = 23
LEFT_BACKWARD = 24
MIN_SPEED = 25
MAX_SPEED = 125


class Drive:
  def __init__(self):
    self._io = pigpio.pi()
    for pin in [RIGHT_FORWARD, RIGHT_BACKWARD, LEFT_FORWARD, LEFT_BACKWARD]:
      self._io.set_PWM_range(pin, MAX_SPEED)
      self._io.set_PWM_frequency(pin, 25)
      self._io.set_PWM_dutycycle(pin, 0)
    self._queue = queue.Queue()
    self._thread = threading.Thread(target=self._run)
    self._thread.start()

  def quit(self):
    self._queue.put(("exit", None))
    self._thread.join()
    self._io.stop()

  def turn(self, speed):
    self._queue.put(("turn", speed))

  def stop(self):
    self._queue.put(("stop", None))

  def _stop(self):
    for pin in [RIGHT_FORWARD, RIGHT_BACKWARD, LEFT_FORWARD, LEFT_BACKWARD]:
      self._io.set_PWM_dutycycle(pin, 0)

  def _run(self):
    while True:
      try:
        cmd, param = self._queue.get()

        if cmd == "exit":
          self._stop()
          return

        elif cmd == "stop":
          self._stop()

        elif cmd == "turn":
          speed = MIN_SPEED + (MAX_SPEED / 4 - MIN_SPEED) * abs(param)
          if param < 0:
            self._io.set_PWM_dutycycle(LEFT_BACKWARD, speed)
            self._io.set_PWM_dutycycle(RIGHT_FORWARD, speed)
          else:
            self._io.set_PWM_dutycycle(RIGHT_BACKWARD, speed)
            self._io.set_PWM_dutycycle(LEFT_FORWARD, speed)

      except KeyboardInterrupt:
        pass