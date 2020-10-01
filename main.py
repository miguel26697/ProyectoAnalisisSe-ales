from  bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pymysql
import datetime

fecha = datetime.datetime.now()
req = requests.get('https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Colombia')
soup = BeautifulSoup(req.content,'html.parser')

datos=soup.find_all('th')
total=list()

for i in datos:
   total.append(i.text)

print("Recuperados "+str(total[49])+" recuperados acumulados "+str(total[50]))
print("Tratamiento es casa "+str(total[52])+" Aculados "+str(total[53]))
print("En hospitales "+str(total[55])+" Acumulados "+str(total[56]))
print("En UCI "+str(58)+" Acumulados "+str(total[59]))
print("Fallecidos "+str(total[61])+" acumulado "+str(total[62]))
print("Contagios hoy "+str(total[75])+" totales "+str(total[89]))

#HOY
Recuperados=int(total[49])
Casa=int(total[52])
Hospital=int(total[55])
UCI=int(total[58])
Fallecidos=int(total[61])
Contagios=int(total[75])

#TOTAL
Recuperados1=int(total[50])
Casa1=int(total[53])
Hospital1=int(total[56])
UCI1=int(total[59])
Fallecidos1=int(total[62])
Contagios1=int(total[89])

fecha = str(fecha.date())
print(fecha)
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='covid',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "select id_casos from casos where id_casos="+fecha+";"
        cursor.execute(sql)
        result = cursor.fetchone()
    if result == None:
        with connection.cursor() as cursor:
            sql = "insert into casos values(" + fecha + "," + str(Contagios1) + "," + str(Contagios) + "," +str(Hospital1)+"," +str(Hospital)+","+str(Fallecidos1)+","+str(Fallecidos)+","+str(Casa1)+","+str(Casa)+","+str(Recuperados1)+","+str(Recuperados)+","+str(UCI1)+","+str(UCI)+");"
            cursor.execute(sql)
            connection.commit()
finally:
    connection.close()
fig= plt.figure()
aux=fig.add_subplot(221)
textos=('Contagios','Recuperados','En casa')
v1=(Contagios1,Recuperados1,Casa1)
plt.title('Casos totales')
plt.ylabel('Pacientes activos')
aux.bar(textos,v1,color='red')


aux_1=fig.add_subplot(224)
ot=('Hospital','UCI','Fallecidos')
otros=(Hospital,UCI,Fallecidos)
aux_1.bar(ot,otros,color='blue') 
plt.title('Casos hoy')
plt.xlabel('Tipos de tratamiento')

aux=fig.add_subplot(223)
textos=('Contagios','Recuperados','En casa')
v1=(Contagios,Recuperados,Casa)
plt.title('Casos hoy')
plt.ylabel('Pacientes activos')
plt.xlabel('Tipos de tratamiento')
aux.bar(textos,v1,color='blue')

aux_1=fig.add_subplot(222)
ot=('Hospital','UCI','Fallecidos')
otros=(Hospital1,UCI1,Fallecidos1)
aux_1.bar(ot,otros,color='red')
plt.title('Casos totales')

fig=plt.figure()
pst=fig.add_subplot(111)
pastel=(Recuperados1,Fallecidos1,Contagios1)
nombres=("Recuperados","Fallecidos","Contagios")
pst.pie(pastel,labels=nombres,autopct="%0.1f %%")
plt.title('Vista General de la pandemia COVID-19')

fig=plt.figure()
huc=fig.add_subplot(111)
pastelh=(Casa1,Hospital1,UCI1)
nombresh=("Tratados en casa","Hospital","UCI")
huc.pie(pastelh,labels=nombresh,autopct="%0.1f %%")
plt.title('Personas contagiadas')

plt.show()