from flask import Blueprint, request, jsonify
from app.models import db, Profesor

profesores_bp = Blueprint('profesores', __name__)

CAMPOS_VALIDOS = {'numeroEmpleado', 'nombres', 'apellidos', 'horasClase'}
CAMPOS_REQUERIDOS = {'numeroEmpleado', 'nombres', 'apellidos', 'horasClase'}

@profesores_bp.route('', methods=['GET'])
def get_all_profesores():
    profesores = Profesor.query.all()
    return jsonify([p.to_dict() for p in profesores]), 200

@profesores_bp.route('', methods=['POST'])
def create_profesor():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request"}), 400

    for key in data.keys():
        if key not in CAMPOS_VALIDOS:
            return jsonify({"error": "Bad Request"}), 400

    for campo in CAMPOS_REQUERIDOS:
        if campo not in data or data[campo] is None or str(data[campo]).strip() == '':
            return jsonify({"error": "Bad Request"}), 400

    try:
        if int(data['horasClase']) < 0:
            return jsonify({"error": "Bad Request"}), 400
        if int(data['numeroEmpleado']) < 0:
            return jsonify({"error": "Bad Request"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Bad Request"}), 400

    try:
        nuevo = Profesor(**data)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify(nuevo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "detalle": str(e)}), 400

@profesores_bp.route('/<int:id>', methods=['GET'])
def get_profesor(id):
    profesor = Profesor.query.get(id)
    if not profesor:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(profesor.to_dict()), 200

@profesores_bp.route('/<int:id>', methods=['PUT'])
def update_profesor(id):
    profesor = Profesor.query.get(id)
    if not profesor:
        return jsonify({"error": "Not Found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request"}), 400

    for key in data.keys():
        if key not in CAMPOS_VALIDOS:
            return jsonify({"error": "Bad Request"}), 400

    for key, value in data.items():
        if value is None or str(value).strip() == '':
            return jsonify({"error": "Bad Request"}), 400

    if 'horasClase' in data:
        try:
            if int(data['horasClase']) < 0:
                return jsonify({"error": "Bad Request"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Bad Request"}), 400

    if 'numeroEmpleado' in data:
        try:
            if int(data['numeroEmpleado']) < 0:
                return jsonify({"error": "Bad Request"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Bad Request"}), 400

    try:
        for key, value in data.items():
            setattr(profesor, key, value)
        db.session.commit()
        return jsonify(profesor.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "detalle": str(e)}), 400

@profesores_bp.route('/<int:id>', methods=['DELETE'])
def delete_profesor(id):
    profesor = Profesor.query.get(id)
    if not profesor:
        return jsonify({"error": "Not Found"}), 404
    db.session.delete(profesor)
    db.session.commit()
    return jsonify({"mensaje": "Eliminado"}), 200
