from flask import Flask, request, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

app = Flask(__name__)

#CONFIGURACION DE CREDENCIALES DE LA BBDD SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///torneos.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CONFIGURACION DE LAS CREDENCIALES DE FLASK MAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'jovellanos.rumble@gmail.com'
app.config['MAIL_PASSWORD'] = 'mxca apkp atet xjde'
app.config['MAIL_DEFAULT_SENDER'] = 'jovellanos.rumble@gmail.com'
mail = Mail(app)


#RUTAS RELATIVAS DE LOS FICHEROS DE LA APLICACION
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/requisitos')
def requisitos():
    return render_template('01-JovellanosRumbleRequisitos.html')

@app.route('/capturas')
def capturas():
    return render_template('02-JovellanosRumbleCapturas.html')

@app.route('/gameplay')
def gameplay():
    return render_template('03-JovellanosRumbleGameplay.html')

@app.route('/torneos')
def torneos():
    return render_template('04-JovellanosRumbleTorneos.html')

@app.route('/controles')
def controles():
    return render_template('06-JovellanosRumbleControles.html')

@app.route('/faq')
def faq():
    return render_template('07-JovellanosRumbleFAQ.html')

@app.route('/privacidad')
def privacidad():
    return render_template('08-JovellanosRumblePrivacidad.html')

@app.route('/creditos')
def creditos():
    return render_template('09-JovellanosRumbleCreditos.html')

@app.route('/jugadores_inscritos')
def jugadores_inscritos():
    return render_template('13-JovellanosRumbleJugadoresInscritos.html')


#TABLEMODEL DE CADA TORNEO
class TorneoMadrid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    dni = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class TorneoGothamCity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    dni = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class TorneoHillValley(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    dni = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)



#ESTOS METODOS SON PARA GUARDAR LOS DATOS DEL FORMULARIO QUE RELLENAMOS CON LOS DATOS DEL USER Y DEL TORNEO EN EL FICHERO .SQLITE
@app.route('/guardar_datos_Madrid', methods=['POST'])
def guardar_datos_Madrid():
    datos = request.form
    print(datos)
    nuevo_participante = TorneoMadrid(
        nombre=datos['nombre'],
        apellidos=datos['apellidos'],
        edad=int(datos['edad']),
        telefono=datos['telefono'],
        dni=datos['dni'],
        email=datos['email']
    )
    db.session.add(nuevo_participante)
    db.session.commit()

    enviar_correo(
        datos['nombre'],
        datos['apellidos'],
        int(datos['edad']),
        datos['telefono'],
        datos['dni'],
        datos['email'],
        "Madrid",
        "23-11-2023 18:00h en Parque del Retiro")
    
    return render_template('10-JovellanosRumbleTorneoMadrid.html')


@app.route('/guardar_datos_GothamCity', methods=['POST'])
def guardar_datos_GothamCity():
    datos = request.form
    print(datos)
    nuevo_participante = TorneoGothamCity(
        nombre=datos['nombre'],
        apellidos=datos['apellidos'],
        edad=int(datos['edad']),
        telefono=datos['telefono'],
        dni=datos['dni'],
        email=datos['email']
    )
    db.session.add(nuevo_participante)
    db.session.commit()

    enviar_correo(
        datos['nombre'],
        datos['apellidos'],
        int(datos['edad']),
        datos['telefono'],
        datos['dni'],
        datos['email'],
        "Gotham City",
        "2-3-2024 18:00h en el Asilo de Arkham")

    return render_template('11-JovellanosRumbleTorneoGothamCity.html')


@app.route('/guardar_datos_HillValley', methods=['POST'])
def guardar_datos_HillValley():
    datos = request.form
    print(datos)
    nuevo_participante = TorneoHillValley(
        nombre=datos['nombre'],
        apellidos=datos['apellidos'],
        edad=int(datos['edad']),
        telefono=datos['telefono'],
        dni=datos['dni'],
        email=datos['email']
    )
    db.session.add(nuevo_participante)
    db.session.commit()

    enviar_correo(
        datos['nombre'],
        datos['apellidos'],
        int(datos['edad']),
        datos['telefono'],
        datos['dni'],
        datos['email'],
        "Hill Valley",
        "2-12-2023 18:00h en La Plaza del Reloj")

    return render_template('12-JovellanosRumbleTorneoHillValley.html')


