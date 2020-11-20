
from flask import Flask
from flask_restx import Api, Resource, fields
from model_deployment_dwh import rec_disp

## creacion app en flask donde se alojara la API
app = Flask(__name__)

api = Api(
    app, 
    title='Recomendación de tecnología a instalar - nuevos comercios Redeban',
    description='''Listado de tecnologías recomendadas para nuevos comercios a partir de sus
                   características geográficas y económicas''')

## definicion de la direccion en la url donde se alojara la API
ns = api.namespace('rec_disp', 
     description='Recomendación de tecnología a instalar')

## definicion de los parametros de entrada
parser = api.parser()

parser.add_argument(
    'tipo_comercio',
    choices=['Corresp Bancarios','Entidades Bancarias','Incocredito',
             'Internacional','RBM','Tarjeta Privada'],
    type=str, 
    required=True, 
    help='Tipo de comercio', 
    location='args')

parser.add_argument(
    'zona_comercial',
    choices=['ZONA COMERCIAL 0','ZONA COMERCIAL 1','ZONA COMERCIAL 2','ZONA COMERCIAL 3',
             'ZONA COMERCIAL 4','ZONA COMERCIAL 5','ZONA COMERCIAL 6','ZONA COMERCIAL 7',
             'ZONA COMERCIAL 8'],
    type=str, 
    required=True, 
    help='Zona comercial', 
    location='args')

parser.add_argument(
    'zona_tecnica',
    choices=['ZONA TECNICA 0','ZONA TECNICA 1','ZONA TECNICA 2','ZONA TECNICA 3',
             'ZONA TECNICA 5','ZONA TECNICA 6','ZONA TECNICA 7','ZONA TECNICA 8',
             'ZONA TECNICA 11'],
    type=str, 
    required=True, 
    help='Zona tecnica', 
    location='args')

parser.add_argument(
    'entidad_financiera', 
    choices=['AVVILLAS                                          ',
             'BANCO AGRARIO                                     ',
             'BANCO DE BOGOTA                                   ',
             'BANCO DE OCCIDENTE                                ',
             'BANCO PICHINCHA                                   ',
             'BANCOLOMBIA                                       ',
             'BBVA                                              ',
             'COLMENA                                           ',
             'COLPATRIA                                         ',
             'DAVIVIENDA 0051                                   ',
             'GNB SUDAMERIS S.A.                                ',
             'ITAU                                              ',
             'No_Aplica',
             'TEMPORARL SIN ADQUIRIENTE                         '],
    type=str, 
    required=True, 
    help='Entidad financiera', 
    location='args')

parser.add_argument(
    'tipo_afiliacion',
    choices=['Asesor Comercial', 'Entidad Emisora'],
    type=str, 
    required=True, 
    help='Tipo afiliacion', 
    location='args')

parser.add_argument(
    'actividad_consolidada',
    choices=['AEROLINEAS','AGENCIAS DE VIAJE','AUTOMOTORES','BENEFICENCIAS',
             'CADENAS MINORISTAS',
             'CARGA,  SERVICIO  DE MENSAJERA','COMERCIO MISCELANEO--TODOS  LO',
             'COMIDA RAPIDA','COMUNICACIONES','DROGUERIAS','EDUCACION',
             'ELECTRODOMESTICOS  Y ELECTRONI','ESTACIONES DE COMBUSTIBLE','EVENTOS',
             'GRANDES CADENAS MINORISTAS','HOTELES Y CLUBES SOCIALES','KIOSKOS',
             'MERCADEO DIRECTO','PAGOS E IMPUESTOS','PAGOS PERSONALES','RESTAURANTES',
             'SERVICIOS DE SALUD','SERVICIOS PROFESIONALES','TIENDAS DE DEPARTAMENTOS Y ALI',
             'TRANSPORTE DIARIO','VENTAS  MINORISTAS GENERALES'],
    type=str, 
    required=True, 
    help='Actividad consolidada', 
    location='args')

