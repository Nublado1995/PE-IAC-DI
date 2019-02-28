#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 14:18:02 2019

    La finalidad de este script es generar un informe que permita la correcta
    comparación entre las medidas obtenidas con el sistema DIMM (D1) y el
    sistema DIMMA (D2) para unas mismas fechas.
    Este script tiene como función generar un archivo XLSX y un archivo PDF
    que contenga información estadística sobre las medidas y las comparaciones
    de las medidas entre ambos sistemas. Para ello, usa dos ficheros en CSV
    de entrada que contiene medidas de D1 y otro con medidas de D2 para un
    mismo día.

@author: Fabricio Manuel Pérez Toledo
"""

#Librerías y su descendencia.
import numpy as np # Multitud de funciones matemáticas.
import pandas as pd #Ya citado.
from jinja2 import Environment, FileSystemLoader # Para operaciones con HTML.
from weasyprint import HTML #Otras operaciones para HTML.
import matplotlib.pyplot as plt #Generar gráficos.
from matplotlib.backends.backend_pdf import PdfPages #Guardar gráficos en PDF.
from PyPDF2 import PdfFileMerger #Operaciones con PDF.

#Constantes y sus madres.
N = 200. #El número máximo de muestras.
Nmin=190. #El número mínimo de muestras para considerar válida la medida.
seemax = 6. #El valor máximo del seeing para considerar válidad la medida.

#Conjunto de nombre que heredarán las columnas de los archivos de D1 una vez
#se haya llamado a la función REPORT().
ListD1=['Fecha_D1', 'Ubicacion_D1', 'Objeto_D1', 'Seeing_D1', 'Maire_D1', 'Flujo1_D1', 'Flujo2_D1',
       'Var_l_D1', 'Var_t_D1', 'Centelleo1_D1', 'Centelleo2_D1', 'r0l_D1', 'r0t_D1', 'fwhml_D1',
       'fwmlt_D1', 'CCD_D1', 'Software_D1', 'Ventana_D1', 'EscalaPlaca_D1', 'Distancia_D1',
       'Diametro_D1', 'WinSpot_D1', 'Gain_D1', 'Texp_D1', 'Sampling_D1', 'N_D1', 'Muestras_D1',
       'Return_D1']
#Lo mismo para D2.
ListD2=['Fecha_D2', 'Ubicacion_D2', 'Objeto_D2', 'Seeing_D2', 'Maire_D2', 'Flujo1_D2', 'Flujo2_D2',
       'Var_l_D2', 'Var_t_D2', 'Centelleo1_D2', 'Centelleo2_D2', 'r0l_D2', 'r0t_D2', 'fwhml_D2',
       'fwmlt_D2', 'CCD_D2', 'Software_D2', 'Ventana_D2', 'EscalaPlaca_D2', 'Distancia_D2',
       'Diametro_D2', 'WinSpot_D2', 'Gain_D2', 'Texp_D2', 'Sampling_D2', 'N_D2', 'Muestras_D2',
       'Return_D2']
#Nombre por defecto que contienen los archivos antes de llamar a REPORT().
ListD1D2=['Fecha', 'Ubicacion', 'Objeto', 'Seeing', 'Maire', 'Flujo1', 'Flujo2',
       'Var_l', 'Var_t', 'Centelleo1', 'Centelleo2', 'r0l', 'r0t', 'fwhml',
       'fwmlt', 'CCD', 'Software', 'Ventana', 'EscalaPlaca', 'Distancia',
       'Diametro', 'WinSpot', 'Gain', 'Texp', 'Sampling', 'N', 'Muestras',
       'Return']

shListD1=[ 'Seeing_D1', 'Maire_D1', 'Flujo1_D1', 'Flujo2_D1',
       'Var_l_D1', 'Var_t_D1', 'Centelleo1_D1', 'Centelleo2_D1', 'r0l_D1', 'r0t_D1', 'fwhml_D1',
       'fwmlt_D1', 'EscalaPlaca_D1', 'Distancia_D1',
       'Diametro_D1', 'WinSpot_D1', 'Gain_D1', 'Texp_D1', 'Sampling_D1', 'N_D1', 'Muestras_D1',
       'Return_D1']
shListD2 = [ 'Seeing_D2', 'Maire_D2', 'Flujo1_D2', 'Flujo2_D2',
       'Var_l_D2', 'Var_t_D2', 'Centelleo1_D2', 'Centelleo2_D2', 'r0l_D2', 'r0t_D2', 'fwhml_D2',
       'fwmlt_D2', 'EscalaPlaca_D2', 'Distancia_D2',
       'Diametro_D2', 'WinSpot_D2', 'Gain_D2', 'Texp_D2', 'Sampling_D2', 'N_D2', 'Muestras_D2',
       'Return_D2']

#Nombre que heredarán las columnas cuando se generen los sheets en el archivo
# XLSX para la comparación entre D1 y D2.
diffD1D2=[ 'Dif_Seeing','Dif_Maire', 'Dif_Flujo1', 'Dif_Flujo2','Dif_Var_l'\
         , 'Dif_Var_t', 'Dif_Centelleo1'\
         , 'Dif_Centelleo2', 'Dif_r0l', 'Dif_r0t', 'Dif_fwhml', 'Dif_fwmlt'\
         ,'Dif_EscalaPlaca', 'Dif_Distancia','Dif_Diametro','Dif_WinSpot','Dif_Gain'\
         ,'Dif_Texp','Dif_Sampling', 'Dif_N', 'Dif_Muestras','Dif_Return']

#Nombre de columnas que recibirán un análisis estadístico determinado.
shdiffD1D2=[ 'Dif_Seeing','Dif_Maire', 'Dif_Flujo1', 'Dif_Flujo2','Dif_Var_l'\
         , 'Dif_Var_t', 'Dif_Centelleo1'\
         , 'Dif_Centelleo2', 'Dif_r0l', 'Dif_r0t', 'Dif_fwhml', 'Dif_fwmlt'\
         ,'Dif_Muestras']

#Nombre de columnas que recibirán un análisis estadístico determinado.
ListD1D2_EST = ['Seeing_D1','Seeing_D2','Flujo1_D1','Flujo1_D2','Flujo2_D1','Flujo2_D2' \
           , 'Var_l_D1','Var_l_D2','Var_t_D1','Var_t_D2','Centelleo1_D1','Centelleo1_D2'\
           ,'Centelleo2_D1','Centelleo2_D2']

#Nombre de la columnas empleadas en la función CompCol1().
comp1 = [ 'Objeto', 'CCD'] # NOTA: El Software no es igual. Y la ventana la tienen que reparar.

comp2 = [ 'EscalaPlaca', 'Distancia','Diametro', 'WinSpot', 'Gain' \
         , 'Texp', 'Sampling', 'N', 'Muestras', 'Return']

#Nombre de la columnas empleadas en la función CompCol2(). A la espera de
#solucionar unos problemas en DIMMA. Una vez resueltos emplear comp2.
comp3 = [  'Gain' \
         , 'Texp', 'Sampling', 'N', 'Muestras', 'Return']

#Funciones:

def Report(x,y):
    """
    La funcion Report() se ha creado para generar un estudio estadístico entre
    las medidas obtenidas por D1 y D2. Así mismo, se encarga de clasificar
    las medidas en función de filtros en el interior de la función.
    Estas clasificaciones son: válidas, válidas-iguales, no-iguales y
    no-válidas. Para más información consultar README.pdf.
    """
    #Crea un documento genérico donde introducir los resultados. Posteriormente
    #se cambiará de nombre.
    writer = pd.ExcelWriter('datasheet.xlsx', datetime_format='yyyy-mm-dd hh:mm:ss')
    D2 = x # arvhivos de D2.
    D1 = y # archivos de D1.
    D21 = D2
    D11 = D1
    def SeeVal(z):
        """
        Esta función SeeVal(z) lee fila por fila el archivo CSV ejecutado
        y compara para determinadas columnas que se cumplen unos criterios 
        para considerar las medidas válidas. Si no es así, será eliminadas 
        del DataFrame.
        Más información en el README.pdf.
        """
        errSeeing = [] #crea una lista vacía.
        for q in z.index: #itera en función de los valores del índice.
            #Si no se cumple la condición la iteración continua, en caso
            #contrario.
            if (z.Seeing[q] > seemax == True) or (((z.Muestras[q] < Nmin).any() == True) \
                or ((z.Return[q] != 0).any() == True)):
                #print (q) 
                #print('Valor de Seeing malo')
                errSeeing.append(q) #Se añade el valor del índice en la lista.
        return z.drop(errSeeing) #Los índices recopilados se eliminan del DataFrame.
            
    def CompTiempo(n,l):
        """
        CompTiempo(n,l) tiene por cometido sincronizar el DataFrame
        correspondiente a D1 con D2, dado que el momento de adquisición
        de la medida deben ser iguales.
        Más información en README.pdf.
        """
        #Cambiamos el formato de contenido de la columna 'Fecha' y cambiamos
        # de calendario gregoriano a calendario juliana por facilidad de las
        # operaciones de comparación.
        n = pd.DatetimeIndex(n['Fecha'].values).to_julian_date()
        l = pd.DatetimeIndex(l['Fecha'].values).to_julian_date()
        interA = np.intersect1d(n,l, return_indices=True) #Compara la columna
        #'Fecha' en ambos DataFrame e indica valores coinciden y cuál es su
        # índice.
        return interA[1].tolist() #Convertimos los índeces recopilados en una
        #lista.
    
    def CompCol1(f,g):
        """
        CompCol1(f,g) compara fila por fila que las columnas contenidas en
        comp1 sea su contenido igual.
        Más información en README.pdf.
        """
        h = [] #Crea una lista vacía.
        for q in range(len(comp1)): # Genera una iteración.
            fcomp = (f[comp1[q]].str.strip()) #Elimina los espacios dentro de
            # la celda a los lados del contenido.
            fcomp = fcomp.str.replace(' ','') #Reemplaza los espacios dentro 
            #de la celda.
            #print(fcomp)
            gcomp = (g[comp1[q]].str.strip())
            gcomp = gcomp.str.replace(' ','')
            #print(gcomp)
            for r in f.index: #Genera una iteración en función del índice de f.
                #print(r)
                if fcomp[r] != gcomp[r]: #Compara fila por fila
                    #print('Hay algo que eliminar')
                    h.append(r) #Si no es igual el contenido, entonces el
                    #índice se agraga ahí.
        return h #Devuelve la lista de índices de filas que no son iguales.
    
    #En la siguiente función se pide lo mismo que en la anterior. No obstante,
    #se aplica a columnas que no tienen problemas con los espacios.
    def CompCol2(f,g):
        """
        CompCol2(f,g) compara fila por fila que las columnas contenidas en
        comp1 sea su contenido igual.
        Más información en README.pdf.
        """
        h = []
        for q in range(len(comp3)):
            for r in f.index:
                fcomp = (f[comp3[q]])
                gcomp = (g[comp3[q]])
                if fcomp[r] != gcomp[r]:
                    #print('Hay algo que eliminar')
                    h.append(r)
        return h
    
    def CreateDF1(j,k):
        """
        CreateDF1(j,k) introduce las columnas de j y k en un nuevo DataFrame vacío
        colocando primero una columnas de D1 seguido de la columna equivalente
        de D2. Ej. primero la columna 'Seeing_D1' y luego la columna 'Seeing_D2'
        Más información en README.pdf.
        """
        cloe = pd.DataFrame() #DataFrame vacío.
        for i in range(len(ListD1)): #Generamos un bucle.
            cloe[ListD1[i]] = j[ListD1D2[i]] #Selecciona una columna en j y la añade.
            cloe[ListD2[i]] = k[ListD1D2[i]] #Selecciona una columna en k y la añade.
        return cloe #Devuelve el nuevo DataFrame.
    
    def CreateDF2(j):
        """
        CreateDF2(j) es una función creada para generar un DataFrame que contenga 
        la diferencia entre columnas con el mismo tipo de información. Ej. 
        'Seeing_D1' - 'Seeing_D2'.
        Más información en README.pdf.
        """
        maria = pd.DataFrame() #DataFrame vacío
        maria['Fecha'] = j['Fecha_D1'] #Añade la columna con la fecha y hora.
        maria['Objeto'] = j['Objeto_D1'] #Añade la columna con el objeto.
        for a in range(len(shListD1)): #Genera una iteración para operar fila a fila.
            #Si el nombre de las columnas coinciden con la indicadas se
            # creará un string que crea un código de error.
            if (shListD1[a]=='Return_D1') & (shListD2[a]=='Return_D2'):
                #Genera un código de error.
                maria[diffD1D2[a]] = (j[shListD1[a]].astype(int)).astype(str)+'-'+(j[shListD2[a]].astype(int)).astype(str)
            else:
                #Realiza una operación de resta entre las columnas.
                maria[diffD1D2[a]] = abs(j[shListD1[a]]-j[shListD2[a]])
                
        return maria #Devuelve un DataFrame con la diferencia.
    
    def EstSee(s):
        """
        EstSee(s) es una función que realiza operaciones estadísticas como
        obtener la media, desviación estándar, valor máximo y valor mínimo
        para las columnas indicadas.
        Más información en README.pdf.
        """
        #Se crea un DataFrame vacío pero con el índice definido.
        EST = pd.DataFrame(index=['Media','Desviacion estandar','Max','Min'])
        for t in range(len(shdiffD1D2)): #Creamos un bucle.
            estad = np.array([]) #Crea un array vacío.
            #La siguiente condición se ha creado en el caso de que se desee
            #añadir cifras decimales a los datos correspondientes al flujo.
            if (shdiffD1D2[t]=='Dif_Flujo1') or (shdiffD1D2[t]=='Dif_Flujo2'):
                #Se añade en el array vacío el valor calculado para una 
                #determinada operación estadística.
                estad = np.append(estad,np.mean(abs(s[shdiffD1D2[t]])).round(4))
                estad = np.append(estad,np.std(abs(s[shdiffD1D2[t]])).round(4))
                estad = np.append(estad,np.max(abs(s[shdiffD1D2[t]])).round(4))
                estad = np.append(estad,np.min(abs(s[shdiffD1D2[t]])).round(4))
            else:
                estad = np.append(estad,np.mean(abs(s[shdiffD1D2[t]])).round(4))
                estad = np.append(estad,np.std(abs(s[shdiffD1D2[t]])).round(4))
                estad = np.append(estad,np.max(abs(s[shdiffD1D2[t]])).round(4))
                estad = np.append(estad,np.min(abs(s[shdiffD1D2[t]])).round(4))                
                #print(estad)
            #Ahora generamos una Serie predefiniendo el índice.
            d = pd.Series(estad.tolist(), index=['Media'\
                          ,'Desviacion estandar','Max','Min']).to_frame(name=diffD1D2[t])
            #Lo introducimos dentro del DataFrame.
            EST.insert(t,shdiffD1D2[t],d)
        return EST

    #La siguiente función es igual que la anterior a excepción de que realiza
    #la operación de mediana.
    def EstCol(s):
        """
        EstCol(s) es una función que realiza operaciones estadísticas como
        obtener la media, mediana, desviación estándar, valor máximo y 
        valor mínimo para las columnas indicadas.
        Más información en README.pdf.
        """
        EST1 = pd.DataFrame(index=['Media','Mediana','Desviacion estandar','Max','Min'])
        for t in range(len(ListD1D2_EST)):
            estad = np.array([])
            estad = np.append(estad,np.mean(abs(s[ListD1D2_EST[t]])).round(4))
            estad = np.append(estad,np.median(abs(s[ListD1D2_EST[t]])).round(4))
            estad = np.append(estad,np.std(abs(s[ListD1D2_EST[t]])).round(4))
            estad = np.append(estad,np.max(abs(s[ListD1D2_EST[t]])).round(4))
            estad = np.append(estad,np.min(abs(s[ListD1D2_EST[t]])).round(4))
            d = pd.Series(estad.tolist(), index=['Media'\
                          ,'Mediana','Desviacion estandar','Max','Min']).to_frame(name=ListD1D2_EST[t])
            EST1.insert(t,ListD1D2_EST[t],d)
        return EST1
    
    
    #Lista de instrucciones a ejecutar por el script.
    
    
    D2 = SeeVal(D2) #Llama SeeVal() para eliminar las medidas no válidas.
    D1 = SeeVal(D1)
    
    intA = CompTiempo(D2, D1) #Obtenemos los índices de los valores que están
    intB = CompTiempo(D1, D2) #sincronizados.
    
    D2clean = D2.iloc[intA] #Seleccionamos sólo las medidas válidas.
    D1clean = D1.iloc[intB]

    D2clean3 = D2clean #Renombramos la misma variable para otros fines.
    D1clean3 = D1clean
    
    NoCoinciden1 = CompCol1(D1clean,D2clean) # Obtenemos la lista de índices.
    D2clean1 = D2clean.drop(NoCoinciden1) #Eliminamos dichos ínidices del
    D1clean1 = D1clean.drop(NoCoinciden1) # DataFrame inicial.

    D2conf1 = D2clean3.loc[NoCoinciden1,:] #Ahora seleccionamos los datos
    D1conf1 = D1clean3.loc[NoCoinciden1,:] # indicados por los índices.

    NoCoinciden2 = CompCol2(D1clean1,D2clean1) #Realizamos la misma 
    D2clean2 = D2clean1.drop(NoCoinciden2) # operación para la siguiente
    D1clean2 = D1clean1.drop(NoCoinciden2) # función.
    D2clean = D2clean2
    D1clean = D1clean2    
    
    D2conf2 = D2clean3.loc[NoCoinciden2,:] 
    D1conf2 = D1clean3.loc[NoCoinciden2,:]
    D2conf = pd.concat([D2conf1,D2conf2]) #Funcionamos contenidos.
    D1conf = pd.concat([D1conf1, D1conf2])

    intC = D2.index #Llama al índice de las medidas válidas.
    ErrD21 = D21.drop(intC) #Se eliminan dichas medidas.
    ErrD11 = D11.drop(intC)
    ErrD2 = ErrD21.reset_index().loc[CompTiempo(ErrD21, ErrD11)]
    ErrD1 = ErrD11.reset_index().loc[CompTiempo(ErrD11, ErrD21)]
    ErrD2 = ErrD2.dropna(axis=0)
    ErrD1 = ErrD1.dropna(axis=0)

    valigu = CreateDF1(D1clean,D2clean) #Crea un DataFrame con las válidas-comparadas.
    valigu.index.name = 'DS2' #Añadimos el nombre de la sheet a la tabla.
    noigu = CreateDF1(D1conf,D2conf) #Crea un DataFrame con las comparadas.
    noigu.index.name = 'DS3'
    val = CreateDF1(D1clean3,D2clean3) # Crea un DataFrame con la válidas.
    val.index.name = 'DS1'
    noval = CreateDF1(ErrD1,ErrD2) #Crea un DataFrame con la no válidas.
    noval.index.name = 'DS4'
    
    val.to_excel(writer,'DS1') #Se guardan en el archivo XLSX creado.
    valigu.to_excel(writer,'DS2')
    noigu.to_excel(writer,'DS3')
    noval.to_excel(writer, 'DS4')
    
    difvaligu = CreateDF2(valigu) #Crea un DataFrame con la comparación de las válidas-comparadas.
    difval = CreateDF2(val) #Crea un DataFrame con la comparación de las válidas.
    difnoigu = CreateDF2(noigu) #Crea un DataFrame con la comparación de las comparadas.
    difnoval = CreateDF2(noval) #Crea un DataFrame con la comparación de las no válidas.
    
    difval.to_excel(writer,'COMP-DS1') #Guardamos resultados en el archivo XLSX.
    difval.index.name = 'COMP-DS1' #Añadimos el nombre de la sheet a la tabla.
    difvaligu.to_excel(writer,'COMP-DS2')
    difvaligu.index.name = 'COMP-DS2'
    difnoigu.to_excel(writer,'COMP-DS3')
    difnoigu.index.name = 'COMP-DS3'
    difnoval.to_excel(writer,'COMP-DS4')
    difnoval.index.name = 'COMP-DS4'
    writer.save() #Guardamos el archivo XLSX.
        
    pd.options.display.float_format = "{0:.6g}".format #Definimos el formato de los números.
    Val = EstSee(difval) #Crea un DataFrame con los resultados estadísticos
    # de la comparación de las medidas válidas. 
    Val.index.name = 'COMP-DS1'
    Valigu = EstSee(difvaligu) # Lo mismo para las medidas válidas-comparadas.
    Valigu.index.name = 'COMP-DS2'
    Noigu = EstSee(difnoigu) # Para las comparadas.
    Noigu.index.name = 'COMP-DS3'
    Noval = EstSee(difnoval) # Para las no válidas.
    Noval.index.name = 'COMP-DS4'

    pd.options.display.float_format = "{0:.6g}".format
    Val_est = EstCol(val) #Crea un DataFrame con los resultados estadísticos
    # de las medidas válidas. 
    Val_est.index.name = 'DS1'
    Valigu_est = EstCol(valigu)#Crea un DataFrame con los resultados estadísticos
    #de las medidas válidas-comparadas. 
    Valigu_est.index.name = 'DS2'

    Nvaligu = difvaligu.shape[0] # Definimos el número de filas.
    Nnoigu = difnoigu.shape[0]
    Nnoval = difnoval.shape[0]
    Nval = difval.shape[0]
    NTD2 = D21.shape[0]
    NTD1 = D11.shape[0]
    DsincD2 = NTD2 - Nvaligu - Nnoigu - Nnoval #Definimos el número de medidas desincronizadas.
    DsincD1 = NTD1 - Nvaligu - Nnoigu - Nnoval
    #Obtenemos los porcentajes de medidas.
    PTEST = (np.asarray([Nval,Nvaligu,Nnoigu,Nnoval,DsincD1,NTD1])*(100./NTD1))
    PSOFT = (np.asarray([Nval,Nvaligu,Nnoigu,Nnoval,DsincD2,NTD2])*(100./NTD2))
    PTEST = PTEST.round(1).tolist()
    PSOFT = PSOFT.round(1).tolist()
    #Generamos a DataFrame con los resultados.
    Num = pd.DataFrame({'Nº de medidas D1':[Nval,Nvaligu,Nnoigu,Nnoval,DsincD1,NTD1] \
                        ,'Porcentajes de D1':PTEST\
                        ,'Nº de Medidas D2':[Nval,Nvaligu,Nnoigu,Nnoval,DsincD2,NTD2] \
                        ,'Porcentaje de D2': PSOFT\
                        }, index=['DS1','DS2' ,'DS3','DS4','Desincronizadas','Total'])
    
    #Creamos un DataFrame para la cebecera del report que indique la ubicación
    #del DIMMA, la fecha de inicio, la fecha de finalización, el software 
    #usado para D1 y el software usado para D2.
    U = val['Ubicacion_D2'].index[0] #El primer valor del ínidice.
    V = val['Ubicacion_D2'].index[-1] #El último valor del ínidice.
    Datos=pd.DataFrame({'Ubicación':[val['Ubicacion_D2'][U]] \
                        ,'Fecha inicial':[val['Fecha_D2'][U]]\
                        ,'Fecha final':[val['Fecha_D2'][V]]
                        ,'D1':[val['Software_D1'][U]]\
                        ,'D2':[val['Software_D2'][U]]})
        
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("report_templates.html") #Carga el archivo HTML
    # report_templates.html para tener una estructura dónde insertar los DataFrames
    # creados anteriormente. Además, el archivo contiene especificaciones sobre
    # el tamaño de la fuente, tipo de borde, etc.
        
    Valigu.style.set_properties(**{'font-size':'8pt'}).render() #Definimos el tamaño de la fuente.
    Val.style.set_properties(**{'font-size':'8pt'}).render()
    Noigu.style.set_properties(**{'font-size':'8pt'}).render()
    Noval.style.set_properties(**{'font-size':'8pt'}).render()
    Num.style.set_properties(**{'font-size':'8pt'}).render()
    Datos.style.set_properties(**{'font-size':'8pt'}).render()
    
    #Las siguiente líneas de código introducen dentro del archivo HTML los
    #DataFrames creados con anterioridad.
    template_vars = {"title" : "Comparativa D1 y D2",
                     "tabla_cero": Datos.to_html(table_id="t01") \
                     ,"primera_tabla": Num.to_html(table_id="t01") \
                     , "segunda_tabla": (Val_est.transpose()).to_html(table_id="t01") \
                     , "tercera_tabla":(Valigu_est.transpose()).to_html(table_id="t01") \
                     , "cuarta_tabla":(Val.transpose()).to_html(table_id="t01") \
                     , "quinta_tabla":(Valigu.transpose()).to_html(table_id="t01")\
                     , "sexta_tabla":(Noigu.transpose()).to_html(table_id="t01")\
                     , "septima_tabla":(Noval.transpose()).to_html(table_id="t01")}

    html_out = template.render(template_vars)
    #print(html_out)
    HTML(string=html_out).write_pdf("report-DIMMA.pdf") #Guardamos el contenido en PDF.
    
    pp = PdfPages('imagenes.pdf') #Crea un PDF donde guardar las gráficas.
    
    #Ahora se generan los gráficos con los resultados de los DataFrames para
    #válidas y válidas-comparadas.
    plt.figure(1,figsize=(8.27, 11.69), dpi=100) #Definimos el tamaño y calidad de las gráficas.
    ax1=plt.subplot(211) #Crea una sub gráfica.
    #Genera el gráfico.
    plt.plot(val['Fecha_D1'], val['Seeing_D1'],val['Fecha_D1'], val['Seeing_D2'])
    plt.legend(('D1','D2')) #Crea una leyenda.
    plt.xticks(rotation='vertical') # Los valores en el eje x están en posición vertical.
    plt.ylabel('Seeing in arcsec') # Nombre del eje y.
    plt.title('Measurements of seeing for DS1') #Título de la gráfica.
    plt.setp(ax1.get_xticklabels(), visible=False) # No muestra el contenido del eje x.
    ax1.yaxis.grid() #Añade un grid sólo para y.
    
    ax2=plt.subplot(212, sharex=ax1) # Indica que el eje x es compartido por las dos gráficas.
    plt.plot(val['Fecha_D1'], difval['Dif_Seeing'])
    plt.xticks(rotation='vertical')
    plt.ylabel('Dif. Seeing in arcsec ')
    plt.setp(ax2.get_xticklabels(), fontsize=6) #Define el tamaño de los números.
    plt.xlabel('Time')
    plt.title('Diference of seeing between D1 and D2, for DS1')
    ax2.yaxis.grid()
        
    pp.savefig() #Guardamos las gráficas en el archivo PDF.
    
    #Borra el contenido de las gráficas para evitar sobreescritura.
    plt.clf()
    plt.cla()
    plt.close()
    
    #Lo mismo que en caso anterior.
    plt.figure(2,figsize=(8.27, 11.69), dpi=100)
    ax3=plt.subplot(211)
    plt.plot(valigu['Fecha_D1'], valigu['Seeing_D1'],valigu['Fecha_D1'], valigu['Seeing_D2'])
    plt.legend(('D1','D2'))
    plt.xticks(rotation='vertical')
    plt.ylabel('Seeing in arcsec')
    plt.title('Measurements of seeing for DS2')
    ax3.yaxis.grid()
    plt.setp(ax3.get_xticklabels(), visible=False)
    
    ax4=plt.subplot(212, sharex=ax1)
    plt.plot(valigu['Fecha_D1'], difvaligu['Dif_Seeing'])
    plt.xticks(rotation='vertical')
    plt.ylabel('Dif. Seeing in arcsec ')
    plt.setp(ax4.get_xticklabels(), fontsize=6)
    plt.xlabel('Time')
    plt.title('Diference of seeing between D1 and D2, for DS2')
    ax4.yaxis.grid()
    
    pp.savefig()
    
    pp.close() #Cerramos el documento PDF.
    
    plt.clf()
    plt.cla()
    plt.close()

    pdfs = ['report-DIMMA.pdf','imagenes.pdf'] #Crea una lista con ambos
    # archivos PDF.
    merger = PdfFileMerger() #Permite fusionar archivos PDF.
    for pdf in pdfs:
        merger.append(pdf) #Fusión de archivos PDF.
    merger.write('resultados.pdf') #Guarda el resultado en otro archivo PDF.

    return writer, merger #Devuelve el archivo XLSX 'datasheet.xlsx' y 
    #el archivo PDF 'resultados.pdf'.
