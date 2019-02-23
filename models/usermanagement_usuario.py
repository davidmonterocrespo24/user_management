# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
from odoo.modules import get_module_resource
import re
import logging

_logger = logging.getLogger(__name__)
try:
    from odoo.tools import image_colorize, image_resize_image_big
except:
    image_colorize = False
    image_resize_image_big = False


class Usuario(models.Model):
    _name = 'usermanagement.usuario'
    _description = 'Usuario'
    _rec_name = 'nombre_usuario'

    nombre = fields.Char('Nombre', required=True)
    apellidos = fields.Char('Apellidos', required=True)
    nombre_usuario = fields.Char('Usuario', required=True)
    cuota = fields.Integer('Cuota')
    direccion = fields.Char('Dirección')
    telefono = fields.Char('Teléfono')
    carnet_identidad = fields.Char('Carnet de Identidad', size=11)
    pasaporte = fields.Char('Pasaporte')
    extranjero = fields.Boolean('Extranjero')
    correo = fields.Char('Correo', required=True)
    foto = fields.Binary('Foto', default=lambda self: self._get_default_image())
    estado = fields.Selection(string='Estado', selection=[('activado', 'Activado'), ('desactivado', 'Desactivado')],
                              required=True)
    contrasena = fields.Char('Contraseña', invisible=True, required=True, copy=False)
    confirmar_contrasena = fields.Char('Confirmar Contraseña', copy=False, store=False)
    tiempo_expiracion = fields.Date('Expira')
    observacion = fields.Text('Observación')
    edit = fields.Boolean(default=False)
    

    # relational fields

    grupo_ids = fields.Many2many('usermanagement.grupo', string='Grupos')
    dominio_id = fields.Many2one('usermanagement.dominio', string='Dominio')
    servicio_ids = fields.Many2many('usermanagement.servicio', string='Servicios')
    log_ids = fields.Many2many('auditlog.log', string='LOG', compute="_calcular_log",
                                        store=False)
    @api.one
    def _calcular_log(self):
        log_ids = self.env['auditlog.log'].search([('name', '=', self.nombre_usuario)])
        for log in log_ids:
            self.log_ids |= log


            # @api.one
            # @api.constrains('tiempo_expiracion')
            # def _check_expiration_date(self):
            #    if self.tiempo_expiracion:
            #        today = datetime.today()
            #       if today >= datetime.strptime(self.tiempo_expiracion, "%Y-%m-%d"):
            #           raise ValidationError('La fecha escogida ya expiró.')

            # @api.one
            # @api.constrains('carnet_identidad')
            # def _check_CI(self):
            #     '''Method allow only numbers'''
            #     pattern = "^[0-9]+$"
            #     if self.carnet_identidad:
            #        if len(self.carnet_identidad) < 11:
            #            raise ValidationError('El Carnet de Identidad debe tener 11 carateres.')
            #         if re.match(pattern, self.carnet_identidad) is None:
            #            raise ValidationError('El Carnet de Identidad solo debe contener números.')

            # @api.one
            #  @api.constrains('extranjero', 'carnet_identidad', 'pasaporte')
            #  def _check_fill_passport_CI(self):
            #      if self.extranjero:
            #          if self.pasaporte is False:
            #              raise ValidationError('Debe ingresar el número de Pasaporte.')
            ##      else:
            #          if self.carnet_identidad is False:
            #             raise ValidationError('Debe ingresar el número de Carnet de Identidad.')

            # @api.one
            # @api.constrains('correo')
            # def _check_email(self):
            #     attributes = self.correo.split("@")
            #     attributes[1] = '@'+attributes[1]
            #     if self.nombre_usuario != attributes[0]:
            #         raise ValidationError('El campo Correo tiene errores con el nombre de usuario.')

    #    if self.dominio_id.dominio != attributes[1]:
    #        raise ValidationError('El campo Correo tiene problemas con el dominio especificado.')

    @api.one
    @api.constrains('contrasena')
    def _check_pass(self):
        if self.contrasena:
            if re.match('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{8,25}$', self.contrasena) is None or len(
                    self.contrasena) < 8 or len(self.contrasena) > 25:
                raise ValidationError(
                    "La contraseña debe tener entre 8 y 25 caracteres, una letra mayúscula, al menos una letra minúscula y un caracter numérico.")
                # raise ValidationError("dfd")

    @api.model
    def _get_default_image(self):
        '''Method to get default Image'''
        # added in try-except because import statements are in try-except
        try:
            img_path = get_module_resource('user_management', 'static',
                                           'avatar.png')
            with open(img_path, 'rb') as f:
                image = f.read()
            image = image_colorize(image)
            return image_resize_image_big(image.encode('base64'))
        except:
            return False

    @api.onchange('dominio_id', 'nombre_usuario')
    def _on_change_dominio(self):
        if self.nombre_usuario != False and self.dominio_id.dominio != False:
            self.correo = str(self.nombre_usuario) + str(self.dominio_id.dominio)

    @api.onchange('nombre', 'apellidos')
    def _on_change_usuario(self):
        # unidecode.unidecode(self.nombre)
        if self.nombre != False and self.apellidos != False:
            self.nombre_usuario = self.replace_chars(str(self.nombre.encode('utf-8')).split()[0].lower() + '.' + str(self.apellidos.encode('utf-8')).split()[0].lower())

    @api.onchange('grupo_ids')
    def _on_change_group(self):
        A = []
        B = []
        A.append(self.cuota)
        if self.grupo_ids:
            for group in self.grupo_ids:
                A.append(group.cuota)
                B.append(group.id)
            if A:
                self.cuota = int(max(A))


    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):

        values['edit'] = True
        if values['contrasena']:
            if values['confirmar_contrasena']:
                if values['contrasena'] != values['confirmar_contrasena']:
                    raise ValidationError('Las contraseñas deben coincidir.')
        res = super(Usuario, self).create(values)
        return res

    @api.multi
    def write(self, values):
        # if 'confirmar_contrasena' in values.keys():
        #    if self.contrasena != values['confirmar_contrasena']:
        #        raise ValidationError('Las contraseñas deben coincidir.')
        #system_user = self.env['res.users'].search([('login', '=', self.nombre_usuario)])
        #if system_user:
        #    if 'nombre_usuario' in values.keys():
        #        system_user.write({'login': values['nombre_usuario']})

        return super(Usuario, self).write(values)

    @api.multi
    def unlink(self):
        for user in self:
            system_user = self.env['res.users'].search([('login', '=', user.nombre_usuario)])
            if system_user:
                system_user.unlink()
        return super(Usuario, self).unlink()

    def replace_chars(self, _string):
        # black_list = ['á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú', 'ñ', 'Ñ']

        no_accent = _string

        if no_accent.find('á') != -1:
            no_accent = no_accent.replace('á', 'a')
        if no_accent.find('é') != -1:
            no_accent = no_accent.replace('é', 'e')
        if no_accent.find('í') != -1:
            no_accent = no_accent.replace('í', 'i')
        if no_accent.find('ó') != -1:
            no_accent = no_accent.replace('ó', 'o')
        if no_accent.find('ú') != -1:
            no_accent = no_accent.replace('ú', 'u')

        if no_accent.find('Á') != -1:
            no_accent = no_accent.replace('Á', 'A')
        if no_accent.find('É') != -1:
            no_accent = no_accent.replace('É', 'E')
        if no_accent.find('Í') != -1:
            no_accent = no_accent.replace('Í', 'I')
        if no_accent.find('Ó') != -1:
            no_accent = no_accent.replace('Ó', 'O')
        if no_accent.find('Ú') != -1:
            no_accent = no_accent.replace('Ú', 'U')

        if no_accent.find('Ñ') != -1:
            no_accent = no_accent.replace('Ñ', 'N')
        if no_accent.find('ñ') != -1:
            no_accent = no_accent.replace('ñ', 'n')

        if no_accent.find('\'') != -1:
            no_accent = no_accent.replace('\'', '')

        # raise ValidationError(no_accent)
        return no_accent

    def find_user(self, user_id):
        return self.env['usermanagement.usuario'].search([('nombre_usuario', '=', user_id)]).id

