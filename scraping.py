from abc import ABCMeta, abstractmethod
from os import link
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import pandas as pd
import re
#----
from bs4 import BeautifulSoup
import time
import math
import matplotlib.pyplot as plt
#---------------------------------CLASE PADRE SCRAPING------------------------------------

class formatoExtraccion(metaclass = ABCMeta):

    produc_precio = []
    produc_titulo = []
    produc_link  = []  
    produc_size = []
    produc_store = []
    home_link = None

    def recargar(self):
        self.produc_precio = []
        self.produc_titulo = []
        self.produc_link  = []  
        self.produc_size = []
        self.produc_store = []
        self.home_link = None
    @abstractmethod
    def recolectar(self):
        pass
    def iniciar_ser(self):
        self.driver = webdriver.Chrome('./chromedriver')

    def crearFormato(self):
        self.data = pd.DataFrame({
            'ENCABEZADO' : self.produc_titulo,
            'PRECIO' :  self.produc_precio,
            'LINK' : self.produc_link,
            'STORE' : self.produc_store  
        })

    def filtrar_best_prices(self,store_names):
        df_bp = pd.DataFrame( columns = ['ENCABEZADO', 'PRECIO', 'LINK', 'STORE'])
        for name in store_names:
            tem=self.data[self.data['STORE'].str.contains(name, case=False)]
            fila=tem['PRECIO'].idxmin()
            df_bp= df_bp.append({
                'ENCABEZADO' : tem['ENCABEZADO'][fila],
                'PRECIO' :  tem['PRECIO'][fila],
                'LINK' : tem['LINK'][fila],
                'STORE' : tem['STORE'][fila]
                }, ignore_index = True) 
        return df_bp       
    def filtrar_referemcia(self, reference):
        
        data2 = self.data[self.data['ENCABEZADO'].str.contains(reference, case=False)]
        data2 = data2.sort_values("PRECIO")          
        return data2   

    def limpiar(self, size, unidad,categoria):
        self.data = self.data[self.data['ENCABEZADO'].str.contains(categoria, case=False)]
        val = True
        if unidad == 'gr':
            unit = 'kg'
        elif unidad == 'ml':
            unit = 'l'
        else:
            val = False
        if val:
            self.data = self.data[self.data['ENCABEZADO'].str.contains(
                str(size), case=False) | self.data['ENCABEZADO'].str.contains(str(round(size/1000)), case=False)] 
        else:
            self.data = self.data[self.data['ENCABEZADO'].str.contains(
                str(size)+''+unidad, case=False)]
        self.data = self.data.sort_values("PRECIO")
        #minimo = self.data.iloc[0].to_numpy()

    def crearGrafica(self,col,tipo,titulo,file_name,df):
        validar = False
        colors  = ("dodgerblue","salmon", "palevioletred", 
                "steelblue", "seagreen", "plum", 
                "blue", "indigo", "beige", "yellow")
        if tipo == 'pie':
            pie = df[col].value_counts().plot(kind = tipo,
            colors = colors, shadow = True, autopct ='%1.1f%%', startangle = 30,
            radius = 1.5, center = (0.5,0.5),textprops = {'fontsize': 12},
            frame =False, pctdistance = .65)
            plt.gca().axis("equal")
            validar = True 
        elif tipo == 'bar':
            print("!!!!!!!!!!!!!")
            print(df)
            pie=df.plot(kind = 'bar', x = 'STORE', y = 'PRECIO')
            pie.set_ylabel('')
        else:
            df[col].value_counts().plot(kind = tipo,
            colors = colors)
            validar = True
        #labels = conteo.index.unique()
        
        #plt.title(titulo, weight = 'bold', size = 14)
        plt.savefig('./static/archivo/'+file_name+'.png',dpi=100,bbox_inches='tight')
        
        #plt.legend(labels)
        plt.show()
        return validar   
    
    def guardar_csv(self,data,name_file):
        data.to_csv(r'./static/archivo/'+name_file+'.csv', index = None, header = True, encoding = 'utf-8-sig')


#--------------------------------------------------MERQUEO.COM-------------------------------------------------






        
    