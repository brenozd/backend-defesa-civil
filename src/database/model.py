from abc import abstractclassmethod, abstractmethod

from bson import ObjectId
from .db import db
import json

class BaseModel(db.Document):
    meta = {'abstract': True}
    @classmethod
    def object2dto(cls, mdb):
        dto = mdb
        dto['id'] = mdb['_id']['$oid']
        del dto['_id']
        return dto

    @classmethod
    def list(cls, filtroWS):
        filtro = cls.preparaFiltro(filtroWS)
        resultado = cls.objects(**filtro)
        if ('orderBy' in filtroWS.keys()):
            resultado = resultado.order_by(filtroWS['orderBy'])
        if ('skip' in filtroWS.keys()):
            skip = filtroWS['skip']
        else:
            skip = 0
        if ('limit' in filtroWS.keys()):
            limit = filtroWS['limit']
        else:
            limit = 1000

        return [cls.object2dto(obj) for obj in json.loads(resultado[skip:skip+limit].to_json())]

    @abstractclassmethod
    def ws2document(cls, ws:dict):
        try:
            return dict(ws)
        except Exception as e:
            raise ValueError("Erro ao converter WS para MongoDocument. - " + e)
    
    @abstractclassmethod
    def preparaFiltro(cls, filtro:dict):
        raise NotImplementedError("preparaFiltro da classe " + cls.__name__ + " nao implementada.")

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

    @classmethod
    def preparaFiltro(cls, filtroWS):
        filtroKeys = filtroWS.keys()
        filtro = {}
        if ('ids' in filtroKeys):
            filtro['id__in'] = [ObjectId(id) for id in filtroWS['ids']]
        if ('lat_min' in filtroKeys or 'lat_max' in filtroKeys):
            if ('lat_min' in filtroKeys):
                filtro['lat__gte'] = filtroWS['lat_min']
            else:
                filtro['lat__gte'] = -90
            if ('lat_max' in filtroKeys):
                filtro['lat__lte'] = filtroWS['lat_max']
            else:
                filtro['lat__lte'] = 90
        if ('lon_min' in filtroKeys or 'lon_max' in filtroKeys):
            if ('lon_min' in filtroKeys):
                filtro['lon__gte'] = filtroWS['lon_min']
            else:
                filtro['lon__gte'] = -180
            if ('lon_max' in filtroKeys):
                filtro['lon__lte'] = filtroWS['lon_max']
            else:
                filtro['lon__lte'] = 180
        
        return filtro

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