# WEB_EA2
# API de Monitoreo Factory

Esta API RESTful permite gestionar módulos de monitoreo y los sensores asociados a cada módulo. 
Se implementan operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre la colección `modulos_monitoreo` en la base de datos MongoDB `monitoreo_factory`.

---

## Requerimientos

- **Python 3.x**
- **Flask**
- **pymongo**
- **MongoDB** (instalación local)

---

## Instrucciones de Configuración

1. **Clonar el Repositorio o Copiar los Archivos**  
   Asegúrate de contar con los siguientes archivos en tu proyecto:
   - `db.py`
   - `routes.py`
   - `server.py`
   - `README.md`

2. **Instalar MongoDB**  
   Si aún no tienes MongoDB instalado, descárgalo e instálalo desde [este enlace](https://www.mongodb.com/try/download/community).  
   La API se conectará a la base de datos `monitoreo_factory` y usará la colección `modulos_monitoreo`. Se creará automáticamente el índice único sobre el campo `modulo_id`.

---

## Instrucciones para Instalar Dependencias

Ejecuta el siguiente comando en la terminal dentro del directorio del proyecto:

```bash
pip install Flask pymongo
```

---

## Iniciar el Servidor Flask

Para ejecutar la API, usa el siguiente comando:

```bash
python server.py
```

Por defecto, la API correrá en `http://localhost:5000`.

---

## **Endpoints de la API**

### 1. Módulos de Monitoreo

#### Crear un nuevo módulo
**POST** `/modulos/`

**Cuerpo de la petición:**
```json
{
    "modulo_id": "modulo_001",
    "ubicacion": "Planta A",
    "sensores": [
        {
            "sensor_id": "sensor_temp_1",
            "tipo": "temperatura",
            "valor": 40,
            "fecha": "2025-03-17T12:00:00Z"
        }
    ]
}
```
**Respuesta esperada:**
```json
{
    "message": "Módulo creado exitosamente"
}
```

---

#### Obtener todos los módulos
**GET** `/modulos/`

**Respuesta esperada:**
```json
[
    {
        "modulo_id": "modulo_001",
        "ubicacion": "Planta A",
        "sensores": []
    }
]
```

---

#### Obtener un módulo por ID
**GET** `/modulos/<modulo_id>`

**Respuesta esperada:**
```json
{
    "modulo_id": "modulo_001",
    "ubicacion": "Planta A",
    "sensores": []
}
```

---

#### Actualizar un módulo
**PUT** `/modulos/<modulo_id>`

**Cuerpo de la petición:**
```json
{
    "ubicacion": "Planta B"
}
```
**Respuesta esperada:**
```json
{
    "message": "Módulo actualizado"
}
```

---

#### Eliminar un módulo
**DELETE** `/modulos/<modulo_id>`

**Respuesta esperada:**
```json
{
    "message": "Módulo eliminado"
}
```

---

### 2. Sensores dentro de un Módulo

#### Agregar un sensor a un módulo
**POST** `/modulos/<modulo_id>/sensores`

**Cuerpo de la petición:**
```json
{
    "sensor_id": "sensor_temp_2",
    "tipo": "temperatura",
    "valor": 22,
    "fecha": "2025-03-17T13:00:00Z"
}
```
**Respuesta esperada:**
```json
{
    "message": "Sensor agregado al módulo"
}
```

---

#### Obtener todos los sensores de un módulo
**GET** `/modulos/<modulo_id>/sensores`

**Respuesta esperada:**
```json
[
    {
        "sensor_id": "sensor_temp_1",
        "tipo": "temperatura",
        "valor": 40,
        "fecha": "2025-03-17T12:00:00Z"
    }
]
```

---

#### Obtener un sensor específico de un módulo
**GET** `/modulos/<modulo_id>/sensores/<sensor_id>`

**Respuesta esperada:**
```json
{
    "sensor_id": "sensor_temp_1",
    "tipo": "temperatura",
    "valor": 40,
    "fecha": "2025-03-17T12:00:00Z"
}
```

---

#### Actualizar un sensor
**PUT** `/modulos/<modulo_id>/sensores/<sensor_id>`

**Cuerpo de la petición:**
```json
{
    "valor": 45
}
```
**Respuesta esperada:**
```json
{
    "message": "Sensor actualizado"
}
```

---

#### Eliminar un sensor de un módulo
**DELETE** `/modulos/<modulo_id>/sensores/<sensor_id>`

**Respuesta esperada:**
```json
{
    "message": "Sensor eliminado"
}
```

---

## Notas
- Todos los datos deben cumplir con las validaciones definidas:
  - `modulo_id` y `sensor_id` deben ser únicos.
  - `tipo` de sensor debe ser "temperatura", "presion", "vibracion" o "humedad".
  - `valor` debe estar dentro de los rangos válidos.
  - `fecha` debe tener el formato ISO 8601.

---
