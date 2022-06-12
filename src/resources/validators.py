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
                return {'message': 'O campo "ids" deve ser uma lista de string.'}, 400
            for id in filtro['ids']:
                if id.__class__ != str:
                    return {'message': 'O campo "ids" deve ser uma lista de string.'}, 400
        if ('ceps' in filtroKeys):
            if filtro['ceps'].__class__ != list:
                return {'message': 'O campo "ceps" deve ser uma lista de string.'}, 400
            for cep in filtro['ceps']:
                if cep.__class__ != str:
                    return {'message': 'O campo "ceps" deve ser uma lista de string.'}, 400
        if ('limit' in filtroKeys):
            if (filtro['limit'].__class__ != int or filtro['limit'] < 1):
                return {'message': 'O campo "limit" deve ser um int maior que 0.'}, 400
        if ('skip' in filtroKeys):
            if (filtro['skip'].__class__ != int or filtro['skip'] < 0):
                return {'message': 'O campo "skip" deve ser um int maior ou igual a 0.'}, 400
        if ('orderBy' in filtroKeys):
            if (filtro['orderBy'].__class__ != str or not filtro['orderBy'].split('-')[-1].split('+')[-1] in Regiao.requireds):
                return {'message': 'O campo "orderBy" deve ser uma str com o símbolo de ordenação (+ ou -) seguido de um dos campos obrigatórios: ' + str(Regiao.requireds) + '.'}, 400
        if ('lat_min' in filtroKeys):
            if ((filtro['lat_min'].__class__ != int and filtro['lat_min'].__class__ != float) or abs(filtro['lat_min']) > 90):
                return {'message': 'O campo "lat_min" deve ser um float entre -90 e 90.'}, 400
        if ('lat_max' in filtroKeys):
            if ((filtro['lat_max'].__class__ != int and filtro['lat_max'].__class__ != float) or abs(filtro['lat_max']) > 90):
                return {'message': 'O campo "lat_max" deve ser um float entre -90 e 90.'}, 400
        if ('lon_min' in filtroKeys):
            if ((filtro['lon_min'].__class__ != int and filtro['lon_min'].__class__ != float) or abs(filtro['lon_min']) > 90):
                return {'message': 'O campo "lon_min" deve ser um float entre -90 e 90.'}, 400
        if ('lon_max' in filtroKeys):
            if ((filtro['lon_max'].__class__ != int and filtro['lon_max'].__class__ != float) or abs(filtro['lon_max']) > 90):
                return {'message': 'O campo "lon_max" deve ser um float entre -180 e 180.'}, 400

        return func(self, *args, **kwargs)
    return wrapper
