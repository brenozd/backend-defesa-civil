from abc import abstractclassmethod, abstractmethod
from sqlite3 import InternalError
import time

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
    requireds =  ["cep", "nome", "lat", "lon"]
    cep = db.StringField(required=True)
    nome = db.StringField(required=True)
    lat = db.FloatField(required=True)
    lon = db.FloatField(required=True)
    usuariosId = db.ListField()

    @classmethod
    def ws2document(cls, ws:dict):
        wsKeys = ws.keys()
        document = {
            'cep': str(ws['cep']),
            'nome': str(ws['nome']),
            'lat': float(ws['lat']),
            'lon': float(ws['lon']),
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
    requireds = ['nome', 'login', 'senha', 'nascimento', 'tipo']
    nome = db.StringField(required=True)
    login = db.StringField(required=True)
    senha = db.StringField(required=True)
    nascimento = db.IntField(required=True)
    tipo = db.IntField(required=True)
    regioesId = db.ListField()

    @classmethod
    def ws2document(cls, ws:dict):
        wsKeys = ws.keys()
        document = {
            'nome': str(ws['nome']),
            'login': str(ws['login']),
            'senha': str(ws['senha']),
            'nascimento': int(ws['nascimento']),
            'tipo': int(ws['tipo']),
            'regioesId': list(ws['regioesId'] if ('regioesId' in wsKeys) else [])
        }

        return super().ws2document(document)

    @classmethod
    def preparaFiltro(cls, filtroWS):
        filtroKeys = filtroWS.keys()
        filtro = {}
        if ('ids' in filtroKeys):
            filtro['id__in'] = [ObjectId(id) for id in filtroWS['ids']]
        if ('tipos' in filtroKeys):
            filtro['tipo__in'] = [tipo for tipo in filtroWS['tipos']]
        if ('nomes' in filtroKeys):
            filtro['nome__in'] = [nome for nome in filtroWS['nomes']]
        if ('logins' in filtroKeys):
            filtro['login__in'] = [login for login in filtroWS['logins']]
        
        return filtro

class Feedback(BaseModel):
    requireds = ['avisoId', 'tipo', 'usuarioId']
    avisoId = db.StringField(required=True)
    tipo = db.IntField(required=True)
    usuarioId = db.StringField(required=True)

    @classmethod
    def ws2document(cls, ws:dict):
        document = {
            'avisoId': str(ws['avisoId']),
            'tipo': int(ws['tipo']),
            'usuarioId': str(ws['usuarioId'])
        }

        return super().ws2document(document)

    @classmethod
    def preparaFiltro(cls, filtroWS):
        filtroKeys = filtroWS.keys()
        filtro = {}
        if ('ids' in filtroKeys):
            filtro['id__in'] = [ObjectId(id) for id in filtroWS['ids']]
        if ('tipos' in filtroKeys):
            filtro['tipo__in'] = [tipo for tipo in filtroWS['tipos']]
        if ('avisoIds' in filtroKeys):
            filtro['avisoId__in'] = [ObjectId(avisoId) for avisoId in filtroWS['avisoIds']]
        if ('usuarioIds' in filtroKeys):
            filtro['usuarioId__in'] = [ObjectId(usuarioId) for usuarioId in filtroWS['usuarioIds']]
        
        return filtro

class Aviso(BaseModel):
    requireds = ['descricao', 'data_inicio', 'data_fim', 'lat_min', 'lat_max', 'lon_min', 'lon_max', 'autor', 'risco', 'tipo']
    descricao = db.StringField(required=True)
    data_inicio = db.IntField(required=True)
    data_fim = db.IntField(required=True)
    regiaoId = db.StringField(required=True)
    autor = db.StringField(required=True)
    risco = db.IntField(required=True)
    tipo = db.IntField(required=True)
    nFeedBacks = db.IntField()

    @classmethod
    def ws2document(cls, ws:dict):
        wsKeys = ws.keys()
        regioes = Regiao.list({
            'lat_min': ws['lat_min'],
            'lat_max': ws['lat_max'],
            'lon_min': ws['lon_min'],
            'lon_max': ws['lon_max'],
            'limit': 1
        })
        if len(regioes) == 0:
            raise InternalError('Nenhuma região encontrada para latitude e lonngitude enviadas.')
        regiao = regioes[0]
        document = {
            'descricao': str(ws['descricao']),
            'data_inicio': int(ws['data_inicio']),
            'data_fim': int(ws['data_fim']),
            'regiaoId': str(regiao['id']),
            'autor': str(ws['autor']),
            'risco': int(ws['risco']),
            'tipo': int(ws['tipo']),
            'nFeedBacks': int(ws['nFeedBacks']) if 'nFeedBacks' in wsKeys else 0
        }

        return super().ws2document(document)

    @classmethod
    def preparaFiltro(cls, filtroWS):
        filtroKeys = filtroWS.keys()
        filtro = {}
        if ('ids' in filtroKeys):
            filtro['id__in'] = [ObjectId(id) for id in filtroWS['ids']]
        if ('tipos' in filtroKeys):
            filtro['tipo__in'] = [tipo for tipo in filtroWS['tipos']]
        if ('riscos' in filtroKeys):
            filtro['risco__in'] = [risco for risco in filtroWS['riscos']]
        if ('autores' in filtroKeys):
            filtro['autor__in'] = [autor for autor in filtroWS['autores']]
        if ('data_inicio_min' in filtroKeys or 'data_inicio_max' in filtroKeys):
            if ('data_inicio_min' in filtroKeys):
                filtro['data_inicio__gte'] = filtroWS['data_inicio_min']
            else:
                filtro['data_inicio__gte'] = 0
            if ('data_inicio_max' in filtroKeys):
                filtro['data_inicio__lte'] = filtroWS['data_inicio_max']
            else:
                filtro['data_inicio__lte'] = time.time() + 604800 # por padrao vai pegar os avisos com inicio ate um mes depois
        if ('data_fim_min' in filtroKeys or 'data_fim_max' in filtroKeys):
            if ('data_fim_min' in filtroKeys):
                filtro['data_fim__gte'] = filtroWS['data_fim_min']
            else:
                filtro['data_fim__gte'] = 0
            if ('data_fim_max' in filtroKeys):
                filtro['data_fim__lte'] = filtroWS['data_fim_max']
            else:
                filtro['data_fim__lte'] = time.time() + 2592000 # por padrao vai pegar os avisos com fim ate um mes depois
        
        return filtro