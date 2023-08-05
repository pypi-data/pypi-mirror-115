
# -*- coding: utf-8 -*-

u'''Extended 3-D vector class L{Vector3d} and functions.

Function L{intersection3d3}, L{intersections2}, L{iscolinearWith},
L{nearestOn}, L{parse3d}, L{sumOf}, L{trilaterate2d2} and
L{trilaterate3d2}.
'''

from pygeodesy.basics import isnear0, len2, map2, _xnumpy
from pygeodesy.errors import _and, _AssertionError, IntersectionError, \
                              NumPyError, _TypeError, _ValueError, \
                              VectorError, _xError, _xkwds, _xkwds_popitem
from pygeodesy.fmath import fdot, fsum, fsum_, hypot, hypot2_
from pygeodesy.formy import _radical2
from pygeodesy.interns import EPS, EPS0, EPS02, EPS1, EPS4, MISSING, NN, \
                             _EPSqrt, _and_, _coincident_, _colinear_, _COMMA_, \
                             _COMMASPACE_, _datum_, _h_, _height_, _intersection_, \
                             _invalid_, _name_, _near_concentric_, _no_, _radius_, \
                             _SPACE_, _too_, _xyz_, _y_, _z_, _0_0, _0_5, _1_0, _2_0
from pygeodesy.lazily import _ALL_DOCS, _ALL_LAZY
from pygeodesy.named import _NamedTuple, _Pass, _xnamed, _xotherError
from pygeodesy.namedTuples import Intersection3Tuple, Vector2Tuple, \
                                  Vector3Tuple  # Vector4Tuple
from pygeodesy.streprs import Fmt
from pygeodesy.units import Float, Radius, Radius_
from pygeodesy.vector3dBase import Vector3dBase

from contextlib import contextmanager
from math import sqrt

__all__ = _ALL_LAZY.vector3d
__version__ = '21.07.31'

_center_ = 'center'
_deltas_ = 'deltas'
_raise_  = 'raise'
_Type_   = 'Type'


class Circum3Tuple(_NamedTuple):  # in .latlonBase
    '''3-Tuple C{(radius, center, deltas)} with the C{circumradius} and trilaterated
       C{circumcenter} of the C{circumcircle} through 3 points (aka {Meeus}' Type II
       circle) or the C{radius} and C{center} of the smallest I{Meeus}' Type I circle.
       The C{center} is unambiguous if C{deltas} is C{None}, otherwise C{center} is
       the mean and C{deltas} the differences of the L{trilaterate3d2} results.
    '''
    _Names_ = (_radius_, _center_, _deltas_)
    _Units_ = ( Radius,  _Pass,    _Pass)


class Meeus2Tuple(_NamedTuple):
    '''2-Tuple C{(radius, Type)} with C{radius} and I{Meeus}' {Type} of the smallest
       circle I{containing} 3 points.  C{Type} is C{None} for a I{Meeus}' Type II
       C{circumcircle} passing though all 3 points.  Otherwise C{Type} is the center
       of a I{Meeus}' Type I circle with 2 points on (a diameter of) and 1 point
       inside the circle.
    '''
    _Names_ = (_radius_, _Type_)
    _Units_ = ( Radius,  _Pass)


