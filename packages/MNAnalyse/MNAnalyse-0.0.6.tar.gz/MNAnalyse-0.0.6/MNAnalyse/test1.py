import pymysql
import requests,os
import DataManager as dm

import pandas as pd
import json
import seaborn as sns
import numpy as np 
from numpy import arange, sin, pi
from matplotlib import pyplot as plt 
connect=dm.DataManager()

samples = connect.GetHIPSamplesID()

neurons =connect.GetNeurons(samples[0])
propertyJson = {}

columns = []
for neuron in neurons:
	property = json.loads(neuron.properties)
	propertyJson[neuron.sampleid+'_'+neuron.name] = property


# print(propertyJson['200335_002.swc']['projectregion'])
projectmat = pd.DataFrame()
print(projectmat)
for key in propertyJson:
	print(key)
	columns.append(key)
	projectpd = pd.DataFrame.from_dict(propertyJson[key]['projectregion'], orient='index').sort_index()
	# print(projectpd)
	projectmat = pd.concat([projectmat, projectpd], axis=1)
projectmat.columns = columns
projectmat.sort_index(axis = 0, ascending = True)
projectmat.fillna(0,inplace=True)
sns.set(style="ticks")

# g = sns.clustermap(projectmat, fmt="d", cmap='YlGnBu',xticklabels=True,yticklabels=True)
x = np.arange(1,11) 
y =  2  * x +  5 
plt.title("Matplotlib demo") 
plt.xlabel("x axis caption") 
plt.ylabel("y axis caption") 
plt.plot(x,y) 
# plt.show()
