from collections import defaultdict
from dataclasses import dataclass

@dataclass
class Sample:
  x: float
  y: float
  a: float
  count: int

  def inc(self):
    self.count += 1


class Hysteresis:
  def __init__(self, frames=5, resolution=20, threshold=3):
    self._positions = []
    self._frames = frames
    self._resolution = resolution
    self._area_resolution = 0.01
    self._threshold = threshold

  def update(self, positions):
    positions = list(positions)
    if len(positions) > 0:
      if not self._positions:
        self._positions = [positions]
      else:
        self._positions.append(positions)
        if len(self._positions) > self._frames:
          self._positions = self._positions[1:]

  def _all_seen(self):
    all = []
    for p in self._positions:
      all.extend(p)
    return all

  def _bucket(self, x, y, a):
    return (int(x*self._resolution), int(y*self._resolution), int(a*self._area_resolution))

  def _unbucket(self, x, y, a):
    return (x/self._resolution, y/self._resolution, a/self._area_resolution)

  def consistent(self):
    buckets = {}
    for x, y, a in self._all_seen():
      b = self._bucket(x, y, a)
      if b in buckets:
        buckets[b].inc()
      else:
        buckets[b] = Sample(x, y, a, 1)

    ordered = sorted(buckets.items(), key = lambda i: i[1].count, reverse=True)
    yield from ((sample.x, sample.y, sample.a) for k,sample in ordered if sample.count > self._threshold)
