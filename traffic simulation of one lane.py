import numpy as np
import random
import os
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import pandas as pd
import csv

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

##Function that slows a car down due to unforseen events
def unexpected(indexes, v, p):
    for index in indexes:
        if v[index] > 0:             #if car is moving
            if random.random() < p:  #if random number is lower than the the probability
                v[index] -= 1        #slows the car down
                if v[index] == 0:    #if new velocity is 0 
                    v[index] = -1    #changes it to -1
    return v

##Function for getting average velocity and standart deviations only when the traffic reaches a steady state
def equilibrium(averagevelocity, averagevelocityforp, std):
    index = 0
    while index < len(averagevelocity):
        if averagevelocity[index + 1] - averagevelocity[index] <= 0.1:
            std.append(np.std(averagevelocity[(index + 1):]))
            averagevelocityforp.append(sum(averagevelocity[(index + 1):])/len(averagevelocity[(index + 1):]))
            break
        index += 1
    return std, averagevelocityforp

##Function for measuring traffic flow at some position along the road
def trafficflow(speed, ind, position, flow):
    if ind < position and (speed + ind) >= position:  #if car's old position is less and new position is more than the tracked position
        flow += 1                                     #then traffic flow increases by one
    return flow



        

position1 = 25
position2 = 50
position3 = 75
position4 = 100
position5 = 125
position6 = 150
position7 = 175
source = r"C:\Users\modestas\Documents\Python\Python Scripts\traffic flow simulation" #change to the source in your computer

p = 0.1 #probability of car slowing down due to unforseen events
#pbar = tqdm(total = 720000) #progress bar reallyuseful for tracking time
while p < 0.7:    
    speed_max = 2
    while speed_max < 8:
        N = 10
        densities = []
        traflowaverage = []
        std = []
        while N < (len(v) - 10):

            traflow = []
            initialdistro = 10
            while initialdistro > 0:
                #std = []               #list for storing standart deviations
                times = []            
                averagevelocities = []
                probability = []
                averagevelocityforp = []
                axisp2 = []  

                time = []
                averagevelocity = []
                v = np.ones(200)       #road of length 200
                v[:len(v) - N] = 0     #add length 200 - N number of empty cells
                np.random.shuffle(v)   #shuffle empty cells and cars randomly
                loop = 0
                flow = 0
                while loop < 200:
                    x = np.array([])
                    indexes = np.array([])

                    for (elements ,i) in zip(v, range(len(v))):
                        if elements != 0:                          #if there's a car
                            indexes = np.append(indexes, i)        #gets its cell number   
                    indexes = indexes.astype(int)                  #transforms from floats to integers
                    averagevelocity.append(sum(v)/N)               
                    time.append(loop)
                    y1 = [0 for i in v[indexes] if i == 1]
                    x1 = [i for i in indexes if v[i] == 1]
                    y2 = [0 for i in v[indexes] if i == 2]
                    x2 = [i for i in indexes if v[i] == 2]
                    y3 = [0 for i in v[indexes] if i == 3]
                    x3 = [i for i in indexes if v[i] == 3]
                    y4 = [0 for i in v[indexes] if i == 4]
                    x4 = [i for i in indexes if v[i] == 4]
                    y5 = [0 for i in v[indexes] if i == 5]
                    x5 = [i for i in indexes if v[i] == 5]

                    fig = plt.plot(x1, y1 ,'co', x2, y2 ,'bo', x3, y3 ,'mo', x4, y4 ,'ro', x5, y5, 'go')
                    plt.axis([0, 200, -3, 3])
                    plt.grid()
                    plt.pause(1)
                    plt.close()
                    v = slowing (indexes, v)                      #slows cars down if there are cars in front of them
                    v = unexpected(indexes, v, p)                 #slows cars down due to unforseen events with probability p
                    speeds = v[indexes]                           #finds velocites of cars
                    variable = 0
                    for speed in speeds:                          #for velocity in velocities
                        ind = indexes[variable]                   #gets index from a cells array
                        if speed == -1:                           #if velocity is "0"
                            x = np.append(x, ind)                 #new coordinate doesn't change
                        else:                                     #if velocity is above 0
                            x = np.append(x, speed + ind)         #gets new coordinate
                            flow = trafficflow(speed, ind, position1, flow)
                            flow = trafficflow(speed, ind, position2, flow)
                            flow = trafficflow(speed, ind, position3, flow)
                            flow = trafficflow(speed, ind, position4, flow)
                            flow = trafficflow(speed, ind, position5, flow)
                            flow = trafficflow(speed, ind, position6, flow)
                            flow = trafficflow(speed, ind, position7, flow)
                        variable += 1
                    x = np.where(x < len(v), x, x-len(v))         #if coordinate is out of bounds, it's taken to the beginning of array
                    #pbar.update(1)                               #progress bar, really useful 
                    x_change = list(map(int, x))                  #transforms from floats to integers
                    v[indexes], v[x_change] = v[x_change], v[indexes] #swaps old coordinates with new ones
                    v[x_change] = v[x_change]
                    v[x_change] = np.where(v[x_change] > 0, v[x_change] + 1, v[x_change])
                    v = np.where(v < 0, v + 2, v)
                    v[x_change] = np.where(v[x_change] > speed_max, v[x_change] - 1, v[x_change])
                    loop += 1

                traflow.append(flow/7)
                initialdistro -= 1
            std.append(np.std(traflow))
            traflowaverage.append(sum(traflow)/len(traflow))
            densities.append(N / len(v))
            N += 1

        path = r"C:\Users\modestas\Documents\Python\Python Scripts\traffic flow simulation" #change to the path in your computer
        name = "traffic flow vs density for probability {0} for max velocity of {1} for one lane.csv".format(round(p,1), speed_max)

        if os.path.isfile(name) == False:                   #if file doesn't exist
            with open(name, 'w', newline = '') as f:        #creates a file, for writing data
                for index in range(len(traflowaverage)):    #for number of elements in the list
                    wr = csv.writer(f)                      #file's format csv
                    row = []                                
                    if (index == 0):                        #for the first row
                        row.append("Average traffic flow")  
                        row.append("Density")
                        row.append("Standard deviation")    
                        wr.writerow(row)                    #write names of columns    
                        row = []
                    row.append(traflowaverage[index])       
                    row.append(densities[index])
                    row.append(std[index])
                    wr.writerow(row)                        #write all the values
        speed_max += 1
    p += 0.1

#pbar.close()
