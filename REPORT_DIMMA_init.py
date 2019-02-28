#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 02:36:42 2018

    La finalidad de este script es generar un informe que permita la correcta
    comparación entre las medidas obtenidas con el sistema DIMM (D1) y el
    sistema DIMMA (D2) para unas mismas fechas.
    La función de este script es convertir los fichero .txt en .csv, así como
    crear el generador de indica los ficheros que debe ser empleados con la 
    función Report(). Una vez devuelto el resultado, se modifican sus nombres
    de acuerdo a la cabecera de los archivos de entrada y se guardan en su
    correspondiente directorio.
    
@author: Fabricio Manuel Pérez Toledo
"""
#librearías usadas y otros scripts empleados.
import pandas as pd #Manejo de gran cantidad de datos.
import glob # Para poder usar todos los archivos de un directorio.
import re # Para cambiar nombres, directorios, etc.
from REPORT_DIMMA_func import * # Script encargado de generar cada report 
#de forma individual.
import os #Para cambiar nombre de archivos.


#Constantes
# Lista de nombres de columnas que sustituirán las generadas por defecto.
stand = ['Fecha','Ubicacion','Objeto','Seeing','Maire','Flujo1','Flujo2'\
         ,'Var_l','Var_t','Centelleo1','Centelleo2','r0l','r0t','fwhml'\
         ,'fwmlt','CCD','Software','Ventana','EscalaPlaca','Distancia'\
         ,'Diametro','WinSpot','Gain','Texp','Sampling','N','Muestras'\
         , 'Return']

#Conjunto de columnas que será seleccionadas por medio de índice.
use_cols = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25 \
            ,26,27]

#Code
# INPUTS
#Comentarios de entrada empleados para informar al usuario.
print("\n"
      "The following script has been desgined to produce reports that \n" 
      "compares D1's measurements and D2's measurements. The statistical \n" 
      " results provide us information whether both systems are comparables.")

print("\n"
      "The following example shows how you should write the directories \n "
      " and files format. IF YOU USE OTHER FORMAT, YOU WILL FIND PROBLEMS. \n"
      "More information in README document.")

print("\n"
      "The directory for input files :./MEDIDAS/"
      "\n"
      "The directory for output files:./REPORTS/"
      "\n"
      "Generic name for input files of D1:IAC_TEST_*.txt"
      "\n"
      "Generic name for input files of D2:RMMSX_*.txt")

dir_in = input('The directory for input files :') #Directorio de entrada
#definido por el usuario.
dir_out = input('The directory for output files:')# Directorio de salida
#definido por el usuario.
file_D1 = input('Generic name for input files of D1:') #Nombre genérico de 
#los archivos de entrada para D1.
file_D2 = input('Generic name for input files of D2:')# Nombre genérico de los 
# archivos de entrada para D2.

listD2A = glob.glob(dir_in + file_D2) #Genera un lista con todos los archivos
listD1A = glob.glob(dir_in + file_D1) #que se localizan en el directorio.

for g in listD2A: # Genera un archivo .csv por cada .txt para D2.
    df = pd.read_csv(g ,delimiter='\t', index_col=None) #Lee el archivo.
    returnindex = df.columns.get_loc('Return') #Devuelve el índice de 'Return'.
    use_cols.append(returnindex + 1)# Sumamos 1 al índice de 'Return' y lo insertamos en use_cols.
    q = re.sub('\.txt$','.csv',g)#Sustituye la raíz del nombre.
    df.to_csv(q) #Guarda el archivo en formato CSV.
    df = pd.read_csv(q, decimal='.', usecols=use_cols)#Relee el archivo 
    #seleccionando un conjunto determinado de columnas.
    colnameD2 = df.columns #Creamos una variable con la lista de columnas 
    #por defecto.
    for i in range(len(stand)): #Empleamos un for para cambiar el nombre de
        #las columnas una a una, ya que el otro script necesita unos nombre
        # determinados.
        df = df.rename(columns={colnameD2[i] : stand[i]}) #Cambia los nombres de las columnas.
    df.to_csv(q, index=False) #Guardamos el resultado en CSV.
   
    
for f in listD1A: # Genera un archivo .csv por cada .txt para D1. Y hace lo
    # mismo que el fragmento de código anterior.
    df = pd.read_csv(f, delimiter='\t', index_col=None)
    returnindex = df.columns.get_loc('Return')
    use_cols.append(returnindex + 1)
    q = re.sub('\.txt$','.csv',f)
    df.to_csv(q)
    df = pd.read_csv(q, decimal='.', usecols= use_cols)
    colnameD1 = df.columns
    for i in range(len(stand)):
        df = df.rename(columns={colnameD1[i] : stand[i]})
    df.to_csv(q, index=False)

for fileD1, fileD2 in zip(sorted(glob.iglob(dir_in + 'IAC_TEST_*.csv')) \
                          , sorted(glob.iglob(dir_in + 'RMMSX_*.csv'))):
    #Su función es crear un for que funciona como un generador de archivos.
    #De esta forma, en cada paso, el for devuelve dos nuevos archivos
    #que pueden ser leídos por las siguientes líneas y llegar al final del
    #proceso sin generar errores.
    #El zip se debe a que son archivos grandes, el sorted ya que 
    #deben estar ordenados por fecha y iglob crea el generador de archivos.
    D2 = pd.read_csv(fileD2, decimal='.', parse_dates=['Fecha'])
    #Lee el archivo generado para D2.
    D1 = pd.read_csv(fileD1, decimal='.', parse_dates=['Fecha'])
    #Lee el archivo generado para D1.
    Report(D2,D1) # Llama a la función contenido en el script REPORT_
    #DIMMA_func.py
    outputfilexlsx = re.sub('.csv','.xlsx',fileD2)#Cambia el nombre de la raíz.
    outputfilepdf = re.sub('.csv','.pdf',fileD2)
    outputfilexlsx = re.sub(dir_in,dir_out,outputfilexlsx)#Cambia el directorio.
    outputfilepdf = re.sub(dir_in,dir_out,outputfilepdf)
    os.rename('datasheet.xlsx', outputfilexlsx)#Modifica el nombre del
    #directorio donde será guardado el archivo final.
    os.rename('resultados.pdf', outputfilepdf)
    print("\n"
            "Completed the analysis of {}".format(outputfilepdf)) 
    #Informa de que se ha finalizado la creación del documentos para el 
    #archivo generado.
    
    
    
    
    