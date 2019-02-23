# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UsuServ(models.Model):
    _name = 'usermanagement.ususerv'

    usuario_id = fields.Many2one('usermanagement.usuario')
    servicio_id = fields.Many2one('usermanagement.servicio')