import ctypes
from typing import *
import numpy

from dhart.raytracer import EmbreeBVH
import dhart.raytracer.raytracer_native_functions as raytracer_native_functions
from dhart.native_numpy_like import NativeNumpyLike
from dhart.utils import is_point

__all__ = ['ResultStruct','RayResultList','isValidBVH','Intersect','IntersectForPoint','IntersectOccluded', 'IntersectDistanceDouble']

class ResultStruct(ctypes.Structure):
    """ A struct of results containing distance, and meshid 

    If the ray didn't hit anything, both distance and MeshID will be
    set to 0

    Attributes:
        [0] = distance to the hitpoint or 0 if no geometry was hit
        [1] = The ID of the geometry hit, or 0 if no geometry was hit
    """

    _fields_ = [("distance", ctypes.c_float), ("meshid", ctypes.c_int)]


class RayResultList(NativeNumpyLike):
    """ A list of results from a set of ray queries. Includes distance/meshid """

    native_type = ResultStruct 
    delete_fp = raytracer_native_functions.DestroyRayResultVector

    def __init__(
        self,
        vector_ptr: ctypes.c_void_p,
        data_ptr: ctypes.c_void_p,
        node_count: int,
        ray_count: int,
    ):
        """ Create a new view analysis result from view analysis in C++
        
        Args:
            vector_ptr: a pointer to a vector of floats
            data_ptr: a pointer to the underlying data of the node vector
            node_count : The number of nodes for this result set
            ray_count : the number of rays cast per node in this result set
        """

        # Make this one dimensional if either node_count or ray_count is 1
        if node_count <= 1 or ray_count <= 1:
            shape = max(node_count, ray_count)
        else:
            shape = (node_count, ray_count)

        super().__init__(
            vector_ptr,
            data_ptr,
            shape,
        )


def isValidBVH(bvh: object) -> bool:
    """ Check if the given object is actually a BVH before sending the pointer to C++

    If this check were not performed, the pointer from any object with the .pointer attribute
    could be sent to C++ with catastrophic results. This check must be performed to ensure that
    every pointer sent to C++ will lead to a valid and fully initialized Raytracer
        
    Raises:
        TypeError: The passed object was not a valid bvh
    """
    if not isinstance(bvh, EmbreeBVH):
        raise TypeError(
            f"The embree_raytracer was passed a {type(bvh)} instead of a {EmbreeBVH}"
        )
    return True