class Vector3d(Vector3dBase):
    '''Extended 3-D vector.

       In a geodesy context, these may be used to represent:
        - n-vector representing a normal to a point on earth's surface
        - earth-centered, earth-fixed cartesian (ECEF)
        - great circle normal to vector
        - motion vector on earth's surface
        - etc.
    '''
    _numpy = None  # module numpy iff imported by trilaterate3d2 below

    def circum3(self, point2, point3, circum=True, eps=EPS4):
        '''Return the radius and center of the smallest circle I{through} or I{containing}
           this and two other points.

           @arg point2: Second point (L{Vector3d}, C{Vector3Tuple} or C{Vector4Tuple}).
           @arg point3: Third point (L{Vector3d}, C{Vector3Tuple} or C{Vector4Tuple}).
           @kwarg circum: If C{True} return the C{circumradius} and C{circumcenter},
                          always, ignoring the I{Meeus}' Type I case (C{bool}).
           @kwarg eps: Tolerance passed to function L{trilaterate3d2}.

           @return: A L{Circum3Tuple}C{(radius, center, deltas)}.  The C{center} is
                    coplanar with all three points.

           @raise ImportError: Package C{numpy} not found, not installed or older than
                               version 1.15.

           @raise IntersectionError: Near-concentric, coincident or colinear points or
                                     a trilateration or C{numpy} issue.

           @raise TypeError: Invalid B{C{point2}} or B{C{point3}}.

           @see: Method C{meeus2} and functions L{circum3} and L{meeus2}.
        '''
        try:
            r, c, d, _, _ = _circum5(self, point2, point3, circum=circum, eps=eps,
                                                           clas=self.classof)
        except (AssertionError, TypeError, ValueError) as x:
            raise _xError(x, point=self, point2=point2, point3=point3, circum=circum)
        return Circum3Tuple(r, c, d)

    def iscolinearWith(self, point1, point2, eps=EPS):
        '''Check whether this and two other points are colinear.

           @arg point1: One point (L{Vector3d}, C{Vector3Tuple}
                                   or C{Vector4Tuple}).
           @arg point2: Another point (L{Vector3d}, C{Vector3Tuple}
                                       or C{Vector4Tuple}).
           @kwarg eps: Tolerance (C{scalar}), same units as C{x},
                       C{y}, and C{z}.

           @return: C{True} if this point is colinear with B{C{point1}}
                    and B{C{point2}}, C{False} otherwise.

           @raise TypeError: Invalid B{C{point1}} or B{C{point2}}.

           @see: Method L{nearestOn}.
        '''
        v = self if self.name else _otherV3d(this=self)
        return _iscolinearWith(v, point1, point2, eps=eps)

    def meeus2(self, point2, point3, circum=False):
        '''Return the radius and I{Meeus}' Type of the smallest I{containing} or
           I{through} this and two other points.

           @arg point2: Second point (L{Vector3d}, C{Vector3Tuple} or C{Vector4Tuple}).
           @arg point3: Third point (L{Vector3d}, C{Vector3Tuple} or C{Vector4Tuple}).
           @kwarg circum: If C{True} return the C{circumradius} and C{circumcenter}
                          always, ignoring the I{Meeus}' Type I case (C{bool}).

           @return: L{Meeus2Tuple}C{(radius, Type)}.

           @raise IntersectionError: Coincident or colinear points, iff C{B{circum}=True}.

           @raise TypeError: Invalid B{C{point2}} or B{C{point3}}.

           @see: Method C{circum3} and functions L{circum3} and L{meeus2}.
        '''
        try:
            r, t, _, _ = _meeus4(self, point2, point3, circum=circum, clas=self.classof)
        except (TypeError, ValueError) as x:
            raise _xError(x, point=self, point2=point2, point3=point3, circum=circum)
        return r, t

    def nearestOn(self, other1, other2, within=True):
        '''Locate the point between two points closest to this point.

           @arg other1: Start point (L{Vector3d}).
           @arg other2: End point (L{Vector3d}).
           @kwarg within: If C{True} return the closest point between
                          the given points, otherwise the closest
                          point on the extended line through both
                          points (C{bool}).

           @return: Closest point (L{Vector3d}).

           @raise TypeError: Invalid B{C{other1}} or B{C{other2}}.

           @see: Method L{sphericalTrigonometry.LatLon.nearestOn3} and
                 U{3-D Point-Line distance<https://MathWorld.Wolfram.com/
                 Point-LineDistance3-Dimensional.html>}.
        '''
        return _nearestOn(self, _otherV3d(other1=other1),
                                _otherV3d(other2=other2), within=within)

    def parse(self, str3d, sep=_COMMA_, name=NN):
        '''Parse an C{"x, y, z"} string to a L{Vector3d} instance.

           @arg str3d: X, y and z string (C{str}), see function L{parse3d}.
           @kwarg sep: Optional separator (C{str}).
           @kwarg name: Optional instance name (C{str}), overriding this name.

           @return: The instance (L{Vector3d}).

           @raise VectorError: Invalid B{C{str3d}}.
        '''
        return parse3d(str3d, sep=sep, Vector=self.classof, name=name or self.name)

    def trilaterate2d2(self, radius, center2, radius2, center3, radius3, eps=EPS, z=0):
        '''Trilaterate this and two other circles, each given as a (2-D) center
           and a radius.

           @arg radius: Radius of this circle (same C{units} as this C{x} and C{y}.
           @arg center2: Center of the 2nd circle (L{Vector3d}, C{Vector2Tuple},
                         C{Vector3Tuple} or C{Vector4Tuple}).
           @arg radius2: Radius of this circle (same C{units} as this C{x} and C{y}.
           @arg center3: Center of the 3rd circle (L{Vector3d}, C{Vector2Tuple},
                         C{Vector3Tuple} or C{Vector4Tuple}).
           @arg radius3: Radius of the 3rd circle (same C{units} as this C{x} and C{y}.
           @kwarg eps: Check the trilaterated point I{delta} on all 3 circles (C{scalar})
                       or C{None}.
           @kwarg z: Optional Z component of the trilaterated point (C{scalar}).

           @return: Trilaterated point as a L{Vector3d}C{(x, y, z=B{z})} instance.

           @raise IntersectionError: No intersection, colinear or near-concentric
                                     centers, trilateration failed some other way
                                     or the trilaterated point is off one circle
                                     by more than B{C{eps}}.

           @raise TypeError: Invalid B{C{center2}} or B{C{center3}}.

           @raise UnitError: Invalid B{C{radius1}}, B{C{radius2}} or B{C{radius3}}.

           @see: Function L{trilaterate2d2}.
        '''
        def _xyr3(r, **name_v):
            v = _otherV3d(useZ=False, **name_v)
            return v.x, v.y, r

        try:
            return trilaterate2d2(*(_xyr3(radius,  center=self) +
                                    _xyr3(radius2, center2=center2) +
                                    _xyr3(radius3, center3=center3)),
                                     eps=eps, Vector=Vector3d, z=z)
        except (AssertionError, TypeError, ValueError) as x:
            raise _xError(x, center=self,     radius=radius,
                             center2=center2, radius2=radius2,
                             center3=center3, radius3=radius3)

    def trilaterate3d2(self, radius, center2, radius2, center3, radius3, eps=EPS):
        '''Trilaterate this and two other spheres, each given as a (3-D) center
           and a radius.

           @arg radius: Radius of this sphere (same C{units} as this C{x}, C{y}
                        and C{z}).
           @arg center2: Center of the 2nd sphere (L{Vector3d}, C{Vector3Tuple}
                         or C{Vector4Tuple}).
           @arg radius2: Radius of this sphere (same C{units} as this C{x}, C{y}
                         and C{z}).
           @arg center3: Center of the 3rd sphere (L{Vector3d}, C{Vector3Tuple}
                         or C{Vector4Tuple}).
           @arg radius3: Radius of the 3rd sphere (same C{units} as this C{x}, C{y}
                         and C{z}).
           @kwarg eps: Tolerance (C{scalar}), same units as C{x}, C{y}, and C{z}.

           @return: 2-Tuple with two trilaterated points, each an instance of this
                    L{Vector3d} (sub-)class.  Both points are the same instance if
                    all three spheres intersect or abut in a single point.

           @raise ImportError: Package C{numpy} not found, not installed or
                               older than version 1.15.

           @raise IntersectionError: Near-concentric, colinear, too distant or
                                     non-intersecting spheres or C{numpy} issue.

           @raise TypeError: Invalid B{C{center2}} or B{C{center3}}.

           @raise UnitError: Invalid B{C{radius}}, B{C{radius2}} or B{C{radius3}}.

           @note: Package U{numpy<https://pypi.org/project/numpy>} is required,
                  version 1.15 or later.

           @see: Norrdine, A. U{I{An Algebraic Solution to the Multilateration
                 Problem}<https://www.ResearchGate.net/publication/
                 275027725_An_Algebraic_Solution_to_the_Multilateration_Problem>}
                 and U{I{implementation}<https://www.ResearchGate.net/publication/
                 288825016_Trilateration_Matlab_Code>}.
        '''
        try:
            return _trilaterate3d2(_otherV3d(center=self, NN_OK=False),
                                    Radius_(radius, low=eps),
                                    center2, radius2, center3, radius3,
                                    eps=eps, Vector=self.classof)
        except (AssertionError, TypeError, ValueError) as x:
            raise _xError(x, center=self,     radius=radius,
                             center2=center2, radius2=radius2,
                             center3=center3, radius3=radius3)


