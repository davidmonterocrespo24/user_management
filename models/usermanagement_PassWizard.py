# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class PassWizard(models.TransientModel):
    _name = 'usermanagement.passwizard'
    _description = u'Cambiar Contraseña'

    def _default_user_id(self):
        #user = self.env['usermanagement.usuario'].browse(self.user_id)
        user_id = self._context.get('active_model') == 'usermanagement.usuario' and self._context.get('active_ids') or []
        #user = self.env['usermanagement.usuario'].search([('id', 'in', user_id)])
        #_logger.error('user_id: %s', user)
        return [
            (0, 0, {'user': user.id})
            for user in self.env['usermanagement.usuario'].browse(user_id)
        ]

    users = fields.One2many('usermanagement.changepassuser', 'wizard_id', string='Usuario', default=_default_user_id)

    @api.multi
    def do_change_pass_button(self):
        self.ensure_one()
        self.users.do_change_pass_button()
        #if self.env.user in self.mapped('users.user'):
        #    return {'type': 'ir.actions.client', 'tag': 'reload'}
        return {'type': 'ir.actions.act_window_close'}

class ChangePassUser(models.TransientModel):
    _name = 'usermanagement.changepassuser'
    _description = u'Cambiar Contraseña'

    wizard_id = fields.Many2one('usermanagement.passwizard', string='Cambiar Contraseña')
    user = fields.Many2one('usermanagement.usuario', string='Usuario', readonly=True)
    #old_pass = fields.Char('Contraseña actual', invisible=True)
    new_pass = fields.Char('Nueva Contraseña', invisible=True)

    @api.multi
    def do_change_pass_button(self):
        for line in self:
            #if line.user.contrasena != line.old_pass:
            #    raise ValidationError('Contraseña actual errónea.')
            #else:
            #    line.user.write({'contrasena': line.new_pass})
            if line.new_pass == False:
                raise ValidationError("Contraseña nueva no válida.")
            else:
                line.user.write({'contrasena': line.new_pass})
        self.write({'old_pass': False, 'new_pass': False})
        #raise ValidationError('entre')
        return