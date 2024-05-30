# models.py

from pymongo import MongoClient
from datetime import datetime


client = MongoClient("mongodb://testuser:testpassword@host.docker.internal:27017/test1?directConnection=true&serverSelectionTimeoutMS=2000&retryWrites=true&w=majority")
db = client.test1

class Cliente:
    def __init__(self, dni, nombre, apellido, direccion, telefono, email):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    def to_dict(self):
        return self.__dict__

class Abogado:
    def __init__(self, dni, nombre, apellido, direccion, telefono, email, gabinete):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.gabinete = gabinete

    def to_dict(self):
        return self.__dict__

class Procurador:
    def __init__(self, dni, nombre, apellido, direccion, telefono, email):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    def to_dict(self):
        return self.__dict__

class Audiencia:
    def __init__(self, fecha, abogado, incidencias):
        self.fecha = fecha
        self.abogado = abogado
        self.incidencias = incidencias

    def to_dict(self):
        return {
            'fecha': self.fecha,
            'abogado': self.abogado.to_dict(),
            'incidencias': self.incidencias
        }

class Asunto:
    def __init__(self, numero_expediente, cliente, fecha_inicio, estado, procuradores, audiencias, fecha_finalizacion=None):
        self.numero_expediente = numero_expediente
        self.cliente = cliente
        self.fecha_inicio = fecha_inicio
        self.fecha_finalizacion = fecha_finalizacion
        self.estado = estado
        self.procuradores = procuradores
        self.audiencias = audiencias

    def to_dict(self):
        return {
            'numero_expediente': self.numero_expediente,
            'cliente': self.cliente.to_dict(),
            'fecha_inicio': self.fecha_inicio,
            'fecha_finalizacion': self.fecha_finalizacion,
            'estado': self.estado,
            'procuradores': [proc.to_dict() for proc in self.procuradores],
            'audiencias': self.audiencias  # Store IDs of audiencias
        }