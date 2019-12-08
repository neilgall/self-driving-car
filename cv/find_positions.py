import cv2
import numpy
import video

WHITE = (255,255,255)
BLUE= (255,0,0)
RED = (0,0,255)

MIN_AREA = 10.0
MAX_AREA = 12000.0
MAX_ROUNDNESS = 4.0

DETECT_MODES = [cv2.CONTOURS_MATCH_I1, cv2.CONTOURS_MATCH_I2, cv2.CONTOURS_MATCH_I3]
DETECT_THRESHOLD = 0.10

def build_cross_image(width=640, height=480, thickness=50):
  image = numpy.zeros((height, width, 3), dtype="uint8")
  length = width // 4
  d = thickness // 2
  cx = width // 2
  cy = height // 2
  cv2.rectangle(image, (cx-d, cy-length), (cx+d, cy+length), WHITE, -1)
  cv2.rectangle(image, (cx-length, cy-d), (cx+length, cy+d), WHITE, -1)
  return image


def contours_fron_image(image, mode=cv2.RETR_EXTERNAL):
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ok, threshold = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
  contours, hierarchy = cv2.findContours(threshold, mode, cv2.CHAIN_APPROX_NONE)
  return contours


class PositionsFinder:
  def __init__(self, debug=False):
    self._reference_contour = contours_fron_image(build_cross_image())[0]
    self._debug = debug

  def positions_in_image(self, image):
    (height, width, depth) = image.shape

    if self._debug:
      draw = image.copy()

    for contour in contours_fron_image(image, mode=cv2.RETR_TREE):
      moments = cv2.moments(contour)
      area = moments['m00']
      if area < MIN_AREA: continue # too small
      if area > MAX_AREA: continue # too big

      length = cv2.arcLength(contour, True)
      roundness = (length * length) / (moments['m00'] * 4 * numpy.pi)
      if roundness < MAX_ROUNDNESS: continue # too round

      color = BLUE
      match = [cv2.matchShapes(self._reference_contour, contour, mode, 0.0) for mode in DETECT_MODES]
      if all(m < DETECT_THRESHOLD for m in match):
        cx = (moments['m10'] / moments['m00']) / width
        cy = (moments['m01'] / moments['m00']) / height
        yield (cx, cy, area)
        color = RED

      if self._debug:
        cv2.drawContours(draw, [contour], 0, color, 2)

    if self._debug:
      cv2.imshow("contours", draw)

if __name__ == "__main__":
  finder = PositionsFinder(debug=True)
  def show(frame):
    return finder.positions_in_image(frame)

  video.feed_video_frames(show)
