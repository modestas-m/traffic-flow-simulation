import numpy as np
##Function for slowing down cars if there's a traffic jam
def slowing (indexes, v, row):
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
print (list(zip(v, range(len(v) * len(v[0])))))
indexesup = carpositions(indexesup, v, row = 0)
indexesup = np.array(indexesup, dtype = np.int8)
indexesdown = carpositions(indexesdown, v, row = 1)
indexesdown = np.array(indexesdown, dtype = np.int8)
print (indexesup, indexesdown)
#v[0] = slowing (indexesup, v[0], row = 0) 
#print (v[0])
#v[1] = slowing (indexesdown, v[1], row = 1)
#print (v)
indexingup = [list(indexesup).index(indexup) for indexup in indexesup]
indexingdown = [list(indexesdown).index(indexdown) for indexdown in indexesdown]
for indexup in indexesup:
    indexingup = list(indexesup).index(indexup)  
    #print (v)
    if indexingup + 1 <= len(indexesup):
        if indexingup + 1 >= len(indexesup):
            print ("indexing up", indexingup)
            indexingup -= (len(indexesup))                 #goes to the start of the array
            print ("indexing up", indexingup)
            carback = [i for i in indexesdown if indexesup[indexingup] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
            carfront = [i for i in indexesdown if indexesup[indexingup] <= i]
            print ("last car's coordinate" , indexesup[indexingup])
            print ("first car's coordinate", indexesup[indexingup + 1])
            distanceup = len(v[0]) - (indexesup[indexingup] - indexesup[indexingup + 1])
            distancedown = len(v[0]) - (indexesup[indexingup] - indexesdown[indexingdown[0]])
            print ("carback", carback, "carfront", carfront, "distanceup", distanceup, "distancedown", distancedown)
            if (v[0][indexesup[indexingup]] - distanceup >= 0) and (distancedown > distanceup) and (carback[-1] + v[1][carback[-1]] < indexesup[indexingup]):
                v = changelane(v, indexesup, indexingup, lane = 0)
#             print ("len v[0]", len(v[0]))
#             print ("len v", len(v))
#             print ("Indexingup", indexingup)
#             print ("indexesup[indexingup]", indexesup[indexingup])
#             print ("indexup", indexup)
#             print ("v[indexup]", v[0][indexup])
            x_new = v[0][indexup] + indexesup[indexingup] - len(v[0])  #get's new coordinate
#             if x_new >= indexesup[indexingup + 1]:         #if new coordinate is more or same than for the next car 
#                 if v[indexup] - 1 == 0:                      #and if the velocity is 1
#                     v[indexup] = -1                          #changes the velocity to -1
#                 else:
#                     v[indexup] = len(v) + indexesup[indexingup + 1] - indexesup[indexingup] - 1 #gets new velocity
#                     if v[indexup] == 0:                                                 #if new velocity is 0 
#                         v[indexup] = -1          
        
        elif v[0][indexup] + indexesup[indexingup] >= indexesup[indexingup + 1]: #if velocity + location is more or same as the location for the car in front
#             indexingup = [list(indexesup).index(indexup) for indexup in indexesup]
#             print ("indexing up works")
#             indexingdown = [list(indexesdown).index(indexdown) for indexdown in indexesdown]
#             print ("indexing down works")
            carback = [i for i in indexesdown if indexesup[indexingup] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
            carfront = [i for i in indexesdown if indexesup[indexingup] <= i]
            distanceup = indexesup[indexingup + 1] - indexesup[indexingup]
#             if len(carback) != 0:
#                 distancedownback = carback[-1] -indexesup[indexingup]
            if len(carfront) != 0:
                distancedownfront = carfront[0] - indexesup[indexingup]
                if len(carback) == 0 and distanceup < distancedownfront: #if there are no cars behind, changes lanes
                    #print ("changing lanes")
                    v = changelane(v, indexesup, indexingup, lane = 0)
                    indexesdown = []
                    indexesdown = carpositions(indexesdown, v, row = 1)
                    indexesdown = np.array(indexesdown, dtype = np.int8)
                    #print ("v", v)
#                 elif len(carback) == 0 and distanceup >= distancedownfront:
#                     print ("slowing down 1")
#                     v = slow (v, indexesup, indexup, indexingup)
                    
                elif len(carback) != 0:


                    if (carback[-1] + v[1][carback[-1]] < indexesup[indexingup]) and (distanceup < distancedownfront):
                        #print ("changing lane 2")
                        v = changelane(v, indexesup, indexingup, lane = 0)
                        indexesdown = []
                        indexesdown = carpositions(indexesdown, v, row = 1)
                        indexesdown = np.array(indexesdown, dtype = np.int8)
                        #print (v)
#                     else:
#                         print ("slowing down 2")
#                         v = slow (v, indexesup, indexup, indexingup) 
            elif len(carfront) == 0:
                if len(carback) != 0:
                    if (carback[-1] + v[1][carback[-1]] < indexesup[indexingup]):
                        #print ("changing lane 2")
                        v = changelane(v, indexesup, indexingup, lane = 0)
                        indexesdown = []
                        indexesdown = carpositions(indexesdown, v, row = 1)
                        indexesdown = np.array(indexesdown, dtype = np.int8)
                        #print (v)
#                     else:
#                         print ("slowing down 2")
#                         v = slow (v, indexesup, indexup, indexingup)
                else:
                    v = changelane(v, indexesup, indexingup, lane = 0)
                    indexesdown = []
                    indexesdown = carpositions(indexesdown, v, row = 1)
                    indexesdown = np.array(indexesdown, dtype = np.int8)

print ("now going through bottom")
print (v)
indexesup = carpositions(indexesup, v, row = 0)
indexesup = np.array(indexesup, dtype = np.int8)
indexesdown = carpositions(indexesdown, v, row = 1)
indexesdown = np.array(indexesdown, dtype = np.int8)
indexingup = [list(indexesup).index(indexup) for indexup in indexesup]
indexingdown = [list(indexesdown).index(indexdown) for indexdown in indexesdown]
for indexdown in indexesdown:
    indexingdown = list(indexesdown).index(indexdown)  
    #print (v)
    if indexingdown + 1 <= len(indexesdown):
        if indexingdown + 1 >= len(indexesdown):
            #print ("indexing up", indexingup)
            indexingdown -= (len(indexesdown))                 #goes to the start of the array
            #print ("indexing up", indexingup)
            carback = [i for i in indexesup if indexesdown[indexingdown] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
            carfront = [i for i in indexesup if indexesdown[indexingdown] <= i]
            #print ("last car's coordinate" , indexesup[indexingup])
            #print ("first car's coordinate", indexesup[indexingup + 1])
            distanceup = len(v[0]) - (indexesdown[indexingdown] - indexesdown[indexingdown + 1])
            distancedown = len(v[0]) - (indexesdown[indexingdown] - indexesup[indexingup[0]])
            print ("carback", carback, "carfront", carfront, "distanceup", distanceup, "distancedown", distancedown)
            if (v[1][indexesdown[indexingdown]] - distancedown >= 0) and (distanceup > distancedown) and (carback[-1] + v[0][carback[-1]] < indexesdown[indexingdown]):
                v = changelane(v, indexesdown, indexingdown, lane = 1)
#             print ("len v[0]", len(v[0]))
#             print ("len v", len(v))
#             print ("Indexingup", indexingup)
#             print ("indexesup[indexingup]", indexesup[indexingup])
#             print ("indexup", indexup)
#             print ("v[indexup]", v[0][indexup])
            #x_new = v[0][indexup] + indexesup[indexingup] - len(v[0])  #get's new coordinate
#             if x_new >= indexesup[indexingup + 1]:         #if new coordinate is more or same than for the next car 
#                 if v[indexup] - 1 == 0:                      #and if the velocity is 1
#                     v[indexup] = -1                          #changes the velocity to -1
#                 else:
#                     v[indexup] = len(v) + indexesup[indexingup + 1] - indexesup[indexingup] - 1 #gets new velocity
#                     if v[indexup] == 0:                                                 #if new velocity is 0 
#                         v[indexup] = -1          
        
        elif v[1][indexdown] + indexesdown[indexingdown] >= indexesdown[indexingdown + 1]: #if velocity + location is more or same as the location for the car in front
#             indexingup = [list(indexesup).index(indexup) for indexup in indexesup]
#             print ("indexing up works")
#             indexingdown = [list(indexesdown).index(indexdown) for indexdown in indexesdown]
#             print ("indexing down works")
            carback = [i for i in indexesup if indexesdown[indexingdown] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
            carfront = [i for i in indexesup if indexesdown[indexingdown] <= i]
            distancedown = indexesdown[indexingdown + 1] - indexesdown[indexingdown]
#             if len(carback) != 0:
#                 distancedownback = carback[-1] -indexesup[indexingup]
            if len(carfront) != 0:
                distanceupfront = carfront[0] - indexesdown[indexingdown]
                if len(carback) == 0 and distancedown < distanceupfront: #if there are no cars behind, changes lanes
                    #print ("changing lanes")
                    v = changelane(v, indexesdown, indexingdown, lane = 1)
                    indexesup = []
                    indexesup = carpositions(indexesup, v, row = 0)
                    indexesup = np.array(indexesup, dtype = np.int8)
                    #print ("v", v)
#                 elif len(carback) == 0 and distanceup >= distancedownfront:
#                     print ("slowing down 1")
#                     v = slow (v, indexesup, indexup, indexingup)
                    
                elif len(carback) != 0:


                    if (carback[-1] + v[0][carback[-1]] < indexesdown[indexingdown]) and (distancedown < distanceupfront):
                        #print ("changing lane 2")
                        v = changelane(v, indexesdown, indexingdown, lane = 1)
                        indexesup = []
                        indexesup = carpositions(indexesup, v, row = 0)
                        indexesup = np.array(indexesup, dtype = np.int8)
                        #print (v)
#                     else:
#                         print ("slowing down 2")
#                         v = slow (v, indexesup, indexup, indexingup) 
            elif len(carfront) == 0:
                if len(carback) != 0:
                    if (carback[-1] + v[0][carback[-1]] < indexesdown[indexingdown]):
                        #print ("changing lane 2")
                        v = changelane(v, indexesdown, indexingdown, lane = 1)
                        indexesup = []
                        indexesup = carpositions(indexesup, v, row = 0)
                        indexesup = np.array(indexesup, dtype = np.int8)
                        #print (v)
#                     else:
#                         print ("slowing down 2")
#                         v = slow (v, indexesup, indexup, indexingup)
                else:
                    v = changelane(v, indexesdown, indexingdown, lane = 1)
                    indexesup = []
                    indexesup = carpositions(indexesup, v, row = 0)
                    indexesup = np.array(indexesup, dtype = np.int8)
                    
print (v)