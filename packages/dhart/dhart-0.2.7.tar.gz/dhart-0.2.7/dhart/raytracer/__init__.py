"""
Perform efficent ray intersections with geometry.
=================================================


This library is focused on performing ray intersections with geometry. The key
datatype for this is the EmbreeBVH, which is required for most functions in 
this package. 

Raytracing involves determining where a line would intersect a mesh
if it were to continue infinitely form a specific point in the space.
Many of the other modules in DHARTAPI make use of ray intersections
in their analysis. 

"""

from .embree_bvh import *
from .embree_raytracer import *

__all__ = ['EmbreeBVH','RayResultList','ResultStruct','IntersectForPoint','Intersect','IntersectOccluded']
