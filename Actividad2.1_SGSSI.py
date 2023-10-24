#Actividad 2.1 Realizar un programa que obtenga el resumen SHA-256 de un fichero de texto

import hashlib
import time

def generar_resumenSHA256_fichero(nombre_fichero):

    sha256 = hashlib.sha256()
    with open(nombre_fichero, "rb") as archivo:
        bloque = archivo.read()
        # Actualiza el objeto SHA-256 con el contenido del bloque
        sha256.update(bloque)

    # Devuelve el resumen SHA-256 como una cadena hexadecimal
    return sha256.hexdigest()

def agregar_resumen_al_archivo(archivo_entrada, archivo_salida):
    # Calcula el resumen SHA-256 del archivo de entrada
    resumen = generar_resumenSHA256_fichero(archivo_entrada)

    # Abre el archivo de entrada en modo lectura
    with open(archivo_entrada, "r") as entrada:
        # Lee el contenido completo del archivo de entrada
        contenido_entrada = entrada.read()

        # Abre el archivo de salida en modo escritura
        with open(archivo_salida, "w") as salida:
            # Escribe el contenido del archivo de entrada en el archivo de salida
            salida.write(contenido_entrada)

            # Escribe una línea adicional con el resumen SHA-256
            salida.write("\n" + resumen)

def verificar_archivos_iguales_con_resumen(archivo1, archivo2):
    # Calcula el resumen SHA-256 del primer archivo
    resumen1 = generar_resumenSHA256_fichero(archivo1)

    # Abre el primer archivo en modo lectura
    with open(archivo1, "r") as archivo1_lectura:
        # Lee el contenido completo del primer archivo
        contenido1 = archivo1_lectura.read()

        # Abre el segundo archivo en modo lectura
        with open(archivo2, "r") as archivo2_lectura:
            # Lee el contenido completo del segundo archivo
            contenido2 = archivo2_lectura.read()

            # Verifica si los contenidos son iguales
            contenido1_sin_resumen = contenido1.split("\n", 1)[0]
            contenido2_sin_resumen = contenido2.split("\n", 1)[0]
            if contenido1_sin_resumen == contenido2_sin_resumen:
                # Verifica si el resumen SHA-256 está presente en el segundo archivo
                if resumen1 in contenido2:
                    return True

    return False

# Función para calcular el tiempo promedio que toma ejecutar la función SHA-256
def calcular_tiempo_promedio():
    num_ejecuciones = 100000  # Puedes ajustar este número según tus necesidades

    # Realiza las ejecuciones de la función SHA-256 y mide el tiempo
    tiempos = []
    for _ in range(num_ejecuciones):
        start_time = time.time()
        generar_resumenSHA256_fichero("SGSSI-23.CB.01.txt")
        end_time = time.time()
        tiempos.append(end_time - start_time)

    # Calcula el tiempo promedio en segundos
    tiempo_promedio = sum(tiempos) / len(tiempos)

    # Calcula las ejecuciones por minuto
    ejecuciones_por_minuto = 60 / tiempo_promedio

    return ejecuciones_por_minuto


#CODIGO DE EXPERIMENTACION

# Llama a la función para calcular el número de ejecuciones por minuto
ejecuciones_por_minuto = calcular_tiempo_promedio()

print(f"Se pueden ejecutar aproximadamente {int(ejecuciones_por_minuto)} veces por minuto la función SHA-256 en este entorno de trabajo.")

nombre_fichero = "SGSSI-23.CB.00.txt"
archivo_salida = "SGSSI-23.CB.00_modificado.txt"
#resumen_fichero = generar_resumenSHA256_fichero(nombre_fichero)
agregar_resumen_al_archivo(nombre_fichero, archivo_salida)
print(f"Se ha agregado el resumen SHA-256 al archivo '{nombre_fichero}'.")

son_iguales_con_resumen = verificar_archivos_iguales_con_resumen(nombre_fichero, archivo_salida)

if son_iguales_con_resumen:
    print("Los archivos son iguales y el segundo archivo contiene el resumen SHA-256 del primero.")
else:
    print("Los archivos no cumplen con los criterios especificados.")