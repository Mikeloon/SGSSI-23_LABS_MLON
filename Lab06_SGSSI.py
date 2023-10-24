import hashlib
import os

def calcular_prefijo_ceros(sha256):
    count = 0
    for char in sha256:
        if char == '0':
            count += 1
        else:
            break
    return count

def comprobar_condicionesV2(archivo1, archivo2, estudiante_id):
    with open(archivo1, "r") as file1:
        contenido1 = file1.read()

    with open(archivo2, "r") as file2:
        contenido2 = file2.read()

    if contenido2.startswith(contenido1):
        lineas_archivo2 = contenido2.split('\n')
        if len(lineas_archivo2) > 1:
            # Obtener la última línea del segundo archivo
            linea_adicional = lineas_archivo2[-1]
            partes = linea_adicional.split('\t')
            if len(partes) == 3:  # Ajustar a tu formato de archivo
                _, id, cien = partes
                if id == estudiante_id and cien == "100":
                    resumen_archivo2 = hashlib.sha256(contenido2.encode()).hexdigest()
                    if resumen_archivo2.startswith("0"):
                        return calcular_prefijo_ceros(resumen_archivo2)
                return 0
    return -1

def obtener_ficheros_aptos(fichero_entrada, directorio):
    
    max_ceros = -1
    fichero_max_ceros = None
    ficheros_cumplen = []
    #Se itera sobre cada uno de los archivos dentro del directorio para comprobar si son candidatos aptos.
    for archivo in os.listdir(directorio):
        if archivo.endswith(".txt"):
            estudiante_id = archivo.split(".")[3]
            prefijo_ceros = comprobar_condicionesV2(fichero_entrada, os.path.join(directorio, archivo), estudiante_id)

            if prefijo_ceros >= 0:
                ficheros_cumplen.append((archivo, prefijo_ceros))
                #Se va comparando en cada iteración el resumen con mayor longitud de ceros.
                if prefijo_ceros > max_ceros:
                    max_ceros = prefijo_ceros
                    fichero_max_ceros = archivo

    ficheros_cumplen.sort(key=lambda x: (-x[1], x[0]))

    return ficheros_cumplen, fichero_max_ceros


#CODIGO DE EXPERIMENTACION

fichero_entrada = "SGSSI-23.CB.03.txt"
directorio = "SGSSI-23.S.6.2.CB.03.Candidatos"
ficheros_cumplen, fichero_max_ceros = obtener_ficheros_aptos(fichero_entrada, directorio)

print("La relación de ficheros que cumplen las condiciones en el directorio:")
for archivo, prefijo_ceros in ficheros_cumplen:
    print(f"- {archivo} (Prefijo de 0's en SHA-256: {prefijo_ceros})")

if fichero_max_ceros:
    print(f"El fichero con la secuencia de 0's más larga en el resumen SHA-256 es '{fichero_max_ceros}'.")