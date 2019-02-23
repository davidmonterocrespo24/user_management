# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class SystemGroupWizard(models.TransientModel):
    _name = "usermanagement.systemgroupwizard"
    _description = "Usuarios del Sistema"
    #_rec_name = 'grupos'

    @api.multi
    def do_add_users_groups_button(self):
        self.ensure_one()
        # implementar aqui
        if self.system_groups:
            if self.users:
                for user in self.users:
                    self.add_system_user(user)
            
            if self.groups:
                for group in self.groups:
                    for user in group.usuarios_ids:
                        self.add_system_user(user)
                    
        return {'type': 'ir.actions.act_window_close'}

    system_groups = fields.Many2many('res.groups', string='Grupos del Sistema')
    users = fields.Many2many('usermanagement.usuario', string='Usuarios')
    groups = fields.Many2many('usermanagement.grupo', string='Grupos')

    #@api.onchange('groups')
    #def _on_change_groups(self):
    #    if self.groups:
    #        for group in self.groups:
    #            self.users += group.usuarios_ids
    #    #raise ValidationError('change!!!')
    

    def add_system_user(self, user):
        result = self.env['res.users'].search([('login', '=', user.nombre_usuario)])
        _logger.error('result_user: %s', result)
        if result:
            all_groups = result.groups_id + self.system_groups
            all_groups |= all_groups
            _logger.error('write: %s', all_groups)
            result.write({'groups_id': all_groups})
        else:
            values = {'login': user.nombre_usuario, 'groups_id': self.system_groups, 'password': user.contrasena, 'name':user.nombre+' '+user.apellidos}
            _logger.error('create: %s', values)
            self.env['res.users'].create(values)
            