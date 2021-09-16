from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from bs4 import BeautifulSoup

import time
from scraping import formatoExtraccion
import re


class Navegacion_exito(formatoExtraccion):

    def __init__(self, categoria, tamano, unidades):
        self.iniciar_ser()
        self.home_link = 'https://www.exito.com/'
        self.ruta1 = categoria+'-'+tamano
        self.ruta2 = self.ruta1.replace('-', '%20')
        self.size = tamano+' '+unidades
        self.categoria = categoria
    #   Self.unidad

    def recolectar(self):  # class="ui-search-layout ui-search-layout--stack"
        self.driver.get(self.home_link+'search?_query='+self.ruta2)
        time.sleep(20)
        #bot=self.driver.find_elements_by_xpath('//*[@id="react-select-2-input"]').
     
        #submit = self.driver.find_element_by_class_name('exito-geolocation-3-x-primaryButton shippingaddress-confirmar')
        #submit.click()
        
        page = BeautifulSoup(self.driver.page_source, 'html.parser')
        print(page.findAll('section', id_='react-select-2-input'))
        #bloque = page.find('ol',attrs = {'class':'ui-search-layout ui-search-layout--stack','data-view':True})
        # print(page.title)
        cont = 1
        #print(page.findAll('section', class_="vtex-product-summary-2-x-container vtex-product-summary-2-x-containerNormal overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc"))
        #print(page.findAll('div', class_ = "flex f5 fw5 pa0 flex items-center justify-start w-100 search-result-exito-vtex-components-selling-price exito-vtex-components-4-x-alliedDiscountPrice"))
        for vendedor in page.findAll('section', class_="vtex-product-summary-2-x-container vtex-product-summary-2-x-containerNormal overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc"):
            cont = cont+1
            titulo = vendedor.find(
                'div', class_="exito-product-details-3-x-stylePlp")
            #print(titulo)
            precio = vendedor.find(
                'div', class_="flex f5 fw5 pa0 flex items-center justify-start w-100 search-result-exito-vtex-components-selling-price exito-vtex-components-4-x-alliedDiscountPrice")
            if precio == None:
                precio = vendedor.find(
                'div', class_="flex f5 fw5 pa0 flex items-end justify-start w-100 search-result-exito-vtex-components-other-selling-price exito-vtex-components-4-x-otherSellingPrice")
            elif precio == None:
                precio = vendedor.find(
                'div', class_="flex f5 fw5 pa0 flex items-center justify-start w-100 search-result-exito-vtex-components-selling-price exito-vtex-components-4-x-alliedDiscountPrice")
            result = precio.text.replace('otros','')
            print(f'titulo:{titulo.text} => {precio.text}')
            link = vendedor.find(
                'a', class_="vtex-product-summary-2-x-clearLink h-100 flex flex-column")
            #print(link['href'])
            # print(f'{size.text.upper()}///{self.size.upper()}')
            if titulo and result and link :
                self.produc_titulo.append((re.sub("\\n", "", titulo.text)).lower())
                self.produc_precio.append(int(re.sub("\\n|\.|\$", "", result)))
                self.produc_link.append(self.home_link+link['href'])
                self.produc_store.append('Exito')
                print(f'Titulo de la pagina { titulo.text } #### Precio{ result }')
            print(cont)



"""prueba1 = Navegacion_exito('leche', '1000', 'ml')
prueba1.recolectar()
prueba1.crearFormato()
print(prueba1.data)
#prueba1.driver.quit()"""

