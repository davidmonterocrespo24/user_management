# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class Servicio(models.Model):
    _name = 'usermanagement.servicio'
    _description = 'Servicio'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre', required=True)
    descripcion = fields.Text('Descripción')
    grupos_ids = fields.Many2many('usermanagement.grupo', string="Grupos")
    cant_users = fields.Integer(string="Usuarios", compute="_calcular_usuarios", store=False)
    usuarios_ids = fields.Many2many('usermanagement.usuario', string="Usuarios")


    def _calcular_usuarios(self):
        for servicio in self:
            servicio.cant_users = self.env['usermanagement.usuario'].search_count([('servicio_ids', '=', servicio.id)])