def circum3(point1, point2, point3, circum=True, eps=EPS4, useZ=True):
    '''Return the radius and center of the smallest circle I{through} or I{containing}
       three points.

       @arg point2: Second point (L{Vector3d}, C{Vector3Tuple} or C{Vector4Tuple}).
       @arg point3: Third point (L{Vector3d}, C{Vector3Tuple} or C{Vector4Tuple}).
       @kwarg circum: If C{True} return the C{circumradius} and C{circumcenter}
                      always, ignoring the I{Meeus}' Type I case (C{bool}).
       @kwarg eps: Tolerance for function L{trilaterate3d2} if C{B{useZ}=True} else
                   L{trilaterate2d2}.
       @kwarg useZ: If C{True}, use the Z components, otherwise use C{z=0} (C{bool}).

       @return: A L{Circum3Tuple}C{(radius, center, deltas)}.  The C{center} is
                coplanar with the three given points.

       @raise ImportError: Package C{numpy} not found, not installed or older than
                           version 1.15 and C{B{useZ}=True}.

       @raise IntersectionError: Near-concentric, coincident or colinear points or
                                 a trilateration or C{numpy} issue.

       @raise TypeError: Invalid B{C{point2}} or B{C{point3}}.

       @see: U{Jean Meeus, "Astronomical Algorithms", 2nd Ed. 1998, page 127ff
             <http://www.Agopax.IT/Libri_astronomia/pdf/Astronomical%20Algorithms.pdf>},
             U{circumradius<https://MathWorld.Wolfram.com/Circumradius.html>},
             U{circumcircle<https://MathWorld.Wolfram.com/Circumcircle.html>}, function
             L{meeus2} and methods C{circum3} and C{meeus2}.
    '''
    try:
        p1 = _otherV3d(useZ=useZ, point1=point1)
        r, c, d, _, _ = _circum5(p1, point2, point3, circum=circum, eps=eps, useZ=useZ,
                                                     clas=point1.classof)
    except (AssertionError, TypeError, ValueError) as x:
        raise _xError(x, point1=point1, point2=point2, point3=point3, circum=circum)
    return Circum3Tuple(r, c, d)


def _circum5(p1, point2, point3, circum=True, eps=EPS4, useZ=True,
                                 clas=Vector3d, **clas_kwds):  # in .latlonBase
    # (INTERNAL) Radius, center and deltas
    r, d, p2, p3 = _meeus4(p1, point2, point3, circum=circum, useZ=useZ,
                                               clas=clas, **clas_kwds)
    if d is None:  # Meeus' Type II or circum=True
        kwds = _xkwds(clas_kwds, eps=eps, Vector=clas, name=circum3.__name__)
        if useZ:
            a, b = _trilaterate3d2(p1, r, p2, r, p3, r, **kwds)
            if a is not b:
                c = a.plus(b).times(_0_5)  # mean
                if not a.isconjugateTo(b, minum=0, eps=eps):
                    d = b.minus(a)  # deltas
            else:  # no unambiguity
                c = a  # == b
        else:
            c = a = b = trilaterate2d2(p1.x, p1.y, r, p2.x, p2.y, r,
                                                      p3.x, p3.y, r, **kwds)
    else:  # Meeus' Type I, s.name=meeus2
        c = a = b = d
        d = None
    return r, c, d, a, b


def intersection3d3(start1, end1, start2, end2, eps=EPS, useZ=True,
                                                Vector=None, **Vector_kwds):
    '''Compute the intersection point of two lines, each defined by
       or through a start and end point.

       @arg start1: Start point of the first line (L{Vector3d},
                    C{Vector3Tuple} or C{Vector4Tuple}).
       @arg end1: End point of the first line (L{Vector3d},
                  C{Vector3Tuple} or C{Vector4Tuple}).
       @arg start2: Start point of the second line (L{Vector3d},
                    C{Vector3Tuple} or C{Vector4Tuple}).
       @arg end2: End point of the second line (L{Vector3d},
                  C{Vector3Tuple} or C{Vector4Tuple}).
       @kwarg eps: Tolerance for skew line distance and length (C{EPS}).
       @kwarg useZ: If C{True}, use the Z components, otherwise use C{z=0} (C{bool}).
       @kwarg Vector: Class to return intersections (L{Vector3d} or
                      C{Vector3Tuple}) or C{None} for L{Vector3d}.
       @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword arguments,
                           ignored if C{B{Vector} is None}.

       @return: An L{Intersection3Tuple}C{(point, outside1, outside2)} with
                C{point} a C{Vector3d} or B{C{Vector}}.

       @raise IntersectionError: Invalid, skew, non-coplanar or otherwise
                                 non-intersecting lines.

       @see: U{Line-line intersection<https://MathWorld.Wolfram.com/Line-LineIntersection.html>}
             and U{line-line distance<https://MathWorld.Wolfram.com/Line-LineDistance.html>},
             U{skew lines<https://MathWorld.Wolfram.com/SkewLines.html>} and U{point-line
             distance<https://MathWorld.Wolfram.com/Point-LineDistance3-Dimensional.html>}.
    '''
    try:
        v, o1, o2 = _intersect3d3(start1, end1, start2, end2, eps=eps, useZ=useZ)
    except (TypeError, ValueError) as x:
        raise _xError(x, start1=start1, end1=end1, start2=start2, end2=end2)
    v = _V_n(v, intersection3d3.__name__, Vector, Vector_kwds)
    return Intersection3Tuple(v, o1, o2)


