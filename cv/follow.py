try:
  from drive import Drive
except:
  pass

from find_positions import PositionsFinder
from hysteresis import Hysteresis
from video import feed_video_frames
import argparse
import sys

class DummyDrive:
  def quit(self):
    pass
  def stop(self):
    pass
  def turn(self, x):
    pass
  def drive(self, x):
    pass


class Follower:
  def __init__(self, args):
    self._args = args
    self._drive = DummyDrive() if args.nohw else Drive()
    self._finder = PositionsFinder(args.debug)
    self._hysteresis = Hysteresis(frames=args.frames, resolution=args.resolution, threshold=args.threshold)

  def stop(self):
    self._drive.quit()

  def __call__(self, frame):
    raw = self._finder.positions_in_image(frame)
    self._hysteresis.update(raw)    
    try:
      x, y, a = next(self._hysteresis.consistent())
      if a > 4000:
        self._drive.drive(-0.05)
      elif 0.4 < x < 0.6 and a < 4000:
        self._drive.drive(0.05)
      else:
        self._drive.turn(x - 0.5)
      yield x, y, a

      if self._args.show_positions:
        print("x:%0.2f y:%0.2f a:%.0f" % (x,y,a))

    except StopIteration:
      self._drive.stop()

if __name__ == "__main__":
  parser = argparse.ArgumentParser("Car")
  parser.add_argument("--frames", "-f", type=int, default=5)
  parser.add_argument("--resolution", "-s", type=int, default=25)
  parser.add_argument("--threshold", "-t", type=int, default=1)
  parser.add_argument("--debug", "-d", action="store_true")
  parser.add_argument("--nohw", action="store_true")
  parser.add_argument("--rotate", type=int, default=180)
  parser.add_argument("--show-image", action="store_true")
  parser.add_argument("--show-fps", action="store_true")
  parser.add_argument("--show-positions", action="store_true")
  args = parser.parse_args()

  follower = Follower(args)
  feed_video_frames(follower, rotate=args.rotate, show_image=args.show_image, show_fps=args.show_fps)
  follower.stop()
