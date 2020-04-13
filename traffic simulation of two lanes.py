import numpy as np


##Function for slowing down cars if there's a traffic jam
def slowing (indexes, v):
    for i in indexes:                                      #for index in indexes where cars are
        indexing = list(indexes).index(i)                  #gets indexes of index array [0,1,2,3,..]
        if indexing + 1 <= len(indexes):                   #if index + 1 is less or equal to the length indexes array
            if indexing + 1 >= len(indexes):               #if it's the last index
                indexing -= (len(indexes))                 #goes to the start of the array
                x_new = v[i] + indexes[indexing] - len(v)  #get's new coordinate
                if x_new >= indexes[indexing + 1]:         #if new coordinate is more or same than for the next car 
                    if v[i] - 1 == 0:                      #and if the velocity is 1
                        v[i] = -1                          #changes the velocity to -1
                    else:
                        v[i] = len(v) + indexes[indexing + 1] - indexes[indexing] - 1 #gets new velocity
                        if v[i] == 0:                                                 #if new velocity is 0 
                            v[i] = -1                                                 #changes it to -1

            elif v[i] + indexes[indexing] >= indexes[indexing + 1]:   #if new coordinate is more or same than for the next car 
                if v[i] >= indexes[indexing + 1] - indexes[indexing]: #if the velocity is bigger than the distance between cars
                    if v[i] - 1 == 0:                                 #and if the velocity is 1
                        v[i] = -1                                     #changes the velocity to -1
                                                        
                    else:
                        v[i] = indexes[indexing + 1] - indexes[indexing] - 1  #gets new velocity
                        if v[i] == 0:                                         #if new velocity is 0 
                            v[i] = -1                                         #changes it to -1
    return v
def sloworchange(indexesup, indexesdown, v):
    indexingup = [list(indexesup).index(indexup) for indexup in indexesup]
    indexingdown = [list(indexesdown).index(indexdown) for indexdown in indexesdown]

def carpositions(indexes, v, row):
    for (elements ,i) in zip(v[row], range(len(v[row]))):
        if elements != 0:                          
            indexes = np.append(indexes, int(i))
    return indexes

def slow (v, indexesup, indexup, indexingup):
    if v[0][indexup] - 1 == 0:                                 #and if the velocity is 1
        v[0][indexup] = -1                                     #changes the velocity to -1
                                                        
    else:
        v[0][indexup] = indexesup[indexingup + 1] - indexesup[indexingup] - 1  #gets new velocity
        if v[0][indexup] == 0:                                         #if new velocity is 0 
            v[0][indexup] = -1                                         #changes it to -1
    return v

def changelane(v, indexesup, indexingup, lane):
    v[lane][indexesup[indexingup]], v[1 if lane == 0 else 0][indexesup[indexingup]] = v[1 if lane == 0 else 0][indexesup[indexingup]], v[lane][indexesup[indexingup]]
    return v

N = 10; emptyspots = 10
v = [1] * N + [0] * emptyspots 
np.random.shuffle(v)
v = np.array(v).reshape(2, 10)
x = np.array([])
indexesup = np.array([])
indexesdown = np.array([])

print (v)

indexesup = carpositions(indexesup, v, row = 0)
indexesup = np.array(indexesup, dtype = np.int8)
indexesdown = carpositions(indexesdown, v, row = 1)
indexesdown = np.array(indexesdown, dtype = np.int8)


