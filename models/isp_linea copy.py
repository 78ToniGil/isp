from odoo import fields, models, api
from pysimplesoap.client import SoapClient

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
        # Credenciales de la API
        params= {
            "user": "B16911893",
            "pass": "im6Njghd8GezCr"
        }

        # Creación del cliente SOAP
        client = SoapClient(
            location="https://wscliente.airenetworks.es/ws_desarrollo/mv/gestMOVIL_2.php?wsdl",
            namespace='http://tempuri.org',
            timeout=60,
            soap_ns="soapenv",
            trace=False,
        )

        # Llamada al método SOAP
        response = client.call("getLineas", datos=params)
        
        # Eliminar esta comprobación cuando funciones
        print("Respuesta de la API", response)
        
        # Comprobar respuesta y procesar datos
        if response and 'linea' in response:
            for data_linea in response['linea']:
                # Buscamos si la línea ya existe en base a su número
                existing_linea = self.env['isp.linea'].search([('numero', '=', data_linea['numero'])], limit=1)
                
                vals = {
                    'numero': data_linea['numero'],
                    'nombre': data_linea['nombre'],
                    'estado': data_linea['estado'],
                    'tipo': data_linea['tipo'],
                    'plan': data_linea['plan'],
                    'fecha_alta': data_linea['fechaAlta'],
                    'fecha_baja': data_linea['fechaBaja'],
                    # ... (otros campos según corresponda)
                }
                
                if existing_linea:
                    # Si la línea ya existe, la actualizamos
                    existing_linea.write(vals)
                else:
                    # Si no existe, creamos una nueva línea
                    self.env['isp.linea'].create(vals)
