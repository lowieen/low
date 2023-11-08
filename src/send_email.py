import smtplib
from flask import url_for
from email.mime.text import MIMEText
import urllib.parse 

def send_report(data):
    usuario = data['user']
    msj = data['message']

    #Establecer conexion al servidor de correos SMTP
    conexion = smtplib.SMTP(host= 'smtp.gmail.com', port= 587)
    conexion.ehlo()

    # Crear el objeto MIMEText para el correo electrónico
    msg = MIMEText(f"Usuario: {usuario}\nMensaje: {msj}")
    msg['Subject'] = 'Mensaje de Reporte'
    msg['From'] = 'testing.lowieen@gmail.com'
    msg['To'] = 'testing.lowieen@gmail.com'

    try: 
        #Encriptacion TLS
        conexion.starttls()
        #Inicio sesión en el servidor SMTP
        conexion.login(user='testing.lowieen@gmail.com', password= 'sxxc yosw qjea wflv')
        #Enviar correo
        conexion.sendmail('testing.lowieen@gmail.com', 'testing.lowieen@gmail.com', msg.as_string())
        #Desconectar el servidor SMTP
        conexion.quit()
        return {'message': 'Correo electrónico enviado exitosamente'}, 200

    except Exception as e:
        print('Error al enviar el correo electrónico:', e)
        return {'error': 'Hubo un error al enviar el correo electrónico'}, 400
    

def send_newPass(email, token):
    conexion = smtplib.SMTP(host= 'smtp.gmail.com', port= 587)
    conexion.ehlo()

    # Codifica el enlace como UTF-8
    encoded_token = urllib.parse.quote(token)

    # Crear el objeto MIMEText para el correo electrónico y especifica la codificación
    # msg_body = f"Utiliza este enlace para restablecer tu contrasena: {url_for('cambiar_contrasena', token=encoded_token, _external=True)}"
    msg_body = f"Utiliza este enlace para restablecer tu contraseña: http://localhost:5173/new-password/{encoded_token}" #Si deseo cambiar la url exacta 
    msg = MIMEText(msg_body.encode('utf-8'), 'plain', 'utf-8')
    msg['Subject'] = 'Restablecer Contraseña'
    msg['From'] = 'testing.lowieen@gmail.com'
    msg['To'] = email

    try: 
        # Encriptación TLS
        conexion.starttls()
        # Inicio sesión en el servidor SMTP
        conexion.login(user='testing.lowieen@gmail.com', password= 'sxxc yosw qjea wflv')
        # Enviar correo
        conexion.sendmail('testing.lowieen@gmail.com', email, msg.as_string())
        # Desconectar el servidor SMTP
        conexion.quit()
        return {'message': 'Correo electrónico enviado exitosamente'}, 200

    except Exception as e:
        print('Error al enviar el correo electrónico:', e)
        return {'message': 'Hubo un error al enviar el correo electrónico'}, 500
