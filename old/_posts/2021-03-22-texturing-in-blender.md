---
layout: post
---

As a component of learning Blender, I decided I would learn the general shader
workflow, creating textures and materials for various objects. It's pretty common
to model and render cars, so that's what I'm starting with. In particular, I'm
working with a 3D model of a 1954 Mercedes-Benz 300 SL Gullwing from
[Sketchfab](https://skfb.ly/6TXpZ).

It's been interesting working with someone else's model. Coming from a
physically-based rendering perspective, I find that a lot of materials are
often not modeled correctly. For example, using opacity for glass is a big
no-no for me. Instead, using the Principled BSDF shader in Blender, we have to
use multiple parameters to correctly model glass: Specular, Roughness,
Transmission, Transmission Roughness, and IOR.

Roughness is pretty simple. This models the roughness of the surface of the
material. Glass is usually quite smooth, so set this fairly high. 1.0 is
perfectly smooth, but to add a hint of imperfection, I usually set this to
around 0.95-0.98.

Transmission models how much light transmits (obviously) _through_ the
material. Glass used for cars is obviously quite clear, so we want the
transmission pretty high. Setting it to 1.0 is the easy way, meaning it fully
transmits all light. Again I find that setting it just a bit below, like
0.95, lends a bit more realism to the glass, since nothing is quite so
perfectly clear.

Transmission roughness provides a way to control how much light is scattered as
it transmits through the material, i.e. internal roughness, as opposed to
surface roughness. This allows the glass to look more diffuse, almost like
sandblasted or etched glass. Something around 0.5 to pretty high for glass in a
car; or useful to make headlight glass look old and fogged. Again, I like to
add a little bit of imperfection here for realism, so normally I set this to
around 0.05 or 0.1.

IOR is fairly straightforward; when light passes through a material, the
material may cause the light to bend, or refract. The amount to which is
happens is called the index of refraction, which is constant for a material.
Glass is 1.5, so that's that. We can then use the IOR to compute the correct
specular reflection amount for a material using [Fresnel's
equations](https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/reflection-refraction-fresnel).
Luckily this is simple for glass, and specular computes to 0.5.

Now, if you've modeled your glass as a flat mesh, which this Gullwing model
has, then you'll notice setting the IOR to 1.5 will cause a weird lensing
effect. Objects behind the glass will look bent and/or magnified. This is
happening because light is refracting once as it passes through the infinitely
thin glass mesh, but in reality it is refracting _within_ a glass with some
depth. What we need to do to combat this is give thickness to the glass.
Thankfully, this is easy by adding a Solidify modifier in Blender. By default
this usually sets thickness to 0.1 m, which is _really_ thick for windshields
and headlights. I usually set the thickness to 0.005 m, or half a centimeter,
for these glass objects.
