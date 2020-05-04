---
layout: post
---

I had a need to plot some numbers that I was receiving from another process.
To make it quick, I wanted to plot in Python using `matplotlib`. It wasn't
quite as quick as I was hoping, however. Hopefully sharing this will speed
things up in the future, though.

I found various answers on StackOverflow suggesting various ways to update a
plot. Ultimately the simplest was using `matplotlib`'s animation library. I
guess that makes sense, since it's designed to update plots!

First, set up your figure and axes. I am also creating a formatter and locator,
which govern how and where tick marks are printed:

```python
fig = pyplot.figure(figsize=(7, 3), tight_layout=True)
fig.canvas.set_window_title('updating plot')
ax = fig.add_subplot(1, 1, 1)

xfmt = dates.DateFormatter('%H:%M:%S')
xloc = ticker.LinearLocator(numticks=5)
```

At this point, you can initialize your axes with any formatting options.  Most
of this is optional, but there is one important setting (for me), which is
setting the x-axis to use dates:

```python
for spine in ['top', 'right', 'bottom', 'left']:
  ax.spines[spine].set_visible(False)
ax.xaxis_date() # tell matplotlib that we're using dates for x-values

ax.set_title('updating measured value')
ax.set_ylabel('measured value')

ax.set_ylim(0, 100) # known value range

# tell the x-axis to place 5 ticks with a simple time format
ax.xaxis.set_major_formatter(xfmt)
ax.xaxis.set_major_locator(xloc)

# set some horizontal lines to quickly read values
ax.grid(True, 'major', 'y', ls='--', lw=0.5, c='k', alpha=0.3)
```

Finally, we can add our updating function using the animation library. The
updating function needs to take at least an `i` parameter which dictates which
iteration being called. This is useful if you have a pre-calculated array of
values that you are animating over. In my case, the values are unknown as they
are coming in as measurements. We can add these as extra arguments to the
`fargs` parameter:

```python
def update(i, x, y):
  '''
  update our plot
  i: current iteration
  x: time
  y: measured values
  '''

  new_x, new_y = get_values() # poll the measurement process for data
  x.append(new_x)
  y.append(new_y)

  # limit plot to the last 30 points
  x = x[-30:]
  y = y[-30:]
  
  ax.plot_date(x, y, fmt='-')
  
t = []
v = []
anim = animation.FuncAnimation(fig, update, fargs=(t, v), interval=1000)
pyplot.show()
```

That will get the plot updating every second! However, you'll notice a lot of
our formatting settings are hosed upon update, so we need to re-apply them. To
keep things clean, I wrapped up most of these settings into their own function.
I call them once after creating the axes (so that the initial window looks
"correct" even without data), and once during the update function.

```python
def format_axes(ax, init=False):
  if not init:
    ax.clear()

  ax.set_title('updating measured value')
  ax.set_ylabel('measured value')
  
  ax.set_ylim(0, 100) # known value range
  
  # tell the x-axis to place 5 ticks with a simple time format
  ax.xaxis.set_major_formatter(xfmt)
  ax.xaxis.set_major_locator(xloc)
  
  # set some horizontal lines to quickly read values
  ax.grid(True, 'major', 'y', ls='--', lw=0.5, c='k', alpha=0.3)
```