def _intersect3d3(start1, end1, start2, end2, eps=EPS, useZ=False):
    # (INTERNAL) Intersect two lines, see L{intersection} above,
    # separated to allow callers to embellish any exceptions

    def _outside(t, d2):  # -1 before start#, +1 after end#
        return -1 if t < 0 else (+1 if t > d2 else 0)  # XXX d2 + eps?

    s1 = _otherV3d(useZ=useZ, start1=start1)
    e1 = _otherV3d(useZ=useZ, end1=end1)
    s2 = _otherV3d(useZ=useZ, start2=start2)
    e2 = _otherV3d(useZ=useZ, end2=end2)

    a  = e1.minus(s1)
    b  = e2.minus(s2)
    c  = s2.minus(s1)

    ab = a.cross(b)
    d  = abs(c.dot(ab))
    e  = max(EPS0, eps or _0_0)
    if d > EPS0 and ab.length > e:
        d = d / ab.length
        if d > e:  # argonic, skew lines distance
            raise IntersectionError(skew_d=d, txt=_no_(_intersection_))

    # co-planar, non-skew lines
    ab2 = ab.length2
    if ab2 < e:  # colinear, parallel or null line(s)
        x = a.length2 > b.length2
        if x:  # make a shortest
            a,  b  = b,  a
            s1, s2 = s2, s1
            e1, e2 = e2, e1
        if b.length2 < e:  # both null
            if c.length < e:
                return s1, 0, 0
            elif e2.minus(e1).length < e:
                return e1, 0, 0
        elif a.length2 < e:  # null (s1, e1), non-null (s2, e2)
            # like _nearestOn(s1, s2, e2, within=False, eps=e)
            t = s1.minus(s2).dot(b)
            v = s2.plus(b.times(t / b.length2))
            if s1.minus(v).length < e:
                o = _outside(t, b.length2)
                return (v, o, 0) if x else (v, 0, (o * 2))
        raise IntersectionError(length2=ab2, txt=_no_(_intersection_))

    cb =  c.cross(b)
    t  =  cb.dot(ab)
    o1 = _outside(t, ab2)
    v  =  s1.plus(a.times(t / ab2))
    o2 = _outside(v.minus(s2).dot(b), b.length2) * 2
    return v, o1, o2


def intersections2(center1, radius1, center2, radius2, sphere=True,
                                                       Vector=None, **Vector_kwds):
    '''Compute the intersection of two spheres or circles, each defined
       by a center point and a radius.

       @arg center1: Center of the first sphere or circle (L{Vector3d},
                     C{Vector3Tuple} or C{Vector4Tuple}).
       @arg radius1: Radius of the first sphere or circle (same units as
                     the B{C{center1}} coordinates).
       @arg center2: Center of the second sphere or circle (L{Vector3d},
                     C{Vector3Tuple} or C{Vector4Tuple}).
       @arg radius2: Radius of the second sphere or circle (same units as
                     the B{C{center1}} and B{C{center2}} coordinates).
       @kwarg sphere: If C{True} compute the center and radius of the
                      intersection of two spheres.  If C{False}, ignore the
                      C{z}-component and compute the intersection of two
                      circles (C{bool}).
       @kwarg Vector: Class to return intersections (L{Vector3d} or
                      C{Vector3Tuple}) or C{None} for L{Vector3d}.
       @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword arguments,
                           ignored if C{B{Vector} is None}.

       @return: If B{C{sphere}} is C{True}, a 2-Tuple of the C{center} and
                C{radius} of the intersection of the spheres.  The C{radius}
                is C{0.0} for abutting spheres.

                If B{C{sphere}} is C{False}, a 2-tuple of the intersection
                points of two circles.  For abutting circles, both points
                are the same B{C{Vector}} instance.

       @raise IntersectionError: Concentric, invalid or non-intersecting
                                 spheres or circles.

       @raise UnitError: Invalid B{C{radius1}} or B{C{radius2}}.

       @see: U{Sphere-Sphere<https://MathWorld.Wolfram.com/Sphere-
             SphereIntersection.html>} and U{circle-circle
             <https://MathWorld.Wolfram.com/Circle-CircleIntersection.html>}
             intersections.
    '''
    try:
        return _intersects2(center1, Radius_(radius1=radius1),
                            center2, Radius_(radius2=radius2),
                            sphere=sphere, Vector=Vector, **Vector_kwds)
    except (TypeError, ValueError) as x:
        raise _xError(x, center1=center1, radius1=radius1,
                         center2=center2, radius2=radius2)


def _intersects2(center1, r1, center2, r2, sphere=True, too_d=None,  # in .ellipsoidalBaseDI._intersections2
                                           Vector=None, **Vector_kwds):
    # (INTERNAL) Intersect two spheres or circles, see L{intersections2}
    # above, separated to allow callers to embellish any exceptions

    def _V3(x, y, z):
        v = Vector3d(x, y, z)
        n = intersections2.__name__
        return _V_n(v, n, Vector, Vector_kwds)

    def _xV3(c1, u, x, y):
        xy1 = x, y, _1_0  # transform to original space
        return _V3(fdot(xy1, u.x, -u.y, c1.x),
                   fdot(xy1, u.y,  u.x, c1.y), _0_0)

    c1 = _otherV3d(useZ=sphere, center1=center1)
    c2 = _otherV3d(useZ=sphere, center2=center2)

    if r1 < r2:  # r1, r2 == R, r
        c1, c2 = c2, c1
        r1, r2 = r2, r1

    m = c2.minus(c1)
    d = m.length
    if d < max(r2 - r1, EPS):
        raise IntersectionError(_near_concentric_)

    o = fsum_(-d, r1, r2)  # overlap == -(d - (r1 + r2))
    # compute intersections with c1 at (0, 0) and c2 at (d, 0), like
    # <https://MathWorld.Wolfram.com/Circle-CircleIntersection.html>
    if o > EPS:  # overlapping, r1, r2 == R, r
        x = _radical2(d, r1, r2).xline
        y = _1_0 - (x / r1)**2
        if y > EPS:
            y = r1 * sqrt(y)  # y == a / 2
        elif y < 0:
            raise IntersectionError(_invalid_)
        else:  # abutting
            y = _0_0
    elif o < 0:
        t = d if too_d is None else too_d
        raise IntersectionError(_too_(Fmt.distant(t)))
    else:  # abutting
        x, y = r1, _0_0

    u = m.unit()
    if sphere:  # sphere center and radius
        c = c1 if x < EPS  else (
            c2 if x > EPS1 else c1.plus(u.times(x)))
        t = _V3(c.x, c.y, c.z), Radius(y)

    elif y > 0:  # intersecting circles
        t = _xV3(c1, u, x, y), _xV3(c1, u, x, -y)
    else:  # abutting circles
        t = _xV3(c1, u, x, 0)
        t = t, t
    return t


