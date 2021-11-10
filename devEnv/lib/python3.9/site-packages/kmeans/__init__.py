"""
.. module:: kmeans
   :synopsis: python wrapper for a basic c implementation of the
              k-means algorithm.

.. moduleauthor:: Joe Cross <joe.mcross@gmail.com>

"""
import os
import ctypes
import random
import sysconfig
from ctypes import Structure, c_uint8, c_uint32, c_uint64, byref
__all__ = ['kmeans']

# ====================================================
# Hook up c module
HERE = os.path.dirname(os.path.realpath(__file__))
'''http://www.python.org/dev/peps/pep-3149/'''
SUFFIX = sysconfig.get_config_var('SO')
if not SUFFIX:  # pragma: no cover
    SOABI = sysconfig.get_config_var('SOABI')
    SUFFIX = ".{}.so".format(SOABI)

SO_PATH = os.path.join(HERE, 'lib' + SUFFIX)
LIB = ctypes.CDLL(SO_PATH)
# ====================================================


class Point(Structure):
    _fields_ = [
        ('r', c_uint8),
        ('g', c_uint8),
        ('b', c_uint8),
        ('center', c_uint8),
        ('count', c_uint32)
    ]


class Center(Structure):
    _fields_ = [
        ('r', c_uint64),
        ('g', c_uint64),
        ('b', c_uint64),
        ('count', c_uint32)
    ]


def _kmeans(points, k, centers, tolerance, max_iterations):

    if centers:
        if k != len(centers):
            raise ValueError(
                "Provided {} centers but k is {}".format(len(centers), k))
    else:
        centers = random.sample(points, k)

    results = pcenters = (Center * k)()
    for i, center in enumerate(centers):
        (r, g, b), count = center
        pcenters[i] = Center(r=r, g=g, b=b, count=count)
    pcenters = byref(pcenters)

    # Generate points
    n = len(points)
    ppoints = (Point * n)()
    for i, point in enumerate(points):
        (r, g, b), count = point
        ppoints[i] = Point(r=r, g=g, b=b, center=-1, count=count)
    ppoints = byref(ppoints)

    # Compute centers
    LIB.kmeans(ppoints, n, pcenters, k, tolerance, max_iterations)

    # Translate
    return [[result.r, result.g, result.b] for result in results]


def kmeans(points, k, centers=None, tolerance=1, max_iterations=0):
    """Return a list of *k* centers (means).  Initial centers are optional.

    :param points: (values, weight) tuples to find centers of.
            value is a list of integer values.
    :type points: list

    :param k: number of centers to calculate
    :type k: int

    :param centers: initial centers, leave blank to randomly select
    :type centers: list

    :param tolerance: maximum delta to consider the centers stable
    :type tolerance: int

    :param max_iterations: maximum assign/update iterations.  0 to loop until
            tolerance is met.
    :type max_iterations: int

    :rtype: list

    """
    return _kmeans(points=points, k=k, centers=centers,
                   tolerance=tolerance, max_iterations=max_iterations)
