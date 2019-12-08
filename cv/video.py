import cv2
import imutils
import sys

def feed_video_frames(process):
  capture = cv2.VideoCapture(0)
  if not capture.isOpened():
    print("Cannot open VideoCapture")
    sys.exit(1)

  try:
    while True:
      ok, frame = capture.read()
      if not ok:
        print("Cannot read frame")
        break

      frame = imutils.rotate(frame, 180)
      pos = process(frame)
      if pos is not None:
        draw = frame.copy()
        h, w, d = draw.shape
        c = 255
        for x,y,a in pos:
          cv2.circle(draw, (int(x*w), int(y*h)), int(a*w*h/100), (0,0,c), -1)
          c //= 2
        cv2.imshow('found', draw)
        cv2.waitKey(10)

  except KeyboardInterrupt:
    pass

  capture.release()
  cv2.destroyAllWindows()