#ESTE METODO LO UTILIZO PARA RECUPERAR TODOS LOS REGISTROS DE CADA TABLA DEL SQLITE Y MANDARLOS A LA TABLA HTML QUE LOS MOSTRARÁ
@app.route('/mostrar_datos_Torneos', methods=['GET'])
def mostrar_datos_Torneos():
    #Consulta para obtener todos los participantes de todos los torneos, los retornamos en el render template para recogerla en el HTML de jugadores inscritos en torneos.
    participantesDeMadrid = TorneoMadrid.query.all()
    participantesDeGothamCity = TorneoGothamCity.query.all()
    participantesDeHillValley = TorneoHillValley.query.all()

    return render_template('13-JovellanosRumbleJugadoresInscritos.html', participantesMadrid=participantesDeMadrid, participantesGothamCity=participantesDeGothamCity, participantesHillValley=participantesDeHillValley)


def enviar_correo(nombre, apellidos, edad, telefono, dni, email, ciudad, fechaYHora):
    # Configura el mensaje de correo
    mensaje = Message(f'Inscripcion Jovellanos Rumble (Torneo {ciudad})', recipients=[email])

    #MENSAJE QUE ENVIAMOS CON ESTRUCTURA HTML PARA PODER CARGAR IMAGENES
    cuerpo_html = f'''
    <p>Buenos días, {nombre} {apellidos}, te has inscrito correctamente en el torneo de {ciudad}.</p>
    <p>Detalles del Usuario Registrado:</p>
    <ul>
        <li><u><b>Nombre y Apellidos:</b></u> {nombre} {apellidos}</li>
        <li><u><b>Edad: </b></u>{edad}</li>
        <li><u><b>Teléfono: </b></u>{telefono}</li>
        <li><u><b>DNI: </b></u>{dni}</li>
        <li><u><b>Ubicacion del Torneo: </b></u>{ciudad}</li>
        <li><u><b>Fecha y Hora: </b></u>{fechaYHora}</li>
    </ul>

    '''

    # Agrega el cuerpo HTML al mensaje
    mensaje.html = cuerpo_html

    # Ruta a la imagen del logotipo
    ruta_imagen = 'static/images/tituloIndexHeader.jpg'
    # Envía el correo electrónico con la imagen adjunta
    with app.open_resource(ruta_imagen) as imagen:
        mensaje.attach(filename='tituloIndexHeader.jpg', content_type='image/jpeg', data=imagen.read(), disposition='inline')
        print('Correo enviado exitosamente')

    try:

        mail.send(mensaje)
        print('Correo enviado exitosamente')
    except Exception as e:
        print(f'Error al enviar el correo: {e}')


@app.route('/descargar', methods=['GET'])
def descargar_archivo():
    # Obtén la ruta absoluta del directorio actual al archivo
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_path = os.path.join(directorio_actual, 'JovellanosRumble.exe')

    # Verifica si el archivo existe
    if os.path.exists(archivo_path):
        return send_file(archivo_path, as_attachment=True)
    else:
        return "Archivo no encontrado", 404


@app.route('/descargar/<video_name>', methods=['GET'])
def descargar_video(video_name):
    # Obtén la ruta absoluta del directorio actual al archivo
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_path = os.path.join(directorio_actual, f'static/videos/{video_name}.mp4')

    # Verifica si el archivo existe
    if os.path.exists(archivo_path):
        return send_file(archivo_path, as_attachment=True)
    else:
        return "Video no encontrado", 404



if __name__ == '__main__':
    with app.app_context():
        # Crear la base de datos y las tablas
        db.create_all()

    # Ejecutar la aplicación Flask
    app.run(debug=True)
