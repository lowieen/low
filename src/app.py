from flask import Flask, jsonify, request, session, flash, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, func
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from flask_bcrypt import generate_password_hash, check_password_hash
import secrets
import uuid
from datetime import datetime, timedelta
from send_email import send_report
from send_email import send_newPass
from io import BytesIO
from PIL import Image
from base64 import b64encode
import os

app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/low'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = secrets.token_hex(32) # Asignar clave secreta generada aleatoriamente
db=SQLAlchemy(app)
ma=Marshmallow(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True, index=True)
    user = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(30))
    follows = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    reset_token = db.Column(db.String(32), unique=True)
    reset_token_expiration = db.Column(db.DateTime)
    def __init__(self, email, user, password, nombre, follows, followers, reset_token, reset_token_expiration):
        self.email = email
        self.user = user
        self.password = password
        self.nombre = nombre
        self.follows = follows
        self.followers = followers
        self.reset_token = reset_token
        self.reset_token_expiration = reset_token_expiration


class profile(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(50), nullable=False)
    user=db.Column(db.String(20), nullable=False)
    nombre=db.Column(db.String(15))
    apellido=db.Column(db.String(15))
    pais=db.Column(db.String(20))
    telefono=db.Column(db.String(20))
    fecha_nacimiento=db.Column(db.Date)
    descripcion=db.Column(db.Text)
    url=db.Column(db.String(255))
    img_perfil=db.Column(db.LargeBinary, nullable=True)
    img_portada=db.Column(db.LargeBinary, nullable=True)
    def __init__(self,email,user,nombre,apellido,pais,telefono,fecha_nacimiento,descripcion,url,img_perfil,img_portada):
        self.email = email
        self.user = user 
        self.nombre = nombre
        self.apellido = apellido
        self.pais = pais
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.descripcion=descripcion
        self.url=url
        self.img_perfil=img_perfil
        self.img_portada=img_portada


class publication(db.Model):
    id=db.Column(db.Integer, primary_key= True)
    contenido=db.Column(db.Text, nullable=False)
    imagen = db.Column(db.LargeBinary)
    fecha_creacion=db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id=db.Column(db.String(20), db.ForeignKey('users.user'), nullable=False)
    likes=db.Column(db.Integer, default=0)
    def __init__(self, contenido, imagen, user_id):
        self.contenido=contenido
        self.user_id=user_id
        self.imagen=imagen


class hiddenPublication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publication_id = db.Column(db.Integer) 
    user = db.Column(db.String(20), db.ForeignKey('users.user'), nullable=False)
    def __init__(self, publication_id, user):
        self.publication_id = publication_id
        self.user = user


