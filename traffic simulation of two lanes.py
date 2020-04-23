import numpy as np
import random
import os
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import pandas as pd
import csv


###For two-lane traffic
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
            indexes = np.append(indexes, i)
    indexes = np.array(indexes, dtype = np.int16)
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

def changeupdatelane(v, indexesup, indexingup, indexesdown, lane = 0, row = 1):
    v = changelane(v, indexesup, indexingup, lane)  
    indexesdown = []
    indexesdown = carpositions(indexesdown, v, row)
    indexesdown = np.array(indexesdown, dtype = np.int16)
    return v, indexesdown

def carsmove (v, indexesup, lane):
    speeds = [i for i in v[lane] if i != 0]
    xnew = [up if v[lane][up] < 0 else (up + v[lane][up]) for up in indexesup]
    xnew = np.array(xnew, dtype = int)
    xnew = np.where(xnew < len(v[0]), xnew, xnew - len(v[0]))
    v[lane][indexesup], v[lane][xnew] = v[lane][xnew], v[lane][indexesup]
    return v

def carspeedincrease (v, lane):
    v[lane] = np.where(v[lane] > 0, v[lane] + 1, v[lane])
    v[lane] = np.where(v[lane] < 0, v[lane] + 2, v[lane])
    v[lane] = np.where(v[lane] > speed_max, v[lane] - 1, v[lane]) 
    return v

def unexpected(indexes, v, p, lane):
    for index in indexes:
        if v[lane][index] > 0:             #if car is moving
            if random.random() < p:  #if random number is lower than the the probability
                v[lane][index] -= 1        #slows the car down
                if v[lane][index] == 0:    #if new velocity is 0 
                    v[lane][index] = -1    #changes it to -1
    return v

def trafficflow(speed, ind, position, flow):
    if ind < position and (speed + ind) >= position:
        flow += 1
    return flow

