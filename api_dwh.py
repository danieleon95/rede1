
from flask import Flask
from flask_restx import Api, Resource, fields
from model_deployment_dwh import rec_disp

app = Flask(__name__)

api = Api(
    app, 
    title='Recomendación de tecnología a instalar - nuevos comercios Redeban',
    description='''Listado de tecnologías recomendadas para nuevos comercios a partir de sus
                   características geográficas y económicas''')

ns = api.namespace('rec-disp', 
     description='Recomendación de tecnología a instalar')

parser = api.parser()

parser.add_argument(
    'actividad',
    choices=['VENTAS  MINORISTAS GENERALES', 'RESTAURANTES','TIENDAS DE DEPARTAMENTOS Y ALI', 'ELECTRODOMESTICOS  Y ELECTRONI',
             'SERVICIOS PROFESIONALES', 'EDUCACION', 'COMIDA RAPIDA','AUTOMOTORES', 'SERVICIOS DE SALUD', 'DROGUERIAS',
             'CARGA,  SERVICIO  DE MENSAJERA', 'COMERCIO MISCELANEO','EVENTOS', 'AGENCIAS DE VIAJE', 'PAGOS E IMPUESTOS',
             'HOTELES Y CLUBES SOCIALES', 'MERCADEO DIRECTO','TRANSPORTE DIARIO', 'GRANDES CADENAS MINORISTAS',
             'COMUNICACIONES', 'ESTACIONES DE COMBUSTIBLE', 'PAGOS PERSONALES','BENEFICENCIAS', 'AEROLINEAS', 'CADENAS MINORISTAS',
             'KIOSKOS','SERVICIOS PUBLICOS', 'SIN CATALOGAR'],
    type=str, 
    required=True, 
    help='Actividad economica', 
    location='args')

parser.add_argument(
    'entidad_fin', 
    choices=['AV Villas','Banco Agrario','Banco de Bogota','Banco de Occidente','Banco Pichincha','Bancolombia','BBVA','Colmena',
             'Colpatria','Coomeva','Davivienda','GNB Sudameris','Itau'],
    type=str, 
    required=True, 
    help='Entidad financiera', 
    location='args')

parser.add_argument(
    'zona_com',
    choices=['Zona 0','Zona 1','Zona 2','Zona 3','Zona 4','Zona 5','Zona 6','Zona 7','Zona 8','Sin asignar'],
    type=str, 
    required=True, 
    help='Zona comercial', 
    location='args')

parser.add_argument(
    'zona_tec',
    choices=['Zona 0','Zona 1','Zona 2','Zona 3','Zona 4','Zona 5','Zona 6','Zona 7','Zona 8','Zona 9','Zona 11','No definida'],
    type=str, 
    required=True, 
    help='Zona tecnica', 
    location='args')

resource_fields = api.model('Resource', {
    'respuesta': fields.String,
})

@ns.route('/')
class DSApi(Resource):
    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)

    def get(self):
        args = parser.parse_args()
        salida = rec_disp(args.actividad,args.entidad_fin,args.zona_com,args.zona_tec)
        return {
         'respuesta': salida
        }, 200
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
