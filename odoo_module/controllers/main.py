import json
from odoo import http
from odoo.http import request

class FilmeController(http.Controller):

    @http.route('/api/filmes', auth='public', methods=['GET'], csrf=False, type='http')
    def get_filmes(self, **kw):
        """
        Retorna uma lista de todos os filmes cadastrados.
        """
        filmes_recs = request.env['locadora.filme'].search([])
        filmes_data = []
        for filme in filmes_recs:
            filmes_data.append({
                'id': filme.id,
                'titulo': filme.name,
                'diretor': filme.diretor,
                'ano': filme.ano,
                'genero': filme.genero,
                'unidades': filme.unidades,
            })
        return request.make_response(
            json.dumps(filmes_data),
            headers={'Content-Type': 'application/json'}
        )

    @http.route('/api/filmes', auth='public', methods=['POST'], csrf=False, type='json')
    def create_filme(self, **kw):
        """
        Cria um novo filme.
        """
        data = request.jsonrequest
        vals = {
            'name': data.get('titulo'),
            'diretor': data.get('diretor'),
            'ano': data.get('ano'),
            'genero': data.get('genero'),
            'unidades': data.get('unidades'),
        }
        novo_filme = request.env['locadora.filme'].create(vals)
        return {'id': novo_filme.id, 'status': 'Filme criado com sucesso!'}