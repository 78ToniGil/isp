from odoo import fields, models, api
import requests

class IspLineaCDR(models.Model):
    _name = "isp.linea_cdr"
    _description = "CDR de Lineas de Telefono"

    tipo_cdr = fields.Selection(
        selection=[
            ('DAT', 'Datos'),
            ('SMS', 'SMS'),
            ('VOZ', 'Voz'),
        ],
        string='Tipo de CDR',
    )
    factura_numero = fields.Char(string='Número de Factura')
    telefono_numero = fields.Char(string='Número de Teléfono')
    destino_numero = fields.Char(string='Número de Teléfono Destino')
    origen_numero = fields.Char(string='Número de Teléfono Origen')
    fecha = fields.Date(string='Fecha')
    hora = fields.Char(string='Hora')
    duracion_segundos = fields.Integer(string='Duración en Segundos')
    tipo_llamada = fields.Char(string='Tipo de Llamada')
    importe = fields.Float(string='Importe')
    linea_id = fields.Many2one('isp.linea', string='Línea Asociada')

    @api.model
    def import_cdr_from_api(self, month, year):
        # URL y parámetros de la API
        url = "https://wscliente.airenetworks.es/ws/mv/gestMOVIL_2.php"
        params = {
            "user": "usuario",
            "pass": "contraseña",
            "mes": month,
            "anio": year,
            # Agregar otros parámetros necesarios
        }

        # Conexión a la API
        response = requests.get(url, params=params)
        response_data = response.json()

        # Procesamiento de la respuesta y creación/actualización de registros
        for item in response_data:
            # Buscar el CDR por algún identificador único, si existe
            cdr = self.search([('identificador', '=', item['identificador'])], limit=1)

            # Si el CDR no existe, crearlo
            if not cdr:
                self.create({
                    'tipo_cdr': item['tipo'],
                    'fecha': item['fecha'],
                    'hora': item['hora'],
                    'origen_numero': item['origen'],
                    'destino_numero': item['destino'],
                    'tipo_llamada': item['tipo_llamada'],
                    'duracion_segundos': item['duracion'],
                    'importe': item['importe'],
                    # Agregar otros campos según corresponda
                })
            else:
                # Si el CDR ya existe, actualizarlo
                cdr.write({
                    # Actualizar campos según corresponda
                })