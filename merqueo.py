from bs4 import BeautifulSoup

import time
from scraping import formatoExtraccion
import re

class Navegacion_merqueo(formatoExtraccion):
 
    def __init__(self, categoria ,tamano, unidades):
        self.iniciar_ser()
        self.home_link = 'https://merqueo.com/bogota/'
        self.ruta1 = categoria+'-'+tamano+unidades
        self.ruta2 = self.ruta1.replace('-','%20')
        
    #
    def recolectar(self):#class="ui-search-layout ui-search-layout--stack"
        self.driver.get(self.home_link+'super-ahorro/search/'+self.ruta2)
        time.sleep(15)
        page = BeautifulSoup(self.driver.page_source,'html.parser')
        #bloque = page.find('ol',attrs = {'class':'ui-search-layout ui-search-layout--stack','data-view':True})
        #print(page.title)
        #print(page.findAll('article', class_ = "mq-product-card mq-default shadow-0 hoverable"))
        cont=1
        for vendedor in page.findAll('article', class_ = "mq-product-card mq-default shadow-0 hoverable"):
            titulo = vendedor.find('h3',class_="mq-product-title")
            precio = vendedor.find('p', class_ = "mq-product-price h6-text tx-pink500")
            size =  vendedor.find('p', class_ = "mq-product-subtitle")
            #print(size)
            link = vendedor.find('a')
            cont=cont+1
            #print(f'{precio.text}///{titulo.text}///{link.txt}')
            if titulo and precio and link and cont<30:
                self.produc_titulo.append((re.sub("\\n","",titulo.text)+re.sub("\\n|\.|\$","",size.text)).lower())
                self.produc_precio.append(int(re.sub("\\n|\.|\$","",precio.text)))
                self.produc_link.append('https://merqueo.com/'+link['href'])
                self.produc_store.append('Merqueo')
                print(f'Titulo de la pagina { titulo.text } #### Precio{ precio.text }')
            print(cont)
                     
##construcccion dataframe

        

#main prueba

"""prueba1 = Navegacion_merqueo('leche','1000','ml')
prueba1.recolectar()
prueba1.crearFormato()"""
#prueba1.data.to_csv(r'./archivo/lista_merqueo.csv', index = None, header = True, encoding = 'utf-8-sig')



#prueba1.driver.quit()