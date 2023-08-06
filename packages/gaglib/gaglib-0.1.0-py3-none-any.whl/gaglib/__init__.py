__version__ = '0.1.0'

import turtle as t

t.hideturtle()
t.speed(0)

hasCollider = False
hasGravity = False




def renderPlayer(size, hasCollider, hasGravity):
  t.pendown()
  t.circle(size, 100)

