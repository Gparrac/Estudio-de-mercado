# from matplotlib import pyplot as plt
import collections
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.core import frame

# importamos csv
df = pd.read_csv('./archivo/lista_prueba.csv', header=0)
#print(df)
store_names=['Merqueo','Exito','Mercado libre']
df_bp = pd.DataFrame( columns = ['ENCABEZADO', 'PRECIO', 'LINK', 'STORE'])
#df = pd.DataFrame(columns=['first_name', 'last_name', 'gender'])
#df = df.append({'first_name': 'Josy', 'last_name':'Clarae', 'gender':'Female'}, ignore_index=True)
print(df)
conteo=1
for name in store_names:
    print(name)
    conteo=1+conteo 
    tem = df[df['STORE'].str.contains(name, case=False)]
    print(tem)
    fila = tem['PRECIO'].idxmin()
    print(fila)
    min={
        'ENCABEZADO': str(tem['ENCABEZADO'][fila]),
        'PRECIO':  str(tem['PRECIO'][fila]),
        'LINK': str(tem['LINK'][fila]),
        'STORE': str(tem['STORE'][fila])
        }
    print(min)
    df_bp = df_bp.append(min, ignore_index = True)
    
print(df_bp)
print(conteo)

# filtro2 = filtro.sort_values("PRECIO")
# minimo = filtro2.iloc[0].to_numpy()

# precioMin.append(filtro2.get_value(filtro2['']))

# graficar
"""
conteo = filtro2['SIZE'].value_counts()
colors  = ("dodgerblue","salmon", "palevioletred", 
           "steelblue", "seagreen", "plum", 
           "blue", "indigo", "beige", "yellow")
pie = filtro2['SIZE'].value_counts().plot(kind = 'pie',
colors = colors,shadow = True,autopct ='%1.1f%%', startangle = 30,
radius = 1.5, center = (0.5,0.5),textprops = {'fontsize': 12},
frame =False, pctdistance = .65)
labels = conteo.index.unique()
plt.gca().axis("equal")
plt.title("Presentaciones encontrados",weight = 'bold', size = 14)


# filtro2.plot.pie(autopct='%1.1f%%')
# filtro2.legend ()
plt.savefig('./static/img/bodegaGraf.png',dpi=100,bbox_inches='tight')
plt.show()
"""
# print (filtro2)