p = 0.1
source = r"C:\Users\modestas\Documents\Python\Python Scripts\traffic flow simulation" #change to the source in your computer
while p < 0.5:
    position1 = 25
    position2 = 50  
    position3 = 75
    position4 = 100
    position5 = 125
    position6 = 150
    position7 = 175
    std = []
    densities = []
    traflow = []
    N = 10
    length = 200
    #pbar = tqdm(total = 360000)
    while N < (length - 10):
        initialdistro = 10
        
        avertraflow = []
        while initialdistro > 0:
            
            flow = 0
            length = 200
            speed_max = 5
            emptyspots = (length * 2) - N
            v = [1] * N + [0] * emptyspots 
            np.random.shuffle(v)
            v = np.array(v).reshape(2, length)
            x = np.array([])
            loop = 0

            while loop < 200:
                indexesup = np.array([], dtype = np.int16)
                indexesdown = np.array([], dtype = np.int16)
                indexesup = carpositions(indexesup, v, row = 0)
                indexesdown = carpositions(indexesdown, v, row = 1)
                indexingup = []
                indexingdown = []
                indexingup = [list(indexesup).index(indexup) for indexup in indexesup]
                indexingdown = [list(indexesdown).index(indexdown) for indexdown in indexesdown]
                for indexup in indexesup:
                    indexingup = list(indexesup).index(indexup)  
                    if indexingup + 1 <= len(indexesup):
                        if indexingup + 1 >= len(indexesup):

                            indexingup -= (len(indexesup))                 #goes to the start of the array
                            carback = [i for i in indexesdown if indexesup[indexingup] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
                            carfront = [i for i in indexesdown if indexesup[indexingup] <= i]
                            distanceup = len(v[0]) - (indexesup[indexingup] - indexesup[indexingup + 1])
                            distancedown = len(v[0]) - (indexesup[indexingup] - indexesdown[indexingdown[0]])
                            if (v[0][indexesup[indexingup]] - distanceup >= 0) and (distancedown > distanceup) and (carback[-1] + v[1][carback[-1]] < indexesup[indexingup]):
                                v, indexesdown = changeupdatelane(v, indexesup, indexingup, indexesdown, lane = 0, row = 1)

                        elif v[0][indexup] + indexesup[indexingup] >= indexesup[indexingup + 1]: #if velocity + location is more or same as the location for the car in front
                            carback = [i for i in indexesdown if indexesup[indexingup] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
                            carfront = [i for i in indexesdown if indexesup[indexingup] <= i]
                            distanceup = indexesup[indexingup + 1] - indexesup[indexingup]

                            if len(carfront) != 0:
                                distancedownfront = carfront[0] - indexesup[indexingup]
                                if len(carback) == 0 and distanceup < distancedownfront: #if there are no cars behind, changes lanes
                                    v, indexesdown = changeupdatelane(v, indexesup, indexingup, indexesdown, lane = 0, row = 1)

                                elif len(carback) != 0:


                                    if (carback[-1] + v[1][carback[-1]] < indexesup[indexingup]) and (distanceup < distancedownfront):
                                        v, indexesdown = changeupdatelane(v, indexesup, indexingup, indexesdown, lane = 0, row = 1)

                            elif len(carfront) == 0:
                                if len(carback) != 0:
                                    if (carback[-1] + v[1][carback[-1]] < indexesup[indexingup]):
                                        v, indexesdown = changeupdatelane(v, indexesup, indexingup, indexesdown, lane = 0, row = 1)
                                else:
                                    v, indexesdown = changeupdatelane(v, indexesup, indexingup, indexesdown, lane = 0, row = 1)
                
                indexesup = np.array([], dtype = np.int16)
                indexesdown = np.array([], dtype = np.int16)
                indexesup = carpositions(indexesup, v, row = 0)
                indexesdown = carpositions(indexesdown, v, row = 1)
                indexingup = [list(indexesup).index(indexup) for indexup in indexesup]
                indexingdown = [list(indexesdown).index(indexdown) for indexdown in indexesdown]
                for indexdown in indexesdown:
                    indexingdown = list(indexesdown).index(indexdown)  
                    if indexingdown + 1 <= len(indexesdown):
                        if indexingdown + 1 >= len(indexesdown):
                            indexingdown -= (len(indexesdown))                 #goes to the start of the array
                            carback = [i for i in indexesup if indexesdown[indexingdown] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
                            carfront = [i for i in indexesup if indexesdown[indexingdown] <= i]
                            distancedown = len(v[0]) - (indexesdown[indexingdown] - indexesdown[indexingdown + 1])
                            distanceup = len(v[0]) - (indexesdown[indexingdown] - indexesup[indexingup[0]])
                            if (v[1][indexesdown[indexingdown]] - distancedown >= 0) and (distanceup > distancedown) and (carback[-1] + v[0][carback[-1]] < indexesdown[indexingdown]):

                                v, indexesup = changeupdatelane(v, indexesdown, indexingdown, indexesup, lane = 1, row = 0)
                        

                        elif (v[1][indexdown] + indexesdown[indexingdown]) >= (indexesdown[indexingdown + 1]):
                            carback = [i for i in indexesup if indexesdown[indexingdown] >= i]    #list of car locations in the other lane that are behind or at the same location as the car
                            carfront = [i for i in indexesup if indexesdown[indexingdown] <= i]
                            distancedown = indexesdown[indexingdown + 1] - indexesdown[indexingdown]

                            if len(carfront) != 0:
                                distanceupfront = carfront[0] - indexesdown[indexingdown]
                                if len(carback) == 0 and distancedown < distanceupfront: #if there are no cars behind, changes lanes
                                    v, indexesup = changeupdatelane(v, indexesdown, indexingdown, indexesup, lane = 1, row = 0)

                                elif len(carback) != 0:


                                    if (carback[-1] + v[0][carback[-1]] < indexesdown[indexingdown]) and (distancedown < distanceupfront):
                                        v, indexesup = changeupdatelane(v, indexesdown, indexingdown, indexesup, lane = 1, row = 0)

                            elif len(carfront) == 0:
                                if len(carback) != 0:
                                    if (carback[-1] + v[0][carback[-1]] < indexesdown[indexingdown]):
                                        v, indexesup = changeupdatelane(v, indexesdown, indexingdown, indexesup, lane = 1, row = 0)
                                else:
                                    v, indexesup = changeupdatelane(v, indexesdown, indexingdown, indexesup, lane = 1, row = 0)
                                    
                
                indexesup = np.array([], dtype = np.int16)
                indexesdown = np.array([], dtype = np.int16)
                indexesup = carpositions(indexesup, v, row = 0)
                indexesdown = carpositions(indexesdown, v, row = 1)

                v[0] = slowing (indexesup, v[0])
                v[1] = slowing (indexesdown, v[1])

                v = unexpected(indexesup, v, p, lane = 0)
                v = unexpected(indexesdown, v, p, lane = 1)

                indexesuppos = [index for index in indexesup if v[0][index] > 0]

                indexdownpos = [index for index in indexesdown if v[1][index] > 0]

                for index in indexesuppos:
                    flow = trafficflow(v[0][index], index, position1, flow)
                    flow = trafficflow(v[0][index], index, position2, flow)
                    flow = trafficflow(v[0][index], index, position3, flow)
                    flow = trafficflow(v[0][index], index, position4, flow)
                    flow = trafficflow(v[0][index], index, position5, flow)
                    flow = trafficflow(v[0][index], index, position6, flow)
                    flow = trafficflow(v[0][index], index, position7, flow)

                for index in indexdownpos:
                    flow = trafficflow(v[1][index], index, position1, flow)
                    flow = trafficflow(v[1][index], index, position2, flow)
                    flow = trafficflow(v[1][index], index, position3, flow)
                    flow = trafficflow(v[1][index], index, position4, flow)
                    flow = trafficflow(v[1][index], index, position5, flow)
                    flow = trafficflow(v[1][index], index, position6, flow)
                    flow = trafficflow(v[1][index], index, position7, flow)
               
                v = carsmove(v, indexesup, lane = 0)
                v = carsmove(v, indexesdown, lane = 1)
            
                v = carspeedincrease (v, lane = 0)
                v = carspeedincrease (v, lane = 1)

                #pbar.update(1)
                loop += 1

            avertraflow.append(flow / (200 * 7))
            initialdistro -= 1
        std.append(np.std(avertraflow))
     
        traflow.append(sum(avertraflow) / len(avertraflow))

        densities.append(N/(length * 2))
        N += 1
    path = source
    name = "traffic flow vs density for probability {0} for max velocity of {1} for two lanes.csv".format(round(p,1), speed_max)
    if os.path.isfile(name) == False:               #if file doesn't exist
        with open(name, 'w', newline = '') as f:
            for index in range(len(traflow)):
                wr = csv.writer(f)
                row = []
                if (index == 0):
                    row.append("Average traffic flow")
                    row.append("Density")
                    row.append("Standard deviation")
                    wr.writerow(row)
                    row = []
                row.append(traflow[index])
                row.append(densities[index])
                row.append(std[index])
                wr.writerow(row)
    p += 0.1