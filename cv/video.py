import cv2
import imutils
import sys
import time

class FPS:
  def __init__(self):
    self._count = 0
    self._time = time.time()

  def ping(self):
    self._count += 1
    t = time.time()
    if t - self._time > 1.0:
      print(f"{self._count} FPS")
      self._count = 0
      self._time = t


def feed_video_frames(process, rotate=0, show_image=False, show_fps=False):
  capture = cv2.VideoCapture(0)
  if not capture.isOpened():
    print("Cannot open VideoCapture")
    sys.exit(1)

  try:
    fps = FPS()
    while True:
      ok, frame = capture.read()
      if not ok:
        print("Cannot read frame")
        break

      if rotate != 0:
        frame = imutils.rotate(frame, rotate)

      if show_image:
        draw = frame.copy()
        h, w, d = draw.shape
        c = 255
        for x,y,a in process(frame):
          cv2.circle(draw, (int(x*w), int(y*h)), int(a/100), (0,0,c), -1)
          c //= 2
        cv2.imshow('found', draw)
        cv2.waitKey(10)

      else:
        for p in process(frame):
          pass

      if show_fps:
        fps.ping()

  except KeyboardInterrupt:
    pass

  capture.release()
  cv2.destroyAllWindows()