class message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_user = db.Column(db.String(20), db.ForeignKey('users.user'), nullable=False)
    recipient_user = db.Column(db.String(20), db.ForeignKey('users.user'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    conversacion_id = db.Column(db.String(100))
    fecha_envio = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __init__(self, sender_user, recipient_user, contenido, conversacion_id):
        self.sender_user = sender_user
        self.recipient_user = recipient_user
        self.contenido = contenido
        self.conversacion_id = conversacion_id


class notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_emisor = db.Column(db.String(20), db.ForeignKey('users.user'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    publicacion_id = db.Column(db.Integer, nullable=True)
    user_receptor = db.Column(db.String(20), nullable=False)
    fecha_notificacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __init__(self, user_emisor, tipo, contenido, publicacion_id, user_receptor):
        self.user_emisor = user_emisor
        self.tipo = tipo
        self.contenido = contenido
        self.publicacion_id = publicacion_id
        self.user_receptor = user_receptor


class followUp(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    follower_user=db.Column(db.String(20), db.ForeignKey('users.user'), nullable=False)
    followed_user=db.Column(db.String(20), db.ForeignKey('users.user'), nullable=False)
    fecha_seguimiento=db.Column(db.DateTime, default=db.func.current_timestamp())
    def __init__(self,follower_user,followed_user):
        self.followed_user=followed_user
        self.follower_user=follower_user


class likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False)
    date_liked = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __init__(self, user_id, publication_id):
        self.user_id = user_id
        self.publication_id = publication_id


with app.app_context():
    db.create_all()



class usersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = users
user_schema = usersSchema()
users_schema = usersSchema(many=True)

class profileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = profile 
profile_schema = profileSchema()
profils_schema = profileSchema(many=True)

class publicationSchema(Schema):
    id = fields.Int()
    contenido = fields.Str()
    imagen = fields.Str()
    fecha_creacion = fields.DateTime()
    user_id = fields.Str()
    likes = fields.Int()
publication_schema = publicationSchema()
publications_schema = publicationSchema(many=True)

class hiddenPublicationSchema(Schema):
    id = fields.Int()
    publication_id = fields.Int()
    user = fields.Str()
hiddenPublication_schema = hiddenPublicationSchema()
hiddenPublications_schema = hiddenPublicationSchema(many=True)

class messageSchema(Schema):
    id = fields.Int()
    sender_user = fields.Str()
    recipient_user = fields.Str()
    contenido = fields.Str()
    conversacion_id = fields.Str()
    fecha_envio = fields.DateTime()
message_schema=messageSchema()
messages_schema=messageSchema(many=True)

class notificationSchema(Schema):
    id = fields.Int()
    user_emisor = fields.Str()
    tipo = fields.Str()
    contenido = fields.Str()
    publicacion_id = fields.Int()
    user_receptor = fields.Str()
    fecha_notificacion = fields.DateTime()
notification_schema=notificationSchema()
notifications_schema=notificationSchema(many=True)

class followUpSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    follower_user = fields.Str()
    followed_user = fields.Str()
    fecha_seguimiento = fields.DateTime()
followUp_schema=followUpSchema()
followsUp_schema=followUpSchema(many=True)

class LikesSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    date_liked = fields.DateTime()
    publication_id = fields.Int()
like_schema = LikesSchema()
likes_schema = LikesSchema(many=True)

#------------------------------------------USERS--------------------------------------------------

#Registro y/o obtención de Usuarios
@app.route('/users', methods=['GET','POST'])
def all_users():
    if request.method == 'POST':
        email=request.json['email']
        user=request.json['user']
        password=request.json['pass']
        nombre='-'
        follows=0
        followers=0
        reset_token=None
        reset_token_expiration=None

        hashed_password = generate_password_hash(password).decode('utf-8')

        new_user = users(email=email, user=user, password=hashed_password, nombre=nombre, follows=follows, followers=followers, reset_token=reset_token, reset_token_expiration=reset_token_expiration)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message':'Usuario creado correctamente.'}), 200

    usuarios=users.query.all()
    result=users_schema.dump(usuarios)

    return jsonify(result)


#Obtener los datos de la cuenta de un user
@app.route('/users/<user>')
def get_user(user):
    usuario = users.query.filter_by(user=user).first()
    resultado = user_schema.dump(usuario)
    return resultado


#Login y autenticación del usuario
@app.route('/logs',methods=['POST'])
def aut_user():
    email=request.json['email']
    user=request.json['user']
    password=request.json['password']

    if not email and not user and not password:
        return jsonify({'error': 'Faltan el correo electrónico o la contraseña.'}), 400
    
    usuario = None

    if email == None:
        usuario = users.query.filter_by(user=user).first()
    else:
        usuario = users.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.password, password):
        return jsonify({'error':'El email/usuario o la contraseña son incorrectas.'}), 400

    return user_schema.jsonify(usuario), 200


#Autenticación de password y cambio de la misma 
@app.route('/password/<user>',methods=['PUT'])
def change_password(user):
    usuario=users.query.filter_by(user=user).first()
    password=request.json['password']
    nueva_password=request.json['nueva_password']

    if not check_password_hash(usuario.password, password):
        return jsonify({'error':'La contraseña es incorrecta.'}), 400
    
    hashed_password=generate_password_hash(nueva_password).decode('utf-8')
    usuario.password=hashed_password

    db.session.commit()

    return jsonify({'message':'Se cambió tu contraseña.'}),200
    

#Eliminar cuenta, perfil y sus publicaciones
@app.route('/delete/<user>',methods=['DELETE'])
def delete_user(user):
    password = request.json['password']
    user_id= request.json['user_id']

    usuario = users.query.filter_by(user=user).first()

    if not check_password_hash(usuario.password, password):
        return jsonify({'error': 'La contraseña ingresada es incorrecta.'}), 400

    # Eliminar publicaciones
    publications_to_delete = publication.query.filter_by(user_id=user).all()
    for pub in publications_to_delete:
        db.session.delete(pub)

    # Eliminar mensajes enviados y recibidos
    messages_to_delete = message.query.filter((message.sender_user == user) | (message.recipient_user == user)).all()
    for msg in messages_to_delete:
        db.session.delete(msg)

    # Eliminar likes
    likes_to_delete = likes.query.filter_by(user_id=user_id).all()
    for like in likes_to_delete:
        db.session.delete(like)

    # Eliminar notificaciones
    notifications_to_delete = notification.query.filter_by(user_emisor=user).all()
    for notification_user in notifications_to_delete:
        db.session.delete(notification_user)

    # Eliminar seguidores y seguidos
    followers_to_delete = followUp.query.filter_by(follower_user=user).all()
    for follower in followers_to_delete:
        db.session.delete(follower)

    followed_to_delete = followUp.query.filter_by(followed_user=user).all()
    for followed in followed_to_delete:
        db.session.delete(followed)

    # Eliminar perfil de usuario
    profile_to_delete = profile.query.filter_by(user=user).first()
    if profile_to_delete:
        db.session.delete(profile_to_delete)

    # Eliminar el usuario
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'Cuenta eliminada exitosamente.'}), 200


# MODIFICAR PASSWORD
#Checkeo de email si existe
@app.route('/restablecer-contrasena', methods=['POST'])
def solicitar_restablecer_contrasena():
    email = request.json.get('email')
    user = users.query.filter_by(email=email).first()

    if user:
        # Genera un token único
        token = secrets.token_hex(16)
        user.reset_token = token
        user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

        # Envía el correo electrónico con el token
        response, status_code = send_newPass(user.email, token)
        return jsonify(response), status_code
    

#Restablecer password
@app.route('/new-password/<token>', methods=['GET', 'POST'])
def cambiar_contrasena(token):
    user = users.query.filter_by(reset_token=token).first()

    if not user or user.reset_token_expiration < datetime.utcnow():
        flash('El enlace para restablecer la contraseña es inválido o ha expirado. Solicita un nuevo enlace.', 'error')
        # Redirige al usuario a la página
        # return redirect(url_for('home'))
        return redirect("http://localhost:5173/login") #redireccionar a url especifica
    
    if request.method == 'GET':
        if user.reset_token is None:  # Verifica si el token ya se ha utilizado
            flash('El enlace para restablecer la contraseña ya ha sido utilizado.', 'error')
            # return redirect(url_for('/'))
            return redirect("http://localhost:5173/login")

        return jsonify({'token': token})

    elif request.method == 'POST':
        new_password = request.json.get('password')
        hashed_password = generate_password_hash(new_password).decode('utf-8')

        if hashed_password:
            # Actualiza la contraseña del usuario
            user.password = hashed_password
            user.reset_token = None
            user.reset_token_expiration = None
            db.session.commit()
            # Devuelve una respuesta JSON para indicar el éxito
            return jsonify({'message': 'Contraseña restablecida con éxito'}), 200
        else:
            # Devuelve una respuesta JSON para indicar un error
            return jsonify({'error': 'Contraseña no válida'}), 400

    # Si no es una solicitud GET o POST, puedes devolver una respuesta de otro tipo si es necesario
    return jsonify({'error': 'Método no permitido'}), 405


# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_email', None)
    return jsonify({'message':'Sesión finalizada con éxito.'})

#----------------------------------------PROFILE-----------------------------------
# Imagenes predeterminadas
default_profile_path = os.path.join('public','default-images', 'perfil_default.jpg')
default_cover_path = os.path.join('public','default-images', 'portada_default.jpg')

def read_image_as_binary(image_path):
    with open(image_path, "rb") as image_file:
        return image_file.read()

# Obtener los datos binarios de las imágenes predeterminadas
default_profile_binary = read_image_as_binary(default_profile_path)
default_cover_binary = read_image_as_binary(default_cover_path)


# Creación del perfil
@app.route('/profiles',methods=['POST'])
def create_profile():
    email=request.json['email']

    usuario=users.query.filter_by(email=email).first()
    user=usuario.user

    img_perfil = default_profile_binary
    img_portada = default_cover_binary

    nombre='-'
    apellido='-'
    pais='-'
    telefono='-'
    fecha_nacimiento=None
    descripcion=None
    url=None

    new_profile=profile(
        email=email,
        user=user,
        nombre=nombre,
        apellido=apellido,
        pais=pais,
        telefono=telefono,
        fecha_nacimiento=fecha_nacimiento,
        descripcion=descripcion,
        url=url,
        img_perfil=img_perfil,
        img_portada=img_portada
    )
    
    db.session.add(new_profile)
    db.session.commit()

    return jsonify({'message':'Perfil creado con exito.'}), 200


# Actualizar datos personales y/o obtenerlos 
@app.route('/profile/<user>',methods=['PUT','GET'])
def edit_profiel(user):
    usuario=users.query.filter_by(user=user).first()   
    perfil_user=profile.query.filter_by(user=user).first()
    if request.method == 'PUT':
        nombre=request.json['nombre']
        apellido=request.json['apellido']
        pais=request.json['pais']
        telefono=request.json['telefono']
        fecha_nacimiento=request.json['fechaNac']
        url=request.json['url']
        descripcion=request.json['description']

        perfil_user.nombre=nombre
        perfil_user.apellido=apellido
        perfil_user.pais=pais
        perfil_user.telefono=telefono
        perfil_user.fecha_nacimiento=fecha_nacimiento
        perfil_user.url=url
        perfil_user.descripcion=descripcion

        usuario.nombre=f'{nombre} {apellido}'
        db.session.commit()

        perfil_user.img_perfil = None
        perfil_user.img_portada = None
        return profile_schema.jsonify(perfil_user)
    
    else:
        perfil_user.img_perfil = None
        perfil_user.img_portada = None
        return profile_schema.jsonify(perfil_user)

#Obtener publicaciones hechas
@app.route('/publications/<user>')
def get_publications_user(user):
    publicaciones=publication.query.filter_by(user_id=user).all()
    all_publications = []

    for publicacion in publicaciones:
        perfil_user = profile.query.filter_by(user=publicacion.user_id).first()
        img_perfil_base64 = b64encode(perfil_user.img_perfil).decode('utf-8')

        if publicacion.imagen:
            img_publicacion_base64 = b64encode(publicacion.imagen).decode('utf-8')
        else:
            img_publicacion_base64 = None

        all_publications.append({
            'id':publicacion.id,
            'contenido':publicacion.contenido,
            'imagen':img_publicacion_base64,
            'fecha_creacion':publicacion.fecha_creacion,
            'user_id':publicacion.user_id,
            'likes':publicacion.likes,
            'img_perfil':img_perfil_base64
        })

    return jsonify(all_publications)


#Obtener publicaciones likeadas 
@app.route('/publication/liked/<user>')
def get_publications_liked(user):
    usuario = users.query.filter_by(user=user).first()

    publicaciones_likeadas = likes.query.filter_by(user_id=usuario.id).all()

    publication_ids = [like.publication_id for like in publicaciones_likeadas]

    publicaciones = publication.query.filter(publication.id.in_(publication_ids)).all()

    publicaciones_ocultas = hiddenPublication.query.filter_by(user=user).all()

    # Crear una lista temporal para almacenar las publicaciones no ocultas
    publicaciones_no_ocultas = []

    for publicacion in publicaciones:
        # Comprobar si la publicación no está en la lista de ocultas
        if not any(oculta.publication_id == publicacion.id for oculta in publicaciones_ocultas):
            perfil_user = profile.query.filter_by(user=publicacion.user_id).first()
            img_perfil_base64 = b64encode(perfil_user.img_perfil).decode('utf-8')
            if publicacion.imagen:
                img_publicacion_base64 = b64encode(publicacion.imagen).decode('utf-8')
            else:
                img_publicacion_base64 = None

            publicaciones_no_ocultas.append({
                'contenido': publicacion.contenido,
                'fecha_creacion': publicacion.fecha_creacion,
                'id': publicacion.id,
                'imagen': img_publicacion_base64,
                'likes': publicacion.likes,
                'user_id': publicacion.user_id,
                'img_perfil': img_perfil_base64
            })

    return jsonify(publicaciones_no_ocultas)


#Obtener datos del usuario
@app.route('/information/<user>/<userLogged>')
def get_infoUser(user,userLogged):
    user = user
    if user:
        usuario = users.query.filter_by(user=user).first()
        dataUser = profile.query.filter_by(user=user).first()
        seguimiento = followUp.query.filter_by(follower_user=userLogged).all()

        img_data_perfil = dataUser.img_perfil 
        img_data_portada = dataUser.img_portada 

        img_perfil_base64 = b64encode(img_data_perfil).decode('utf-8')
        img_portada_base64 = b64encode(img_data_portada).decode('utf-8')
        dataUser.img_perfil = img_perfil_base64
        dataUser.img_portada = img_portada_base64

        serializacion_dataUser = profile_schema.dump(dataUser)
        serializacion_seguimiento = followsUp_schema.dump(seguimiento)

        return jsonify({
            'dataUser': serializacion_dataUser,
            'seguidores': usuario.followers,
            'seguidos': usuario.follows,
            'seguimiento': serializacion_seguimiento,
        })

    else:
        return jsonify({'error':'No se encontró el perfil del usuario'})
    

#Subir nueva foto de perfil
@app.route('/upload/img-profile/<user>', methods=['PUT'])
def upload_img_profile(user):
    user_profile = profile.query.filter_by(user=user).first()
    try:
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_data = image.read()  # Lee los datos binarios de la imagen

                # Redimensionar la imagen
                max_width = 220  
                max_height = 220
                img = Image.open(BytesIO(image_data))
                img.thumbnail((max_width, max_height))

                # Convertir la imagen redimensionada de nuevo a datos binarios
                output_buffer = BytesIO()
                img.save(output_buffer, format='JPEG')
                image_data_resized = output_buffer.getvalue()

                # Guardar los datos binarios de la imagen redimensionada
                user_profile.img_perfil = image_data_resized

                # Guarda los cambios en la base de datos
                db.session.commit()

                image_data_base64 = b64encode(image_data_resized).decode('utf-8')
                objeto = {
                    'perfil': image_data_base64
                }
                return jsonify(objeto)

    except Exception as e:
        return jsonify({'error': 'Error al subir la imagen de perfil'}), 400
        

#Subir nueva foto de portada
@app.route('/upload/img-portada/<user>', methods=['PUT'])
def upload_img_portada(user):
    user_profile = profile.query.filter_by(user=user).first()
    try:
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_data = image.read()

                # Redimensionar la imagen
                max_width = 600 
                max_height = 600 
                img = Image.open(BytesIO(image_data))
                img.thumbnail((max_width, max_height))

                # Convertir la imagen redimensionada de nuevo a datos binarios
                output_buffer = BytesIO()
                img.save(output_buffer, format='JPEG')
                image_data_resized = output_buffer.getvalue()

                # Guardar los datos binarios de la imagen redimensionada
                user_profile.img_portada = image_data_resized

                db.session.commit()

                image_data_base64 = b64encode(image_data_resized).decode('utf-8')
                objeto = {
                    'portada': image_data_base64
                }
                return jsonify(objeto)
            
    except Exception as e:
        return jsonify({'error': 'Error al subir la imagen de portada: ' + str(e)}), 400



#Obtener imagen de perfil y portada
@app.route('/profile-image/<user>')
def get_img_profile(user):
    try:
        user_profile = profile.query.filter_by(user=user).first()
        if user_profile and user_profile.img_perfil and user_profile.img_portada:
            # Lee los datos binarios de la imagen almacenada
            image_data_perfil = user_profile.img_perfil
            image_data_portada = user_profile.img_portada

            # Convierte los datos binarios a base64
            image_perfil_base64 = b64encode(image_data_perfil).decode('utf-8')
            image_portada_base64 = b64encode(image_data_portada).decode('utf-8')

            imagenes = {
                'img_perfil': image_perfil_base64,
                'img_portada': image_portada_base64,
            }

            return jsonify(imagenes)

        # Devuelve una respuesta por defecto si no se encuentra la imagen
        return jsonify({'error': 'No se encontró la imagen de perfil'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener la imagen de perfil: ' + str(e)}), 400


#Obtener imagenes perfil de los usuarios
@app.route('/profile/all-images')
def get_all_profileImgs():
    all_perfiles = profile.query.all()
    perfiles = {}

    for perfil in all_perfiles:
        image_data_perfil = perfil.img_perfil
        image_perfil_base64 = b64encode(image_data_perfil).decode('utf-8') 
        perfiles[perfil.user] = image_perfil_base64

    return jsonify(perfiles)

#----------------------------------------PUBLICACIONES Y NOTIFICACION LIKE-----------------------------------
#Obtener publicaciones de los usuarios seguidos y propias
@app.route('/followed_publications/<user>')
def get_publications(user):
    user = user
    resultados = []
    perfil_users = []

    publicaciones = publication.query.filter_by(user_id=user).all()
    resultados.extend(publicaciones)

    seguimiento = followUp.query.filter_by(follower_user=user).all()
    for seguidos in seguimiento:
        # Obtener las publiaciones de los usuarios seguidos
        resultado = publication.query.filter_by(user_id=seguidos.followed_user).all()
        resultados.extend(resultado)
        # Obtener los perfiles de los usuarios seguidos
        usuario = profile.query.filter_by(user=seguidos.followed_user).first()
        perfil_users.append(usuario)

    publicaciones_ocultas = hiddenPublication.query.filter_by(user=user).all()
    # Crear una lista temporal para almacenar las publicaciones no ocultas
    resultados_filtrados = []
    for publicacion in resultados:
        # Comprobar si la publicación no está en la lista de ocultas
        # Crea un diccionario con los datos de la publicación y la img de perfil 
        if not any(oculta.publication_id == publicacion.id for oculta in publicaciones_ocultas):
            perfil_user = profile.query.filter_by(user=publicacion.user_id).first()
            image_perfil_base64 = b64encode(perfil_user.img_perfil).decode('utf-8')

            if(publicacion.imagen != None):
                image_publicacion_base64 = b64encode(publicacion.imagen).decode('utf-8')
            else:
                image_publicacion_base64 = None

            resultados_filtrados.append({
                'contenido': publicacion.contenido,
                'fecha_creacion': publicacion.fecha_creacion,
                'id': publicacion.id,
                'imagen': image_publicacion_base64,
                'likes': publicacion.likes,
                'user_id': publicacion.user_id,
                'img_perfil': image_perfil_base64
            })

    return jsonify({'publicaciones':resultados_filtrados})

#Nueva publicación
@app.route('/publications',methods=['POST'])
def create_publication():
    if 'image' in request.files:
        imagen = request.files['image']
        if imagen.filename != '':
            image_data = imagen.read()

            # Redimensionar la imagen
            max_width = 800
            max_height = 500
            img = Image.open(BytesIO(image_data))
            img.thumbnail((max_width, max_height))

            # Convertir la imagen redimensionada de nuevo a datos binarios
            output_buffer = BytesIO()
            img.save(output_buffer, format='JPEG')
            image_data_resized = output_buffer.getvalue()

            contenido = request.form['contenido']
            usuario = request.form['usuario']
            nueva_publicacion = publication(contenido=contenido, user_id=usuario, imagen=image_data_resized)
    else :
        contenido = request.json['contenido']
        usuario = request.json['usuario']
        imagen = None

        nueva_publicacion = publication(contenido=contenido, user_id=usuario, imagen=imagen)

    db.session.add(nueva_publicacion)
    db.session.commit()

    return jsonify({'message': 'Publicación creada exitosamente'}), 200

    
#Dar like a una publicacion y Crear notificación
@app.route('/publications/<id>/like', methods=['POST','DELETE'])
def like_publication(id):
    user = request.json['user']
    usuario = users.query.filter_by(user=user).first()
    publicacion_user = publication.query.filter_by(id=id).first()

    if request.method == 'POST':
        try:
            # Nuevo like
            like = likes(user_id=usuario.id, publication_id=id)
            db.session.add(like)

            # Actualizar los likes
            publicacion = db.session.get(publication,id)
            publicacion.likes += 1

            #Verifica si ya existe la notificación de like 
            notificacion_like=notification.query.filter_by(user_emisor=usuario.user, tipo='like', publicacion_id=id, user_receptor=publicacion_user.user_id).first()
            if notificacion_like:
                db.session.commit()

            else:
                # Verifica si el like es a una publicación propia
                auto_like=publication.query.filter_by(user_id=usuario.user, id=id).first()
                if auto_like:
                    db.session.commit()

                else:
                    # Crear notificación
                    contenido = 'le gustó tu publicación'
                    tipo = 'like'
                    publicacion_id = id
                    notificacion = notification(user_emisor=usuario.user, tipo=tipo, contenido=contenido, publicacion_id=publicacion_id, user_receptor=publicacion_user.user_id)
                    db.session.add(notificacion)

                    db.session.commit()

            return get_publications_user(usuario.user)
        
        except Exception as e:
            print(f"Error al agregar registros: {str(e)}")
            db.session.rollback()
            return jsonify({'message':'Error de integridad en la base de datos.'})
        
    elif request.method == 'DELETE':
        like = db.session.query(likes).filter_by(user_id=usuario.id, publication_id=id).first()
        if like:
            db.session.delete(like)

            publicacion = db.session.get(publication, id)
            publicacion.likes -= 1
            
            db.session.commit()
            return get_publications_user(usuario.user)
        else:
            return jsonify({'message': 'No se encontró el like'}), 404



#Obtener publicacion likeadas por user
@app.route('/publications/likes/<user>')
def check_like(user):
    usuario = users.query.filter_by(user=user).first()
    likes_query = likes.query.filter_by(user_id=usuario.id).all()
    
    if likes_query:
        likes_data = likes_schema.dump(likes_query)
        return jsonify(likes_data)
    else:
        return jsonify({'message': 'El usuario no ha dado like a ninguna publicación'})



#Eliminar publicación, sus likes y notificaciones
@app.route('/publications/<id>/delete', methods=['DELETE'])
def delete_publication(id):
    id=id
    publicacion=publication.query.filter_by(id=id).first()
    result_data = []

    if publicacion:
        like_publicaciones = likes.query.filter_by(publication_id=id).all()
        for like_publicacion in like_publicaciones:
            db.session.delete(like_publicacion)

        notificaciones = notification.query.filter_by(publicacion_id=id).all()
        for notificacion in notificaciones:
            db.session.delete(notificacion)

        db.session.delete(publicacion)
        db.session.commit()

       
        img_data_base64 = b64encode(publicacion.imagen).decode('utf-8')

        result_data.append({
            'id' : publicacion.id,
            'contenido' : publicacion.contenido,
            'imagen' : img_data_base64,
            'fecha_creacion' : publicacion.fecha_creacion,
            'user_id' : publicacion.user_id,
            'likes' : publicacion.likes
        })

        return jsonify(result_data)
    
    else:
        return jsonify({'error':'No se econtró la publicación.'}), 400
    

#Ocultar publicaciones
@app.route('/publications/hidden', methods=['POST'])
def hidden_publications():
    id = request.json['id']
    user = request.json['user']

    usuario = users.query.filter_by(user=user).first()

    if usuario:
        publicacion_oculta = hiddenPublication(publication_id=id, user=user)
        db.session.add(publicacion_oculta)
        db.session.commit()
        
        resultado = hiddenPublication_schema.dump(publicacion_oculta)
        return jsonify(resultado)

    else:
        return jsonify({'message': 'Usuario no encontrado.'}), 404
        

#Obtener publicaciones ocultas
@app.route('/publication/hidden/<user>')
def get_hidden_publication(user):
    resultado_publicaciones = []
    publicaciones_filtradas = []
    publicaciones_ocultas = hiddenPublication.query.filter_by(user=user).all()

    if publicaciones_ocultas:
        for publicacion in publicaciones_ocultas:
            publicaciones = publication.query.filter_by(id=publicacion.publication_id).all()
            publicaciones_filtradas.extend(publicaciones)

        if publicaciones_filtradas:
            for publicacion in publicaciones_filtradas:
                perfil_user = profile.query.filter_by(user=publicacion.user_id).first()
                image_perfil_base64 = b64encode(perfil_user.img_perfil).decode('utf-8')

                if(publicacion.imagen != None):
                    image_publicacion_base64 = b64encode(publicacion.imagen).decode('utf-8')
                else:
                    image_publicacion_base64 = None

                resultado_publicaciones.append({
                    'contenido': publicacion.contenido,
                    'fecha_creacion': publicacion.fecha_creacion,
                    'id': publicacion.id,
                    'imagen': image_publicacion_base64,
                    'likes': publicacion.likes,
                    'user_id': publicacion.user_id,
                    'img_perfil': image_perfil_base64
                })

            
            return jsonify(resultado_publicaciones)
    
    else:
        return jsonify({'message':'No se encontraron publicaciones ocultas.'})
    

#Eliminar publicaciones ocultas
@app.route('/publication/hidden/delete',methods=['DELETE'])
def delete_publication_hidden():
    id = request.json['id']
    user = request.json['user']

    publicacion = hiddenPublication.query.filter(and_(hiddenPublication.publication_id==id, hiddenPublication.user==user)).first()
    db.session.delete(publicacion)
    db.session.commit()

    resultado = hiddenPublication_schema.dump(publicacion)
    return jsonify(resultado)

#----------------------------------------SOPORTE-----------------------------------
#Enviar mail del Reporte
@app.route('/report',methods=['POST'])
def handle_send_report():
    data = request.json
    response, status_code = send_report(data)
    return jsonify(response), status_code


#----------------------------------------NOTIFICACIONES-----------------------------------
#Obtener todas las notificaciones
@app.route('/notifications/<user>')
def get_notifications(user):
    notificaciones_user=notification.query.filter_by(user_receptor=user).all()
    info_notificaciones = []

    for notificacion in notificaciones_user:
        perfil_usuario = profile.query.filter_by(user = notificacion.user_emisor).first()
        img_perfil_base64 = b64encode(perfil_usuario.img_perfil).decode('utf-8')

        info_notificaciones.append({
            'contenido' : notificacion.contenido,
            'fecha_notificacion' : notificacion.fecha_notificacion,
            'id' : notificacion.id,
            'publicacion_id' : notificacion.publicacion_id,
            'tipo' : notificacion.tipo,
            'user_emisor' : notificacion.user_emisor,
            'user_receptor' : notificacion.user_receptor,
            'img_perfil' : img_perfil_base64
        })

    return jsonify(info_notificaciones)

#----------------------------------------SEGUIMIENTO-----------------------------------
#Nuevo seguimiento y actualización de seguidos/seguidores de cada usuario 
@app.route('/follow', methods=['POST','DELETE'])
def new_follow():
    follower_user = request.json['follower_user']
    followed_user = request.json['followed_user']

    if request.method == 'POST':
        if follower_user and followed_user:
            seguimiento = followUp(follower_user=follower_user, followed_user=followed_user)
            db.session.add(seguimiento)

            #Actualiza los seguidores y seguidos de los usuarios
            seguidor=users.query.filter_by(user=follower_user).first()
            seguido=users.query.filter_by(user=followed_user).first()
            seguidor.follows += 1
            seguido.followers += 1

            #Verifica si ya existe la notificación de seguimiento 
            notificacion_seguimiento=notification.query.filter_by(user_emisor=follower_user, user_receptor=followed_user).first()
            if notificacion_seguimiento:
                db.session.commit()

            else:
                #Genera nueva notificación de seguimiento
                contenido='te ha comenzado a seguir'
                tipo='follow'
                publicacion_id=None
                user_receptor=followed_user
                user_emisor=follower_user

                notificacion=notification(user_emisor=user_emisor, tipo=tipo, contenido=contenido, publicacion_id=publicacion_id, user_receptor=user_receptor)
                db.session.add(notificacion)

                db.session.commit()

            return get_follows_user(follower_user), 200

        else:
            return jsonify({'error':'No se recibio los datos requeridos para la solicitud.'}), 400
        
    elif request.method == 'DELETE':
        seguimiento = followUp.query.filter_by(follower_user=follower_user, followed_user=followed_user).first()

        if seguimiento:
            db.session.delete(seguimiento)

            #Actualiza los seguidores y seguidos de los usuarios
            seguidor=users.query.filter_by(user=follower_user).first()
            seguido=users.query.filter_by(user=followed_user).first()
            seguidor.follows -= 1
            seguido.followers -=1

            db.session.commit()

            return get_follows_user(follower_user), 200
        
        else:
            return jsonify({'error':'No se recibio los datos requeridos para la solicitud.'}), 400
        
        

#Obtener todos los seguimientos hechos por el usuario recibido por parametro y sus respectivas img de perfil
@app.route('/follow/<user>')
def get_follows_user(user):
    follows_user = followUp.query.filter_by(follower_user=user).all()

    usuarios = []

    for seguimiento in follows_user:
        usuario_seguido = seguimiento.followed_user
        perfil_usuario_seguido = profile.query.filter_by(user=usuario_seguido).first()

        img_perfil_base64 = b64encode(perfil_usuario_seguido.img_perfil).decode('utf-8')

        usuarios.append({
            'fecha_seguimiento' : seguimiento.fecha_seguimiento,
            'followed_user' : seguimiento.followed_user,
            'follower_user' : seguimiento.follower_user,
            'id' : seguimiento.id,
            'img_perfil' : img_perfil_base64
        })

    all_follows = followUp.query.all()
    todos_seguimientos = followsUp_schema.dump(all_follows)
    return jsonify({'user':usuarios, 'all':todos_seguimientos})

#----------------------------------------MENSAJES-----------------------------------
# Obtener la conversación o guardar nuevos mensajes 
@app.route('/message/<user>/<receptor>', methods=['POST','GET'])
def new_message(user,receptor):
    emisor = user
    receptor = receptor

    if request.method == 'POST':
        contenido = request.json['contenido']

        # Verifica si ya existe una conversación entre los usuarios
        check_conversacion_existente = message.query.filter(and_(message.sender_user==emisor,message.recipient_user==receptor)).first()
        second_check_conversacion_existente = message.query.filter(and_(message.sender_user==receptor,message.recipient_user==emisor)).first()
        
        # Crea un nuevo mensaje con la conversación existente o una nueva con un identificador único
        if check_conversacion_existente:
            new_message = message(sender_user=emisor,recipient_user=receptor,contenido=contenido,conversacion_id=check_conversacion_existente.conversacion_id)
        elif second_check_conversacion_existente:
            new_message = message(sender_user=emisor,recipient_user=receptor,contenido=contenido,conversacion_id=second_check_conversacion_existente.conversacion_id)
        else:
            nuevo_uuid = str(uuid.uuid4())
            conversacion_id = nuevo_uuid

            new_message = message(sender_user=emisor,recipient_user=receptor,contenido=contenido,conversacion_id=conversacion_id)
            
        db.session.add(new_message)
        db.session.commit()

        # Obtiene todos los mensajes en la conversación
        chat = message.query.filter_by(sender_user=emisor,recipient_user=receptor).all()
        resultado = messages_schema.dump(chat)

        return jsonify(resultado)
    
    else:
        # Verifica si ya existe una conversación entre los usuarios
        conversacion = message.query.filter(and_(message.sender_user==emisor, message.recipient_user==receptor)).first()
        if conversacion:
            all_conversacion = message.query.filter_by(conversacion_id=conversacion.conversacion_id).all()
        else:
            conversacion = message.query.filter(and_(message.sender_user==receptor, message.recipient_user==emisor)).first()
            if conversacion:
                all_conversacion = message.query.filter_by(conversacion_id=conversacion.conversacion_id).all()
            else:
                return jsonify({'id':0, 'emisor':emisor, 'receptor':receptor})

        resultado = messages_schema.dump(all_conversacion)
        return jsonify({'chats':resultado,'emisor':emisor,'receptor':receptor})


# Obtener los ultimos mensajes de cada conversación
@app.route('/message/<user>')
def get_latest_messages(user):
    # Se crea una subconsulta (subquery) que busca las conversaciones más recientes para el usuario dado. 
    subquery = db.session.query(
        # Busca el ID de la conversación y la fecha del mensaje más reciente para el usuario. 
        message.conversacion_id,
        func.max(message.fecha_envio).label("latest_date")
    ).filter(
        or_(message.sender_user == user, message.recipient_user == user)
    ).group_by(message.conversacion_id).subquery()

    # Consulta para obtener los mensajes más recientes
    latest_messages = db.session.query(message, subquery.c.latest_date).join(
        subquery,
        and_(
            message.conversacion_id == subquery.c.conversacion_id,
            message.fecha_envio == subquery.c.latest_date
        )
    ).all()

    # Lista para almacenar información sobre las conversaciones más recientes
    chats = []
    # Itera sobre los mensajes más recientes y recopila información relevante
    for chat in latest_messages:
        sender_user = get_user(chat.message.sender_user)
        recipient_user = get_user(chat.message.recipient_user)
        # Consulta para obtener la img de perfil del usuario
        recipient_user_name = recipient_user['user']
        recipient_profile = profile.query.filter_by(user=recipient_user_name).first()
        
        img_perfil_base64 = b64encode(recipient_profile.img_perfil).decode('utf-8')
        
        chats.append({
            "sender_user": sender_user,
            "recipient_user": recipient_user,
            "latest_message_id": chat.message.id,
            "latest_message_content": chat.message.contenido,
            "latest_message_date": chat.message.fecha_envio.strftime('%Y-%m-%d %H:%M:%S'),
            "img_perfil":img_perfil_base64
        })
    
    return jsonify(chats)


#----------------------------------------BUSCADOR-----------------------------------
# Obtiene la union de datos de dos tablas (users y profile), solo aquellas que su user sean iguales
@app.route('/search_users')
def get_info_users():
    users_with_profile = []

    # Realizar una consulta que une ambas tablas solo cuando los valores de 'user' sean iguales
    query_result = db.session.query(users.user, users.nombre, users.follows, users.followers, profile.img_perfil).join(
        profile, users.user == profile.user).all()

    for user, nombre, follows, followers, img_perfil in query_result:

        img_perfil_base64 = b64encode(img_perfil).decode('utf-8')

        user_data = {
            'user': user,
            'nombre': nombre,
            'follows': follows,
            'followers': followers,
            'img': img_perfil_base64,
        }

        users_with_profile.append(user_data)

    return jsonify({'users_with_profile': users_with_profile})

if __name__=='__main__':
    app.run(debug=True, port=5000)
