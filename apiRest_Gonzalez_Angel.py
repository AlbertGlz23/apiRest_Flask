from flask import Flask, jsonify, request

app = Flask(__name__)

#Diccionario usado como BD

db = {
    "alumnos": {},
    "profesores": {}
}

#Función de apoyo para la validación de campos

def validar_campos(datos, campos_esperados, entidad):
    if not datos:
        return False, "No se enviaron datos"
    
    for campo, tipo in campos_esperados.items():
        if campo not in datos or datos[campo] is None or datos[campo] == "":
            return False, f"El campo {campo} es obligatorio"
        
        if not isinstance(datos[campo], tipo):
            return False, f"El campo {campo} debe ser de tipo {tipo}"
            
    if entidad == "alumno" and datos.get('promedio', 0) < 0:
        return False, "El promedio no puede ser negativo"
    
    if entidad == "profesor" and datos.get('horasClase', 0) < 0:
        return False, "Las horas no pueden ser negativas"
        
    return True, None

#Definición de los atributos de alumnos y profesores

campos_alumno = {
    "nombres": str,
    "apellidos": str,
    "matricula": str,
    "promedio": (int, float)
}

campos_profesor = {
    "numeroEmpleado": int,
    "nombres": str,
    "apellidos": str,
    "horasClase": int
}

#Lógica de la API para los alumnos.

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
    data = request.get_json()
    es_valido, mensaje = validar_campos(data, campos_alumno, "alumno")
    if not es_valido:
        return jsonify({"error": mensaje}), 400
        
    nuevo_id = data.get('id', max(db["alumnos"].keys() or [0]) + 1)
    nuevo_alumno = {
        "id": nuevo_id,
        "nombres": data['nombres'],
        "apellidos": data['apellidos'],
        "matricula": data['matricula'],
        "promedio": data['promedio']
    }
    db["alumnos"][nuevo_id] = nuevo_alumno
    return jsonify(nuevo_alumno), 201

@app.route('/alumnos/<int:id>', methods=['PUT'])
def put_alumno(id):
    if id not in db["alumnos"]:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    data = request.get_json()
    es_valido, mensaje = validar_campos(data, campos_alumno, "alumno")
    if not es_valido:
        return jsonify({"error": mensaje}), 400
        
    db["alumnos"][id].update({
        "nombres": data['nombres'],
        "apellidos": data['apellidos'],
        "matricula": data['matricula'],
        "promedio": data['promedio']
    })
    return jsonify(db["alumnos"][id]), 200

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    if id in db["alumnos"]:
        del db["alumnos"][id]
        return jsonify({"mensaje": "Alumno eliminado"}), 200
    return jsonify({"error": "Alumno no encontrado"}), 404

#Lógica de la API para los profesores

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
    data = request.get_json()
    es_valido, mensaje = validar_campos(data, campos_profesor, "profesor")
    if not es_valido:
        return jsonify({"error": mensaje}), 400
        
    nuevo_id = data.get('id', max(db["profesores"].keys() or [0]) + 1)
    nuevo_profesor = {
        "id": nuevo_id,
        "numeroEmpleado": data['numeroEmpleado'],
        "nombres": data['nombres'],
        "apellidos": data['apellidos'],
        "horasClase": data['horasClase']
    }
    db["profesores"][nuevo_id] = nuevo_profesor
    return jsonify(nuevo_profesor), 201

@app.route('/profesores/<int:id>', methods=['PUT'])
def put_profesor(id):
    if id not in db["profesores"]:
        return jsonify({"error": "Profesor no encontrado"}), 404
    
    data = request.get_json()
    es_valido, mensaje = validar_campos(data, campos_profesor, "profesor")
    if not es_valido:
        return jsonify({"error": mensaje}), 400
        
    db["profesores"][id].update({
        "numeroEmpleado": data['numeroEmpleado'],
        "nombres": data['nombres'],
        "apellidos": data['apellidos'],
        "horasClase": data['horasClase']
    })
    return jsonify(db["profesores"][id]), 200

@app.route('/profesores/<int:id>', methods=['DELETE'])
def delete_profesor(id):
    if id in db["profesores"]:
        del db["profesores"][id]
        return jsonify({"mensaje": "Profesor eliminado"}), 200
    return jsonify({"error": "Profesor no encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)