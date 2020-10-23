#!/usr/bin/env python3

data = [[7*60*100, 10*60*100]]
# data = [[7*60*100, 10*60*100], [8*60*100, 9*60*100]]
# data = [[7*60*100, 10*60*100], [13*60*100, 14*60*100]]
# data = [[1*60*100, 5*60*100], [2*60*100, 3*60*100], [3*60*100, 6*60*100]]
# data = [[1*60*100, 5*60*100], [2*60*100, 3*60*100], [4*60*100, 5*60*100]]
# data = [[4*60*100, 5*60*100], [1*60*100, 5*60*100], [2*60*100, 3*60*100]]
# data = [[1*60*100, 5*60*100], [2*60*100, 3*60*100], [2*60*100+30, 6*60*100], [10*60*100, 11*60*100], [10*60*100, 11*60*100], [10*60*100, 11*60*100]]
# data = [[1*60*100, 5*60*100], [2*60*100, 3*60*100], [2*60*100+30, 6*60*100], [10*60*100, 11*60*100], [10*60*100, 11*60*100], [10*60*100, 11*60*100], [12*60*100, 13*60*100], [12*60*100, 13*60*100], [12*60*100, 13*60*100]]

result = []
start = []
end = []
count = 0
isdownpre = False
isdown = False
for i in range(0, 24*60*100):
  for d in data:
    if i == d[0]:
      count = count + 1
      start.append([i, count])
      isdown = False
    elif i == d[1]:
      count = count - 1
      end.append([i, count])
      isdown = True  

    if not isdownpre and isdown:
      result.append([start[-1][0], i, start[-1][1]])

    isdownpre = isdown
    
print(start)
print(end)
print("====")
# print(result)
for item in result:
  print("start: {} end: {} count: {}".format(item[0], item[1], item[2]))