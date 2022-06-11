from abc import abstractclassmethod, abstractmethod
from .db import db
import json

class BaseModel(db.Document):
    meta = {'abstract': True}
    @classmethod
    def objects2dto(cls, mdb):
        dto = mdb
        dto['id'] = mdb['_id']['$oid']
        del dto['_id']
        return dto

    @abstractclassmethod
    def ws2document(cls, ws:dict):
        try:
            return dict(ws)
        except Exception as e:
            raise ValueError("Erro ao converter WS para MongoDocument. - " + e)
    
    @abstractclassmethod
    def preparaFiltro(cls, filtro:dict):
        raise ("")

class Regiao(BaseModel):
    cep = db.StringField(required=True)
    nome = db.StringField(required=True)
    lat = db.FloatField(required=True)
    lon = db.FloatField(required=True)
    usuariosId = db.ListField()

    @classmethod
    def ws2document(cls, ws:dict):
        wsKeys = ws.keys()
        document = {
            'cep': str(ws['cep'] if ('cep' in wsKeys) else ""),
            'nome': str(ws['nome'] if ('nome' in wsKeys) else ""),
            'lat': float(ws['lat'] if ('lat' in wsKeys) else 0),
            'lon': float(ws['lon'] if ('lon' in wsKeys) else 0),
            'usuariosId': list(ws['usuariosId'] if ('usuariosId' in wsKeys) else []),
        }

        return super().ws2document(document)


class Usuario(BaseModel):
    nome = db.StringField(required=True)
    login = db.StringField(required=True)
    senha = db.StringField(required=True)
    nascimento = db.IntField(required=True)
    tipo = db.IntField(required=True)
    regioesId = db.ListField()

class Feedback(BaseModel):
    avisoId = db.StringField(required=True)
    tipo = db.IntField(required=True)
    risco = db.IntField(required=True)
    usuarioId = db.StringField(required=True)

class Aviso(BaseModel):
    descricao = db.StringField(required=True)
    data_inicio = db.IntField(required=True)
    data_fim = db.IntField(required=True)
    regiaoId = db.StringField(required=True)
    autor = db.StringField(required=True)
    risco = db.IntField(required=True)
    tipo = db.IntField(required=True)
    nFeedBacks = db.IntField(required=True)