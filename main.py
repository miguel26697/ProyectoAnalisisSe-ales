#!/usr/bin/env python
# coding: utf-8

# In[37]:


from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import requests
import pandas as pd
import numpy as np
import folium
import datetime
import pymysql
import mysql.connector
from mysql.connector import errorcode

fecha = datetime.datetime.now()
fecha = str(fecha.date())
url='https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Colombia'
req=requests.get(url)
soup=BeautifulSoup(req.content,'html.parser')
datos=soup.find_all('th')
total=list()

for i in datos:
    total.append(i.text)

Casos=str(total[89])
Recuperados=str(total[50])
Hospitalizados=str(total[56])
Unidades=str(total[59])
Muertes=str(total[62])

print(Casos,Recuperados,Hospitalizados,Unidades,Muertes)

try:
   cnx = mysql.connector.connect(user='root', password='1234', database='covid', host='localhost')
   cursor = cnx.cursor()
   print('Conectado')
   sentencia = ("insert into total(fecha,Casos,Recuperados,Hospitalizados,Unidades,Muertes) values (%s,%s,%s,%s,%s,%s);")
   datos =(fecha,Casos,Recuperados,Hospitalizados,Unidades,Muertes)
   cursor.execute(sentencia,datos)
   cnx.commit()

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()

#Variables de control para web scraping contagiós Bogotá
auxsuma=0
longitud=0
valor=0
localidades=[]
localidades_nom=[]
Cpl=[]
aux=[]
recorrer=0
espacio=0
cont=0

#Variables de control para web scraping contagiós Colombia
conteo=0
conteoaux=0
auxdato=0
departamentos=[]
cpd=[]


#----------------------------Web scraping-------------------------------------------------------------------------------
url_1='https://canaltrece.com.co/noticias/cuantos-casos-coronavirus-covid-19-bogota-barrios-localidades-hoy/'
url_2='https://colombia.as.com/colombia/2020/10/29/actualidad/1603970788_671558.html'
url_3='https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Colombia'
page_1=requests.get(url_1)
page_2=requests.get(url_2)
page_3=requests.get(url_3)
soup_1=BeautifulSoup(page_1.content,'html.parser')
soup_2=BeautifulSoup(page_2.content,'html.parser')
soup_3=BeautifulSoup(page_3.content,'html.parser')


contagios_bogota=soup_1.find_all('li')
contagios_localidad=soup_1.find_all('strong')
contagios_colombia=soup_2.find_all('span')
datos=soup_3.find_all('th')

Total_cbta=list()
Total_cbta_1=list()
Total_ccol=list()
total=list()

#Web scraping por localidades Bogotá
for i in contagios_bogota:
   Total_cbta.append(i.text)


for i in Total_cbta:
    if(recorrer<19):
        for e in i:
            if(e==':'):
                espacio=1
            if((espacio==1)and(e!=(".")and(e!=':')and(e!=" ")and(e!=('\xa0')))):
                longitud=longitud+1
                #print(e)
                localidades.insert(0,e)


        #print('\n'+str(longitud)+'\n')
        aux.insert(0,longitud)
        espacio = 0
        longitud=0
        recorrer+=1


recorrer=18
vaus=86
otraux=86
while(recorrer>=0):
    otraux=otraux-aux[recorrer]

    if(aux[recorrer]==5):
        auxsuma=10000

    if(aux[recorrer]==4):
        auxsuma=1000

    while(vaus>otraux):
        valor=valor+auxsuma*float(localidades[vaus])
        vaus-=1
        auxsuma=auxsuma/10
    recorrer-=1
    Cpl.insert(0,valor)
    valor=0

print(Cpl)

for i in contagios_localidad:
    Total_cbta_1.append(i.text)

for o in Total_cbta_1:
    if((cont>=5)and(cont<24)):
        localidades_nom.insert(0,Total_cbta_1[cont])
    cont+=1
print(localidades_nom)
print('\n')

#Web scraping por Departamentos Colombia

for i in contagios_colombia:
   Total_ccol.append(i.text)

print("Contagios hoy "+str(Total_ccol[82]))
print("Contagios Totales  "+str(Total_ccol[83]))
print("Muertes hoy "+str(Total_ccol[84]))
print("Total Muertes "+Total_ccol[86])
print("Recuperados hoy "+str(Total_ccol[85]))
print("Total Recuperados "+Total_ccol[87])
print("Activos "+Total_ccol[88])
print("Muestras procesadas "+Total_ccol[89])
print("\n")

for i in Total_ccol:
    if((conteo>89)and(conteo<156)):
        if((conteo%2)==(0)):
            departamentos.insert(0,Total_ccol[conteo])
            conteoaux+=1
        else:
            auxdato=1000
            auxdato=float(Total_ccol[conteo])*1000
            cpd.insert(0,auxdato)

    conteo+=1
cpd[0]=cpd[0]/1000
print(departamentos)
print(cpd)

