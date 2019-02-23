# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
from odoo.modules import get_module_resource
import re
import logging
_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"
