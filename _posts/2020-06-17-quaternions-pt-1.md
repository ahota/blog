---
layout: post
---

Quaternions are a good way to represent rotations for objects in 3D space. But
they can also be used for rotating or orbiting a camera around objects.
Rotating the camera about a central point -- i.e. moving the camera along the
surface of an invisible -- is the basis of an "arcball" camera. And the fact
that it rotates on a sphere makes quaternions perfect.  The other option is
Euler angles, which are mathematically much simpler. But you quickly run into
"gimbal lock" [^gimbal]

The downside of quaternions are that they are a bit abstract, especially if you
read the mathematically rigorous definitions of them.  My understanding of them
was shaky; I pretty much only learned of them in school, but not about them.  I
needed to add keyframing to an arcball camera, which required interpolating
quaternions, so I needed to learn more. I'm writing these blog posts to share
what I learned.

## what are quaternions?

The first thing I struggled a bit with was understanding _what_ a quaternion
was and what it was doing in the context of rotating objects or the camera. I
knew it was a four-valued "thing", hence quat-ernion, but I didn't understand
much more.

The basic description is that a quaternion represents a rotation about an axis.
Those are our four values: the rotation, θ, and the 3 components of our axis,
<x, y, z>. Mathematically, I understood this, but I didn't quite get how it
applied until I had my "aha" moment.

Suppose someone hands you a toy and you look at it, so you turn it over and
rotate it around in your hand. When you do this, you wouldn't rotate it around
one axis at a time. That would look robotic, and probably make the person who
gave you the toy suspicious. The natural way we handle objects is we just
rotate them intuitively. To look at one side, we just rotate it so that side
faces us. In other words, we _rotate it by some angle about some arbitrary
axis_. We've been using quaternions this whole time.

### representations

Thinking about quaternions as a rotation around an axis uses the appropriately-named axis-angle notation. For a quaternion **q**, 

**q** = <θ, **a**>, where **a** is a vector in 3D space

This is our intuitive representation. From this, we can bring back into the more traditional form:

**q** = _a_ + **a**

or equivalently,

**q** = _a_ + _b_**i** + _c_**j** + _d_**k**, where _a_, _b_, _c_, and _d_ are
real numbers, and **i**, **j**, and **k** are quaternion unit vectors

These unit vectors are... weird. Quaternions actually depict a 4D space, where
**i**, **j**, and **k** are unit vectors in _complex_ 3D space. In other words,
**i**, **j**, and **k** are imaginary. However, and here's something that
confused me for a while, they are _not_ the imaginary numbers you typically
think of when you see **i**.

Finally, we can also represent it in this trignometric form:

**q** = cos(θ/2) + sin(θ/2) \* **a**

This form will be useful later when we interpolate.

### properties

I won't go into all the properties here, because there are a lot (and I don't
fully understand them all) [^props]. But I will talk about the most important ones for
my use case, interpolating quaternions for a camera path. I'm also going to
leave out deriving the math behind these statements, just for space.

First, we need a unit quaternion.  There are multiple ways to describe a unit
quaternion. The most intuitive is that the axis **e** is a unit vector (it has
a magnitude of 1).  This is the case when the magnitude of the axis **e**
components _b_, _c_, and _d_ have magnitude 1 -- in other words it has a norm
of 1. We want unit quaternions because they actually describe rotations along
the surface of the unit sphere. This is the basis of the arcball camera.

Multiplying quaternions isn't quite as easy as you might hope. It breaks down
into several components, including a cross product and a dot product. Using the
form **q** = _a_ + **a**:

**qp** = _ab_ + _a_**b** + _b_**a** + **a**×**b** - **a**⋅**b**

One thing to note is that quaternion multiplication is NOT commutative, so
**q** \* **p** is not the same as **p** \* **q**. Multiplying two quaternions
together will always produce the same resulting rotation. Think about
interacting with an object in 3D space, i.e. rotating the camera around it.
Each rotation can be described as a quaternion, so every time you rotate, you
are effectively adding a quaternion to a stack. If we reset our camera, we can
then "replay" all of our rotations again by applying the quaternions
one-by-one, and we will arrive at our final rotation again.

Does that sound familiar? That's exactly what an animation is. That's what the
keyframed camera motion will be.

Two more properties.

A quaternion **q** produces the same rotation as its negated version, -**q**.
This will be really useful for when we need to optimize our interpolated path.

Finally, we need to know the conjugate and inverse of quaternions. The conjugate of a quaternion just negates the vector component:

**q**\* = _a_ + -**a**

What's the conjugate useful for? Well, despite the notation, the scalar and
vector components of a quaternion are not easily separable. That is, you
couldn't just say _a_ is the scalar for **q**. However, you can separate these
two components with the conjugate:

The scalar part _s_ of **q** = (**q** + **q**\*) / 2  
The vector part **v** of **q** = (**q** - **q**\*) / 2

One special property of the conjugate is that "re-conjugating" it gives you the
original quaternion back, i.e. (**q**\*)\* = q.

We use the conjugate the compute the inverse, which is a very important
property for us. The inverse is:

**q**^-1 = **q**\* / |**q**|^2

The denomatinator is the norm, or magnitude, of the quaternion, squared. This
is just the usual Euclidean norm of _a_, _b_, _c_, and _d_. The inverse will
allow us to "undo" a rotation from a quaternion.

Here's the crazy part, for a unit quaternion, the inverse and conjugate are
equal! What's useful about this? Well for one, we don't need to compute the
norm and in order to calculate the inverse; we can just negate the axis.This
makes it easy to rotate an object(or camera) with a quaternion, which
mathematically is called the conjugation of each point(or vector) by a
quaternion **q**:

**p**' = **qpq**^-1, which is equivalent to **qpq**\* for unit quaternions.

From here on in this series I'll be exclusively talking about unit quaternions.

---

[^props]: http://www.ncsa.illinois.edu/People/kindr/emtc/quaternions/
[^gimbal]: https://en.wikipedia.org/wiki/Gimbal_lock#In_three_dimensions
