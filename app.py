from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import subprocess  # Para ejecutar el script generate_graphs.py

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'encuestaa'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'experiencia_general': request.form['experiencia_general'],
            'satisfaccion_atencion': request.form['satisfaccion_atencion'],
            'calidad_precio': request.form['calidad_precio'],
            'recomendacion': request.form['recomendacion'],
            'comentarios': request.form['comentarios']
        }

        # Verificar si el correo ya existe en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM encuesta WHERE correo = %s", (data['email'],))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            flash('El correo electrónico ya está registrado.', 'error')
            return redirect(url_for('index'))

        # Inserta los datos en la base de datos
        cursor.execute("""
            INSERT INTO encuesta (nombre, correo, experiencia_general, satisfaccion_atencion, calidad_precio, recomendacion, comentarios)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data['name'], data['email'], data['experiencia_general'], data['satisfaccion_atencion'], data['calidad_precio'], data['recomendacion'], data['comentarios']))
        
        mysql.connection.commit()
        cursor.close()

        # Ejecutar el script para generar gráficos
        subprocess.run(['python', 'generate_graphs.py'])

        # Guardar el email en la sesión
        session['email'] = data['email']

        return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    email = session.get('email')  # Obtener el email de la sesión
    return render_template('thank_you.html', email=email)

@app.route('/resultados')
def resultados():
    email = request.args.get('email')  # Obtener el email de la consulta
    if not email:
        return redirect(url_for('index'))  # Redirigir si no se proporciona un email

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT nombre, correo, experiencia_general, satisfaccion_atencion, calidad_precio, recomendacion, comentarios FROM encuesta WHERE correo = %s", (email,))
    user_data = cursor.fetchone()
    cursor.close()

    if not user_data:
        return redirect(url_for('index'))  # Redirigir si no se encuentran datos

    return render_template('resultados.html', user_data=user_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'clave123':  # Cambia esto a tu contraseña
            session['logged_in'] = True
            return redirect(url_for('graficas'))
        else:
            flash('Contraseña incorrecta', 'error')
    return render_template('login.html')

@app.route('/graficas')
def graficas():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Consultar datos para las gráficas
        cursor.execute("SELECT experiencia_general, COUNT(*) AS cantidad FROM encuesta GROUP BY experiencia_general")
        experiencia_data = cursor.fetchall()

        cursor.execute("SELECT satisfaccion_atencion, COUNT(*) AS cantidad FROM encuesta GROUP BY satisfaccion_atencion")
        satisfaccion_data = cursor.fetchall()

        cursor.execute("SELECT calidad_precio, COUNT(*) AS cantidad FROM encuesta GROUP BY calidad_precio")
        calidad_precio_data = cursor.fetchall()

        cursor.execute("SELECT recomendacion, COUNT(*) AS cantidad FROM encuesta GROUP BY recomendacion")
        recomendacion_data = cursor.fetchall()

        cursor.close()
        
        return render_template(
            'graficas.html',
            experiencia_data=experiencia_data,
            satisfaccion_data=satisfaccion_data,
            calidad_precio_data=calidad_precio_data,
            recomendacion_data=recomendacion_data
        )
    except Exception as e:
        print(f"Error: {e}")
        return "Se produjo un error al procesar la solicitud."

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

