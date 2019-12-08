from drive import Drive
from find_positions import PositionsFinder
from hysteresis import Hysteresis
from video import feed_video_frames
import sys


class Follower:
  def __init__(self, debug):
    self._drive = Drive()
    self._finder = PositionsFinder(debug)
    self._hysteresis = Hysteresis()

  def stop(self):
    self._drive.quit()

  def __call__(self, frame):
    raw = self._finder.positions_in_image(frame)
    self._hysteresis.update(raw)    
    pos = list(self._hysteresis.consistent())
    if pos:
      x, y, a = pos[0]
      self._drive.turn(x - 0.5)
    else:
      self._drive.stop()
    return pos

if __name__ == "__main__":
  debug = len(sys.argv) > 1 and sys.argv[1] == "-d"
  follower = Follower(debug)
  feed_video_frames(follower)
  follower.stop()
