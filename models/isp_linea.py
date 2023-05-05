from odoo import fields, models, api

class IspLinea(models.Model):
    _name = "isp.linea"
    _description = "Lineas de telefono"

    name = fields.Char(
        string = 'Teléfono',
        required = True
    )

    secuencia = fields.Integer()

    partner_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = 'Titular'
    )

    tarifa = fields.Selection(
        selection = [
        ('10Gb', 'Ilimitadas y 10Gb'),
        ('24Gb', 'Ilimitadas y 24Gb'),
        ('V50Gb', 'Ilimitadas y 50Gb'),
        ('90Gb', 'Ilimitadas y 90Gb'),
        ('150Gb', 'Ilimitadas y 150Gb'),
        ('30Gb', 'Ilimitadas y 30Gb'),
        ('50Gb', 'Ilimitadas y 50Gb'),
        ('70Gb', 'Ilimitadas y 70Gb'),
        ],
        required = True,
        string = 'Tarifa'
    )

    operador = fields.Char(
        compute = '_compute_operador',
        string = 'Cobertura'
    )

    @api.depends('tarifa')
    def _compute_operador(self):
        for record in self:
            if record.tarifa == '30Gb':
                record.operador = 'Movistar'
            elif record.tarifa == '50Gb':
                record.operador = 'Movistar'
            elif record.tarifa == '70Gb':
                record.operador = 'Movistar'
            else:
                record.operador = 'Vodafone'

    estado = fields.Selection(
        selection = [
            ('00', 'Pendiente alta'),
            ('01', 'Activado'),
            ('02', 'Cambio de titular'),
            ('03', 'Baja'),
            ('04', 'Portado'),
        ],
        required = True,
        default = '01',
        string = 'Estado'
    )

    fecha_alta = fields.Datetime(
        string = 'Fecha Alta'
    )
    fecha_baja = fields.Datetime(
        string = 'Fecha Baja'
    )

    iccid = fields.Char(
        string = 'ICCID'
    )

    puk = fields.Char(
        string = 'PUK'
    )

    fup = fields.Integer(
        compute = '_compute_fup',
        string = 'FUP'
    )

    @api.depends('tarifa')
    def _compute_fup(self):
        for record in self:
            if record.tarifa == '10Gb':
                record.fup = 7
            elif record.tarifa == '24Gb':
                record.fup = 9
            elif record.tarifa == 'V50Gb':
                record.fup = 11
            elif record.tarifa == '90Gb':
                record.fup = 13
            elif record.tarifa == '150Gb':
                record.fup = 9
            else:
                record.fup = 0