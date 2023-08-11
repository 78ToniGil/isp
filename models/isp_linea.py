from odoo import fields, models, api
from zeep import Client

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
        ('50Gb', 'Ilimitadas y 50Gb'),
        ('90Gb', 'Ilimitadas y 90Gb'),
        ('150Gb', 'Ilimitadas y 150Gb'),
        ('20Gb', 'Ilimitadas y 20Gb'),
        ('40Gb', 'Ilimitadas y 40Gb'),
        ('60Gb', 'Ilimitadas y 60Gb'),
        ('80Gb', 'Ilimitadas y 80Gb'),
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
            if record.tarifa == '20Gb':
                record.operador = 'Movistar'
            elif record.tarifa == '40Gb':
                record.operador = 'Movistar'
            elif record.tarifa == '60Gb':
                record.operador = 'Movistar'
            elif record.tarifa == '80Gb':
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
            elif record.tarifa == '50Gb':
                record.fup = 11
            elif record.tarifa == '90Gb':
                record.fup = 13
            elif record.tarifa == '150Gb':
                record.fup = 9
            else:
                record.fup = 0

    cdr_ids = fields.One2many('isp.linea_cdr', 'linea_id', string='CDRs Asociados')

    @api.model
    def import_lineas_from_api(self):
        # Configuración para la conexión SOAP
        WSDL_URL = 'https://wscliente.airenetworks.es/ws_desarrollo/mv/gestMOVIL_2.php?wsdl'
        params = {
            "user": "usuario",
            "pass": "contraseña",
            "pagina": 1,
            "registro": 10
            }
        
        # Crear el cliente Zeep para el servicio SOAP
        client = Client(WSDL_URL)

        # Llamar al método del servicio SOAP
        response = client.service.getLineas(datos = params)

        # Procesar la respuesta
        # Asumiendo que la respuesta tiene una estructura similar a la que vimos anteriormente
        if response and response.get('resultado') == '0':
            lineas = response.get('lineas', [])
            for linea_data in lineas:
                # Aquí procesas y guardas cada línea en la base de datos de Odoo
                pass
        else:
            # Manejar errores aquí
            pass