# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class DelServiceUserWizard(models.TransientModel):
    _name = "usermanagement.delserviceuserwizard"
    _description = "Eliminar Servicio a Usuario"
    #_rec_name = 'grupos'

    @api.multi
    def do_del_service_user_button(self):
        self.ensure_one()
        # implementar aqui
        if self.users and self.services:
            for user in self.users:
                for service in self.services:
                    _logger.error("user: %s", user)
                    _logger.error("service: %s", service)
                    self.del_service_from_user(user, service)
        else:
            raise ValidationError("Debe seleccionarse mínimo un usuario y un servicio.")
                    
        return {'type': 'ir.actions.act_window_close'}

    services = fields.Many2many('usermanagement.servicio', string='Grupos del Sistema')
    users = fields.Many2many('usermanagement.usuario', string='Usuarios')
    notes = fields.Text('Notas')

    def del_service_from_user(self, user, service):
        if user.observacion != False:
            obs = user.observacion+'\n'+self.notes
            user.write({'observacion': obs})
        else:
            user.write({'observacion': self.notes})
        self.env['usermanagement.ususerv'].search([('usuario_id', '=', user.id), ('servicio_id', '=', service.id)]).unlink()
    
    def do_restore_service_user_button(self):
        if self.users:
            for user in self.users:
                user.recalculate_services()
        else:
            raise ValidationError("No se ha seleccionado ningún usuario.")