def Intersect(
    bvh: EmbreeBVH,
    origin: Union[Tuple[float, float, float], List[Tuple[float, float, float]]],
    direction: Union[Tuple[float, float, float], List[Tuple[float, float, float]]],
    max_distance: float = -1.0,
    ) -> Union[numpy.array, Tuple[float, int]]:
    """ Cast one or more rays to get the distance to their point of intersection
    and the ID of the mesh they intersected.
    
    In situations where multiple rays are shot, rays will be cast in parallel. 

    Note:
        Accepts the following configurations:
            1) Single origin, single direction
            2) Multiple origins, multiple directions
            3) Single origin, multiple directions
            4) Multiple origins, single direction

    Args:
        bvh: A valid Embree BVH
        origin: a single tuple of x,y,z coordinates, or a list of x,y,z tuples
        direction: A single direction or list of directions
        max_distance: the maximum distance tto still be considered a hit for the ray
    
    Returns:
        Union[RayResultList, Tuple[float, int]]: If a single ray, then a tuple of float
            for distance and an int for meshid. If multiple rays are casted, an array of
            RayResult structs is returned in a RayResult List. In all cases, a 
            distance/meshid of -1 indicates a miss.

    Examples:
        Casting a single ray

        >>> import numpy as np
        >>> from numpy.lib import recfunctions as rfn
        >>> from dhart.geometry import LoadOBJ, CommonRotations, ConstructPlane
        >>> from dhart.raytracer import EmbreeBVH, Intersect
        >>> 
        >>> loaded_obj = ConstructPlane()
        >>> loaded_obj.Rotate(CommonRotations.Yup_to_Zup)
        >>> bvh = EmbreeBVH(loaded_obj)
        >>> 
        >>> result = Intersect(bvh, (0,0,1), (0,0,-1))
        >>> print(np.around(result,5))
        [1. 0.]

        >>> #Casting rays with an equal number of directions and origins
        >>> 
        >>> loaded_obj = ConstructPlane()
        >>> loaded_obj.Rotate(CommonRotations.Yup_to_Zup)
        >>> bvh = EmbreeBVH(loaded_obj)
        >>> 
        >>> hit_point = Intersect(bvh, [(0,0,1)] * 10, [(0,0,-1)] * 10)
        >>> # Convert to numpy unstructured and round
        >>> print(np.around(rfn.structured_to_unstructured(hit_point.array),5))
        [[1. 0.]
         [1. 0.]
         [1. 0.]
         [1. 0.]
         [1. 0.]
         [1. 0.]
         [1. 0.]
         [1. 0.]
         [1. 0.]
         [1. 0.]]

        >>> #Casting multiple rays with one direction and multiple origins
        >>> 
        >>> loaded_obj = ConstructPlane()
        >>> loaded_obj.Rotate(CommonRotations.Yup_to_Zup)
        >>> bvh = EmbreeBVH(loaded_obj)
        >>> 
        >>> origins = [(0,0,x) for x in range(0,5)]
        >>> hit_point = Intersect(bvh, origins, (0,0,-1))
        >>> print(np.around(rfn.structured_to_unstructured(hit_point.array),5))
        [[-1. -1.]
         [ 1.  0.]
         [ 2.  0.]
         [ 3.  0.]
         [ 4.  0.]]

    """
    # Check if origin and direction can be used as points
    origin_is_point = is_point(origin)
    direction_is_point = is_point(direction)
    
    # If both are points, cast a single ray
    if origin_is_point and direction_is_point: 
        return raytracer_native_functions.CastRaySingleDistance(
            bvh.pointer, origin, direction, max_distance
        )

    else:
        # Determine size of result array. This should be the largest
        # out of the two arrays. 
        origin_size = 0 if origin_is_point else len(origin)
        direction_size = 0 if direction_is_point else len(direction)
        result_size = max(origin_size, direction_size)
        
        # If this is zero, then there's a problem with the above block
        assert result_size != 0

        # Call native function
        vector_ptr, array_ptr = raytracer_native_functions.CastMultipleRaysDistance(
            bvh.pointer, origin, direction, max_distance
        )

        # Construct RayResultList and return
        return RayResultList(vector_ptr, array_ptr, result_size, 1)


def IntersectForPoint(
    bvh: EmbreeBVH,
    origins: Union[Iterable[Tuple[float, float, float]], Tuple[float, float, float]],
    directions: Union[Iterable[Tuple[float, float, float]], Tuple[float, float, float]],
    max_distance: float = -1,
) -> List[Union[Tuple[float, float, float], None]]:
    """ Cast one or more rays based on input origins and directions 
        and get the hit point.
    
    To shoot multiple rays from one origin, or cast rays from multiple origins
    in a single direction, set origins OR directions to a single value. If
    they are both set to a single value then the ray will be cast as a single 
    ray via CastRay.

    Note:
        Accepts the following configurations:
            1) Single origin, single direction
            2) Multiple origins, multiple directions
            3) Single origin, multiple directions
            4) Multiple origins, single direction
    Args:
        origins: A list of origins or the origin point to shoot from
        directions: A list of directions or the direction to shoot in
        max_distance: Maximum distance that a ray can travel. Any hits beyond this point
            are not counted
    Returns:
        List: an ordered list containing None where rays did not intersect any geometry
            and tuples of 3 floats where the rays did intersect geometry
    Raises:
        TypeError : When the passed BVH is invalid

    Examples:
        Cast a single ray straight downwards

        >>> from dhart.geometry import LoadOBJ, CommonRotations, ConstructPlane
        >>> from dhart.raytracer import EmbreeBVH, IntersectForPoint

        >>> loaded_obj = ConstructPlane()
        >>> loaded_obj.Rotate(CommonRotations.Yup_to_Zup)
        >>> bvh = EmbreeBVH(loaded_obj)

        >>> hit_point = IntersectForPoint(bvh, (0,0,1), (0,0,-1))
        >>> print(hit_point)
        (0.0, 0.0, 5.960464477539063e-08)
    """
    isValidBVH(bvh)
    origins_is_list = False
    directions_is_list = False
    origin = None
    direction = None

    # Check if origins is a list
    if isinstance(origins, list):
        # If origin only has a single element then just take the first
        # value and act as if it was a single instance
        if len(origins) == 1:
            origin = origins[0]
        else:
            origins_is_list = True
    else:
        origin = origins

    # Check if Directions is a list
    if isinstance(directions, list):
        # If directions only has a single element then just take the first
        # value and act as if it was a single instance
        if len(directions) == 1:
            direction = directions[0]
        else:
            directions_is_list = True
    else:
        direction = directions

    # They are both lists so we're casting
    if directions_is_list and origins_is_list:
        # this will cause a problem in C if it isn't caught
        if len(directions) != len(origins):
            print("Length of directions and origins do not match!")
            raise RuntimeError()
        return raytracer_native_functions.CastMultipleRays(
            bvh.pointer, origins, directions, max_distance
        )
    elif directions_is_list and not origins_is_list:
        return raytracer_native_functions.CastOneOriginMultipleDirections(
            bvh.pointer, origin, directions, max_distance
        )
    elif not directions_is_list and origins_is_list:
        return raytracer_native_functions.CastMultipleOriginsOneDirection(
            bvh.pointer, origins, direction, max_distance
        )
    elif not directions_is_list and not origins_is_list:
        return raytracer_native_functions.CastRay(
            bvh.pointer, origin, direction, max_distance
        )


