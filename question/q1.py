#!/usr/bin/env python3

ways = 0
def step(n):
  if (n < 0):
    return 

  if (n == 0): 
    global ways
    ways = ways + 1
    return

  step(n-1)
  step(n-2)

step(5)
print(ways)
