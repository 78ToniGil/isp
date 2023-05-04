from odoo import fields, models, api

class line(models.Model):
    _name = "isp.line"
    _description = "Lineas de telefono"

    name = fields.Integer(
        string = 'Teléfono',
        required = True,
        hint = 'Número de Teléfono'
    )

    partner_id = fields.Many2one(
        comodel_name = 'res.partners',
        string = 'Titular'
    )

    tarifa = fields.Selection(
        selection = [
        ('10Gb', 'Ilimitadas y 10Gb de datos'),
        ('24Gb', 'Ilimitadas y 24Gb de datos'),
        ('50Gb', 'Ilimitadas y 50Gb de datos'),
        ('90Gb', 'Ilimitadas y 90Gb de datos'),
        ('150Gb', 'Ilimitadas y 150Gb de datos'),
        ('30Gb', 'Ilimitadas y 30Gb de datos'),
        ('50Gb', 'Ilimitadas y 50Gb de datos'),
        ('70Gb', 'Ilimitadas y 70Gb de datos'),
        ],
        default = '24Gb'
    )

    operador = fields.Char(
        compute = '_compute_operador',
        required = True
    )

    @api.depends(tarifa)
    def _compute_operador(self):
        for record in self:
            switch record.tarifa