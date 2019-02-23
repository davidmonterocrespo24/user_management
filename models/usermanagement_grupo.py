# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
import logging
_logger = logging.getLogger(__name__)

class Grupo(models.Model):
    _name = 'usermanagement.grupo'
    _description = 'Grupo'
    _rec_name = 'nombre'
    
    nombre = fields.Char('Nombre', required=True)
    tiempo_expiracion = fields.Date('Expira')
    cuota = fields.Integer('Cuota')
    descripcion = fields.Text('Descripcion')
    #relational fields
    usuarios_ids = fields.Many2many('usermanagement.usuario', string="Usuarios")
    #compute fields
    cant_user = fields.Integer(string='Usuarios', compute="_calcular_usuarios", store=False)


    _sql_constraints = [(
        'nombre_unique',
        'UNIQUE (nombre)',
        'El grupo ya existe.'
    )]
   
    @api.one
    @api.constrains('tiempo_expiracion')
    def _check_expiration_date(self):
        if self.tiempo_expiracion:
            today = datetime.today()
            if today >= datetime.strptime(self.tiempo_expiracion, "%Y-%m-%d"):
                raise ValidationError('La fecha escogida ya expiró.')

    def _calcular_usuarios(self):
        for group in self:
            group.cant_user = self.env['usermanagement.usuario'].search_count([('grupo_ids', '=', group.id)])


    @api.multi
    def write(self, values):
        if 'cuota' in values.keys():
            val_cuota = {'cuota': values['cuota']}
            if 'usuarios_ids' not in values.keys():
                for user in self.usuarios_ids:
                    _logger.error("user: %s", user)
                    if user.cuota < values['cuota']:
                        user.write(val_cuota)
            else:
                for user in values['usuarios_ids']:
                    us = self.env['usermanagement.usuario'].search([('id', '=', user)])
                    if us.cuota < values['cuota']:
                        us.write(val_cuota)
        return super(Grupo, self).write(values)

    @api.multi
    def unlink(self):
        for grupos in self:
            for user in grupos.usuarios_ids:
                user_groups = self.env['usermanagement.grupo'].search([('usuarios_ids', '=', user.id), ('id', 'not in', self.ids)])
                new_cuota = self.find_bigger(user_groups)
                if user.cuota == grupos.cuota:
                    val_cuota = {'cuota': new_cuota}
                    user.write(val_cuota)
        return super(Grupo, self).unlink()
    def find_bigger(self, grupos):
        bigger = 0
        if grupos:
            for grupo in grupos:
                if grupo.cuota > bigger:
                    bigger = grupo.cuota
        return bigger
