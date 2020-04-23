import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

source = r"C:\Users\modestas\Documents\Python\Python Scripts\traffic flow simulation" #path which used to search for files


##Goes through all the csv files and plots graphs


#v_max is varied against different p values
p = 0.1      
path = source
while p < 0.5: #p range
    v_max = 4
    data = []
    traflow = []
    densities = []
    error = []
    while v_max < 8: #v_max range
        for directories in os.walk(source, topdown = True):
            if directories[0] == source:            #if directory has the same path as "source"
                for files in directories[2]:        #for files in the directory
                    if files.find(".csv") != -1:    #if file is csv
                        if files.find("traffic flow vs density for probability {0} for max velocity of {1} for one lane".format(str(round(p,1)), str(v_max))) != -1:
                            data = pd.read_csv(os.path.join(source, files))                     #reads csv file 
                            maximum = max(data["Average traffic flow"])                         #maximum traffic flow
                            index = data[data["Average traffic flow"]==maximum].index.values    #finds the density of that maximum
                            maxdata = data.iloc[index[0]]
                            if files.find("0.2") != -1 and files.find("7") != -1:
                                traflow.append(data["Average traffic flow"] / 400)
                                error.append(data["Standard deviation"] / 400)
                            else:
                                traflow.append(data["Average traffic flow"] / 200)

                            densities.append(data["Density"])
                            
                            df = pd.DataFrame(data)
                            plt.errorbar(df["Density"], df["Average traffic flow"], yerr = df["Standard deviation"],  fmt = '.k', ecolor = "black")                            
                            plt.title("traffic flow against density for {0} probability of slowing for {1} v_max".format(round(p,1), v_max))
                            plt.xlabel("Density (Cars/Road Length)")
                            plt.ylabel("Traffic flow (Cars/s)")
                            plt.xticks(np.arange(0, 1, step = 0.1))
                            plt.savefig(os.path.join(source,"Traffic flow vs density for {0} probability of slowing for {1} vmax.png".format(round(p,1), v_max)))
                            plt.show()
                            plt.close()

        v_max += 1

    labels = ['v_max 4', 'v_max 5','v_max 6', 'v_max 7']
    for y_arr,  label in zip(traflow, labels):
        plots = plt.plot(data["Density"], y_arr, label=label)
    plt.title("traffic flow against density for {0} probability of slowing".format(round(p,1)))
    plt.xlabel("Density (Cars/Road Length)")
    plt.ylabel("Traffic flow (Cars/s)")
    plt.legend()
    plt.xticks(np.arange(0, 1, step = 0.1))
    plt.savefig(os.path.join(source,"Traffic flow vs density for {0} probability of slowing for various vmax.png".format(round(p,1))))
    plt.show()
    plt.close()
    p += 0.1

## p is varied against different v_max    
v_max = 4
while v_max < 8:
    p = 0.1
    data = []
    traflow = []
    densities = []
    while p < 0.5:
        for directories in os.walk(source, topdown = True):
            if directories[0] == source:
                for files in directories[2]:
                    if files.find(".csv") != -1:
                        if files.find("traffic flow vs density for probability {0} for max velocity of {1} for one lane".format(str(round(p,1)), str(v_max))) != -1:
                            data = pd.read_csv(os.path.join(source, files))
                            maximum = max(data["Average traffic flow"])
                            index = data[data["Average traffic flow"]==maximum].index.values
                            maxdata = data.iloc[index[0]]
                            if files.find("0.2") != -1 and files.find("7") != -1:
                                traflow.append(data["Average traffic flow"] / 400)
                                print ("max traffic flow", maxdata[0]/400)
                                print ("density", maxdata[1])
                                print ("standart deviation", maxdata[2]/400)
                            else:
                                traflow.append(data["Average traffic flow"] / 200)
                                print ("max traffic flow", maxdata[0]/200)
                                print ("density", maxdata[1])
                                print ("standart deviation", maxdata[2]/200)
                            densities.append(data["Density"])
        p += 0.1
    labels = ['p 0.1', 'p 0.2', 'p 0.3', 'p 0.4']
    for y_arr, label in zip(traflow, labels):
        plots = plt.plot(data["Density"], y_arr, label=label)
    plt.title("traffic flow against density for {0} max velocity for one lane".format(v_max))
    plt.xlabel("Density (Cars/Road Length)")
    plt.ylabel("Traffic flow (Cars/s)")
    plt.legend()
    plt.xticks(np.arange(0, 1, step = 0.1))
    plt.savefig(os.path.join(source,"Traffic flow vs density for {0} max velocity for various probabilities of slowing down.png".format(v_max)))
    plt.show()
    plt.close()
    v_max += 1