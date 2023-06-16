---
layout: post
---

- quaternions are good for describing arbitrary rotations
  - much better than euler angles, no gimbal lock
  - much less loss of precision compared to matrix multiplication
  - unfortunately a bit confusing to understand
  - axis-angle representation makes it easier to understand, some rotation angle _theta_ around an axis _a_
- so far we have actually described using quaternions for rotation in object space
  - usually we are rotating the camera about the object, not just rotating the object
  - this is the basis for an arcball camera: moving the camera along the surface of an invisible sphere (pointing inward) that encloses the object
  - we can create the same effective rotation by conjugating the camera position by the quaternion rotation
    - the camera position can be described as a zero-angle quaternion (i.e. the axis equals the 3D Cartesian coordinates)
