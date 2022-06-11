from tokenize import Double
from bson import ObjectId
from flask_restful import Resource, reqparse

class RegiaoResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('_id', type=str, location='json')
        self.reqparse.add_argument('cep', type=str, location='json', required=True, help='O campo "cep" deve estar preenchido.')
        self.reqparse.add_argument('lat', type=float, location='json', required=True, help='O campo "lat" deve estar preenchido.')
        self.reqparse.add_argument('lon', type=float, location='json', required=True, help='O campo "lon" deve estar preenchido.')
        self.reqparse.add_argument('nome', type=float, location='json', required=True, help='O campo "nome" deve estar preenchido.')
        self.reqparse.add_argument('usuariosId', type=list, location='json')
        super(RegiaoResource, self).__init__()
    
    