def iscolinearWith(point, point1, point2, eps=EPS):
    '''Check whether a point is colinear with two other points.

       @arg point: The point (L{Vector3d}, C{Vector3Tuple} or
                              C{Vector4Tuple}).
       @arg point1: First point (L{Vector3d}, C{Vector3Tuple}
                                 or C{Vector4Tuple}).
       @arg point2: Second point (L{Vector3d}, C{Vector3Tuple}
                                  or C{Vector4Tuple}).
       @kwarg eps: Tolerance (C{scalar}), same units as C{x},
                   C{y} and C{z}.

       @return: C{True} if B{C{point}} is colinear B{C{point1}}
                and B{C{point2}}, C{False} otherwise.

       @raise TypeError: Invalid B{C{point}}, B{C{point1}} or
                         B{C{point2}}.

       @see: Function L{nearestOn}.
    '''
    return _iscolinearWith(_otherV3d(point=point),
                            point1, point2, eps=eps)


def _iscolinearWith(v, p1, p2, eps=EPS):
    # (INTERNAL) Check colinear, see L{isColinear} above,
    # separated to allow callers to embellish any exceptions
    v1 = _otherV3d(point1=p1)
    v2 = _otherV3d(point2=p2)
    n  = _nearestOn(v, v1, v2, within=False, eps=eps)
    return n is v1 or n.minus(v).length2 < eps


def meeus2(point1, point2, point3, circum=False, useZ=True):
    '''Return the radius and I{Meeus}' Type of the smallest circle I{containing}
       or I{through} three points.

       @arg point1: First point (L{Vector3d}, C{Vector3Tuple}, C{Vector4Tuple}
                    or C{Vector2Tuple} if C{B{useZ}=False}).
       @arg point2: Second point (L{Vector3d}, C{Vector3Tuple}, C{Vector4Tuple}
                    or C{Vector2Tuple} if C{B{useZ}=False}).
       @arg point3: Third point (L{Vector3d}, C{Vector3Tuple}, C{Vector4Tuple}
                    or C{Vector2Tuple} if C{B{useZ}=False}).
       @kwarg circum: If C{True} return the C{circumradius} and C{circumcenter}
                      always, ignoring the I{Meeus}' Type I case (C{bool}).
       @kwarg useZ: If C{True}, use the Z components, otherwise use C{z=0} (C{bool}).

       @return: L{Meeus2Tuple}C{(radius, Type)}.

       @raise IntersectionError: Coincident or linear points, iff C{B{circum}=True}.

       @raise TypeError: Invalid B{C{point1}}, B{C{point2}} or B{C{point3}}.

       @see: U{Jean Meeus, "Astronomical Algorithms", 2nd Ed. 1998, page 127ff
             <http://www.Agopax.IT/Libri_astronomia/pdf/Astronomical%20Algorithms.pdf>},
             U{circumradius<https://MathWorld.Wolfram.com/Circumradius.html>},
             U{circumcircle<https://MathWorld.Wolfram.com/Circumcircle.html>}, function
             L{circum3} and methods C{circum3} and C{meeus2}.
    '''
    try:
        A = _otherV3d(useZ=useZ, point1=point1)
        r, t, _, _ = _meeus4(A, point2, point3, circum=circum, useZ=useZ, classof=point1.classof)
    except (TypeError, ValueError) as x:
        raise _xError(x, point1=point1, point2=point2, point3=point3, circum=circum)
    return Meeus2Tuple(r, t)


def _meeus4(A, point2, point3, circum=False, useZ=True, clas=None, **clas_kwds):
    # (INTERNAL) Radius and Meeus' Type
    B = p2 = _otherV3d(useZ=useZ, point2=point2)
    C = p3 = _otherV3d(useZ=useZ, point3=point3)

    a = B.minus(C).length2
    b = C.minus(A).length2
    c = A.minus(B).length2
    if a < b:
        a, b, A, B = b, a, B, A
    if a < c:
        a, c, A, C = c, a, C, A

    if a > EPS02 and (circum or a < (b + c)):  # circumradius
        b = sqrt(b / a)
        c = sqrt(c / a)
        r = fsum_(_1_0, b, c) * fsum_(_1_0, b, -c) * fsum_(-_1_0, b, c) * fsum_(_1_0, -b, c)
        if r < EPS02:
            raise IntersectionError(_coincident_ if b < EPS0 or c < EPS0 else (
                                    _colinear_ if _iscolinearWith(A, B, C) else _invalid_))
        r = sqrt(a / r) * b * c
        t = None  # Meeus' Type II
    else:  # obtuse or right angle
        r = sqrt(a) * _0_5
        t = B.plus(C).times(_0_5)  # Meeus' Type I
        if clas is not None:
            t = clas(t.x, t.y, t.z, **_xkwds(clas_kwds, name=meeus2.__name__))
    return r, t, p2, p3


def nearestOn(point, point1, point2, within=True,
                                     Vector=None, **Vector_kwds):
    '''Locate the point between two points closest to a reference.

       @arg point: Reference point (L{Vector3d}, C{Vector3Tuple}
                                    or C{Vector4Tuple}).
       @arg point1: Start point (L{Vector3d}, C{Vector3Tuple} or
                                 C{Vector4Tuple}).
       @arg point2: End point (L{Vector3d}, C{Vector3Tuple} or
                               C{Vector4Tuple}).
       @kwarg within: If C{True} return the closest point between
                      both given points, otherwise the closest
                      point on the extended line through both
                      points (C{bool}).
       @kwarg Vector: Class to return closest point (L{Vector3d} or
                      C{Vector3Tuple}) or C{None} for L{Vector3d}.
       @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword
                           arguments, ignored if C{B{Vector} is None}.

       @return: Closest point (L{Vector3d} or C{Vector}).

       @raise TypeError: Invalid B{C{point}}, B{C{point1}} or B{C{point2}}..

       @see: Methods L{sphericalTrigonometry.LatLon.nearestOn3} and
             L{sphericalTrigonometry.LatLon.nearestOn3}
             U{3-D Point-Line distance<https://MathWorld.Wolfram.com/
             Point-LineDistance3-Dimensional.html>}.
    '''
    v = _nearestOn(_otherV3d(point =point),
                   _otherV3d(point1=point1),
                   _otherV3d(point2=point2), within=within)
    return _V_n(v, nearestOn.__name__, Vector, Vector_kwds)


