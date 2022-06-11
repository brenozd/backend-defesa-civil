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
            print(Regiao.objects(cep="12061100").order_by('-cep'))
        except Exception as e:
            return {'message': 'Erro ao listar regioes - %x' % str(e)}, 500
