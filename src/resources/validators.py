from functools import wraps
from flask import request

from database.model import Regiao, Aviso, Feedback, Usuario

def RegiaoValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['id', 'cep', 'nome', 'lat', 'lon', 'usuariosId']
        regiao = request.get_json()
        regiaoKeys = regiao.keys()
        for key in regiaoKeys:
            if not key in campos:
                return  {'message': 'O campo "' + key + '" não é reconhecido. Campos conhecidos: ' + str(campos)}, 400
        
        missing = [key for key in Regiao.requireds if not key in regiaoKeys]

        if len(missing) > 0:
            return {'message': 'O(s) campo(s) ' + str(missing) + ' deve(m) estar preenchido(s).'}, 400

        if ('id' in regiaoKeys and regiao['id'].__class__ != str):
            return {'message': 'O campo "id" deve ser uma string.'}, 400
        if (not 'cep' in regiaoKeys or regiao['cep'].__class__ != str):
            return {'message': 'O campo "cep" deve ser uma string.'}, 400
        if (not 'nome' in regiaoKeys or regiao['nome'].__class__ != str):
            return {'message': 'O campo "nome" deve ser uma string.'}, 400
        if (not 'lat' in regiaoKeys or regiao['lat'].__class__ != float or abs(regiao['lat']) > 90):
            return {'message': 'O campo "lat" deve ser um float entre -90 e 90.'}, 400
        if (not 'lon' in regiaoKeys or regiao['lon'].__class__ != float or abs(regiao['lon']) > 180):
            return {'message': 'O campo "lon" deve ser um float entre -180 e 180.'}, 400
        if ('usuariosId' in regiaoKeys):
            for usuarioId in regiao['usuariosId']:
                if usuarioId.__class__ != str:
                    return {'message': 'O campo "usuariosId" deve ser uma lista de string.'}, 400

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
            if ((filtro['lon_min'].__class__ != int and filtro['lon_min'].__class__ != float) or abs(filtro['lon_min']) > 180):
                return {'message': 'O campo "lon_min" deve ser um float entre -180 e 180.'}, 400
        if ('lon_max' in filtroKeys):
            if ((filtro['lon_max'].__class__ != int and filtro['lon_max'].__class__ != float) or abs(filtro['lon_max']) > 180):
                return {'message': 'O campo "lon_max" deve ser um float entre -180 e 180.'}, 400

        return func(self, *args, **kwargs)
    return wrapper

def AvisoValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['id', 'descricao', 'data_inicio', 'data_fim', 'lat_min', 'lat_max', 'lon_min', 'lon_max', 'regiaoId', 'autor', 'risco', 'tipo', 'nFeedBacks']
        camposLat = ['lat_min', 'lat_max', 'lon_min', 'lon_max']
        aviso = request.get_json()
        avisoKeys = aviso.keys()
        for key in avisoKeys:
            if not key in campos:
                return  {'message': 'O campo "' + key + '" não é reconhecido. Campos conhecidos: ' + str(campos)}, 400
        
        missing = [key for key in Aviso.requireds if not key in avisoKeys]

        if len(missing) > 0:
            return {'message': 'O(s) campo(s) ' + str(missing) + ' deve(m) estar preenchido(s).'}, 400

        if ('id' in avisoKeys and aviso['id'].__class__ != str):
            return {'message': 'O campo "id" deve ser uma string.'}, 400
        if (not 'descricao' in avisoKeys or aviso['descricao'].__class__ != str):
            return {'message': 'O campo "descricao" deve ser uma string.'}, 400
        if (not 'data_inicio' in avisoKeys or aviso['data_inicio'].__class__ != int or aviso['data_inicio'] < 0):
            return {'message': 'O campo "data_inicio" deve ser um int em timestamp.'}, 400
        if (not 'data_fim' in avisoKeys or aviso['data_fim'].__class__ != int or aviso['data_fim'] < 0):
            return {'message': 'O campo "data_fim" deve ser um int em timestamp.'}, 400
        if ('regiaoId' in avisoKeys):
            if (aviso['regiaoId'].__class__ != str):
                return {'message': 'O campo "regiaoId" deve ser uma string.'}, 400
        else:
            missing = [key for key in camposLat if not key in avisoKeys]
            if len(missing) > 0:
                return {'message': 'O(s) campo(s) ' + str(missing) + ' deve(m) estar preenchido(s).'}, 400
            else:
                if ('lat_min' in avisoKeys):
                    if ((aviso['lat_min'].__class__ != int and aviso['lat_min'].__class__ != float) or abs(aviso['lat_min']) > 90):
                        return {'message': 'O campo "lat_min" deve ser um float entre -90 e 90.'}, 400
                if ('lat_max' in avisoKeys):
                    if ((aviso['lat_max'].__class__ != int and aviso['lat_max'].__class__ != float) or abs(aviso['lat_max']) > 90):
                        return {'message': 'O campo "lat_max" deve ser um float entre -90 e 90.'}, 400
                if ('lon_min' in avisoKeys):
                    if ((aviso['lon_min'].__class__ != int and aviso['lon_min'].__class__ != float) or abs(aviso['lon_min']) > 180):
                        return {'message': 'O campo "lon_min" deve ser um float entre -180 e 180.'}, 400
                if ('lon_max' in avisoKeys):
                    if ((aviso['lon_max'].__class__ != int and aviso['lon_max'].__class__ != float) or abs(aviso['lon_max']) > 180):
                        return {'message': 'O campo "lon_max" deve ser um float entre -180 e 180.'}, 400
        
        if (not 'autor' in avisoKeys or aviso['autor'].__class__ != str):
            return {'message': 'O campo "autor" deve ser uma string.'}, 400
        if (not 'risco' in avisoKeys or aviso['risco'].__class__ != int):
            return {'message': 'O campo "risco" deve ser um int.'}, 400
        if (not 'tipo' in avisoKeys or aviso['tipo'].__class__ != int):
            return {'message': 'O campo "tipo" deve ser um int.'}, 400
        if ('nFeedBacks' in avisoKeys and aviso['nFeedBacks'].__class__ != int):
            return {'message': 'O campo "nFeedBacks" deve ser um int.'}, 400
        
        return func(self, *args, **kwargs)
    return wrapper

def AvisoFiltroValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['ids', 'tipos', 'riscos', 'autores', 'data_inicio_min', 'data_inicio_max', 'data_fim_min', 'data_fim_max', 'limit', 'orderBy', 'skip']
        camposLat = ['lat_min', 'lon_min', 'lat_max', 'lon_max']
        filtro = request.get_json()
        filtroKeys = filtro.keys()

        for key in filtroKeys:
            if not key in campos + camposLat:
                return  {'message': 'O campo "' + key + '" não é reconhecido. Campos conhecidos: ' + str(campos+camposLat)}, 400 

        if ('ids' in filtroKeys):
            if filtro['ids'].__class__ != list:
                return {'message': 'O campo "ids" deve ser uma lista de string.'}, 400
            for id in filtro['ids']:
                if id.__class__ != str:
                    return {'message': 'O campo "ids" deve ser uma lista de string.'}, 400

        if (any(key in camposLat for key in filtroKeys)):
            missing = [key for key in camposLat if not key in filtroKeys]
            if len(missing) > 0:
                return {'message': 'Todos os campos ' + str(camposLat) + ' devem estar preenchidos para filtrar por coordenadas.'}, 400

        if ('limit' in filtroKeys):
            if (filtro['limit'].__class__ != int or filtro['limit'] < 1):
                return {'message': 'O campo "limit" deve ser um int maior que 0.'}, 400
        if ('skip' in filtroKeys):
            if (filtro['skip'].__class__ != int or filtro['skip'] < 0):
                return {'message': 'O campo "skip" deve ser um int maior ou igual a 0.'}, 400
        if ('orderBy' in filtroKeys):
            if (filtro['orderBy'].__class__ != str or not filtro['orderBy'].split('-')[-1].split('+')[-1] in Aviso.requireds):
                return {'message': 'O campo "orderBy" deve ser uma str com o símbolo de ordenação (+ ou -) seguido de um dos campos obrigatórios: ' + str(Aviso.requireds) + '.'}, 400

        if ('autores' in filtroKeys):
            if filtro['autores'].__class__ != list:
                return {'message': 'O campo "autores" deve ser uma lista de string.'}, 400
            for autor in filtro['autores']:
                if autor.__class__ != str:
                    return {'message': 'O campo "autores" deve ser uma lista de string.'}, 400
        if ('tipos' in filtroKeys):
            if filtro['tipos'].__class__ != list:
                return {'message': 'O campo "tipos" deve ser uma lista de int.'}, 400
            for tipo in filtro['tipos']:
                if tipo.__class__ != int:
                    return {'message': 'O campo "tipos" deve ser uma lista de int.'}, 400
        if ('riscos' in filtroKeys):
            if filtro['riscos'].__class__ != list:
                return {'message': 'O campo "riscos" deve ser uma lista de int.'}, 400
            for risco in filtro['riscos']:
                if risco.__class__ != int:
                    return {'message': 'O campo "riscos" deve ser uma lista de int.'}, 400
        if ('data_inicio_min' in filtroKeys):
            if (filtro['data_inicio_min'].__class__ != int):
                return {'message': 'O campo "data_inicio_max" deve ser um int timestamp.'}, 400
        if ('data_inicio_max' in filtroKeys):
            if (filtro['data_inicio_max'].__class__ != int):
                return {'message': 'O campo "data_inicio_max" deve ser um int timestamp.'}, 400
        if ('data_fim_min' in filtroKeys):
            if (filtro['data_fim_min'].__class__ != int):
                return {'message': 'O campo "data_fim_max" deve ser um int timestamp.'}, 400
        if ('data_fim_max' in filtroKeys):
            if (filtro['data_fim_max'].__class__ != int):
                return {'message': 'O campo "data_fim_max" deve ser um int timestamp.'}, 400

        return func(self, *args, **kwargs)
    return wrapper

def FeedbackValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['id', 'avisoId', 'tipo', 'usuarioId']
        feedback = request.get_json()
        feedbackKeys = feedback.keys()
        for key in feedbackKeys:
            if not key in campos:
                return  {'message': 'O campo "' + key + '" não é reconhecido. Campos conhecidos: ' + str(campos)}, 400
        
        missing = [key for key in Feedback.requireds if not key in feedbackKeys]

        if len(missing) > 0:
            return {'message': 'O(s) campo(s) ' + str(missing) + ' deve(m) estar preenchido(s).'}, 400

        if ('id' in feedbackKeys and feedback['id'].__class__ != str):
            return {'message': 'O campo "id" deve ser uma string.'}, 400
        if (not 'avisoId' in feedbackKeys or feedback['avisoId'].__class__ != str):
            return {'message': 'O campo "avisoId" deve ser uma string.'}, 400
        if (not 'tipo' in feedbackKeys or feedback['tipo'].__class__ != int):
            return {'message': 'O campo "tipo" deve ser um int em timestamp.'}, 400
        if (not 'usuarioId' in feedbackKeys or feedback['usuarioId'].__class__ != str):
            return {'message': 'O campo "usuarioId" deve ser uma string.'}, 400
        
        return func(self, *args, **kwargs)
    return wrapper

def FeedbackFiltroValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['ids', 'tipos', 'avisoIds', 'usuarioIds', 'limit', 'orderBy', 'skip']
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
        if ('limit' in filtroKeys):
            if (filtro['limit'].__class__ != int or filtro['limit'] < 1):
                return {'message': 'O campo "limit" deve ser um int maior que 0.'}, 400
        if ('skip' in filtroKeys):
            if (filtro['skip'].__class__ != int or filtro['skip'] < 0):
                return {'message': 'O campo "skip" deve ser um int maior ou igual a 0.'}, 400
        if ('orderBy' in filtroKeys):
            if (filtro['orderBy'].__class__ != str or not filtro['orderBy'].split('-')[-1].split('+')[-1] in Feedback.requireds):
                return {'message': 'O campo "orderBy" deve ser uma str com o símbolo de ordenação (+ ou -) seguido de um dos campos obrigatórios: ' + str(Feedback.requireds) + '.'}, 400

        if ('avisoIds' in filtroKeys):
            if filtro['avisoIds'].__class__ != list:
                return {'message': 'O campo "avisoIds" deve ser uma lista de string.'}, 400
            for avisoId in filtro['avisoIds']:
                if avisoId.__class__ != str:
                    return {'message': 'O campo "avisoIds" deve ser uma lista de string.'}, 400
        if ('usuarioIds' in filtroKeys):
            if filtro['usuarioIds'].__class__ != list:
                return {'message': 'O campo "usuarioIds" deve ser uma lista de string.'}, 400
            for usuarioId in filtro['usuarioIds']:
                if usuarioId.__class__ != str:
                    return {'message': 'O campo "usuarioIds" deve ser uma lista de string.'}, 400
        if ('tipos' in filtroKeys):
            if filtro['tipos'].__class__ != list:
                return {'message': 'O campo "tipos" deve ser uma lista de int.'}, 400
            for tipo in filtro['tipos']:
                if tipo.__class__ != int:
                    return {'message': 'O campo "tipos" deve ser uma lista de int.'}, 400

        return func(self, *args, **kwargs)
    return wrapper

def UsuarioValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['id', 'nome', 'login', 'senha', 'nascimento', 'tipo', 'regioesId']
        usuario = request.get_json()
        usuarioKeys = usuario.keys()
        for key in usuarioKeys:
            if not key in campos:
                return  {'message': 'O campo "' + key + '" não é reconhecido. Campos conhecidos: ' + str(campos)}, 400
        
        missing = [key for key in Usuario.requireds if not key in usuarioKeys]

        if len(missing) > 0:
            return {'message': 'O(s) campo(s) ' + str(missing) + ' deve(m) estar preenchido(s).'}, 400

        if ('id' in usuarioKeys and usuario['id'].__class__ != str):
            return {'message': 'O campo "id" deve ser uma string.'}, 400
        if (not 'nome' in usuarioKeys or usuario['nome'].__class__ != str):
            return {'message': 'O campo "nome" deve ser uma string.'}, 400
        if (not 'login' in usuarioKeys or usuario['login'].__class__ != str):
            return {'message': 'O campo "login" deve ser uma string.'}, 400
        if (not 'senha' in usuarioKeys or usuario['senha'].__class__ != str):
            return {'message': 'O campo "senha" deve ser uma string.'}, 400
        if (not 'nascimento' in usuarioKeys or usuario['nascimento'].__class__ != int or usuario['nascimento'] < 0):
            return {'message': 'O campo "nascimento" deve ser um int em timestamp.'}, 400
        if (not 'tipo' in usuarioKeys or usuario['tipo'].__class__ != int):
            return {'message': 'O campo "tipo" deve ser um int.'}, 400
        if ('regioesId' in usuarioKeys):
            for regiaoId in usuario['regioesId']:
                if regiaoId.__class__ != str:
                    return {'message': 'O campo "regioesId" deve ser uma lista de string.'}, 400
        
        return func(self, *args, **kwargs)
    return wrapper

def UsuarioFiltroValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['ids', 'tipos', 'nomes', 'logins', 'limit', 'orderBy', 'skip']
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
        if ('limit' in filtroKeys):
            if (filtro['limit'].__class__ != int or filtro['limit'] < 1):
                return {'message': 'O campo "limit" deve ser um int maior que 0.'}, 400
        if ('skip' in filtroKeys):
            if (filtro['skip'].__class__ != int or filtro['skip'] < 0):
                return {'message': 'O campo "skip" deve ser um int maior ou igual a 0.'}, 400
        if ('orderBy' in filtroKeys):
            if (filtro['orderBy'].__class__ != str or not filtro['orderBy'].split('-')[-1].split('+')[-1] in Usuario.requireds):
                return {'message': 'O campo "orderBy" deve ser uma str com o símbolo de ordenação (+ ou -) seguido de um dos campos obrigatórios: ' + str(Usuario.requireds) + '.'}, 400

        if ('nomes' in filtroKeys):
            if filtro['nomes'].__class__ != list:
                return {'message': 'O campo "nomes" deve ser uma lista de string.'}, 400
            for nome in filtro['nomes']:
                if nome.__class__ != str:
                    return {'message': 'O campo "nomes" deve ser uma lista de string.'}, 400
        if ('logins' in filtroKeys):
            if filtro['logins'].__class__ != list:
                return {'message': 'O campo "logins" deve ser uma lista de string.'}, 400
            for login in filtro['logins']:
                if login.__class__ != str:
                    return {'message': 'O campo "logins" deve ser uma lista de string.'}, 400
        if ('tipos' in filtroKeys):
            if filtro['tipos'].__class__ != list:
                return {'message': 'O campo "tipos" deve ser uma lista de int.'}, 400
            for tipo in filtro['tipos']:
                if tipo.__class__ != int:
                    return {'message': 'O campo "tipos" deve ser uma lista de int.'}, 400

        return func(self, *args, **kwargs)
    return wrapper

def UsuarioAuthValidator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        campos = ['login', 'senha']
        filtro = request.get_json()
        filtroKeys = filtro.keys()

        for key in filtroKeys:
            if not key in campos:
                return  {'message': 'O campo "' + key + '" não é reconhecido. Campos conhecidos: ' + str(campos)}, 400 

        if (not 'login' in filtroKeys or filtro['login'].__class__ != str):
            return {'message': 'O campo "login" deve ser uma string.'}, 400
        
        if (not 'senha' in filtroKeys or filtro['senha'].__class__ != str):
            return {'message': 'O campo "senha" deve ser uma string.'}, 400

        return func(self, *args, **kwargs)
    return wrapper