def _nearestOn(p0, p1, p2, within=True, eps=EPS):
    # (INTERNAL) Get closest point, see L{nearestOn} above,
    # separated to allow callers to embellish any exceptions
    p21 = p2.minus(p1)
    d2 = p21.length2
    if d2 < eps:  # coincident
        p = p1  # ... or p2
    else:
        t = p0.minus(p1).dot(p21) / d2
        p = p1 if (within and t < eps) else (
            p2 if (within and t > (_1_0 - eps)) else
            p1.plus(p21.times(t)))
    return p


def _null_space2(numpy, A, eps):
    # (INTERNAL) Return the nullspace and rank of matrix A
    # @see: <https://SciPy-Cookbook.ReadTheDocs.io/items/RankNullspace.html>,
    # <https://NumPy.org/doc/stable/reference/generated/numpy.linalg.svd.html>,
    # <https://StackOverflow.com/questions/19820921>,
    # <https://StackOverflow.com/questions/2992947> and
    # <https://StackOverflow.com/questions/5889142>
    A = numpy.array(A)
    m = max(numpy.shape(A))
    if m != 4:  # for this usage
        raise _AssertionError(shape=m, txt=_null_space2.__name__)
    # if needed, square A, pad with zeros
    A = numpy.resize(A, m * m).reshape(m, m)
#   try:  # no numpy.linalg.null_space <https://docs.SciPy.org/doc/>
#       return scipy.linalg.null_space(A)  # XXX no scipy.linalg?
#   except AttributeError:
#       pass
    _, s, v = numpy.linalg.svd(A)
    t = max(eps, eps * s[0])  # tol, s[0] is largest singular
    r = numpy.sum(s > t)  # rank
    if r == 3:  # get null_space
        n = numpy.transpose(v[r:])
        s = numpy.shape(n)
        if s != (m, 1):  # bad null_space shape
            raise _AssertionError(shape=s, txt=_null_space2.__name__)
        e = float(numpy.max(numpy.abs(numpy.dot(A, n))))
        if e > t:  # residual not near-zero
            raise _AssertionError(res=e, tol=t, txt=_null_space2.__name__)
    else:  # coincident, colinear, concentric centers, ambiguous, etc.
        n = None
    # del A, s, vh  # release numpy
    return n, r


def _otherV3d(useZ=True, NN_OK=True, **name_v):  # in .ellipsoids.height4, .formy.hartzell3
    # check B{C{name#}} vector instance, return Vector3d
    if not name_v:
        raise _AssertionError(name_v=MISSING)

    name, v = _xkwds_popitem(name_v)
    if useZ and isinstance(v, Vector3dBase):
        return v if NN_OK or v.name else v.copy(name=name)

    try:
        return Vector3d(v.x, v.y, v.z if useZ else _0_0, name=name)
    except AttributeError:  # no _x_ or _y_ attr
        pass
    raise _xotherError(Vector3d(0, 0, 0), v, name=name, up=2)


def parse3d(str3d, sep=_COMMA_, name=NN, Vector=Vector3d, **Vector_kwds):
    '''Parse an C{"x, y, z"} string.

       @arg str3d: X, y and z values (C{str}).
       @kwarg sep: Optional separator (C{str}).
       @kwarg name: Optional instance name (C{str}).
       @kwarg Vector: Optional class (L{Vector3d}).
       @kwarg Vector_kwds: Optional B{C{Vector}} keyword arguments,
                           ignored if C{B{Vector} is None}.

       @return: New B{C{Vector}} or if B{C{Vector}} is C{None},
                a L{Vector3Tuple}C{(x, y, z)}.

       @raise VectorError: Invalid B{C{str3d}}.
    '''
    try:
        v = [float(v.strip()) for v in str3d.split(sep)]
        n = len(v)
        if n != 3:
            raise _ValueError(len=n)
    except (TypeError, ValueError) as x:
        raise VectorError(str3d=str3d, txt=str(x))
    return _V_n(Vector3Tuple(*v), name, Vector, Vector_kwds)


def sumOf(vectors, Vector=Vector3d, **Vector_kwds):
    '''Compute the vectorial sum of several vectors.

       @arg vectors: Vectors to be added (L{Vector3d}[]).
       @kwarg Vector: Optional class for the vectorial sum (L{Vector3d}).
       @kwarg Vector_kwds: Optional B{C{Vector}} keyword arguments,
                           ignored if C{B{Vector} is None}.

       @return: Vectorial sum as B{C{Vector}} or if B{C{Vector}} is
                C{None}, a L{Vector3Tuple}C{(x, y, z)}.

       @raise VectorError: No B{C{vectors}}.
    '''
    n, vectors = len2(vectors)
    if n < 1:
        raise VectorError(vectors=n, txt=MISSING)

    v = Vector3Tuple(fsum(v.x for v in vectors),
                     fsum(v.y for v in vectors),
                     fsum(v.z for v in vectors))
    return _V_n(v, sumOf.__name__, Vector, Vector_kwds)


