import os
import matplotlib.pyplot as plt
import mysql.connector

# Crear el directorio si no existe
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Directorio donde se guardarán las gráficas
graph_dir = 'static/graficas'
ensure_directory_exists(graph_dir)

# Conectar a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="encuestaa"
)

cursor = db.cursor()

# Consultar los datos para cada gráfico
cursor.execute("SELECT experiencia_general, COUNT(*) FROM encuesta GROUP BY experiencia_general")
experiencia_data = cursor.fetchall()

cursor.execute("SELECT satisfaccion_atencion, COUNT(*) FROM encuesta GROUP BY satisfaccion_atencion")
satisfaccion_data = cursor.fetchall()

cursor.execute("SELECT calidad_precio, COUNT(*) FROM encuesta GROUP BY calidad_precio")
calidad_precio_data = cursor.fetchall()

cursor.execute("SELECT recomendacion, COUNT(*) FROM encuesta GROUP BY recomendacion")
recomendacion_data = cursor.fetchall()

# Extraer los datos para cada gráfico
def extract_data(data):
    labels, values = zip(*data) if data else ([], [])
    return labels, values

# Crear la gráfica de experiencia general
def plot_experiencia_general(labels, values):
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.xlabel('Experiencia General', fontsize=12)
    plt.ylabel('Cantidad de Respuestas', fontsize=12)
    plt.title('Distribución de la Experiencia General', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'experiencia_general.png'), bbox_inches='tight')
    plt.close()

# Crear la gráfica de satisfacción con la atención
def plot_satisfaccion_atencion(labels, values):
    plt.figure(figsize=(10, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3'])
    plt.title('Satisfacción con la Atención', fontsize=14)
    plt.savefig(os.path.join(graph_dir, 'satisfaccion_atencion.png'), bbox_inches='tight')
    plt.close()

# Crear la gráfica de relación calidad-precio
def plot_calidad_precio(labels, values):
    plt.figure(figsize=(10, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['#1b9e77', '#d95f02', '#7570b3', '#e7298a'])
    plt.title('Relación Calidad-Precio', fontsize=14)
    plt.savefig(os.path.join(graph_dir, 'calidad_precio.png'), bbox_inches='tight')
    plt.close()

# Crear la gráfica de recomendación
def plot_recomendacion(labels, values):
    plt.figure(figsize=(10, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3'])
    plt.title('Recomendación del Producto', fontsize=14)
    plt.savefig(os.path.join(graph_dir, 'recomendacion.png'), bbox_inches='tight')
    plt.close()

# Extraer datos y crear gráficos
experiencia_labels, experiencia_values = extract_data(experiencia_data)
plot_experiencia_general(experiencia_labels, experiencia_values)

satisfaccion_labels, satisfaccion_values = extract_data(satisfaccion_data)
plot_satisfaccion_atencion(satisfaccion_labels, satisfaccion_values)

calidad_precio_labels, calidad_precio_values = extract_data(calidad_precio_data)
plot_calidad_precio(calidad_precio_labels, calidad_precio_values)

recomendacion_labels, recomendacion_values = extract_data(recomendacion_data)
plot_recomendacion(recomendacion_labels, recomendacion_values)

# Cerrar la conexión
cursor.close()
db.close()
