from collections import defaultdict

class Hysteresis:
  def __init__(self):
    self._positions = []

  def update(self, positions):
    positions = list(positions)
    if len(positions) > 0:
      if not self._positions:
        self._positions = [positions]
      else:
        self._positions.append(positions)
        if len(self._positions) > 8:
          self._positions = self._positions[1:]

  def all_seen(self):
    all = []
    for p in self._positions:
      all.extend(p)
    return all

  def consistent(self):
    all = self.all_seen()
    threshold = len(self._positions) / 2
    buckets = defaultdict(int)
    for x, y, a in all:
      bx = int(x*10)
      by = int(y*10)
      buckets[(bx,by,1)] += 1

    ordered = (k for k,v in sorted(buckets.items(), key = lambda i: i[1], reverse=True) if v > threshold)
    yield from ((x/10.0, y/10.0, a/100.0) for x,y,a in ordered)
