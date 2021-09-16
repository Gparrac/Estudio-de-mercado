from pyasn1.type.univ import Null
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


class bs_fire():
    config = {
        'apiKey': "AIzaSyAOAJkrJbC-KQ_O5w1jbkSmMgt5Gs0bCGU",
        'authDomain': "angcrud-1d08b.firebaseapp.com",
        'databaseURL': "https://angcrud-1d08b-default-rtdb.firebaseio.com",
        'projectId': "angcrud-1d08b",
        'storageBucket': "angcrud-1d08b.appspot.com",
        'messagingSenderId': "91060917992",
        'appId': "1:91060917992:web:c91f1d5ebc2efe8bdadb5d",
        'measurementId': "G-L7HEL06FYR"
    }
    cred = credentials.Certificate('angcrud-1d08b-firebase-adminsdk-kuix0-5024b4eabc.json')
    firebase_admin.initialize_app(cred, {
    'storageBucket': 'angcrud-1d08b.appspot.com'
    })
    def __init__(self):
        self.firebase = pyrebase.initialize_app(self.config)

    def val_login(self, email, pwd):
        auth = self.firebase.auth()
        validar = False
        try:
            auth.sign_in_with_email_and_password(email, pwd)
            print('exito en autenticacion')
            validar = True
        except:
            print("invalido ")
            print(f"{email}/{pwd}")
        return validar

    def val_signup(self, name, email, pwd, urlPhoto):
        auth = self.firebase.auth()
        db = self.firebase.database()
        storage = self.firebase.storage()
        validar = False
        nameCloud = f'users/{name}/perfilePhoto.png'
        try:
            auth.create_user_with_email_and_password(email, pwd)
            storage.child(nameCloud).put(urlPhoto)
            urlPhoto = storage.child(nameCloud).get_url(None)
            data = {'name': name, 'email': email, 'pwd': pwd, 'url': urlPhoto}
            db.child("Users").child(name).set(data)

            print('exito en regitros')
            validar = True
        except:
            print("invalido ")
            print(f"{email}/{pwd}")
        return validar

    def find_User(self, email):
        db = self.firebase.database()
        users = db.child('Users').get()
        for user in users.each():
            if user.val()['email'] == email:
                data = {'name': user.val()['name'], 'email': email, 'pwd': user.val()[
                    'pwd'], 'url': user.val()['url']}
                return data
        return Null

    def save_files(self, name, urlFile, busqueda):
        path = './static/archivo'        
        storage = self.firebase.storage()
        db = self.firebase.database()
        # -----ALMACENADO EN EL STORAGE
        for file in urlFile:
            nameCloud = f'users/{name}/registros/{busqueda}/{file}'
            pathfile = f'{path}/{file}'
            print(file)
            storage.child(nameCloud).put(pathfile)
            url = storage.child(nameCloud).get_url(None)
            # -----CREANDO RUTAS DEL SOTRAGE EN REALTIME            
        db.child("Users").child(name).child('register').child(busqueda).set({'titulo':busqueda})
    def get_registers(self, name):
        keys = []
        db = self.firebase.database()
        scoreds = db.child("Users").child(name).child('register').get()
        for scored in scoreds.each():
            keys.append(scored.key())
        return keys

    def descargar(self, key, name):
        cadena = ['df_bp.csv', 'df_ofertas.csv',
                  'df_reference.csv', 'graf_bp.png', 'graf_total.png']
        storage = self.firebase.storage()
        
        for file in cadena:
            storage.child(
                f'/users/{name}/registros/{key}/{file}').download(f'./static/archivo/{file}')

    def eliminar(self, key, name, cadena):
        #elimina en storage
        for file in cadena:
            bucket = storage.bucket()
            blob = bucket.blob(f'users/{name}/registros/{key}/{file}')            
            print(blob)
            blob.delete() 
        #eliminar en realtime
        db = self.firebase.database()
        scoreds = db.child("Users").child(name).child('register').get()
        for scored in scoreds.each():
            if scored.key() == key:
                print(scored.key())
                db.child("Users").child(name).child('register').child(scored.key()).child('titulo').remove() 
        



"""db = bs_fire()

cadena = [ 'df_bp.csv', 'df_ofertas.csv',
          'df_reference.csv', 'graf_bp.png', 'graf_total.png']
#db.eliminar('arroz-1000-gr-diana','Gabriel',cadena)
db.save_files('Gabriel',cadena, 'arroz-1000-gr-diana')"""
# db.descargar('leche-1000-ml-alpina','Gabriel')