parser.add_argument(
    'mcc_normal',
    choices=['ABOGADOS, SERVICIOS JURIDICOS','ACCESORIOS DE COSTURA','ACCESORIOS DEPORTIVOS',
             'ACCESORIOS FOTOGRAFIAS','AG MUDANZAS Y BODEGA','AGENCIAS DE VIAJE Y OPERADORES TURISTICOS',
             'AGENTES Y ADMINISTRADORES DE BIENES RAICES ALQUILE','ALARMAS Y SEGURIDAD',
             'ALM X DPTO CON SUPERMERCADO','ALM X DPTO SIN SUPERMERCADO',
             'ALMACENES DE CALZADO Y REMONTADORAS','ALMACENES DE DISCOS','ALMCENES DE TAPETES Y ALFOMBRAS',
             'ALQUILER PELICULAS-VIDEOJUEGOS','ALQUILER VEHICULOS NACIONALES',
             'ALQUILER VESTIDOS-DISFRACES','ALTERACIONES, REMIENDOS, COSTURERAS, SASTRES',
             'ARTESANIAS EN GENERAL','ARTICULOS DE OFICINA','ARTICULOS DEPORTIVOS',
             'ARTICULOS PARA COSTURA Y OTROS ARTICULOS TEXTILES','ARTICULOS PARA EL HOGAR',
             'ARTICULOS PERECEDEROS (NO CLASIFICADOS EN OTRO LUG','ASEO Y MANTENIMIENTO-INMUEBLES',
             'ASOCIACIONES PROFESIONALES-GREMIOS','AVIANCA','BANDAS-ORQUESTAS-DIVERSION',
             'BARES,TABERNAS Y DISCOTECAS','BICICLETAS REP-VENTA','BIENES  DIGITALES--MEDIOS  AUDIOVISUALES  INCLUIDO',
             'BIENES DIGITALES--APLICACIONES DE SOFTWARE (EXCLUI','BIENES DIGITALES-CATEGORIAS MULTIPLES',
             'CACHARRERIAS','CAMPOS DE ATLETISMO, DEPORTES COMERCIALES','CENTROS EDUCATIVOS',
             'CENTROS Y OFICINAS DE SERVICIOS METALURGICOS','CIAS.DE AVIACION NAL','CIGARRERIAS-LICORES',
             'CLINICAS-HOSPITALES','CLUBES SOCIAL-DEPORTIVO','COMBUSTIBLES-NO GASO',
             'COMERCIO DE CATALOGO','COMERCIO MERCADEO DIRECTO','COMIDAS RAPIDAS,OTRAS',
             'CONTRATISTAS DE AISLAMIENTO, ALBANILERIA, ENYESADO','CONTRATISTAS GENERALESâ??EDIFICIOS RESIDENCIALES',
             'CONTRATISTAS, OFICIOS ESPECIALES NO CLASIFICADOS E','COOPERATIVAS AGRICOLAS',
             'CORREO Y ENCOMIENDAS','COSMETICOS Y PERFUMERIA','CUASI EFECTIVOÃ?COMERCIO',
             'CUERO Y DEMAS ACCESORIOS','DENTISTAS, ORTODONCISTAS','DOCTORES (NO CLASIFICADOS EN OTRO LUGAR)',
             'DROGUERIAS-TIENDA NATURAL','DULCERIAS','ELECTRODOMESTICOS','EMPRESAS ARRENDA. EQUIPOS',
             'EQUIPAMIENTO MISCELANEO AUTOMOVILES AVIONES AGR','EQUIPO  PARA  OFICINAS,  FOTOGRAFIA,  FOTOCOPIAS',
             'EQUIPO Y MATERIALES DE FERRETERIA','EQUIPOS MUSICALES','ESCUELAS Y SERVICIOS EDUCACIONALES NO CLASIFICADOS',
             'ESPECTACULOS BOLETAS-ABONOS','ESTABLECIMIENTOS-DIVERSION','ESTACIONAMIENTOS Y GARAJES DE AUTOMOVILES',
             'ESTACIONES DE SERVICIO','EVENTOS,FIESTAS,BANQUETES','FARMACOS, ESPECIALIDADES FARMACEUTICAS Y ARTICULOS',
             'FERREELECTRICOS','FLORISTERIAS','FOTOCOPIAS-EDITORIALES','GALERIAS ARTE-MARQUETERIAS',
             'GIMNASIOS','GRILES,WHISKERIAS,OTROS','HARDWARE COMPUTADOR','HOTEL HILTON',
             'HOTELES MELIA','HOTELES NACIONALES','IMPUESTOS NACIONALES Y MUNIPALES',
             'INSTITUCION FINANCIERA CLIENTE--MERCANCIA Y SERVIC','INSTITUT-FINANCIERAS',
             'INSTRUMENTOS MEDICOS-ODONTOLOGICOS','INSUMOS Y EQUIPOS INDUSTRIALES',
             'JOYERIAS-RELOJERIAS','JUGUETERIA Y DEMAS','LABORATORIOS MEDICOS Y DENTALES',
             'LAVADO AUTOS','LIBRERIAS-PAPELERIAS','LIMPIEZA DE ALFOMBRAS Y DE TAPICERIA',
             'MANTENIMIENTO Y ACCESORIOS ELECTRICOS','MATERIAL-CONSTRUCCION','MATERIALES_INDUSTRIALES_NO CLASIFICADOS_EN_OTRO',
             'MERCADEO AEROLINEAS','MERCADEO DE  SEGUROS','MOTELES,ESTADEROS-AMOBLADOS',
             'MUEBLES PARA HOGAR','OPTICAS, PRODUCTOS DE LAS OPTICAS Y LENTES','ORGANIZACIONES DE CARIDAD-SOCIAL',
             'ORGANIZACIONES RELIGIOSAS','PANADERIAS Y REPOSTE','PAPEL COLGADURA','PARABOL-COMUN CABLE',
             'PERFUMERIAS Y COSMETICOS','PIEZAS Y EQUIPOS ELECTRICOS','PISCINAS VENTAS SERVICIOS',
             'PRENDERIAS-COMPRAVENTA','PRODUCTOS QUIMICOS','PROFESIONALES  DE  LA  SALUD,  SERVICIOS  MEDICOS',
             'PROGRAMACION DE COMPUTADORES','QUIROPRACTICOS','REGALOS Y CACHARRERIAS',
             'REP MISCELANEAS','RESTAURANTES Y DEMAS','SALON BELLEZA-BARBERIAS',
             'SALSAMENTARIA LACTEO','SEGUROS/MEDICINA PREPAGADA','SERVICIO DE  AMBULANCIA',
             'SERVICIOS DE ASESORIA PROFESIONAL','SERVICIOS DE CONTABILIDAD, AUDITORIA Y TENEDURIA D',
             'SERVICIOS DE CUIDADO DE NINOS','SERVICIOS DE EXTERMINACION Y DE DESINFECCION',
             'SERVICIOS DE LIMPIEZA, PRENDAS DE VESTIR Y DE LAVA','SERVICIOS DE PAISAJISMO Y HORTICULTURA',
             'SERVICIOS DE TRANSPORTE NO CLASIFICADOS EN OTRO LU','SERVICIOS FUNERARIOS Y CREMATORIOS',
             'SERVICIOS PROFESIONALES NO CLASIFICADOS EN OTRO LU','SERVICIOS PUBLICIDAD-MEDIOS',
             'SERVICIOS PUBLICOS','SERVICIOS VETERINARIOS','SUMINISTROS Y PIEZAS NUEVAS PARA VEHICULOS A MOTOR',
             'SUPERMERCADOS','SUSCRIPCIONES- PERIODICOS - REVISTAS','TALLERES DE REPARACION DE CARROCERIA DE AUTOMOVILE',
             'TALLERES DE SERVICIO AUTOMOTRIZ','TEATROS Y EVENTOS CULTURALES','TELEMERCADEO',
             'TELEMERCADEO-CORREO','TIENDAS  DE  MASCOTAS ALIMENTOS  Y  ARTICULOS  PAR',
             'TIENDAS DE MATERIALES DE ARTE, ARTESANIA','TIENDAS DE NEUMATICOS PARA VEHICULOS',
             'TIENDAS DE REPUESTOS Y ACCESORIOS PARA AUTOMOVILES','TIENDAS DE ROPA Y ACCESORIOSâ??MISCELANEAS',
             'TRANSACCIONES DE JUEGOS DE AZAR','TRANSP DE PASAJEROS','UNIFORMES Y ROPA COMERCIAL PARA LA FAMILIA',
             'VENDEDORES  DE  AUTOMOVILES  Y CAMIONES--ARRENDAMI','VENDEDORES DE BOTES',
             'VENTA DE EQUIPOS ELECTRONICOS','VENTA SOFTWARE COMPUTADORES','VENTAS DE EQUIPO DE TELECOMUNICACIONES INCLUYENDO',
             'VENTAS PUERTA A PUERTA','VESTUARIO CABALLERO','VESTUARIO FAMILIAR','VESTUARIO-ARTICULOS-NINOS',
             'VIDRIERIAS Y ESPEJOS'],
    type=str, 
    required=True, 
    help='MCC normal', 
    location='args')

parser.add_argument(
    'longitud_ubicacion',
    type=float, 
    required=True, 
    help='Longitud ubicacion comercio', 
    location='args')

parser.add_argument(
    'latitud_ubicacion',
    type=float, 
    required=True, 
    help='Latitud ubicacion comercio', 
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
        recomendaciones = rec_disp(args.tipo_comercio,args.zona_comercial,args.zona_tecnica,
                          args.entidad_financiera,args.tipo_afiliacion,args.actividad_consolidada,
                          args.mcc_normal,args.longitud_ubicacion,args.latitud_ubicacion)
        return {
         'respuesta': recomendaciones
        }, 200
   
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
