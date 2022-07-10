from flask_restful import Api
from resources.avisoResource import AvisoList, AvisoSave
from resources.feedbackResource import FeedbackList, FeedbackSave
from resources.usuarioResource import UsuarioAuth, UsuarioList, UsuarioSave
from .regiaoResource import RegiaoSave, RegiaoList

def initialize_routes(api: Api):
    api.add_resource(RegiaoSave, '/api/regiao/save')
    api.add_resource(RegiaoList, '/api/regiao/list')
    api.add_resource(UsuarioSave, '/api/usuario/save')
    api.add_resource(UsuarioList, '/api/usuario/list')
    api.add_resource(UsuarioAuth, '/api/usuario/auth')
    api.add_resource(AvisoSave, '/api/aviso/save')
    api.add_resource(AvisoList, '/api/aviso/list')
    api.add_resource(FeedbackSave, '/api/feedback/save')
    api.add_resource(FeedbackList, '/api/feedback/list')
