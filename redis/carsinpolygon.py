import redis
from shapely.geometry import Point, Polygon


redis = redis.Redis(
     host= '127.0.0.1',
     port= '6379')


cararray = []
parkarray = []
coordinates = []
carswithinpoly = []
d = {}
dist = float(0)
mindist = float(0)
parkslot = ''
carlocation = 'carlocation'
parklocation = 'parklocation'
combine = 'combine'

cararray = redis.zrange(carlocation, 0, -1)
parkarray = redis.zrange(parklocation, 0, -1)

polycoord = [(53.5957650, 6.6906738), (52.7994403, 7.2290039), (53.0246963, 9.3273926), (53.7876718, 10.5743408), (54.7531612, 9.9810791), (54.8291723, 8.3001709), (53.5957650, 6.6906738)]

northcoastpoly = Polygon(polycoord)

for i in cararray:
     coordinates = redis.geopos(carlocation, i)
     pointcoord = Point(coordinates)
     if pointcoord.within(northcoastpoly) == True:
          carswithinpoly.append(i)

#print()
#print(len(cararray))

#print(carswithinpoly)

redis.zunionstore(combine,[carlocation, parklocation], aggregate='min')

for i in carswithinpoly:
     for j in parkarray:
          dist = redis.geodist(combine, i, j)
          #print(j)
          #print(dist)
          if mindist == 0.0:
               mindist = dist
               parkslot = j
          else:
               if dist < mindist:
                    mindist = dist
                    parkslot = j
     d[i] = parkslot
     
for i in d:
     print(i)
     print(d[i])