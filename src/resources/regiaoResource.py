import json
from bson import ObjectId
from flask import request
from database.model import Regiao
from flask_restful import Resource
from .validators import RegiaoValidator, RegiaoFiltroValidator

class RegiaoSave(Resource):
    @RegiaoValidator
    def post(self):
        try:
            body = request.get_json()
            if 'id' in body.keys():
                objects = Regiao.objects(id=ObjectId(body['id']))
                if len(objects) == 0:
                    return {'message': 'Região não encontrada.', 'id':str(body['id'])}, 400
                id = body['id'] 
                del body['id']
                objects.update_one(**body)
                return {'message': 'Região editada com sucesso.', 'id':str(id)}, 200
            else:
                regiao = Regiao(**Regiao.ws2document(body)).save()
                id = regiao.id
                return {'message': 'Região salva com sucesso.', 'id':str(id)}, 200
        except Exception as e:
            return {'message': 'Erro ao salvar regiao - %x' % str(e)}, 500


class RegiaoList(Resource):    
    @RegiaoFiltroValidator
    def post(self):
        try:
            body = request.get_json()
            return {"resultado": Regiao.list(body)}, 200
        except Exception as e:
            return {'message': 'Erro ao listar regioes - ' + str(e)}, 500
        
