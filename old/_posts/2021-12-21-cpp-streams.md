---
layout: post
---

I had an idea to inherit from the C++ standard library `ostream` to deal with
logging/information messages in a C++-based application I work on.  I'm not
entirely sure it's the right approach, and I get the feeling I am developing a
solution and finding the problem it solves in parallel. Not always the best
sign, but it has been a fun learning experience so far.

## the stream stack

So as I quickly found out, inheriting from `std::ostream` isn't so simple,
because that class itself isn't so simple.  Despite this, getting a working
inherited version doesn't actually take too much code, for example (this
StackOverflow answer)[https://stackoverflow.com/a/2212940/4765406].

The core of it involves creating your own inherited stream buffer, and
overloading the appropriate methods within it.
