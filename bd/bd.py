import couchdb
import json

# Conexión a la base de datos CouchDB (asegúrate de tener CouchDB ejecutándose localmente o ajusta la URL según tu configuración)
couch = couchdb.Server('http://admin:admin@localhost:5984')  # Cambia localhost y el puerto según tu configuración
db_name = 'bd2'  # Nombre de la base de datos que quieres utilizar
db = couch[db_name]

# Ruta al archivo JSON que contiene los datos
json_file = 'C:\\Users\\USER\\Desktop\\Uni\\BD2-Proyect\\bd\\tu_archivo_transformado.json'  # Cambia esto a la ruta de tu archivo JSON

# Función para cargar los datos del archivo JSON a CouchDB
def import_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for doc in data:
            # Guardar el documento en la base de datos CouchDB
            db.save(doc)

# Llamar a la función para importar los datos
import_data_from_json(json_file)

print(f'Datos importados exitosamente a la base de datos {db_name}.')