from bson import ObjectId
from flask import request
from database.model import Usuario
from flask_restful import Resource
from .validators import UsuarioValidator, UsuarioFiltroValidator

class UsuarioSave(Resource):
    @UsuarioValidator
    def post(self):
        try:
            body = request.get_json()
            if 'id' in body.keys():
                objects = Usuario.objects(id=ObjectId(body['id']))
                if len(objects) == 0:
                    return {'message': 'Usuário não encontrado.', 'id':str(body['id'])}, 400
                id = body['id'] 
                del body['id']
                objects.update_one(**body)
                return {'message': 'Usuário editado com sucesso.', 'id':str(id)}, 200
            else:
                usuario = Usuario(**Usuario.ws2document(body)).save()
                id = usuario.id
                return {'message': 'Usuário salvo com sucesso.', 'id':str(id)}, 200
        except Exception as e:
            return {'message': 'Erro ao salvar usuário - ' + str(e)}, 500


class UsuarioList(Resource):    
    @UsuarioFiltroValidator
    def post(self):
        try:
            body = request.get_json()
            return {"resultado": Usuario.list(body)}, 200
        except Exception as e:
            return {'message': 'Erro ao listar usuários - ' + str(e)}, 500
        
