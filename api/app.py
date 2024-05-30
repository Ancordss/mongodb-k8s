from flask import Flask, request, jsonify, render_template
from bson import ObjectId
from models import db, Cliente, Abogado, Procurador, Audiencia, Asunto
from datetime import datetime
import random
from faker import Faker

app = Flask(__name__)
fake = Faker()

# Helper function to convert ObjectId to string
def convert_object_id(document):
    if isinstance(document, list):
        return [convert_object_id(doc) for doc in document]
    if isinstance(document, dict):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in document.items()}
    return document

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.json
    cliente = Cliente(**data)
    db.clientes.insert_one(cliente.to_dict())
    return jsonify(convert_object_id(cliente.to_dict())), 201

@app.route('/clientes/<dni>', methods=['GET'])
def get_cliente(dni):
    cliente = db.clientes.find_one({'dni': dni})
    if cliente:
        return jsonify(convert_object_id(cliente))
    else:
        return jsonify({'error': 'Cliente no encontrado'}), 404

@app.route('/clientes/<dni>', methods=['PUT'])
def update_cliente(dni):
    data = request.json
    result = db.clientes.update_one({'dni': dni}, {'$set': data})
    if result.matched_count:
        return jsonify({'msg': 'Cliente actualizado'}), 200
    else:
        return jsonify({'error': 'Cliente no encontrado'}), 404

@app.route('/clientes/<dni>', methods=['DELETE'])
def delete_cliente(dni):
    result = db.clientes.delete_one({'dni': dni})
    if result.deleted_count:
        return jsonify({'msg': 'Cliente eliminado'}), 200
    else:
        return jsonify({'error': 'Cliente no encontrado'}), 404

@app.route('/asuntos', methods=['POST'])
def create_asunto():
    data = request.json
    cliente_data = data.pop('cliente')
    cliente_data.pop('_id', None)  # Elimina el campo '_id' si está presente
    cliente = Cliente(**cliente_data)
    data['cliente'] = cliente
    
    procuradores_data = data.pop('procuradores')
    procuradores = [Procurador(**proc) for proc in procuradores_data]
    data['procuradores'] = procuradores
    
    audiencias_data = data.pop('audiencias')
    audiencia_ids = []
    for aud in audiencias_data:
        audiencia = Audiencia(
            fecha=datetime.strptime(aud['fecha'], '%Y-%m-%d'),
            abogado=Abogado(**aud['abogado']),
            incidencias=aud['incidencias']
        )
        result = db.audiencias.insert_one(audiencia.to_dict())
        audiencia_ids.append(result.inserted_id)
    data['audiencias'] = audiencia_ids

    fecha_finalizacion = data.get('fecha_finalizacion')
    if fecha_finalizacion:
        fecha_finalizacion = datetime.strptime(fecha_finalizacion, '%Y-%m-%d')

    asunto = Asunto(
        numero_expediente=data['numero_expediente'],
        cliente=cliente,
        fecha_inicio=datetime.strptime(data['fecha_inicio'], '%Y-%m-%d'),
        estado=data['estado'],
        procuradores=procuradores,
        audiencias=audiencia_ids,
        fecha_finalizacion=fecha_finalizacion
    )
    
    db.asuntos.insert_one(asunto.to_dict())
    return jsonify(convert_object_id(asunto.to_dict())), 201

@app.route('/asuntos/<numero_expediente>', methods=['GET'])
def get_asunto(numero_expediente):
    asunto = db.asuntos.find_one({'numero_expediente': numero_expediente})
    if asunto:
        return jsonify(convert_object_id(asunto))
    else:
        return jsonify({'error': 'Asunto no encontrado'}), 404

@app.route('/asuntos/<numero_expediente>', methods=['PUT'])
def update_asunto(numero_expediente):
    data = request.json
    result = db.asuntos.update_one({'numero_expediente': numero_expediente}, {'$set': data})
    if result.matched_count:
        return jsonify({'msg': 'Asunto actualizado'}), 200
    else:
        return jsonify({'error': 'Asunto no encontrado'}), 404

@app.route('/asuntos/<numero_expediente>', methods=['DELETE'])
def delete_asunto(numero_expediente):
    result = db.asuntos.delete_one({'numero_expediente': numero_expediente})
    if result.deleted_count:
        return jsonify({'msg': 'Asunto eliminado'}), 200
    else:
        return jsonify({'error': 'Asunto no encontrado'}), 404

@app.route('/insert_much_data', methods=['POST'])
def insert_much_data():
    num_records = request.json.get('num_records', 100)
    for _ in range(num_records):
        cliente = Cliente(
            dni=fake.unique.random_number(digits=8),
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            direccion=fake.address(),
            telefono=fake.phone_number(),
            email=fake.email()
        )
        db.clientes.insert_one(cliente.to_dict())

        abogado = Abogado(
            dni=fake.unique.random_number(digits=8),
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            direccion=fake.address(),
            telefono=fake.phone_number(),
            email=fake.email(),
            gabinete=random.choice(['Guatemala', 'México', 'El Salvador'])
        )
        db.abogados.insert_one(abogado.to_dict())

        procurador = Procurador(
            dni=fake.unique.random_number(digits=8),
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            direccion=fake.address(),
            telefono=fake.phone_number(),
            email=fake.email()
        )
        db.procuradores.insert_one(procurador.to_dict())

        audiencia = Audiencia(
            fecha=fake.date_time_this_decade(),
            abogado=abogado,
            incidencias=fake.text()
        )
        result = db.audiencias.insert_one(audiencia.to_dict())
        audiencia_id = result.inserted_id

        asunto = Asunto(
            numero_expediente=fake.unique.random_number(digits=8),
            cliente=cliente,
            fecha_inicio=fake.date_time_this_decade(),
            estado=random.choice(['en trámite', 'archivado', 'finalizado', 'en apelación', 'amparo provisional', 'amparo definitivo', 'cerrado']),
            procuradores=[procurador],
            audiencias=[audiencia_id]
        )
        db.asuntos.insert_one(asunto.to_dict())
    
    return jsonify({'msg': f'{num_records} registros insertados con éxito'}), 201

@app.route('/grafica/estado_asuntos', methods=['GET'])
def grafica_estado_asuntos():
    pipeline = [
        {"$group": {"_id": "$estado", "count": {"$sum": 1}}}
    ]
    resultado = list(db.asuntos.aggregate(pipeline))
    return jsonify(convert_object_id(resultado))

@app.route('/grafica/asuntos_por_gabinete', methods=['GET'])
def grafica_asuntos_por_gabinete():
    pipeline = [
        {"$lookup": {
            "from": "clientes",
            "localField": "cliente.dni",
            "foreignField": "dni",
            "as": "cliente_data"
        }},
        {"$unwind": "$cliente_data"},
        {"$group": {"_id": "$cliente_data.gabinete", "count": {"$sum": 1}}}
    ]
    resultado = list(db.asuntos.aggregate(pipeline))
    return jsonify(convert_object_id(resultado))


@app.route('/grafica/abogados_por_gabinete', methods=['GET'])
def grafica_abogados_por_gabinete():
    pipeline = [
        {"$group": {"_id": "$gabinete", "count": {"$sum": 1}}}
    ]
    resultado = list(db.abogados.aggregate(pipeline))
    return jsonify(convert_object_id(resultado))

if __name__ == '__main__':
    app.run(debug=True)
