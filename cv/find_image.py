import cv2
import numpy
import video

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (0,0,255)
GREEN = (0,255,0)
YELLOW = (0,255,255)

def build_cross_image(width=640, height=480, thickness=50):
  image = numpy.zeros((height, width, 3), dtype="uint8")
  length = width // 4
  d = thickness // 2
  cx = width // 2
  cy = height // 2
  cv2.rectangle(image, (cx-d, cy-length), (cx+d, cy+length), WHITE, -1)
  cv2.rectangle(image, (cx-length, cy-d), (cx+length, cy+d), WHITE, -1)
  return image


def reference_contour(image):
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ok, threshold = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
  contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  return contours[0]


def find_matching(image, contour_to_match):
  def roundness(contour, moments):
    length = cv2.arcLength(contour, True)
    roundness = (length * length) / (moments['m00'] * 4 * numpy.pi)
    return roundness

  def area(moments):
    return moments['m00']

  def filter_contour(contour, moments):
      r = roundness(contour, moments)
      if r < 4.0: return "too round %.1f" % r
      if area(moments) > 8000: return "too big"

  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ok, threshold = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
  contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

  draw = image.copy()
  for c in contours:
    try:
      m = cv2.moments(c)
      m1 = cv2.matchShapes(contour_to_match, c, cv2.CONTOURS_MATCH_I1, 0.0)
      m2 = cv2.matchShapes(contour_to_match, c, cv2.CONTOURS_MATCH_I2, 0.0)
      m3 = cv2.matchShapes(contour_to_match, c, cv2.CONTOURS_MATCH_I3, 0.0)
      if m1 < 0.2 and m2 < 0.2 and m3 < 0.2 and filter_contour(c, m) is None:
        match = (m1 + m2 + m3 ) / 3.0
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])
        cv2.drawContours(draw, [c], 0, RED, 2)
        cv2.putText(draw, "%.1f" % match, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1.0, GREEN, 2)
      # else:
      #   cv2.drawContours(draw, [c], 0, YELLOW, 1)
      #   cv2.putText(draw, f, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, YELLOW, 1)
    except ZeroDivisionError as e:
      pass
  cv2.imshow('Contours', draw)
  cv2.waitKey(20)


if __name__ == "__main__":
  cross_contour = reference_contour(build_cross_image())
  video.feed_video_frames(lambda f: find_matching(f, cross_contour))
