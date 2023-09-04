import os
from zebra import Zebra
import time

# Inicializar la impresora (sustituye con el nombre de tu impresora)
printer = Zebra("ZDesigner Zt410-300dpi ZPL")

# Ruta de la carpeta donde se encuentran los archivos
carpeta_archivos = 'C:\\Users\\user1\\Desktop\\Test'

# Configurar la lista inicial de archivos en la carpeta
archivos_previos = set(os.listdir(carpeta_archivos))

# Cola para almacenar los valores DATAV en espera de impresión
cola_impresion = []
while True:
    try:
        archivos_en_carpeta = os.listdir(carpeta_archivos)
        archivos_nuevos = [archivo for archivo in archivos_en_carpeta if archivo not in archivos_previos]
        if archivos_nuevos and archivos_previos:
            for nombre_archivo in archivos_nuevos:
                DATAV = os.path.splitext(nombre_archivo)[0]
                zpl_code = f"""
                ~TA000
                ~JSN
                ^LT0
                ^MNW
                ^MTT
                ^PON
                ^PMN
                ^LH0,0
                ^JMA
                ^PR2,2
                ~SD21
                ^JUS
                ^LRN
                ^CI27
                ^PA0,1,1,0
                ^XZ
                ^XA
                ^MMT
                ^PW402
                ^LL1181
                ^LS0
                ^FT227,345^A0I,29,23^FH\^CI28^FDAUDI MEX^FS^CI27
                ^FT279,310^A0I,29,23^FH\^CI28^FDDRÄXLMAIER MEXICO^FS^CI27
                ^FT273,274^A0I,29,23^FH\^CI28^FDSan Luis Potosi YWX^FS^CI27
                ^FT121,845^A0N,29,23^FH\^CI28^FDAUDI MEX^FS^CI27
                ^FT70,880^A0N,29,23^FH\^CI28^FDDRÄXLMAIER MEXICO^FS^CI27
                ^FT76,911^A0N,29,23^FH\^CI28^FDSan Luis Potosi YWX^FS^CI27
                ^FT90,702^BQN,2,7
                ^FH\^FDLA,{DATAV}^FS
                ^FT90,295^BQN,2,7
                ^FH\^FDLA,{DATAV}^FS
                ^FT90,1152^BQN,2,7
                ^FH\^FDLA,{DATAV}^FS
                ^FT349,29^A0I,21,23^FB349,1,5,C^FH\^CI28^FD{DATAV}^FS^CI27
                ^FT0,1152^A0N,21,23^FB349,1,5,C^FH\^CI28^FD{DATAV}^FS^CI27
                ^FT349,426^A0I,21,23^FB349,1,5,C^FH\^CI28^FD{DATAV}^FS^CI27
                ^FT0,715^A0N,21,23^FB349,1,5,C^FH\^CI28^FD{DATAV}^FS^CI27
                ^PQ1,0,1,Y
                ^XZ
                """
                
                # Intentar enviar el código ZPL a la impresora
                try:
                    printer.output(zpl_code)
                    print(f"Código ZPL con valor {DATAV} enviado a la impresora Zebra.")
                except Exception as e:
                    print(f"Error al enviar a la impresora: {str(e)}")
                    cola_impresion.append(DATAV)
                
                archivos_previos.add(nombre_archivo)
        
        archivos_previos.update(archivos_en_carpeta)
        # Imprimir elementos en la cola de impresión si hay conexión con la impresora
        if cola_impresion:
            if printer.is_connected():
                datav_a_imprimir = cola_impresion.pop(0)
                zpl_code = f"""
                ~TA000
                ~JSN
                ^LT0
                ^MNW
                ^MTT
                ^PON
                ^PMN
                ^LH0,0
                ^JMA
                ^PR2,2
                ~SD21
                ^JUS
                ^LRN
                ^CI27
                ^PA0,1,1,0
                ^XZ
                ^XA
                ^MMT
                ^PW402
                ^LL1181
                ^LS0
                ^FT227,345^A0I,29,23^FH\^CI28^FDAUDI MEX^FS^CI27
                ^FT279,310^A0I,29,23^FH\^CI28^FDDRÄXLMAIER MEXICO^FS^CI27
                ^FT273,274^A0I,29,23^FH\^CI28^FDSan Luis Potosi YWX^FS^CI27
                ^FT121,845^A0N,29,23^FH\^CI28^FDAUDI MEX^FS^CI27
                ^FT70,880^A0N,29,23^FH\^CI28^FDDRÄXLMAIER MEXICO^FS^CI27
                ^FT76,911^A0N,29,23^FH\^CI28^FDSan Luis Potosi YWX^FS^CI27
                ^FT90,702^BQN,2,7
                ^FH\^FDLA,{datav_a_imprimir}^FS
                ^FT90,295^BQN,2,7
                ^FH\^FDLA,{datav_a_imprimir}^FS
                ^FT90,1152^BQN,2,7
                ^FH\^FDLA,{datav_a_imprimir}^FS
                ^FT349,29^A0I,21,23^FB349,1,5,C^FH\^CI28^FD{datav_a_imprimir}^FS^CI27
                ^FT0,1152^A0N,21,23^FB349,1,5,C^FH\^CI28^FD{datav_a_imprimir}^FS^CI27
                ^FT349,426^A0I,21,23^FB349,1,5,C^FH\^CI28^FD{datav_a_imprimir}^FS^CI27
                ^FT0,715^A0N,21,23^FB349,1,5,C^FH\^CI28^FD{datav_a_imprimir}^FS^CI27
                ^PQ1,0,1,Y
                ^XZ
                """
                printer.output(zpl_code)
                print(f"Código ZPL con valor {datav_a_imprimir} enviado a la impresora Zebra desde la cola.")
        time.sleep(2)
    
    except Exception as e:
        print(f"Error general: {str(e)}")
        # Manejar el error si es necesario
    
    # Agregar un retraso más largo en caso de errores repetidos para evitar saturar la impresora
    time.sleep(2)
