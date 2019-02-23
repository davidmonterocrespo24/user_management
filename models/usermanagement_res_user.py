# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
import logging
_logger = logging.getLogger(__name__)


class res_user(models.Model):
    _inherit = 'res.users'

    # for own purposes
    area = fields.Char(string='Area', invisible=True, compute='_compute_area')

    def _compute_area(self):
        user = self.env['usermanagement.usuario'].search([('nombre_usuario', '=', self.login)])
        if user:
            self.area = user.area_id.nombre
        else:
            self.area = False
    



