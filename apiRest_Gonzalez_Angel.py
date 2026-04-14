from flask import Flask, jsonify, request

app = Flask(__name__)

# Diccionario de alumnos y profesores
db = {
    "alumnos": {},
    "profesores": {}
}

# Estructura para las validaciones
def validar_campos(datos, campos_esperados):
    for campo, tipo in campos_esperados.items():

        if campo not in datos or str(datos[campo]).strip() == "":
            return False, f"El campo {campo} es obligatorio y no puede estar vacío."
        
        if not isinstance(datos[campo], tipo):
            return False, f"El campo {campo} debe ser de tipo {tipo}."
    return True, None

# Campos de las entidades
campos_alumno = {
    "nombres": str,
    "apellidos": str,
    "matricula": str,
    "promedio": (int, float)
}

campos_profesor = {
    "numeroEmpleado": (int, float),
    "nombres": str,
    "apellidos": str,
    "horasClase": (int, float)
}

# Lógica de los alumnos

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    return jsonify(list(db["alumnos"].values())), 200

@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    alumno = db["alumnos"].get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify(alumno), 200

@app.route('/alumnos', methods=['POST'])
def post_alumno():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400
            
        es_valido, mensaje = validar_campos(data, campos_alumno)
        if not es_valido:
            # Cambiado de 500 a 400 porque es error del cliente
            return jsonify({"error": mensaje}), 400 
        
        nuevo_id = max(db["alumnos"].keys() or [0]) + 1
        nuevo_alumno = {"id": nuevo_id, **data}
        db["alumnos"][nuevo_id] = nuevo_alumno
        return jsonify(nuevo_alumno), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/alumnos/<int:id>', methods=['PUT'])
def put_alumno(id):
    if id not in db["alumnos"]:
        return jsonify({"error": "No encontrado"}), 404
    
    data = request.get_json()
    es_valido, mensaje = validar_campos(data, campos_alumno)
    if not es_valido:
        return jsonify({"error": mensaje}), 500
        
    db["alumnos"][id] = {"id": id, **data}
    return jsonify(db["alumnos"][id]), 200

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    if id in db["alumnos"]:
        del db["alumnos"][id]
        return jsonify({"res": "Eliminado"}), 200
    return jsonify({"error": "No encontrado"}), 404

# Lógica de los profesores

@app.route('/profesores', methods=['GET'])
def get_profesores():
    return jsonify(list(db["profesores"].values())), 200

@app.route('/profesores/<int:id>', methods=['GET'])
def get_profesor(id):
    profesor = db["profesores"].get(id)
    if not profesor:
        return jsonify({"error": "Profesor no encontrado"}), 404
    return jsonify(profesor), 200

@app.route('/profesores', methods=['POST'])
def post_profesor():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400

        es_valido, mensaje = validar_campos(data, campos_profesor)
        if not es_valido:

            return jsonify({"error": mensaje}), 400
        
        nuevo_id = max(db["profesores"].keys() or [0]) + 1
        nuevo_profesor = {"id": nuevo_id, **data}
        db["profesores"][nuevo_id] = nuevo_profesor
        return jsonify(nuevo_profesor), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/profesores/<int:id>', methods=['PUT'])
def put_profesor(id):
    if id not in db["profesores"]:
        return jsonify({"error": "No encontrado"}), 404
    
    data = request.get_json()
    es_valido, mensaje = validar_campos(data, campos_profesor)
    if not es_valido:
        return jsonify({"error": mensaje}), 500
        
    db["profesores"][id] = {"id": id, **data}
    return jsonify(db["profesores"][id]), 200

@app.route('/profesores/<int:id>', methods=['DELETE'])
def delete_profesor(id):
    if id in db["profesores"]:
        del db["profesores"][id]
        return jsonify({"res": "Eliminado"}), 200
    return jsonify({"error": "No encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)