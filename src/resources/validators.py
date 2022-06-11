from functools import wraps
from flask import request

def RegiaoValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['cep', 'nome', 'lat', 'lon', 'usuariosId']
        regiao = request.get_json()
        regiaoKeys = regiao.keys()
        for key in regiaoKeys:
            if not key in campos:
                return  {'message': 'O campo "' + key + '" não é reconhecido. Campos conhecidos: ' + str(campos)}, 400
        
        if (not 'cep' in regiaoKeys or regiao['cep'].__class__ != str):
            return {'message': 'O campos "cep" deve ser uma string.'}, 400
        if (not 'nome' in regiaoKeys or regiao['nome'].__class__ != str):
            return {'message': 'O campos "nome" deve ser uma string.'}, 400
        if (not 'lat' in regiaoKeys or regiao['lat'].__class__ != float):
            return {'message': 'O campos "lat" deve ser um float.'}, 400
        if (not 'lon' in regiaoKeys or regiao['lon'].__class__ != float):
            return {'message': 'O campos "lon" deve ser uma float.'}, 400
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
            for id in filtro['ids']:
                if id.__class__ != str:
                    return {'message': 'O campos "ids" deve ser uma lista de string.'}, 400

        return func(self, *args, **kwargs)
    return wrapper
