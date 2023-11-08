Documentación del Proyecto "LOW"

Resumen
"LOW" es una web social simplificada desarrollado utilizando Vue.js y Python. Donde cumpliría con funciones escenciales o básicas de cualquier red social como un Inicio de sesión o Registro de usuarios, secciones como :
- Perfil: individual de cada usuario al cual se puede visitar y cambiar foto de perfil y portada. Ver las publicaciones hechas, fotos subidas y likes realizados.
- Mensajes: compuesto por chat y conversaciones realizadas con cada usuario.
- Notificaciones: notificaciones de seguimiento o likes recibidos.
- Configuración: donde puedes modificar tu información personal, ver/deshacer publicaciones ocultadas anteriormente y eliminar cuenta.
- Buscador: se puede buscar cualquier usuario registrado ya sea por su username o nombre o apellido, y poder seguirlo o visitar su perfil.
- Soporte: donde muestra información esencial del sitio.
- Inicio: crear una publicación (con o sin imagen), y ver todas las publicaciones de usuarios seguidos.

- Tecnologías Utilizadas:
● Vue.js
● Python
● Flask
● MySQL
● HTML/CSS
● JavaScript
● SMTP (para envío de correos electrónicos)

- Instalación:
Para instalar y ejecutar el proyecto en tu entorno local, sigue estos pasos:
1. Clona el repositorio desde GitHub: git clone https://github.com/lowieen/low
2. Accede al directorio del proyecto: cd low
3. Crea un entorno virtual de Python: python -m venv low_env
4. Activa el entorno virtual:
    ● En Windows: venv\Scripts\activate
    ● En macOS y Linux: source venv/bin/activate
5. Instala las dependencias de Python: pip install -r requirements.txt
6. Inicia la aplicación: python app.py

- Configuración:
● Base de Datos: Configura la conexión a la base de datos en el archivo app.py.
● Envío de Correos Electrónicos: Configura las credenciales de tu cuenta de correo electrónico Gmail en el archivo send_email.py.

- Funcionalidades:
Registro de Usuarios
● Los usuarios pueden registrarse en la plataforma utilizando su correo electrónico, username y contraseña.

Inicio de Sesión
● Los usuarios registrados pueden iniciar sesión en sus cuentas con el username o email. El username tendra un uso predeterminado para visitar a perfiles de otros usuarios y será por el nombre por el cual se te encuentre en el buscador hasta que agreges datos personales.

Publicaciones
● Se podra likear cualquier publicación como a su vez eliminarlo.
● Visitar el perfil del usuario a través de la misma.
● Ocultar publicaciones ajenas o eliminar las propias.
● Posibilidad de agregar una imagen.

Mensajes
● Poder enviar mensajes a aquellos usuarios que sigas.
● Ver conversaciones hechas y fecha del ultimo mensaje. 

Perfil
● Lugar donde se visualiza todo tipo de información con respecto al usuario, como nombre, ubicación o seguidores.
● Botón de follow/unfollow y mensaje si es que ya existe un seguimiento.
● Publicaciones hechas y likes realizados.
● Imagen de perfil y portada.

Uso
1. Registro de usuario e inicio de sesión.
2. Empezar a buscar y seguir otros usuarios para poder interactuar con ellos.
3. Agregar información personal si es que asi lo desea.
4. Cambiar las fotos del perfil.

Contribuciones:
¡Agradecemos las contribuciones de la comunidad! Si deseas contribuir al proyecto, sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama para tu contribución: git checkout -b mi-contribucion
3. Realiza tus cambios y verifica que todo funcione correctamente.
4. Envía un pull request con tus cambios.

Contacto
Para cualquier pregunta o comentario, contactame alexismunioz4@gmail.com.

Licencia
Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más información.

Agradecimientos
Agradecemos a todos los desarrolladores que contribuyeron a este proyecto y a la comunidad de código abierto por su apoyo.