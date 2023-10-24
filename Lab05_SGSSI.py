import hashlib
import random
import time

def generar_resumenSHA256_fichero(nombre_fichero):

    sha256 = hashlib.sha256()
    with open(nombre_fichero, "rb") as archivo:
        bloque = archivo.read()
        # Actualiza el objeto SHA-256 con el contenido del bloque
        sha256.update(bloque)

    # Devuelve el resumen SHA-256 como una cadena hexadecimal
    return sha256.hexdigest()

def generar_secuencia_identificador(estudiante_id):
    # Genera una secuencia de 8 caracteres en hexadecimal
    secuencia_hex = ''.join(random.choice('abcdef0123456789') for _ in range(8))
    
    # Genera la línea con la secuencia hexadecimal, el identificador público y 100
    linea = f"{secuencia_hex}\t{estudiante_id}\t100"
    return linea

def crear_archivo_modificado(archivo_entrada, archivo_salida, estudiante_id):
    
    with open(archivo_entrada, "r") as entrada:
        # Lee el contenido completo del archivo de entrada
        contenido_entrada = entrada.read()

    start_time = time.time()
    max_ceros_resumen = None
    resumen_almacenado = None

    while time.time() - start_time < 60:
        # Genera una cadena aleatoria y calcula su resumen SHA-256
        cadena_aleatoria = ''.join(random.choices('0123456789abcdef', k=32)) + contenido_entrada
        resumen = hashlib.sha256(cadena_aleatoria.encode()).hexdigest()

        long_prefijo_ceros = len(resumen) - len(resumen.lstrip('0'))

        # Verifica si el resumen comienza con un prefijo de ceros más largo que el máximo encontrado hasta ahora
        if resumen_almacenado is None or long_prefijo_ceros > max_ceros_resumen:
            max_ceros_resumen = long_prefijo_ceros
            resumen_almacenado = resumen

    if max_ceros_resumen is not None and resumen_almacenado:
        # Abre el archivo de salida en modo escritura
        print("Resumen con secuencia mas larga de ceros obtenida en el tiempo de computación previsto: " + resumen_almacenado)
        with open(archivo_salida, "w") as salida:
            # Escribe el contenido del archivo de entrada en el archivo de salida
            salida.write(contenido_entrada)

            # Escribe la línea adicional con la secuencia y el resumen SHA-256 con el mayor prefijo de ceros
            secuencia_identificador = generar_secuencia_identificador(estudiante_id)
            salida.write("\n" + secuencia_identificador)
    else:
        print("No se encontró un resumen que cumpla con los criterios en un minuto.")

def comprobar_condiciones(archivo1, archivo2, estudiante_id):
    # Leer el contenido del primer archivo
    with open(archivo1, "r") as file1:
        contenido1 = file1.read()

    # Leer el contenido del segundo archivo
    with open(archivo2, "r") as file2:
        contenido2 = file2.read()

    # Verificar si el contenido de archivo2 comienza con el contenido de archivo1
    if contenido2.startswith(contenido1):
        print("El segundo archivo comienza con el mismo contenido que el primero.")

        # Extraer la línea adicional del segundo archivo
        lineas_archivo2 = contenido2.split('\n')
        if len(lineas_archivo2) > 1:
            linea_adicional = lineas_archivo2[-1]  # Suponemos que la línea adicional es la segunda línea

            # Dividir la línea adicional en sus partes
            partes = linea_adicional.split('\t')
            if len(partes) == 3:
                secuencia_hexadecimal, id, cien = partes

                # Verificar que la secuencia hexadecimal tenga 8 caracteres
                if len(secuencia_hexadecimal) == 8 and all(c in "0123456789abcdefABCDEF" for c in secuencia_hexadecimal):
                    # Verificar que el ID, el número 100 y el resumen SHA-256 estén presentes en sus posiciones correspondientes
                    if id == estudiante_id and cien == "100":
                        # Calcular el resumen SHA-256 del contenido del segundo archivo
                        resumen_archivo2 = hashlib.sha256(contenido2.encode()).hexdigest()
                        # Verificar si el resumen_archivo2 comienza con una secuencia de 0's
                        if resumen_archivo2.startswith("00"):
                            print("La línea adicional cumple con las condiciones y el resumen SHA-256 tiene un prefijo de 0's.")
                        else:
                            print("La línea adicional cumple con las condiciones, pero el resumen SHA-256 no tiene un prefijo de 0's.")
                    else:
                        print("La línea adicional no cumple con las condiciones especificadas.")
                else:
                    print("La secuencia hexadecimal no tiene 8 caracteres.")
            else:
                print("La línea adicional no tiene el formato esperado.")
        else:
            print("El segundo archivo no contiene una línea adicional.")
    else:
        print("El segundo archivo no comienza con el mismo contenido que el primero.")



#CODIGO DE EXPERIMENTACION
crear_archivo_modificado("SGSSI-23.CB.03.txt", "SGSSI-23.CB.03.4e.txt", "4e")
comprobar_condiciones("SGSSI-23.CB.02.txt", "SGSSI-23.CB.02_modificado.txt", "4e")