def IntersectOccluded(
    bvh: EmbreeBVH,
    origins: Union[Iterable[Tuple[float, float, float]], Tuple[float, float, float]],
    directions: Union[Iterable[Tuple[float, float, float]], Tuple[float, float, float]],
    max_distance: float = -1,
) -> Union[List[bool], bool]:
    """ Cast one or more occlusion rays in C++

    Occlusion rays are faster than standard rays, however can only return whether
    or not they hit anything. 
    
    Returns:
        List[bool] or bool : an ordered list of booleans where true indicates a
            hit, and false indicates a miss. If a single element is passed, only
            bool is returned.
    
    Args:
        origins : A list of origin points, or a single origin point
        directions : A list of directions or a single direction
        max_distance : Maximum distance that a ray can travel. Any hits beyond this point
            are not counted
    
    Raises:
        TypeError: BVH is not a valid EmbreeBVH

    Example:
        Casting multiple rays from a single origin in multiple directions

        >>> from dhart.geometry import LoadOBJ, CommonRotations, ConstructPlane
        >>> from dhart.raytracer import EmbreeBVH, IntersectOccluded

        >>> loaded_obj = ConstructPlane()
        >>> loaded_obj.Rotate(CommonRotations.Yup_to_Zup)
        >>> bvh = EmbreeBVH(loaded_obj)

        >>> directions = [(0,0,-1), (0,1,0), (1,0,0)]
        >>> hit_point = IntersectOccluded(bvh, (0,0,1), directions)
        >>> print(hit_point)
        [True, False, False]
    """
    isValidBVH(bvh)

    if len(origins) == 1 or not isinstance(origins, List):
        origins = (origins[0], origins[1], origins[2])

    res = raytracer_native_functions.CastOcclusionRays(
        bvh.pointer, origins, directions, max_distance
    )

    if len(res) == 1:
        return res[0]
    else:
        return res

def IntersectDistanceDouble(bvh: EmbreeBVH, origin:Tuple[float, float, float], direction:Tuple[float, float, float]) -> float:
    """ Obtain the distance between a raycast and a point of intersection with double precision

    Args:
        bvh (EmbreeBVH): BVH to intersect with
        origin (Tuple[float, float, float]): Origin point of the ray
        direction (Tuple[float, float, float]): Direction the ray is cast in

    Returns:
        float: Distance from origin to the point of intersection. If this value is less than 1 then 
                no intersection could be found.
    """
   
    return raytracer_native_functions.C_PreciseIntersection(bvh.pointer, origin, direction)
