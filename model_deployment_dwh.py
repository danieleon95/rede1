
principal_path = r'C:\Rede'

import pandas as pd
import random
import sys

def rec_disp(actividad,entidad_fin,zona_com,zona_tec):           

    opciones = ['ESTANDAR','PAGOS_PERIODICOS','MPOS','QRCODE_ESTATICO','QRCODE_DINAMICO','EPOS','OTROS']

    rand = random.randint(0,len(opciones))
    
    recomendaciones = [opciones[rand],opciones[rand-1]]    
    
    return recomendaciones

if __name__ == "__main__":   
        salida = rec_disp(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
        print(salida)