#Web scraping por general Colombia
for i in datos:
   total.append(i.text)

print("Recuperados acumulados "+str(total[48]))
print("Tratamiento es casa Aculados "+str(total[50]))
print("En hospitales Acumulados "+str(total[52]))
print("En UCI "+str(total[54]))

#Variables importantes
Recuperados1=float(total[50])
Casa1=float(total[53])
Hospital1=float(total[56])
UCI1=float(total[59])


#---------------------------Gráficas------------------------------------------------------------------------------------
#Diagrama de torta para localidades
fig_1= plt.figure()
Grafica_1=fig_1.add_subplot(111)
plt.title("Contagio por localidad")
Grafica_1.pie(Cpl,labels=localidades_nom,autopct="%0.1f %%")

fig_111= plt.figure()
Grafica_111=fig_111.add_subplot(111)
plt.title("Contagio por localidad")
Grafica_111.bar(localidades_nom,Cpl,color="blue")

#Diagrama de torta para departamentos
fig_2= plt.figure()
Grafica_2=fig_2.add_subplot(111)
plt.title("Contagio por departamento")
Grafica_2.pie(cpd,labels=departamentos,autopct="%0.1f %%")

#Diagrama de barras movimiento del covid
fig_3=plt.figure()
Grafica_3=fig_3.add_subplot(221)
textos=('Muertes','Recuperados','Contagios','Pacientes activos')
v1=(Total_ccol[84],Total_ccol[85],Total_ccol[82],Total_ccol[88])
plt.title('Covid-19 hoy')
plt.ylabel('Pacientes')
Grafica_3.bar(textos,v1,color='red')

Grafica_4=fig_3.add_subplot(222)
textos_2=('Muertes','Pacientes activos','Recuperados','Contagios')
v2=(Total_ccol[86],Total_ccol[88],Total_ccol[87],Total_ccol[83])
plt.title('Totales Covid-19')
plt.ylabel('Pacientes')
Grafica_4.bar(textos_2,v2,color='blue')

Grafica_5=fig_3.add_subplot(223)
textos_3=('Hospital','UCI')
v3=(Hospital1,UCI1)
plt.title('Covid-19 Hospitales')
plt.ylabel('Pacientes')
Grafica_5.bar(textos_3,v3,color='red')

Grafica_6=fig_3.add_subplot(224)
textos_4=('Muestras')
v4=(Total_ccol[89])
plt.title('Muestras procesadas')
Grafica_6.bar(textos_4,v4,color='red')

#Diagrama de torta para hospitales
fig_4= plt.figure()
Grafica_7=fig_4.add_subplot(111)
labels=('Hospilales','UCI')
value=(Hospital1,UCI1)
plt.title("Movimiento Hospitales")
Grafica_7.pie(value,labels=labels,autopct="%0.1f %%")

#Diagrama de torta movimiento covid
fig_5= plt.figure()
Grafica_8=fig_5.add_subplot(111)
labels_1=('Muertes','Pacientes activos','Recuperados')
value_1=(Total_ccol[86],Total_ccol[88],Total_ccol[87])
plt.title("Movimiento totales Covid-19")
Grafica_8.pie(value_1,labels=labels_1,autopct="%0.1f %%")

plt.show()

#-----------------------------------Mapas---------------------------------------------------------------------------
#Variables importantes
vconteo=0
vaux=0
radio=[]
colores_1=''
poscirculos=[[4.643493, -74.097520],[6.217,-75.567],[3.42158,-76.5205],[10.9878,-74.7889],[	4.4259,-74.1243],[7.11392,-73.1198],
             [ 8.817,-74.717],[8.75,-75.883],[10.45,-73.2510],[4.15,-73.633],[1.2136,-77.2811],[7.9,-72.57],[2.92504,-75.2897],
             [4.433,-75.217],[11.1450,-74.1206],[4.813,-75.694],[9.3,-75.491],[5.533,-73.367],[2.433,-76.617],[5.067,-75.517],
             [1.612,-75.6],[11.533,-72.911],[4.532,-75.652],[5.35,-72.452],[1.159,-76.647],[5.683,-76.655],[7.083,-70.757],[-4.208,-69.943],
             [12.537,-81.7313],[2.567,-72.633],[3.867,-67.917],[1.255, -70.235],[4.433,-69.84]]

for i in cpd:
    vaux=i/2
    radio.insert(0,vaux)

print(radio)
#Mapa de Colombia
Colombia=folium.Map(location=[4.643493, -74.097520],zoom_start=5)

#Para elegir tipo de vista
folium.raster_layers.TileLayer('Open Street Map').add_to(Colombia)
folium.raster_layers.TileLayer('Stamen Terrain').add_to(Colombia)
folium.raster_layers.TileLayer('Stamen Toner').add_to(Colombia)
folium.raster_layers.TileLayer('Stamen Watercolor').add_to(Colombia)
folium.raster_layers.TileLayer('CartoDB Positron').add_to(Colombia)
folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(Colombia)
folium.LayerControl(position='topright',collapsed=False).add_to(Colombia)
#Circulos

