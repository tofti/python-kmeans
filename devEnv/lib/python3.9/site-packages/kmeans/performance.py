"""
Utils for generating random data and comparing performance
"""
import os
import time
import pickle
import random
from kmeans import kmeans, here
here = here(__file__)

try:
    range = xrange
except NameError:
    pass


def timer():
    start = time.clock()
    return lambda: time.clock() - start


def random_points(n):
    """Returns n random [(x_1, x_2, x_3), w] tuples.

        Constraints:
        0 <= abs(x_N) <= 1<<8
        0 <= w <= 100
        x_N, w are non-negative integers
    """
    rx = lambda: random.randrange(0, 1 << 8)
    rw = lambda: random.randrange(1, 10)
    point = lambda: [(rx(), rx(), rx()), rw()]
    filename = os.path.join(here, "_perf.sample")
    try:
        with open(filename, 'rb') as f:
            points = pickle.load(f)
    except:
        points = []

    diff = n - len(points)
    if diff > 0:
        print("Cache was missing {} points".format(diff))
        t = timer()
        points.extend(point() for _ in range(diff))
        with open(filename, 'wb') as f:
            pickle.dump(points, f)
        elapsed = t()
        print("Added {} points to the cache ({}s)".format(diff, elapsed))

    return ListProxy(points)


class ListProxy(list):
    """Fake sizes by setting length"""
    def __init__(self, data):
        super().__init__(data)
        self.max_length = len(data)
        self.length = self.max_length

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, n):
        if n > self.max_length:
            raise ValueError(
                "Maximum possible length is " + str(self.max_length))
        self._length = n

    def __len__(self):
        return self.length

    def __iter__(self):
        for i in range(self.length):
            yield self[i]


def main():
    samples = [
        # ~ Common "large" image sizes
        (1920 * 1200,  3),
        (1920 * 1200,  5),
        (1920 * 1200, 15),

        # Personal benchmarks
        (747116, 5),   # Unique pixels in 1920 x 1080 image
        (1095169, 5),  # Unique pixels in 15530 x 8591 image

        # Max unique pixels in rgb 256 image
        (16581375, 5)
    ]

    max_sample = max(sample[0] for sample in samples)
    print("Generating {} random points".format(max_sample))
    t = timer()
    points = random_points(max_sample)
    elapsed = t()
    print("Random points generated ({}s)".format(elapsed))

    def run_test(n, k):
        points.length = n
        t = timer()
        kmeans(points, k)
        elapsed = t()
        return elapsed

    for n, k in samples:
        print("Running test: {} points, {} centers".format(n, k))
        elapsed = run_test(n, k)
        print("N {:9} || K {:3} || E {}".format(n, k, elapsed))

if __name__ == "__main__":
    main()
