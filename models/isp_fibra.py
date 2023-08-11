from odoo import fields, models, api
from datetime import timedelta, datetime

class IspFibra(models.Model):
    _name = "isp.fibra"
    _description = "Conexión Fibra / Wimax"

    partner_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = 'Titular'
    )

    name = fields.Selection(
        selection = [
        ('S150', 'Fibra 150 Mbps'),
        ('S300', 'Fibra 300 Mbps'),
        ('S600', 'Fibra 600 Mbps'),
        ('S1000', 'Fibra 1000 Mbps'),
        ('W30', 'Wimax 30 Mbps'),
        ('W50', 'Wimax 50 Mbps'),
        ('W100', 'Wimax 100 Mbps'),
        ('V100', 'Vodafone 100 Mbps'),
        ('V300', 'Vodafone 300 Mbps'),
        ('V600', 'Vodafone 600 Mbps'),
        ('A300', 'Avanza 300 Mbps'),
        ('A600', 'Avanza 600 Mbps'),
        ('A1000', 'Avanza 1000 Mbps'),
        ],
        required = True,
        string = 'Tarifa'
    )

    fecha_alta = fields.Datetime(
        string = 'Fecha Alta',
        default = datetime.now()
    )
    fecha_baja = fields.Datetime(
        string = 'Fecha Baja'
    )

    estado = fields.Selection(
        selection = [
            ('00', 'Pendiente alta'),
            ('01', 'Activado'),
            ('02', 'Baja'),
        ],
        required = True,
        default = '01',
        string = 'Estado'
    )

    permanencia = fields.Selection(
        selection = [
            ('12', '12 meses'),
            ('18', '18 meses'),
        ],
        default = '18',
        string = 'Permanencia'
    )

    fin_permanencia = fields.Date(
        compute = '_compute_permanencia',
        string = 'Fin Permanencia'
    )

    @api.depends('permanencia', 'fecha_alta')
    def _compute_permanencia(self):
        for record in self:
            if record.permanencia == '12':
                dias = timedelta(365)
                record.fin_permanencia = record.fecha_alta + dias
            elif record.permanencia == '18':
                dias = timedelta(548)
                record.fin_permanencia = record.fecha_alta + dias
            else:
                record.fin_permanencia = ''