while(vconteo<33):

    if((radio[vconteo]<150000)and(radio[vconteo]>30000)):
        colores_1='orange'
    elif(radio[vconteo]<30000):
        colores_1='yellow'
    else:
        colores_1='red'

    folium.Circle(radius=radio[vconteo], location=poscirculos[vconteo], color=colores_1, fill=True, fill_color=colores_1).add_to(Colombia)
    vconteo+=1

#Ponomos en el mapa a la izquierda las opciones y guardamos el mapa

Colombia.save("C:\\Users\\migue\\PycharmProjects\\ProyectoAnalisis2\\mapas\\Colombia.html")



#Guardamos el mapa de Bogotá
Bogota=folium.Map(location=[4.643493, -74.097520],zoom_start=11)

folium.raster_layers.TileLayer('Open Street Map').add_to(Bogota)
folium.raster_layers.TileLayer('Stamen Terrain').add_to(Bogota)
folium.raster_layers.TileLayer('Stamen Toner').add_to(Bogota)
folium.raster_layers.TileLayer('Stamen Watercolor').add_to(Bogota)
folium.raster_layers.TileLayer('CartoDB Positron').add_to(Bogota)
folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(Bogota)

folium.LayerControl(position='topright',collapsed=False).add_to(Bogota)

radio_2=[]
v2conteo=0
colores_2=''


poscirculos_1=[[4.56619,-74.16198],[4.565,-74.116],[4.594,-74.074],[4.61341,-74.10623],[4.58940,-74.10472],[4.603,-74.091],
               [4.645,-74.094],[4.66405,-74.07501],[4.72859,-74.08219],[4.707,-74.107],[4.67472,-74.13223],[4.627,-74.157],
               [4.631,-74.195],[4.57228,-74.13507],[4.51465,-74.09739],[4.55840,-74.08884],[4.610,-74.070],[4.657,-74.047],[4.71199,-74.04306]]
v2aux=0

for i in Cpl:
    v2aux=i/10
    radio_2.insert(19,v2aux)


print(radio_2[0])
print(poscirculos_1[0])
while(v2conteo<19):

    if((radio_2[v2conteo]<2000)and(radio_2[v2conteo]>1000)):
        colores_2='orange'
    elif(radio_2[v2conteo]<1000):
        colores_2='yellow'
    else:
        colores_2='red'

    folium.Circle(radius=radio_2[v2conteo], location=poscirculos_1[v2conteo], color=colores_2, fill=True, fill_color=colores_2).add_to(Bogota)
    v2conteo+=1

Bogota.save("C:\\Users\\migue\\PycharmProjects\\ProyectoAnalisis2\\mapas\\Bogota.html")

try:
   cnx = mysql.connector.connect(user='root', password='1234', database='covid', host='localhost')
   cursor = cnx.cursor()
   print('Conectado')
   for i in range (len(Cpl)):
       sentencia = ("insert into localidades(fecha,nombre,casos) values (%s,%s,%s);")
       nombre= str(localidades_nom[i])
       casos= str(Cpl[i])
       datos =(fecha,nombre,casos)
       cursor.execute(sentencia,datos)
       cnx.commit()

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()
try:
   cnx = mysql.connector.connect(user='root', password='1234', database='covid', host='localhost')
   cursor = cnx.cursor()
   print('Conectado')
   for i in range (len(cpd)):
       sentencia = ("insert into depa(fecha,nombre,casos) values (%s,%s,%s);")
       nombre= str(departamentos[i])
       casos= str(cpd[i])
       datos =(fecha,nombre,casos)
       cursor.execute(sentencia,datos)
       cnx.commit()

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()

#-----------------------------------Prediccion---------------------------------------------------------------------------

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from google.colab import files
from matplotlib import pyplot as plt

time = []
datos = pd.read_csv('bateriaco.csv')
x = datos['fecha']
y = datos['datos']
X = x[:, np.newaxis]

X_train, X_test, y_train, y_test = train_test_split(X, y)

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor

datos = pd.read_csv('bateriaco.csv')
x = datos['fecha']
y = datos['datos']
X = x[:, np.newaxis]

X_train, X_test, y_train, y_test = train_test_split(X, y)

while True:

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    mlr = MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(3, 3), random_state=1)
    mlr.fit(X_train, y_train)
    print(mlr.score(X_train, y_train))
    if mlr.score(X_train, y_train) > 0.95:
        break

predicciones = []
aux = 0
for i in range(60, 120):
    print(i)
    time.append(aux)
    predicciones.append(mlr.predict([[i]]))
    print(predicciones[aux])
    aux = aux + 1

plt.plot(time, predicciones, 'o')
plt.title('Predicciones Contagiados en 2 meses Colombia')
plt.ylabel('Contagios')
plt.xlabel('Tiempo-Dias')
plt.show()





