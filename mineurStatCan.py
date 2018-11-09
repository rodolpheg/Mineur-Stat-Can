# -*- coding: utf-8 -*-

# Mineur de données du recensement Statistiques Canada 2016

import urllib2
from bs4 import BeautifulSoup
import csv
import shapefile
from pyproj import Proj, transform
from shapely.geometry import Polygon,Point
import time

municipalities = []

for i in range(1000,9999):
	municipalities.append(str(i))

inProj = Proj(init='epsg:3347')
outProj = Proj(init='epsg:4326')

def digitOnly(d):
	w = ""
	for l in d:
		if l.isdigit():
			w += l
	return float(w)

def column(matrix, i):
	return [row[i] for row in matrix]

myshp = open("/Volumes/Seagate Backup Plus Drive/Departement_de_geo/Statistiques-Canada/lada000a16a_e.shp", "rb")
mydbf = open("/Volumes/Seagate Backup Plus Drive/Departement_de_geo/Statistiques-Canada/lada000a16a_e.dbf", "rb")
r = shapefile.Reader(shp=myshp, dbf=mydbf)
shapes = r.shapes()
fields = r.fields
records = r.records

try:
	with open('latlong.csv', 'rt') as f:
		reader = csv.reader(f)
		latlong = list(reader)
except:
	latlong = []
	for m in municipalities:
		shapeRecs = r.iterShapeRecords()
		
		for shapeRec in shapeRecs:
			
			if m in shapeRec.record[0]:
				
				p = shapeRec.shape.points
				listP = []
				points = []
				for i in p:
					x1,y1 = i[0],i[1]
					x2,y2 = transform(inProj,outProj,x1,y1)
					points.append((x2,y2))
				polygon = Polygon(points)
				centroid = polygon.centroid.wkt[7:][:-1].split(" ")
				latlong.append([int(shapeRec.record[0]),float(centroid[1]),float(centroid[0]),shapeRec.record[4].decode('iso-8859-1').encode('utf8')])

	for ll in latlong:
		
		myshpArr = open("/Volumes/Seagate Backup Plus Drive/Departement_de_geo/Statistiques-Canada/LIMADMIN.shp", "rb")
		mydbfArr = open("/Volumes/Seagate Backup Plus Drive/Departement_de_geo/Statistiques-Canada/LIMADMIN.dbf", "rb")
		rArr = shapefile.Reader(shp=myshpArr, dbf=mydbfArr)
		shapesArr = rArr.shapes()
		fieldsArr = rArr.fields
		recordsArr = rArr.records
		shapeRecsArr = rArr.iterShapeRecords()
		for shapeRec in shapeRecsArr:
			p = shapeRec.shape.points
			arr = Polygon(shapeRec.shape.points)
			point = Point((ll[2],ll[1]))
			if arr.contains(point):
				ll.append(shapeRec.record[3].decode('iso-8859-1').encode('utf8'))
		if len(ll) == 3:
			ll.append('autre')
		
		myFile = open('latlong.csv', 'w')
		with myFile:
			writer = csv.writer(myFile)
			writer.writerows(latlong)

try:
	with open('revenus_.csv', 'rt') as f:
		reader = csv.reader(f)
		revenuList = list(reader)
	first = int(revenuList[len(revenuList)-1][0]) + 1
except:
	revenuList = []
	first = int(str(municipalities[0][1]) + '0001') 

num = first

