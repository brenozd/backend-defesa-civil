from .regiaoResource import RegiaoSave, RegiaoList


def initialize_routes(api):
    api.add_resource(RegiaoSave, '/api/regiao/save')
    api.add_resource(RegiaoList, '/api/regiao/list')
