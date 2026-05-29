# Proyecto AWS - API Flask

API REST desarrollada con Flask y desplegada en AWS EC2, con integración a RDS (MySQL), S3 y SNS.

## Estructura del proyecto

```
proyecto-aws/
├── app/
│   ├── __init__.py          # Factory de la app Flask
│   ├── models.py            # Modelos SQLAlchemy (Alumno, Profesor)
│   ├── aws_services.py      # Clientes boto3 (S3, SNS, DynamoDB)
│   └── routes/
│       ├── alumnos.py       # Endpoints /alumnos
│       └── profesores.py    # Endpoints /profesores
├── config.py                # Configuración (lee variables de entorno)
├── run.py                   # Punto de entrada
├── requirements.txt         # Dependencias
├── .env.example             # Plantilla de variables de entorno
└── .gitignore
```

## Endpoints principales

### Alumnos (`/alumnos`)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/alumnos` | Obtener todos los alumnos |
| POST | `/alumnos` | Crear alumno |
| GET | `/alumnos/{id}` | Obtener alumno por ID |
| PUT | `/alumnos/{id}` | Actualizar alumno |
| DELETE | `/alumnos/{id}` | Eliminar alumno |
| POST | `/alumnos/{id}/email` | Enviar email |
| POST | `/alumnos/{id}/fotoPerfil` | Subir foto a S3 |
| POST | `/alumnos/{id}/session/login` | Iniciar sesión |
| POST | `/alumnos/{id}/session/verify` | Verificar sesión |
| POST | `/alumnos/{id}/session/logout` | Cerrar sesión |

### Profesores (`/profesores`)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/profesores` | Obtener todos los profesores |
| POST | `/profesores` | Crear profesor |
| GET | `/profesores/{id}` | Obtener profesor por ID |
| PUT | `/profesores/{id}` | Actualizar profesor |
| DELETE | `/profesores/{id}` | Eliminar profesor |

## Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales reales
```

### 4. Ejecutar
```bash
python run.py
```

## Servicios AWS utilizados
- **EC2** — Servidor de la aplicación
- **RDS MySQL** — Base de datos relacional
- **S3** — Almacenamiento de fotos de perfil
- **SNS** — Notificaciones
- **DynamoDB** — Tabla de sesiones
