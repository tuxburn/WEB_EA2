from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import datetime

# Conexión a la base de datos y colección
clientDB = MongoClient('localhost', 27017)
db = clientDB['monitoreo_factory']
modules_collection = db["modulos_monitoreo"]

# Crear un índice único en modulo_id para evitar duplicados
modules_collection.create_index("modulo_id", unique=True)

# Rangos válidos por tipo de sensor
VALID_SENSOR_TYPES = {
    "temperatura": (-10, 100),
    "presion": (0, 500),
    "vibracion": (0, 5),
    "humedad": (0, 99)
}

def validate_sensor(sensor, existing_sensor_ids):
    """Valida que cada sensor incluya los campos obligatorios y cumpla los rangos y formato."""
    required_fields = ["sensor_id", "tipo", "valor", "fecha"]
    for field in required_fields:
        if field not in sensor:
            return f"{field} es obligatorio en cada sensor."
    # sensor_id único dentro del módulo
    if sensor["sensor_id"] in existing_sensor_ids:
        return f"El sensor_id {sensor['sensor_id']} ya existe en este módulo."
    # Validar tipo de sensor
    tipo = sensor["tipo"]
    if tipo not in VALID_SENSOR_TYPES:
        return f"Tipo de sensor inválido: {tipo}. Debe ser uno de {list(VALID_SENSOR_TYPES.keys())}."
    # Validar rango de valor
    valor = sensor["valor"]
    min_val, max_val = VALID_SENSOR_TYPES[tipo]
    if not (min_val <= valor <= max_val):
        return f"El valor {valor} para el sensor de tipo {tipo} debe estar entre {min_val} y {max_val}."
    # Validar formato de fecha (ISO 8601)
    try:
        datetime.datetime.fromisoformat(sensor["fecha"].replace("Z", "+00:00"))
    except ValueError:
        return f"Formato de fecha inválido para el sensor {sensor['sensor_id']}. Debe ser ISO 8601."
    return None

def add_module(module):
    """Agrega un nuevo módulo de monitoreo a la base de datos."""
    if "modulo_id" not in module or not module["modulo_id"]:
        return {"error": "El campo modulo_id es obligatorio."}
    if "ubicacion" not in module or not module["ubicacion"]:
        return {"error": "El campo ubicacion es obligatorio."}
    if "sensores" not in module or not isinstance(module["sensores"], list):
        return {"error": "El campo sensores debe ser una lista."}

    sensor_ids = set()
    for sensor in module["sensores"]:
        error = validate_sensor(sensor, sensor_ids)
        if error:
            return {"error": error}
        sensor_ids.add(sensor["sensor_id"])

    try:
        modules_collection.insert_one(module)
    except DuplicateKeyError:
        return {"error": f"Ya existe un módulo con modulo_id {module['modulo_id']}."}
    return get_module(module["modulo_id"])

def get_modules():
    """Recupera todos los módulos."""
    modules = list(modules_collection.find({}, {"_id": 0}))
    return modules

def get_module(modulo_id):
    """Recupera un módulo específico por modulo_id."""
    module = modules_collection.find_one({"modulo_id": modulo_id}, {"_id": 0})
    if not module:
        return {"error": f"Módulo con modulo_id {modulo_id} no encontrado."}
    return module

def update_module(modulo_id, data):
    """Actualiza los datos de un módulo existente."""
    if "sensores" in data:
        if not isinstance(data["sensores"], list):
            return {"error": "El campo sensores debe ser una lista."}
        sensor_ids = set()
        for sensor in data["sensores"]:
            error = validate_sensor(sensor, sensor_ids)
            if error:
                return {"error": error}
            sensor_ids.add(sensor["sensor_id"])
    result = modules_collection.update_one({"modulo_id": modulo_id}, {"$set": data})
    if result.matched_count == 0:
        return {"error": f"Módulo con modulo_id {modulo_id} no encontrado."}
    return get_module(modulo_id)

def delete_module(modulo_id):
    """Elimina un módulo específico."""
    result = modules_collection.delete_one({"modulo_id": modulo_id})
    if result.deleted_count == 0:
        return {"error": f"Módulo con modulo_id {modulo_id} no encontrado."}
    return {"message": f"Módulo con modulo_id {modulo_id} eliminado."}

# Métodos para operaciones CRUD sobre sensores dentro de un módulo

def add_sensor_to_module(modulo_id, sensor):
    """Agrega un sensor a un módulo específico."""
    module = modules_collection.find_one({"modulo_id": modulo_id})
    if not module:
        return {"error": f"Módulo con modulo_id {modulo_id} no encontrado."}
    sensors = module.get("sensores", [])
    existing_sensor_ids = {s["sensor_id"] for s in sensors}
    error = validate_sensor(sensor, existing_sensor_ids)
    if error:
        return {"error": error}
    sensors.append(sensor)
    modules_collection.update_one({"modulo_id": modulo_id}, {"$set": {"sensores": sensors}})
    return sensor

def get_sensor(modulo_id, sensor_id):
    """Recupera un sensor específico de un módulo."""
    module = modules_collection.find_one({"modulo_id": modulo_id})
    if not module:
        return {"error": f"Módulo con modulo_id {modulo_id} no encontrado."}
    for sensor in module.get("sensores", []):
        if sensor["sensor_id"] == sensor_id:
            return sensor
    return {"error": f"Sensor con sensor_id {sensor_id} no encontrado en el módulo {modulo_id}."}

def update_sensor(modulo_id, sensor_id, data):
    """Actualiza un sensor específico dentro de un módulo."""
    module = modules_collection.find_one({"modulo_id": modulo_id})
    if not module:
        return {"error": f"Módulo con modulo_id {modulo_id} no encontrado."}
    sensors = module.get("sensores", [])
    updated = None
    for i, sensor in enumerate(sensors):
        if sensor["sensor_id"] == sensor_id:
            updated_sensor = sensor.copy()
            updated_sensor.update(data)
            # Validar sensor actualizado, excluyendo el sensor actual
            sensor_ids = {s["sensor_id"] for s in sensors if s["sensor_id"] != sensor_id}
            error = validate_sensor(updated_sensor, sensor_ids)
            if error:
                return {"error": error}
            sensors[i] = updated_sensor
            updated = updated_sensor
            break
    if updated is None:
        return {"error": f"Sensor con sensor_id {sensor_id} no encontrado en el módulo {modulo_id}."}
    modules_collection.update_one({"modulo_id": modulo_id}, {"$set": {"sensores": sensors}})
    return updated

def delete_sensor(modulo_id, sensor_id):
    """Elimina un sensor de un módulo específico."""
    module = modules_collection.find_one({"modulo_id": modulo_id})
    if not module:
        return {"error": f"Módulo con modulo_id {modulo_id} no encontrado."}
    sensors = module.get("sensores", [])
    new_sensors = [sensor for sensor in sensors if sensor["sensor_id"] != sensor_id]
    if len(new_sensors) == len(sensors):
        return {"error": f"Sensor con sensor_id {sensor_id} no encontrado en el módulo {modulo_id}."}
    modules_collection.update_one({"modulo_id": modulo_id}, {"$set": {"sensores": new_sensors}})
    return {"message": f"Sensor con sensor_id {sensor_id} eliminado del módulo {modulo_id}."}