for m in municipalities:
	fail = 0
	for nm in range(1,1000):
		
		t0 = time.time()
		
		if nm < 10:
			nnum = '000' + str(nm)
		if nm >= 10 and nm < 100:
			nnum = '00' + str(nm)
		if nm >= 100 and nm < 1000:
			nnum = '0' + str(nm)
		if nm >= 1000 and nm < 10000:
			nnum = str(nm)
		
		num = int(m + nnum)
		
		if str(num) not in column(revenuList,0):

			for j in latlong:
				if j[0] == str(num):
					lat = j[1]
					lng = j[2]
					try:
						j[4] != ''
					except:
						j.append('')
					if j[4] != '':
						arr = j[3] + " - " + j[4]
					else:
						arr = j[3]
					break
				print(num)
			statPage = 'http://www12.statcan.gc.ca/census-recensement/2016/dp-pd/adaprof/details/page.cfm?Lang=F&ADA_UID=' + str(num) + '&TABID=1&DGUID=2016A00052466023&SEX=1'

			page = urllib2.urlopen(statPage)
			
			# parse the html using beautiful soup and store in variable `soup`
			soup = BeautifulSoup(page, 'html.parser')	
			
			try:
				# Take out the <div> of name and get its value
				b0 = digitOnly(soup.find('td', attrs={'headers': 'L12012 geoADA estimateADA'}).text.strip()) #Nombre de bénéficiaires d'un revenu total âgés de 15 ans et plus dans les ménages privés - Données-échantillon (25 %)
				b1 = digitOnly(soup.find('td', attrs={'headers': 'L12013 geoADA estimateADA'}).text.strip()) #Revenu total moyen en 2015 parmi les bénéficiaires ($)
				b2 = digitOnly(soup.find('td', attrs={'headers': 'L12015 geoADA estimateADA'}).text.strip()) #Revenu après impôt moyen en 2015 parmi les bénéficiaires ($)
				b3 = digitOnly(soup.find('td', attrs={'headers': 'L12017 geoADA estimateADA'}).text.strip()) #Revenu du marché moyen en 2015 parmi les bénéficiaires ($)
				b4 = digitOnly(soup.find('td', attrs={'headers': 'L12019 geoADA estimateADA'}).text.strip()) #Transferts gouvernementaux moyens en 2015 parmi les bénéficiaires ($)
				b5 = digitOnly(soup.find('td', attrs={'headers': 'L12024 geoADA estimateADA'}).text.strip()) #Revenu d'emploi médian en 2015 pour les travailleurs qui ont travaillé toute l'année à plein temps en 2015 ($)
				b6 = digitOnly(soup.find('td', attrs={'headers': 'L12025 geoADA estimateADA'}).text.strip()) #Revenu d'emploi moyen en 2015 pour les travailleurs qui ont travaillé toute l'année à plein temps en 2015 ($)
				b7 = digitOnly(soup.find('td', attrs={'headers': 'L13010 geoADA estimateADA'}).text.strip()) #Revenu total moyen des ménages en 2015 ($)
				b8 = digitOnly(soup.find('td', attrs={'headers': 'L13011 geoADA estimateADA'}).text.strip()) #Revenu après impôt moyen des ménages en 2015 ($)
				b9 = digitOnly(soup.find('td', attrs={'headers': 'L13013 geoADA estimateADA'}).text.strip()) #Revenu total moyen des ménages comptant une personne en 2015 ($)
				b10 = digitOnly(soup.find('td', attrs={'headers': 'L13014 geoADA estimateADA'}).text.strip()) #Revenu après impôt moyen des ménages comptant une personne en 2015 ($)
				b11 = digitOnly(soup.find('td', attrs={'headers': 'L13016 geoADA estimateADA'}).text.strip()) #Revenu total moyen des ménages comptant deux personnes ou plus en 2015 ($)
				b12 = digitOnly(soup.find('td', attrs={'headers': 'L13017 geoADA estimateADA'}).text.strip()) #Revenu après impôt moyen des ménages comptant deux personnes ou plus en 2015 ($)
				b13 = digitOnly(soup.find('td', attrs={'headers': 'L20000 geoADA estimateADA'}).text.strip()) #lieux de naissance pour la population des immigrants dans les ménages privés - Données-échantillon (25 %) Total
				b13b = digitOnly(soup.find('td', attrs={'headers': 'L18000 geoADA estimateADA'}).text.strip()) # Total - Immigrant status and period of immigration for the population in private households - 25% sample data
				b14 = digitOnly(soup.find('td', attrs={'headers': 'L20016 geoADA estimateADA'}).text.strip()) #lieux de naissance pour la population des immigrants dans les ménages privés - Données-échantillon (25 %) FRANCE
				b15 = digitOnly(soup.find('td', attrs={'headers': 'L27050 geoADA estimateADA'}).text.strip()) #Total - Ménages propriétaires et locataires dont le revenu total du ménage est supérieur à zéro, dans les logements privés non agricoles, hors réserve selon le rapport des frais de logement au revenu - Données-échantillon (25 %)
				b16 = digitOnly(soup.find('td', attrs={'headers': 'L27052 geoADA estimateADA'}).text.strip()) #30 % ou plus du revenu est consacré aux frais de logement
				revenuList.append([num,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b13b,b14,b14/b13,b14/b13b,b15,b16,b16/b15,lat,lng,arr,b0])
				print (num,int(time.time()-t0),'s')
				fail = 0
			except:
				fail += 1
				print (num,', Not an ADA (or not enough data on this ADA)...',int(time.time()-t0),'s, fail:',fail)
			
			if fail >= 10:
				#numTps = str(num)
				#num = int(numTps[:3] + str(int(numTps[3])+1) + '0000')
				#print num
				break

			myFile = open('revenus_.csv', 'w')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerows(revenuList)
