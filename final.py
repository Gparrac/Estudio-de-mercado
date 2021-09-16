import matplotlib.pyplot as plt
import pandas as pd
from scraping import formatoExtraccion

class final(formatoExtraccion):
    def set_data(self,titulo, precio, link, size, store):
        print(len(titulo))
        print(len(precio))
        print(len(link))
        print(len(size))
        print(len(store ))
        for i in range(0,len(titulo)):
            self.produc_precio.append(precio[i]) 
            self.produc_titulo.append(titulo[i])
            self.produc_link.append(link[i])
            self.produc_size.append(size[i])
            self.produc_store.append(store[i])  
    
    def recolectar(self):
        print('Usuarios ya recolectados')

    def filtrar_corp(self):
        pr=self.data['STORE'].value_counts()
        return pr.to_frame(name='#ofertas')
    def crearGrafica(self,col,tipo,titulo,file_name):
        validar = False
        colors  = ("dodgerblue","salmon", "palevioletred", 
                "steelblue", "seagreen", "plum", 
                "blue", "indigo", "beige", "yellow")
        if tipo is 'pie':
            pie = self.data[col].value_counts().plot(kind = tipo,
            colors = colors, shadow = True, autopct ='%1.1f%%', startangle = 30,
            radius = 1.5, center = (0.5,0.5),textprops = {'fontsize': 12},
            frame =False, pctdistance = .65)
            plt.gca().axis("equal")
            validar = True 
        elif tipo is 'pp':
            self.data.bar.scatter(y = 'PRECIO',x = 'STORE')
        else:
            pie = self.data[col].value_counts().plot(kind = tipo,
            colors = colors)
            validar = True
        #labels = conteo.index.unique()
        
        plt.title(titulo, weight = 'bold', size = 14)
        plt.savefig('./static/img/'+file_name+'.png',dpi=100,bbox_inches='tight')
        pie.set_ylabel('')
        #plt.legend(labels)
        plt.show()
        return validar                
        

"""p = pd.DataFrame({
    'a':[3, 1, 2, 3, 4]
})
p=p['a'].value_counts()
print(p)
print(p.array)
print(p.to_frame(name='a'))"""
