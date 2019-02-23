# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Dominio(models.Model):
    _name = 'usermanagement.dominio'
    _description = 'Dominio'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre', required=True)
    dominio = fields.Char('Dominio', required=True)
    descripcion = fields.Text('Descripción')

    @api.one
    @api.constrains('dominio')
    def _check_dom(self):
        pattern = "^@{1}([a-z]+\.(uo\.edu\.cu)$|(uo\.edu\.cu)$)"
        if self.dominio:
            if re.match(pattern, self.dominio) is None:
                raise ValidationError('Dominio de correo no válido.')
