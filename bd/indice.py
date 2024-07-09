import couchdb

# Conectar a CouchDB
couch = couchdb.Server('http://admin:admin@localhost:5984')  # Cambia la URL según tu configuración de CouchDB
db = couch['bd2']  # Asegúrate de usar el nombre correcto de tu base de datos

# Definir el índice
index_definition = {
    "index": {
        "fields": [
            {"grades.0.score": "asc"}  # Cambia "asc" a "desc" si prefieres el orden descendente
        ]
    },
    "name": "grades_score_index",
    "type": "json"
}

# Crear el índice
db.index(index_definition)