def trilaterate2d2(x1, y1, radius1, x2, y2, radius2, x3, y3, radius3,
                                    eps=None, Vector=None, **Vector_kwds):
    '''Trilaterate three circles, each given as a (2-D) center and a radius.

       @arg x1: Center C{x} coordinate of the 1st circle (C{scalar}).
       @arg y1: Center C{y} coordinate of the 1st circle (C{scalar}).
       @arg radius1: Radius of the 1st circle (C{scalar}).
       @arg x2: Center C{x} coordinate of the 2nd circle (C{scalar}).
       @arg y2: Center C{y} coordinate of the 2nd circle (C{scalar}).
       @arg radius2: Radius of the 2nd circle (C{scalar}).
       @arg x3: Center C{x} coordinate of the 3rd circle (C{scalar}).
       @arg y3: Center C{y} coordinate of the 3rd circle (C{scalar}).
       @arg radius3: Radius of the 3rd circle (C{scalar}).
       @kwarg eps: Check the trilaterated point I{delta} on all 3
                   circles (C{scalar}) or C{None}.
       @kwarg Vector: Class to return the trilateration (L{Vector3d}) or C{None}.
       @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword arguments,
                           ignored if C{B{Vector} is None}.

       @return: Trilaterated point as C{B{Vector}(x, y, **B{Vector_kwds})}
                or L{Vector2Tuple}C{(x, y)} if C{B{Vector} is None}..

       @raise IntersectionError: No intersection, colinear or near-concentric
                                 centers, trilateration failed some other way
                                 or the trilaterated point is off one circle
                                 by more than B{C{eps}}.

       @raise UnitError: Invalid B{C{radius1}}, B{C{radius2}} or B{C{radius3}}.

       @see: U{Issue #49<https://GitHub.com/mrJean1/PyGeodesy/issues/49>},
             U{Find X location using 3 known (X,Y) location using trilateration
             <https://math.StackExchange.com/questions/884807>} and L{trilaterate3d2}.
    '''
    def _abct4(x1, y1, r1, x2, y2, r2):
        a =  x2 - x1
        b =  y2 - y1
        t = _tri_r2h(r1, r2, hypot(a, b))
        c = _0_0 if t else (hypot2_(r1, x2, y2) - hypot2_(r2, x1, y1))
        return a, b, c, t

    def _astr(**kwds):  # kwds as (name=value, ...) strings
        return Fmt.PAREN(_COMMASPACE_(*(Fmt.EQUAL(*t) for t in kwds.items())))

    r1 = Radius_(radius1=radius1)
    r2 = Radius_(radius2=radius2)
    r3 = Radius_(radius3=radius3)

    a, b, c, t = _abct4(x1, y1, r1, x2, y2, r2)
    if t:
        raise IntersectionError(_and(_astr(x1=x1, y1=y1, radius1=r1),
                                     _astr(x2=x2, y2=y2, radius2=r2)), txt=t)

    d, e, f, t = _abct4(x2, y2, r2, x3, y3, r3)
    if t:
        raise IntersectionError(_and(_astr(x2=x2, y2=y2, radius2=r2),
                                     _astr(x3=x3, y3=y3, radius3=r3)), txt=t)

    _, _, _, t = _abct4(x3, y3, r3, x1, y1, r1)
    if t:
        raise IntersectionError(_and(_astr(x3=x3, y3=y3, radius3=r3),
                                     _astr(x1=x1, y1=y1, radius1=r1)), txt=t)

    q = (a * e - b * d) * _2_0
    if isnear0(q):
        t = _no_(_intersection_)
        raise IntersectionError(_and(_astr(x1=x1, y1=y1, radius1=r1),
                                     _astr(x2=x2, y2=y2, radius2=r2),
                                     _astr(x3=x3, y3=y3, radius3=r3)), txt=t)
    t = Vector2Tuple((c * e - b * f) / q,
                     (a * f - c * d) / q, name=trilaterate2d2.__name__)

    if eps and eps > 0:
        for x, y, r in ((x1, y1, r1), (x2, y2, r2), (x3, y3, r3)):
            d = hypot(x - t.x, y - t.y)
            e = abs(d - r)
            if e > eps:
                t = _and(Float(delta=e).toRepr(), r.toRepr(),
                         Float(distance=d).toRepr())
                raise IntersectionError(t, txt=Fmt.exceeds_eps(eps))

    if Vector is not None:
        t = Vector(t.x, t.y, **_xkwds(Vector_kwds, name=t.name))
    return t


def trilaterate3d2(center1, radius1, center2, radius2, center3, radius3,
                                     eps=EPS, Vector=None, **Vector_kwds):
    '''Trilaterate three spheres, each given as a (3-D) center and a radius.

       @arg center1: Center of the 1st sphere (L{Vector3d}, C{Vector3Tuple}
                     or C{Vector4Tuple}).
       @arg radius1: Radius of the 1st sphere (same C{units} as C{x}, C{y}
                     and C{z}).
       @arg center2: Center of the 2nd sphere (L{Vector3d}, C{Vector3Tuple}
                     or C{Vector4Tuple}).
       @arg radius2: Radius of this sphere (same C{units} as C{x}, C{y}
                     and C{z}).
       @arg center3: Center of the 3rd sphere (L{Vector3d}, C{Vector3Tuple}
                     or C{Vector4Tuple}).
       @arg radius3: Radius of the 3rd sphere (same C{units} as C{x}, C{y}
                     and C{z}).
       @kwarg eps: Tolerance (C{scalar}), same units as C{x}, C{y}, and C{z}.
       @kwarg Vector: Class to return intersections (L{Vector3d} or
                      C{Vector3Tuple}) or C{None} for L{Vector3d}.
       @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword arguments,
                           ignored if C{B{Vector} is None}.

       @return: 2-Tuple with two trilaterated points, each a B{C{Vector}}
                instance.  Both points are the same instance if all three
                spheres abut/intersect in a single point.

       @raise ImportError: Package C{numpy} not found, not installed or
                           older than version 1.15.

       @raise IntersectionError: Near-concentric, colinear, too distant or
                                 non-intersecting spheres.

       @raise NumPyError: Some C{numpy} issue.

       @raise TypeError: Invalid B{C{center1}}, B{C{center2}} or B{C{center3}}.

       @raise UnitError: Invalid B{C{radius1}}, B{C{radius2}} or B{C{radius3}}.

       @note: Package U{numpy<https://pypi.org/project/numpy>} is required,
              version 1.15 or later.

       @see: Norrdine, A. U{I{An Algebraic Solution to the Multilateration
             Problem}<https://www.ResearchGate.net/publication/
             275027725_An_Algebraic_Solution_to_the_Multilateration_Problem>}
             and U{I{implementation}<https://www.ResearchGate.net/publication/
             288825016_Trilateration_Matlab_Code>} and L{trilaterate2d2}.
    '''
    try:
        return _trilaterate3d2(_otherV3d(center1=center1, NN_OK=False),
                                Radius_(radius1=radius1, low=eps),
                                center2, radius2, center3, radius3,
                                eps=eps, Vector=Vector, **Vector_kwds)
    except (AssertionError, NumPyError, TypeError, ValueError) as x:
        raise _xError(x, center1=center1, radius1=radius1,
                         center2=center2, radius2=radius2,
                         center3=center3, radius3=radius3)


