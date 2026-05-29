from flask import Blueprint, request, jsonify, current_app
from app.models import db, Alumno
import boto3, uuid, os, secrets

alumnos_bp = Blueprint('alumnos', __name__)

CAMPOS_VALIDOS = {'nombres', 'apellidos', 'matricula', 'promedio', 'password'}
CAMPOS_REQUERIDOS = {'nombres', 'apellidos', 'matricula', 'promedio', 'password'}

@alumnos_bp.route('', methods=['GET'])
def get_all_alumnos():
    alumnos = Alumno.query.all()
    return jsonify([a.to_dict() for a in alumnos]), 200

@alumnos_bp.route('', methods=['POST'])
def create_alumno():
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
        promedio = float(data['promedio'])
        if promedio < 0 or promedio > 10:
            return jsonify({"error": "Bad Request"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Bad Request"}), 400

    try:
        nuevo = Alumno(**data)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify(nuevo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "detalle": str(e)}), 400

@alumnos_bp.route('/<int:id>', methods=['GET'])
def get_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(alumno.to_dict()), 200

@alumnos_bp.route('/<int:id>', methods=['PUT'])
def update_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
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

    if 'promedio' in data:
        try:
            promedio = float(data['promedio'])
            if promedio < 0 or promedio > 10:
                return jsonify({"error": "Bad Request"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Bad Request"}), 400

    try:
        for key, value in data.items():
            setattr(alumno, key, value)
        db.session.commit()
        return jsonify(alumno.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "detalle": str(e)}), 400

@alumnos_bp.route('/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Not Found"}), 404
    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"mensaje": "Eliminado"}), 200

# --- ENDPOINTS ADICIONALES ---

@alumnos_bp.route('/<int:id>/email', methods=['POST'])
def send_email(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Not Found"}), 404
    return jsonify({"mensaje": "Email enviado"}), 200

@alumnos_bp.route('/<int:id>/fotoPerfil', methods=['POST'])
def upload_foto(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Not Found"}), 404

    if 'foto' not in request.files:
        return jsonify({"error": "Bad Request"}), 400

    archivo = request.files['foto']
    bucket = current_app.config['BUCKET_NAME']
    nombre_archivo = f"fotos/{id}/{uuid.uuid4()}_{archivo.filename}"

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
            aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
            aws_session_token=current_app.config['AWS_SESSION_TOKEN'],
            region_name=current_app.config['AWS_REGION']
        )
        s3.upload_fileobj(
            archivo,
            bucket,
            nombre_archivo,
            ExtraArgs={
                'ContentType': archivo.content_type,
                'ACL': 'public-read'
            }
        )
    except Exception as e:
        return jsonify({"error": "Error al subir archivo", "detalle": str(e)}), 500

    url = f"https://{bucket}.s3.amazonaws.com/{nombre_archivo}"
    alumno.fotoPerfilUrl = url
    db.session.commit()

    return jsonify({"fotoPerfilUrl": url}), 200

@alumnos_bp.route('/<int:id>/session/login', methods=['POST'])
def login(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Not Found"}), 404

    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({"error": "Bad Request"}), 400

    if data['password'] != alumno.password:
        return jsonify({"error": "Bad Request"}), 400

    token = secrets.token_hex(64)
    alumno.sessionToken = token
    db.session.commit()

    return jsonify({"mensaje": "Login exitoso", "sessionString": token}), 200

@alumnos_bp.route('/<int:id>/session/verify', methods=['POST'])
def verify(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Not Found"}), 404

    data = request.get_json()
    if not data or 'sessionString' not in data:
        return jsonify({"error": "Bad Request"}), 400

    if data['sessionString'] != alumno.sessionToken:
        return jsonify({"error": "Bad Request"}), 400

    return jsonify({"mensaje": "Verificado"}), 200

@alumnos_bp.route('/<int:id>/session/logout', methods=['POST'])
def logout(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Not Found"}), 404

    alumno.sessionToken = None
    db.session.commit()

    return jsonify({"mensaje": "Logout exitoso"}), 200
