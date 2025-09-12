from odoo import models, fields

class Filme(models.Model):
    _name = 'locadora.filme' # Nome técnico do modelo
    _description = 'Cadastro de Filmes'

    name = fields.Char(string='Título', required=True)
    diretor = fields.Char(string='Diretor')
    ano = fields.Integer(string='Ano de Lançamento')
    genero = fields.Char(string='Gênero')
    unidades = fields.Integer(string='Unidades Disponíveis', default=1)