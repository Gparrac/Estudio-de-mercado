from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import date
import time
from scraping import formatoExtraccion
class Navegacion_Ml(formatoExtraccion):
 

    def __init__(self, categoria ,tamano, unidades):
        self.iniciar_ser()
        self.home_link = 'https://listado.mercadolibre.com.co/'
        self.ruta1 = categoria+'-'+tamano+unidades
        self.ruta2 = self.ruta1.replace('-','%20')
        self.size = tamano+" "+unidades
#   self.categoria
    def recolectar(self):#class="ui-search-layout ui-search-layout--stack"
        self.driver.get(self.home_link+self.ruta1+'#D[A:'+self.ruta2+']')
        page = BeautifulSoup(self.driver.page_source,'html.parser')
        #bloque = page.find('ol',attrs = {'class':'ui-search-layout ui-search-layout--stack','data-view':True})
        for vendedor in page.findAll('li', class_ ="ui-search-layout__item"):
            titulo = vendedor.find('h2', class_ = "ui-search-item__title")
            precio = vendedor.find('span', class_ = "price-tag-fraction")
            link = vendedor.find('a', class_ = "ui-search-link")
            #print(link)
            if titulo and precio and link:
                self.produc_titulo.append((re.sub("\\n", "", titulo.text)).lower())
                self.produc_precio.append(int(re.sub("\\n|\.|\$", "", precio.text)))
                self.produc_link.append(link['href'])
                self.produc_store.append('Mercado libre')
                
                



##construcccion dataframe
"""
    def crearExcel(self):
        data = pd.DataFrame({
            'ENCABEZADO' : self.produc_titulo,
            'PRECIO' :  self.produc_precio,
            'LINK' : self.produc_link})
        data.to_csv(r'./archivo/lista_prueba.csv', index = None, header = True, encoding = 'utf-8-sig')
"""
#main prueba
"""
prueba1 = Navegacion('Arroz','1000','gr')
prueba1.recolectar()
prueba1.crearFormato()
print (prueba1.data)
min = prueba1.filtrar_final(1000,'gr','Arroz')
print (prueba1.data)
#prueba1.driver.quit()
"""