
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import load_model

def rec_disp(Nm_Tipo_Comercio,Nm_Zona_Comercial,Nm_Zona_Tecnica,Nm_Ent_Finan,
             Nm_Tipo_Afil,Actividad_Consolidada,MCC_Normal,Longitud_Ubicacion_Comercio,
             Latitud_Ubicacion_Comercio):

### parametros de entrada:
    ## caracteristicas del comercio, 9 variables en total. 7 categoricas y 2 numericas    
### informacion de salida:
    ## diccionario con el top 3 de las recomendaciones para el nuevo comercio
        
## creacion dataframe con variables de entrada
    data = pd.DataFrame(np.array([[Nm_Tipo_Comercio,Nm_Zona_Comercial,Nm_Zona_Tecnica,
                                   Nm_Ent_Finan,Nm_Tipo_Afil,Actividad_Consolidada,
                                   MCC_Normal,Longitud_Ubicacion_Comercio,Latitud_Ubicacion_Comercio]]),
                        columns=['Nm_Tipo_Comercio','Nm_Zona_Comercial','Nm_Zona_Tecnica',
                                 'Nm_Ent_Finan','Nm_Tipo_Afil','Actividad_Consolidada',
                                 'MCC_Normal','Longitud_Ubicacion_Comercio','Latitud_Ubicacion_Comercio'])

### transformacion informacion ###
## conversion a dummies variables categoricas
    X = pd.get_dummies(data[['Nm_Tipo_Comercio','Nm_Zona_Comercial','Nm_Zona_Tecnica',
                           'Nm_Ent_Finan','Nm_Tipo_Afil','Actividad_Consolidada','MCC_Normal']])
## normalizacion de variables numericas
    var_std = pd.DataFrame(StandardScaler().fit_transform(data[['Longitud_Ubicacion_Comercio','Latitud_Ubicacion_Comercio']]),columns=['Longitud_Ubicacion_Comercio','Latitud_Ubicacion_Comercio'])
## merge de las variables de entrada
    X = X.merge(var_std,left_index=True,right_index=True,how='inner')
## lectura titulos columnas variables de entrada
    df = pd.read_csv("columnas_x.csv",sep=';')  
## append de la informacion de entrada con el total de variables dummies
    df = df.append(X).fillna(0)

## cargue modelo de redes neuronales entrenado
    model = load_model('mod_entrenado.h5')        

## prediccion valores de salida
    preds = model.predict(df)

## creacion diccionario con probabilidades para cada tecnologia
    d = {'EPOS':preds[0][0], 'INGENICO ICT 220':preds[0][1], 'INGENICO ICT 220 CTL':preds[0][2],
         'INGENICO ICT 250 CTL':preds[0][3], 'INGENICO IWL 220CTL-3G':preds[0][4], 'INGENICO IWL 250CTL -3G':preds[0][5],
         'INGENICO IWL281 CTL':preds[0][6], 'INGENICO MOVE / 2500':preds[0][7], 'INGENICO MOVE / 2500W':preds[0][8],
         'MINIDATAFONO M010':preds[0][9], 'NOTEC':preds[0][10], 'NOTRANS':preds[0][11], 'OTROS':preds[0][12]}

## seleccion del top 3 de tecnologias con mayor probabilidad
    top_3 = [(k,v) for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)][:3]

## creacion diccionario con tecnologias a recomendar t las probabilidades correspondientes
    recomendaciones = {}
    recomendaciones['lista'] = top_3
    
    return recomendaciones

if __name__ == "__main__":   
        recomendaciones = rec_disp(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],
                          sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9])
        print(recomendaciones)
