from re import S
from typing import Sized
from flask import Flask, request, url_for, redirect, flash
import numpy as np
from flask.templating import render_template
from pyasn1.type.univ import Null
from werkzeug.utils import secure_filename
from confDb import bs_fire
import os
import io
import merqueo
import exito
import mercadoLibre
import scraping
from final import final
import base64
import matplotlib.pyplot as plt
import pandas as pd
#import formulario


app = Flask(__name__)
app.secret_key = 'holaa!!'
app.config['ACTUALIZAR_ARCHIVO'] = "./static/archivo/"

UserName = Null
UserPwd = Null
bdf = bs_fire()
data = {'name': '', 'email': '', 'pwd': '', 'url':''}
titulo = Null
cadena=['df_bp.csv','df_ofertas.csv','df_reference.csv','graf_bp.png','graf_total.png']
def eliminar(folder):
    print(f'eliminando!!')
    folder = folder
    contador = True
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        print(f'{file_path}#####')
        os.unlink(file_path)



@app.route('/')
def index():
    global UserName, UserPwd, data, titulo
    UserName = Null
    UserPwd = Null    
    data = {'name': '', 'email': '', 'pwd': '', 'url':''}
    titulo = Null
    return render_template('index.html')


@app.route('/espera')
def espera():
    return render_template('signup.html', alert = False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    global bdf
    email = request.form['email']
    UserPwd = request.form['password']
    nameUser = request.form['nick']
    UserImage = request.files['file']
    print(UserImage.filename)
    if request.method == 'POST' and email != '' and UserName != '' and nameUser != '' and UserPwd != '' and len(UserImage.filename) != 0 :
        print('entrado')
        sf = secure_filename(UserImage.filename)
        UserImage.save(os.path.join(app.config['ACTUALIZAR_ARCHIVO'], sf))
        ruta = './static/archivo/ImgUser.png'
        os.rename('./static/archivo/'+UserImage.filename.replace(' ','_'),ruta)
        bdf.val_signup(nameUser,email,UserPwd,ruta)
        return render_template('index.html')
    else:
        alert = "Error en credenciales"
        return render_template('signup.html',alert=alert)

@app.route('/login',  methods=['GET', 'POST'])
def login():
    
    global UserName, UserPwd, bdf  
    UserName = request.form['username']
    UserPwd = request.form['password']
    if bdf.val_login(UserName, UserPwd):
        
        return redirect(url_for('panel'))
    alert = "Error en credenciales"
    return render_template('index.html', alert=alert)


@app.route('/panel')
def panel():    
    global bdf, UserName, data
    if len(data['name']) == 0 or len(UserName) == 0:
        print(UserName,'!!!')
        data=bdf.find_User(UserName)
        units = ['gr', 'ml', 'und']
        category = ['arroz', 'leche', 'huevo',
                    'atun', 'frijoles', 'lentejas', 'queso']
        print(data,'!!!')
        eliminar(folder='./static/archivo/')   
        return render_template('panel.html', units=units, ciclosU=len(units), ciclosC=len(category), category=category,data=data)
        
    else:
        return redirect(url_for('index'))
@app.route('/save/', methods=['POST','GET'])
def save():
    global bdf, titulo, data, cadena    
    print(UserName ,data['name'])
    bdf.save_files(data['name'] , cadena, titulo)
    return redirect(url_for('panel'))
@app.route('/registros', methods=['POST','GET'])
def registros():
    global bdf,data
    if len(data['name']) == 0:
        return redirect(url_for('index'))
    else:
        title=[]
        reference=[]
        unit=[] 
        scoreds = bdf.get_registers('Gabriel')
        for  i in range(0,len(scoreds)):
            temp = scoreds[i].split('-')
            title.append(temp[0])
            unit.append(f'{temp[1]} {temp[2]}')
            reference.append(temp[3])
        return render_template('registros.html',scoreds=scoreds,title=title, reference=reference,unit=unit, data=data, ciclo=len(scoreds) )
@app.route('/descargar/<pasado>', methods=['GET', 'POST'])
def descargar(pasado):
    global bdf, data, titulo
    conv=str(f'{pasado}')
    conv=conv.replace(' ','-')    
    bdf.descargar(conv,data['name'])
    titulo =conv
    return redirect(url_for('buscar'))
@app.route('/borrar/<pasado>', methods=['GET', 'POST'])
def borrar(pasado):    
    global bdf, data, cadena
    
    conv=str(f'{pasado}')
    conv=conv.replace(' ','-')    
    print(f'{conv}***{data["name"]}***{len(cadena)}')
    bdf.eliminar(conv,data['name'],cadena)
    print(conv)
    return redirect(url_for('registros'))    
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    global UserName, titulo, cadena
    if request.method == 'POST':
        category = request.form['category']
        size = request.form['size']
        unit = request.form['unit']
        references = request.form['references']
    else:
        datos=titulo.split('-')
        category=datos[0]
        size=datos[1]
        unit=datos[2]
        references=datos[3]
    if  category and size and unit:
        titulo = f'{category}-{size}-{unit}-{references}'
        val=False        
        for item in cadena:
            if os.path.exists(f"./static/archivo/{item}") : 
                val = True 
            else:
                 val = False 
        if val:
            print("EXIIIISTE")
            df_ofertas = pd.read_csv('./static/archivo/df_ofertas.csv', header=0)
            df_bp = pd.read_csv('./static/archivo/df_bp.csv', header=0)
            df_reference = pd.read_csv('./static/archivo/df_reference.csv', header=0)
        else:
            print(f'{category}///{size}////{unit}////{references}')

            # mercado libre
            web_merL = mercadoLibre.Navegacion_Ml(category, size, unit)
            #web_merL.recargar()
            web_merL.recolectar()
            web_merL.crearFormato()
            web_merL.driver.quit()

            # merqueo
            print("----------------------------------------------------")
            web_mer = merqueo.Navegacion_merqueo(category, size, unit)
            web_mer.recolectar()
            web_mer.crearFormato()

            web_mer.driver.quit()
            #web_mer.data.to_csv(r'./static/archivo/lista_pr2.csv', index = None, header = True, encoding = 'utf-8-sig')

            # exito
            web_exit = exito.Navegacion_exito(category, size, unit)
            web_exit.recolectar()
            web_exit.crearFormato()
            web_exit.driver.quit()

            # preparar datos
            web_exit.limpiar(int(size), unit, category)
            print("#######")
            print(web_exit.data)
            print("#######")

            # best_price
            store_names = ['Merqueo', 'Exito', 'Mercado libre']
            df_bp = web_exit.filtrar_best_prices(store_names)
            print(df_bp)
            web_exit.guardar_csv(df_bp, "df_bp")
            web_exit.crearGrafica(
                'STORE', 'bar', 'Ofertas por almacen', 'graf_bp', df_bp)
            # ofertas
            df_ofertas = web_exit.data
            web_exit.guardar_csv(df_ofertas, "df_ofertas")
            web_exit.crearGrafica(
                'STORE', 'pie', 'Ofertas por almacen', 'graf_total', df_ofertas)
            # referencias
            
            df_reference = web_exit.filtrar_referemcia(references)
            web_exit.guardar_csv(df_reference, "df_reference")
            # ---min precios

            # ---En bodega

            # grafica'registros'
            #web_all.crearGrafica('STORE','pie','Ofertas por almacen','graf_total')
            #pythoweb_min.crearGrafica('PRECIO','pp','precios minimos','precios_min')
            # --Por referencia

            # dataF2=web_all.filtrar_referemcia(references)

            # return render_template("patient_list.html", )
        print(UserName)
        return render_template('resultados.html', column_names=df_ofertas.columns.values, row_data=list(df_ofertas.values.tolist()),
                               link_column="LINK", zip=zip, column_names2=df_reference.columns.values, row_data2=list(df_reference.values.tolist()),
                               column_names3=df_bp.columns.values, row_data3=list(
                                   df_bp.values.tolist()),
                               title=category, size=size,unit=unit,reference=references,data=data)
    return redirect(url_for('panel'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
