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
            return {"resultado": self.listById(body)}, 200
        except Exception as e:
            return {'message': 'Erro ao listar regioes - ' + str(e)}, 500
    
    def listById(self, filtro):
        ids = [ObjectId(id) for id in filtro['ids']]
        resultado = [Regiao.objects2dto(obj) for obj in json.loads(Regiao.objects(id__in=ids).to_json())]
        return resultado
