from functools import wraps
from flask import request

from database.model import Regiao

def RegiaoValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['cep', 'nome', 'lat', 'lon', 'usuariosId']
        regiao = request.get_json()
        regiaoKeys = regiao.keys()
        for key in regiaoKeys:
            if not key in campos:
                return  {'message': 'O campo "' + key + '" não é reconhecido. Campos conhecidos: ' + str(campos)}, 400
        
        missing = [key for key in Regiao.requireds if not key in regiaoKeys]

        if len(missing) > 0:
            return {'message': 'O(s) campo(s) ' + str(missing) + ' deve(m) estar preenchido(s).'}, 400

        if (not 'cep' in regiaoKeys or regiao['cep'].__class__ != str):
            return {'message': 'O campos "cep" deve ser uma string.'}, 400
        if (not 'nome' in regiaoKeys or regiao['nome'].__class__ != str):
            return {'message': 'O campos "nome" deve ser uma string.'}, 400
        if (not 'lat' in regiaoKeys or regiao['lat'].__class__ != float or abs(regiao['lat']) > 90):
            return {'message': 'O campos "lat" deve ser um float entre -90 e 90.'}, 400
        if (not 'lon' in regiaoKeys or regiao['lon'].__class__ != float or abs(regiao['lon']) > 180):
            return {'message': 'O campos "lon" deve ser um float entre -180 e 180.'}, 400
        if ('usuariosId' in regiaoKeys):
            for usuarioId in regiao['usuariosId']:
                if usuarioId.__class__ != str:
                    return {'message': 'O campos "usuariosId" deve ser uma lista de string.'}, 400

        return func(self, *args, **kwargs)
    return wrapper

def RegiaoFiltroValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['ids', 'lat_min', 'lon_min', 'lat_max', 'lon_max', 'ceps', 'limit', 'orderBy', 'skip']
        filtro = request.get_json()
        filtroKeys = filtro.keys()

        for key in filtroKeys:
            if not key in campos:
                return  {'message': 'O campo "' + key + '" não é reconhecido. Campos conhecidos: ' + str(campos)}, 400 

        if ('ids' in filtroKeys):
            if filtro['ids'].__class__ != list:
                return {'message': 'O campos "ids" deve ser uma lista de string.'}, 400
            for id in filtro['ids']:
                if id.__class__ != str:
                    return {'message': 'O campos "ids" deve ser uma lista de string.'}, 400

        return func(self, *args, **kwargs)
    return wrapper
