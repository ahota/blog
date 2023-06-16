---
layout: post
---

suppose we have a cube and we want to rotate it. The Euler angles approach
would decompose this into up to 3 sub-rotations: one for each axis. While this
works, you will inevitably run into gimbal lock, which is discussed at length
on other websites.

in reality, if we had a cube to rotate, we would probably simply rotate into
position without decomposing it into sub-rotations. The decomposition isn't
physically intuitive, it's just a simplified way to deal with rotations
programmatically. what we are really doing is rotating the cube about some
arbitrary axis by some arbitrary angle.

and that's exactly what the axis-angle representation is for: rotating about an
axis **_a_** by _theta_.

we can keep this information as a vector (the axis) and a scalar (the angle).
we can also keep this information in a 4-element vector, which is exactly what
a quaternion does. note, every time I say quaternion here, I'm specifically
talking about a unit quaternion (i.e. the axis vector is a unit vector), also
known as a versor.

_C_ = cos(_theta_/2)  
_S_ = sin(_theta_/2)  
q = <_C_, _S_**_a_**>

vector form here

using quaternions for rotations is better than matrices, as we avoid the
accumulation of error while still allowing for rotation from the current
transformation. so in terms of the traditional graphics matrix transformation
process, we simply need to apply a new quaternion onto our matrix to update the
object's rotation.

cool, that lets us rotate an object. but what about the camera? typically when
we talk about raster graphics like GL, we are _emulating_ rotating the camera
around a world by rotating the world in the opposite direction. but I'm actually trying to rotate the camera about the world in world space.

rotate the camera on an invisible sphere that surrounds our world. this is the
approach for an arcball camera. camera moves get mapped to this sphere, and we
rotate by some angle. the axis we rotate by is determined by which direction we
want to rotate the camera (usually dictated by a mouse move).

given a camera starting point _p_ at (0, 0, -5) with an object at the origin, we can rotate the camera using a quaternion _q_ by "conjugating" _p_ by _q_ and getting our new position _p'_:

_p'_ = _qpq^-1_

where _q^-1_ is the inverse of the quaternion _q_. btw, _p_ can be thought of
as a quaternion where the axis equals _p_ and the angle is 0.  we just need a
way to convert a mouse move into a quaternion, but that's a separate problem.

okay, so we have camera movements around an object. what if we want to create a
path for the camera to follow? in other words, we want to keyframe camera
motion. what's great with quaternions here is we can simply "save" the current
rotation quaternion each time we want to create a keyframe without worrying
about any past or future keyframes. This is because the "current" quaternion
actually describes the rotation from a previous position. therefore, each
successive keyframe comes with this "path" built in.

the real problem is how to create all the rotations in between our keyframes.
for this, we can use slerp: spherical linear interpolation. The parameterizes
the rotation from _q1_ to _q2_, and creates a geodesic path for the camera to
follow on our invisible sphere. actually, we really want nlerp, which is simply the normalization of slerp to maintain our unit quaternions.

(there's a gotcha with slerp, where we want to avoid the long way around)

_unfortunately_ this is where every page I've read ends when talking about
quaternion interpolation. interpolating from _q1_ to _q2_ is great, but it's
only one segment of our path. What you'll find is applying slerp/nlerp to each
segment results in jerky camera movements where you hit a "corner" at each
keyframe. this problem persists unless you manually create a _lot_ of
keyframes. what we _really_ want is to create a smooth path.

paul bourke has a [great
page](http://paulbourke.net/miscellaneous/interpolation/) explaining some
common interpolation methods with examples on how to use them for a series of
points. from this, it seems like catmull-rom gives us the best balance between
smoothness and computational complexity.

from there, we can take a look at the book Graphics Gems 2, specifically at
section VIII.4, written by John Schlag[^1]. He gives the geometric simplification
for constructing a catmull-rom quaternion interpolation from known control
points (our keyframes).  essentially, what we will be doing is interpolating
between our original points a few times, then interpolating between those
interpolated points, then once again to get our "real" interpolated point.  he
also gives some pseudocode on how to do this.

Thanks, John Schlag! (not sarcasm)

here's the problem I haven't seen tackled: catmull-rom (or any of the higher
order interpolation functions) requires _four_ control points in order to
interpolate between _two_. That is, we need a control point before and after
the two points we are interpolating between. so, if we have 4 keyframes, we
don't get interpolated rotations for our first and last segments, only the
middle segment. taking a look back at paul bourke's page, he states:

> This does raise issues for how to interpolate between the first and last
> segments. In the examples here I just haven't bothered.

Thanks, Paul Bourke! (yes sarcasm)

But he also says:

> A common solution is the dream up two extra points at the start and end of
> the sequence, the new points are created so that they have a slope equal to
> the slope of the start or end segment.

okay, this is helpful, so legitimate thanks to Paul Bourke.

So, how do we create two new quaternions -- one before our known keyframes and
one after?

naively, I tried just duplicating the first and last quaternion.
this will result in garbage. slerp/nlerp need the dot product between the
two quaternions. Since they're the same quaternion, this is 1. The arccos of
this dot product is our quaternion's angle _theta_, which is 0. We end up
needing to divide by _sin(theta)_, and _sin(0) = 0_, so we're hosed.

what we want is to create two control points that roughly continue the path at
the beginning and end of our known control points. I'll call them the prefix
and suffix point. In 2d/3d cartesian coordinates, we could simply calculate the
slope between the first and second control points to extrapolate where our
prefix point should be, and likewise for the suffix point. 

"undo" the second quaternion to get an inverse transformed control point from the first??

[^1]: There are PDF copies of this book available online. But, it's worth
    owning a personal copy of, even if it's just shy of 20 years old now. The
    older books contain good wisdom! Also see
    [this](http://www.graphicsgems.org/) repository of all the gems from all the
    books. And get "Physically Based Rendering, 3rd Edition" while you're there;
    it's free.
