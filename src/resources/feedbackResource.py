from bson import ObjectId
from flask import request
from database.model import Feedback
from flask_restful import Resource
from .validators import FeedbackValidator, FeedbackFiltroValidator

class FeedbackSave(Resource):
    @FeedbackValidator
    def post(self):
        try:
            body = request.get_json()
            if 'id' in body.keys():
                objects = Feedback.objects(id=ObjectId(body['id']))
                if len(objects) == 0:
                    return {'message': 'Feedback não encontrado.', 'id':str(body['id'])}, 400
                id = body['id'] 
                del body['id']
                objects.update_one(**body)
                return {'message': 'Feedback editado com sucesso.', 'id':str(id)}, 200
            else:
                feedback = Feedback(**Feedback.ws2document(body)).save()
                id = feedback.id
                return {'message': 'Feedback salvo com sucesso.', 'id':str(id)}, 200
        except Exception as e:
            return {'message': 'Erro ao salvar feedback - %x' % str(e)}, 500


class FeedbackList(Resource):
    @FeedbackFiltroValidator
    def post(self):
        try:
            body = request.get_json()
            return {"resultado": Feedback.list(body)}, 200
        except Exception as e:
            return {'message': 'Erro ao listar feedbacks - ' + str(e)}, 500
        
