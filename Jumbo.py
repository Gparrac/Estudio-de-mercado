from bs4 import BeautifulSoup

import pandas as pd
from datetime import date
import time
from scraping import formatoExtraccion
import re

class Navegacion(formatoExtraccion):
 

    def __init__(self, categoria ,tamano, unidades):
        self.iniciar_ser()
        self.home_link = 'https://www.tiendasjumbo.co/'
        self.ruta1 = categoria+'-'+tamano
        self.ruta2 = self.ruta1.replace('-','%20')
        self.size = tamano+' '+unidades
    #
    def recolectar(self):#class="ui-search-layout ui-search-layout--stack"
        self.driver.get(self.home_link+'buscar?q='+self.ruta2)
        time.sleep(10)
        page = BeautifulSoup(self.driver.page_source,'html.parser')
        bloque = page.findAll('section', class_= "search-container")
        print(page)
        print(page.title)
        #print(page.title)
        print(page.findAll('div', class_ = "impulse-card impulse-product-card product product grid"))
        for vendedor in page.findAll('div', class_ = "group-impulse-card-content"):
            titulo = vendedor.find('span',class_="formatted-text")
            precio = vendedor.find('span', class_ = "impulse-currency")
            size = self.size
            
            link = vendedor.find('a')
            
            
            if titulo.text.find('Arroz') and precio and link :
                self.produc_titulo.append(re.sub("\\n","",titulo.text))
                self.produc_size.append(re.sub("\\n|\.|\$","",size.text))
                self.produc_precio.append(re.sub("\\n|\.|\$","",precio.text))
                self.produc_link.append(self.home_link+link['href'])

                #print(f'Titulo de la pagina { titulo } #### Precio{ precio }')
            
##construcccion dataframe

        

#main prueba

prueba1 = Navegacion('Arroz','500','gr')
prueba1.recolectar()
prueba1.crearFormato()
#print(prueba1.data)
#prueba1.data.to_csv(r'./archivo/lista_merqueo.csv', index = None, header = True, encoding = 'utf-8-sig')"""



#prueba1.driver.quit()