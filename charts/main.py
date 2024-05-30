import requests
import matplotlib.pyplot as plt

# Obtener datos para gráfica de estado de asuntos
response = requests.get('http://localhost:5000/grafica/estado_asuntos')
data = response.json()

# Preparar datos para la gráfica
labels = [item['_id'] for item in data]
sizes = [item['count'] for item in data]

# Crear gráfica de pastel
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Distribución de Estados de Asuntos')
plt.show()

# Obtener datos para gráfica de asuntos por gabinete
response = requests.get('http://localhost:5000/grafica/asuntos_por_gabinete')
data = response.json()

# Preparar datos para la gráfica
labels = [item['_id'] for item in data]
sizes = [item['count'] for item in data]

# Crear gráfica de barras
plt.bar(labels, sizes)
plt.xlabel('Gabinete')
plt.ylabel('Cantidad de Asuntos')
plt.title('Cantidad de Asuntos por Gabinete')
plt.show()
