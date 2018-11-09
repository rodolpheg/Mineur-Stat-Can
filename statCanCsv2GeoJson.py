# -*- coding: utf-8 -*-
    
import csv
import math
import struct 
import copy
import random
import numpy as np
from math import sin, cos, sqrt, atan2, radians

# variable à afficher (colonne)
var = 674 # Revenu total moyen en 2015 parmi les bénéficiaires ($)
var = 749 # Revenu après impôt médian des ménages comptant deux personnes ou plus en 2015 ($)
var = 752 # Revenu après impôt moyen des ménages en 2015 ($)
var = 751 # Revenu total moyen des ménages en 2015 ($)

fileName = '/Volumes/Seagate Backup Plus Drive/Departement_de_geo/Statistiques-Canada/revenus_tout_can.csv'

def hex_to_rgb(rgb_str):    
    int_tuple = struct.unpack('BBB', bytes.fromhex(rgb_str))    
    return tuple([val/255 for val in int_tuple]) 

colourDiv = ['#c0392b','#cc5a2b','#d8772a','#e39327','#edaf22','#f7ca18','#d2bc2c','#abae38','#85a041','#5a9147','#1e824c']

dictColourArr = {}

countColour = 0

arrN = []
	
csvfile = open(fileName)
t = csv.reader(csvfile, delimiter=',', quotechar='"')
t = list(t)

#c = 0
#for i in t[0]:
#    if "Revenu total moyen des ménages en 2015 ($)" in i:
#        print(c,i)
#    c += 1
#print(t[0])

c = 0

listVar = []
listVar2 = []
for i in t:
    if i[0] != 'num' and i[var] != 'x' and i[var] != '..' and i[var] != 'F' and i[1] != '..':
        for ii in range(int(float(i[1])/100)):
            listVar.append(float(i[var]))
        listVar2.append(float(i[var]))

deciles = np.percentile(np.asarray(listVar), np.arange(0, 100, 10)).tolist()

maxVar = max(listVar)
maxVar = 66.0
minVar = min(listVar)

count = 0
counter = 0

showArr = True
    
geoJson = ' {"type": "FeatureCollection","features": ['

for i in t:
    
    if i[0] != 'num' and i[var] != 'x' and i[var] != '..' and i[var] != 'F' and i[var] != '0':
                    
        counter += 1
                
        lon1 = float(i[2249])
        lat1 = float(i[2248])
        rev =  float(i[var])

        c = 0
        for d in deciles:
            if float(i[var]) <= d:
                break
            else:
                c += 1
        
        count += 1.0
        col = colourDiv[c]
        
        i[var] = float(i[var])
        step = 66.0/10
        if i[var] < step * 1:
            col = colourDiv[len(colourDiv)-1]
        if i[var] >= step * 1 and i[var] < step * 2:
            col = colourDiv[len(colourDiv)-2]
        if i[var] >=  step * 2 and i[var] <  step * 3:
            col = colourDiv[len(colourDiv)-3]
        if i[var] >=  step * 3 and i[var] <  step * 4:
            col = colourDiv[len(colourDiv)-4]
        if i[var] >=  step * 4 and i[var] <  step * 5:
            col = colourDiv[len(colourDiv)-5]
        if i[var] >=  step * 5 and i[var] <  step * 6:
            col = colourDiv[len(colourDiv)-6]
        if i[var] >=  step * 6 and i[var] <  step * 7:
            col = colourDiv[len(colourDiv)-7]
        if i[var] >=  step * 7 and i[var] <  step * 8:
            col = colourDiv[len(colourDiv)-8]
        if i[var] >=  step * 8 and i[var] <  step * 9:
            col = colourDiv[len(colourDiv)-9]
        if i[var] >=  step * 9:
            col = colourDiv[len(colourDiv)-10]
        
        geoJson += '{ "type": "Feature","geometry": {"type": "Point", "coordinates": [' + str(lon1) + ',' + str(lat1) + ']},"properties": {"Rev":' + str(rev) + '}},'
        

geoJson = geoJson[:-1] + "]}"
print(geoJson)