indexingup = [list(indexesup).index(indexup) for indexup in indexesup]
indexingdown = [list(indexesdown).index(indexdown) for indexdown in indexesdown]
for indexup in indexesup:
    indexingup = list(indexesup).index(indexup)  
    if indexingup + 1 <= len(indexesup):
        if indexingup + 1 >= len(indexesup):

            indexingup -= (len(indexesup))                 #goes to the start of the array
            carback = [i for i in indexesdown if indexesup[indexingup] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
            carfront = [i for i in indexesdown if indexesup[indexingup] <= i]
            print ("last car's coordinate" , indexesup[indexingup])
            print ("first car's coordinate", indexesup[indexingup + 1])
            distanceup = len(v[0]) - (indexesup[indexingup] - indexesup[indexingup + 1])
            distancedown = len(v[0]) - (indexesup[indexingup] - indexesdown[indexingdown[0]])
            print ("carback", carback, "carfront", carfront, "distanceup", distanceup, "distancedown", distancedown)
            if (v[0][indexesup[indexingup]] - distanceup >= 0) and (distancedown > distanceup) and (carback[-1] + v[1][carback[-1]] < indexesup[indexingup]):
                v = changelane(v, indexesup, indexingup, lane = 0)  
        
        elif v[0][indexup] + indexesup[indexingup] >= indexesup[indexingup + 1]: #if velocity + location is more or same as the location for the car in front
            carback = [i for i in indexesdown if indexesup[indexingup] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
            carfront = [i for i in indexesdown if indexesup[indexingup] <= i]
            distanceup = indexesup[indexingup + 1] - indexesup[indexingup]

            if len(carfront) != 0:
                distancedownfront = carfront[0] - indexesup[indexingup]
                if len(carback) == 0 and distanceup < distancedownfront: #if there are no cars behind, changes lanes
                    v = changelane(v, indexesup, indexingup, lane = 0)
                    indexesdown = []
                    indexesdown = carpositions(indexesdown, v, row = 1)
                    indexesdown = np.array(indexesdown, dtype = np.int8)

                elif len(carback) != 0:


                    if (carback[-1] + v[1][carback[-1]] < indexesup[indexingup]) and (distanceup < distancedownfront):
                        v = changelane(v, indexesup, indexingup, lane = 0)
                        indexesdown = []
                        indexesdown = carpositions(indexesdown, v, row = 1)
                        indexesdown = np.array(indexesdown, dtype = np.int8)

            elif len(carfront) == 0:
                if len(carback) != 0:
                    if (carback[-1] + v[1][carback[-1]] < indexesup[indexingup]):
                        v = changelane(v, indexesup, indexingup, lane = 0)
                        indexesdown = []
                        indexesdown = carpositions(indexesdown, v, row = 1)
                        indexesdown = np.array(indexesdown, dtype = np.int8)
                else:
                    v = changelane(v, indexesup, indexingup, lane = 0)
                    indexesdown = []
                    indexesdown = carpositions(indexesdown, v, row = 1)
                    indexesdown = np.array(indexesdown, dtype = np.int8)

print (v)
indexesup = carpositions(indexesup, v, row = 0)
indexesup = np.array(indexesup, dtype = np.int8)
indexesdown = carpositions(indexesdown, v, row = 1)
indexesdown = np.array(indexesdown, dtype = np.int8)
indexingup = [list(indexesup).index(indexup) for indexup in indexesup]
indexingdown = [list(indexesdown).index(indexdown) for indexdown in indexesdown]
for indexdown in indexesdown:
    indexingdown = list(indexesdown).index(indexdown)  
    if indexingdown + 1 <= len(indexesdown):
        if indexingdown + 1 >= len(indexesdown):
            indexingdown -= (len(indexesdown))                 #goes to the start of the array
            carback = [i for i in indexesup if indexesdown[indexingdown] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
            carfront = [i for i in indexesup if indexesdown[indexingdown] <= i]
            distanceup = len(v[0]) - (indexesdown[indexingdown] - indexesdown[indexingdown + 1])
            distancedown = len(v[0]) - (indexesdown[indexingdown] - indexesup[indexingup[0]])
            if (v[1][indexesdown[indexingdown]] - distancedown >= 0) and (distanceup > distancedown) and (carback[-1] + v[0][carback[-1]] < indexesdown[indexingdown]):
                v = changelane(v, indexesdown, indexingdown, lane = 1)     
        
        elif v[1][indexdown] + indexesdown[indexingdown] >= indexesdown[indexingdown + 1]: #if velocity + location is more or same as the location for the car in front
            carback = [i for i in indexesup if indexesdown[indexingdown] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
            carfront = [i for i in indexesup if indexesdown[indexingdown] <= i]
            distancedown = indexesdown[indexingdown + 1] - indexesdown[indexingdown]

            if len(carfront) != 0:
                distanceupfront = carfront[0] - indexesdown[indexingdown]
                if len(carback) == 0 and distancedown < distanceupfront: #if there are no cars behind, changes lanes
                    v = changelane(v, indexesdown, indexingdown, lane = 1)
                    indexesup = []
                    indexesup = carpositions(indexesup, v, row = 0)
                    indexesup = np.array(indexesup, dtype = np.int8)
                elif len(carback) != 0:


                    if (carback[-1] + v[0][carback[-1]] < indexesdown[indexingdown]) and (distancedown < distanceupfront):
                        v = changelane(v, indexesdown, indexingdown, lane = 1)
                        indexesup = []
                        indexesup = carpositions(indexesup, v, row = 0)
                        indexesup = np.array(indexesup, dtype = np.int8)

            elif len(carfront) == 0:
                if len(carback) != 0:
                    if (carback[-1] + v[0][carback[-1]] < indexesdown[indexingdown]):
                        v = changelane(v, indexesdown, indexingdown, lane = 1)
                        indexesup = []
                        indexesup = carpositions(indexesup, v, row = 0)
                        indexesup = np.array(indexesup, dtype = np.int8)
                else:
                    v = changelane(v, indexesdown, indexingdown, lane = 1)
                    indexesup = []
                    indexesup = carpositions(indexesup, v, row = 0)
                    indexesup = np.array(indexesup, dtype = np.int8)
                    
print (v)
print ("indexesup", indexesup)
print ("indexesdown", indexesdown)
indexesup = []
indexesdown = []
indexesup = carpositions(indexesup, v, row = 0)
indexesup = np.array(indexesup, dtype = np.int8)
indexesdown = carpositions(indexesdown, v, row = 1)
indexesdown = np.array(indexesdown, dtype = np.int8)

print ("indexesup", indexesup)
print ("indexesdown", indexesdown)
v[0] = slowing (indexesup, v[0])
v[1] = slowing (indexesdown, v[1])

print ("after slowing")
print (v)