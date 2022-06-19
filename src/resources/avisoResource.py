from bson import ObjectId
from flask import request
from database.model import Aviso
from flask_restful import Resource
from .validators import AvisoValidator, AvisoFiltroValidator

class AvisoSave(Resource):
    @AvisoValidator
    def post(self):
        try:
            body = request.get_json()
            if 'id' in body.keys():
                objects = Aviso.objects(id=ObjectId(body['id']))
                if len(objects) == 0:
                    return {'message': 'Aviso não encontrado.', 'id':str(body['id'])}, 400
                id = body['id'] 
                del body['id']
                body = Aviso.findRegiao(body)
                objects.update_one(**body)
                return {'message': 'Aviso editado com sucesso.', 'id':str(id)}, 200
            else:
                aviso = Aviso(**Aviso.ws2document(body)).save()
                id = aviso.id
                return {'message': 'Aviso salvo com sucesso.', 'id':str(id)}, 200
        except Exception as e:
            return {'message': 'Erro ao salvar aviso - ' + str(e)}, 500


class AvisoList(Resource):
    @AvisoFiltroValidator
    def post(self):
        try:
            body = request.get_json()
            return {"resultado": Aviso.list(body)}, 200
        except Exception as e:
            return {'message': 'Erro ao listar avisos - ' + str(e)}, 500
        