def _trilaterate3d2(c1, r1, c2, r2, c3, r3, eps=EPS, Vector=None, **Vector_kwds):  # MCCABE 13
    # (INTERNAL) Intersect three spheres or circles, see L{trilaterate3d2}
    # above, separated to allow callers to embellish any exceptions, like
    # C{FloatingPointError}s from C{numpy}

    def _0f3d(F):
        # map numpy 4-vector to floats and split
        F0, x, y, z = map(float, F)
        return F0, Vector3d(x, y, z)

    def _N3(t01, x, z):
        # compute x, y and z and return as Vector
        v = x.plus(z.times(t01))
        n = trilaterate3d2.__name__
        return _V_n(v, n, Vector, Vector_kwds)

    @contextmanager  # <https://www.python.org/dev/peps/pep-0343/> Examples
    def _numpy(p):
        # get numpy with any errors raised as NumPyError
        np = Vector3d._numpy
        if np is None:  # get numpy, once or ImportError
            Vector3d._numpy = np = _xnumpy(trilaterate3d2, 1, 10)  # macOS' Python 2.7 numpy 1.8 OK
        try:  # <https://NumPy.org/doc/stable/reference/generated/numpy.seterr.html>
            e = np.seterr(all=_raise_)  # throw FloatingPointError for numpy errors
            yield np
        except Exception as x:  # mostly FloatingPointError?
            raise NumPyError(x.__class__.__name__, p, txt=str(x))
        finally:  # restore numpy error handling
            np.seterr(**e)

    def _roots(numpy, *coeffs):
        # only real, non-complex roots of a polynomial, if any
        rs = numpy.polynomial.polynomial.polyroots(coeffs)
        return tuple(float(r) for r in rs if not numpy.iscomplex(r))

    c2 = _otherV3d(center2=c2, NN_OK=False)
    c3 = _otherV3d(center3=c3, NN_OK=False)
    R  = [r1, Radius_(radius2=r2, low=eps),
              Radius_(radius3=r3, low=eps)]

    # get null_space Z, pseudo-inverse A and vector B, once
    t = -_2_0
    A = [(_1_0, t * c.x, t * c.y, t * c.z) for c in (c1, c2, c3)]  # 3 x 4
    with _numpy(None) as np:
        Z, _ = _null_space2(np, A, eps)
        A    =  np.linalg.pinv(A)  # Moore-Penrose pseudo-inverse
    if Z is None:  # coincident, colinear, concentric, etc.
        raise _trilaterror(c1, r1, c2, r2, c3, r3, eps)
    B = [c.length2 for c in (c1, c2, c3)]

    # perturbe radii to handle corner cases like this
    # <https://GitHub.com/mrJean1/PyGeodesy/issues/49>
    P = (_0_0,)
    if eps and eps > 0:
        p1 = max(eps,  EPS)
        p2 = max(eps, _EPSqrt)
        P += p1, -p1
        if p2 > p1:
            P += p2, -p2
    for p in P:
        b = [((r + p)**2 - b) for r, b in zip(R, B)]  # 1 x 3 or 3 x 1
        with _numpy(p) as np:
            X = np.dot(A, b)
            X0, x = _0f3d(X)
            Z0, z = _0f3d(Z)
            # quadratic polynomial coefficients, ordered (^0, ^1, ^2)
            t = _roots(np, x.length2       - X0,  # fdot(X, -_1_0, *x.xyz)
                           z.dot(x) * _2_0 - Z0,  # fdot(Z, -_0_5, *x.xyz) * 2
                           z.length2)             # fdot(Z,  _0_0, *z.xyz)
            if t:
                break
    else:  # coincident, concentric, colinear, too distant, no intersection, etc.
        raise _trilaterror(c1, r1, c2, r2, c3, r3, eps)

    v = _N3(t[0], x, z)
    if len(t) < 2:  # one intersection
        t = v, v
    elif abs(t[0] - t[1]) < eps:  # abutting
        t = v, v
    else:  # "lowest" intersection first (to avoid test failures)
        u = _N3(t[1], x, z)
        t = (u, v) if u < v else (v, u)
    return t


def _trilaterror(c1, r1, c2, r2, c3, r3, eps):
    # return IntersectionError with the cause of the error

    def _txt(c1, r1, c2, r2):
        t = _tri_r2h(r1, r2, c1.minus(c2).length)
        return _SPACE_(c1.name, _and_, c2.name, t) if t else t

    t = _txt(c1, r1, c2, r2) or \
        _txt(c1, r1, c3, r3) or \
        _txt(c2, r2, c3, r3) or (_colinear_ if
        _iscolinearWith(c1, c2, c3, eps=eps) else
        _no_(_intersection_))
    return IntersectionError(t, txt=None)


def _tri_r2h(r1, r2, h):
    # check for near-concentric or too distant spheres/circles
    return _too_(Fmt.distant(h)) if h > (r1 + r2) else (
           _near_concentric_ if h < abs(r1 - r2) else NN)


def _V_n(v, name, Vector, Vector_kwds={}):
    # return a named Vector instance
    if Vector is not None:
        v = Vector(v.x, v.y, v.z, **Vector_kwds)
    return _xnamed(v, name)


def _xyzn4(xyz, y, z, Error=_TypeError):  # see: .ecef
    '''(INTERNAL) Get an C{(x, y, z, name)} 4-tuple.
    '''
    try:
        t = xyz.x, xyz.y, xyz.z
        n = getattr(xyz, _name_, NN)
    except AttributeError:
        t = xyz, y, z
        n = NN
    try:
        x, y, z = map2(float, t)
    except (TypeError, ValueError) as x:
        d = dict(zip((_xyz_, _y_, _z_), t))
        raise Error(txt=str(x), **d)

    return x, y, z, n


def _xyzhdn6(xyz, y, z, height, datum, ll, Error=_TypeError):  # by .cartesianBase, .nvectorBase
    '''(INTERNAL) Get an C{(x, y, z, h, d, name)} 6-tuple.
    '''
    x, y, z, n = _xyzn4(xyz, y, z, Error=Error)

    h = height or getattr(xyz, _height_, None) \
               or getattr(xyz, _h_, None) \
               or getattr(ll,  _height_, None)

    d = datum or getattr(xyz, _datum_, None) \
              or getattr(ll,  _datum_, None)

    return x, y, z, h, d, n


__all__ += _ALL_DOCS(intersections2, sumOf, Vector3dBase)

# **) MIT License
#
# Copyright (C) 2016-2021 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
