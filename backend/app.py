from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from datetime import datetime
from zoneinfo import ZoneInfo


app = Flask(__name__)
CORS(app)
# Cargar los datos una sola vez cuando inicia el servidor

ARCHIVO_DATOS = "Datos_SIATA_Aire_pm25_corregido.json"

df = pd.read_json(ARCHIVO_DATOS)

df["fecha"] = pd.to_datetime(df["fecha"])
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

# Nos aseguramos de trabajar solamente con PM2.5
df = df[df["variableConsulta"] == "pm25"].copy()

# Eliminar registros sin valor
df = df.dropna(subset=["valor"])

def calcular_aqi_pm25(pm25):

    # Truncar PM2.5 a una decimal
    pm25 = np.floor(pm25 * 10) / 10

    if pm25 <= 12.0:
        bp_lo = 0.0
        bp_hi = 12.0
        aqi_lo = 0
        aqi_hi = 50
        categoria = "Bueno"
        color = "verde"

    elif pm25 <= 35.4:
        bp_lo = 12.1
        bp_hi = 35.4
        aqi_lo = 51
        aqi_hi = 100
        categoria = "Moderado"
        color = "amarillo"

    elif pm25 <= 55.4:
        bp_lo = 35.5
        bp_hi = 55.4
        aqi_lo = 101
        aqi_hi = 150
        categoria = "Insalubre para grupos sensibles"
        color = "naranja"

    elif pm25 <= 150.4:
        bp_lo = 55.5
        bp_hi = 150.4
        aqi_lo = 151
        aqi_hi = 200
        categoria = "Insalubre"
        color = "rojo"

    elif pm25 <= 250.4:
        bp_lo = 150.5
        bp_hi = 250.4
        aqi_lo = 201
        aqi_hi = 300
        categoria = "Muy insalubre"
        color = "morado"

    elif pm25 <= 350.4:
        bp_lo = 250.5
        bp_hi = 350.4
        aqi_lo = 301
        aqi_hi = 400
        categoria = "Peligroso"
        color = "morado"

    elif pm25 <= 500.4:
        bp_lo = 350.5
        bp_hi = 500.4
        aqi_lo = 401
        aqi_hi = 500
        categoria = "Peligroso"
        color = "morado"

    else:
        return 500, "Peligroso", "morado"

    # Fórmula de interpolación del AQI
    aqi = (
        ((aqi_hi - aqi_lo) / (bp_hi - bp_lo))
        * (pm25 - bp_lo)
        + aqi_lo
    )
    aqi = round(aqi)
    return aqi, categoria, color

@app.route("/")
def inicio():

    return "Servidor SIATA funcionando"


@app.route("/medir", methods=["POST"])
def medir():
    # 4.1 Recibir JSON desde App Inventor
    datos = request.get_json()
    if not datos:

        return jsonify({
            "error": "No se recibieron datos"
        }), 400

    latitud = datos.get("latitud")
    longitud = datos.get("longitud")


    if latitud is None or longitud is None:
        return jsonify({
            "error": "Faltan latitud o longitud"
        }), 400

    print("Latitud recibida:", latitud)
    print("Longitud recibida:", longitud)

    # Obtener fecha y hora actual de Colombia
    ahora = datetime.now(
        ZoneInfo("America/Bogota")
    )
    print("Fecha y hora actual en Colombia:", ahora)

    # Extraer mes, día y hora
    mes_actual = ahora.month
    dia_actual = ahora.day
    hora_actual = ahora.hour

    print("Mes buscado:", mes_actual)
    print("Día buscado:", dia_actual)
    print("Hora buscada:", hora_actual)

    # Buscar la misma fecha y hora en el dataset sin importar el año
    df_hora = df[
        (df["fecha"].dt.month == mes_actual) &
        (df["fecha"].dt.day == dia_actual) &
        (df["fecha"].dt.hour == hora_actual)
    ].copy()

    # Comprobar si existen datos para esa fecha/hora
    if df_hora.empty:

        return jsonify({
            "error": (
                "No hay datos históricos disponibles "
                "para esta fecha y hora"
            )
        }), 400
    
    # Si hay varios años disponibles, utilizar el año más reciente
    anio_utilizado = df_hora["fecha"].dt.year.max()

    df_hora = df_hora[
        df_hora["fecha"].dt.year == anio_utilizado
    ].copy()


    # Obtener la fecha exacta utilizada
    fecha_utilizada = df_hora["fecha"].iloc[0]
    meses = [ "enero", "febrero", "marzo", "abril",
        "mayo", "junio", "julio", "agosto",
        "septiembre", "octubre", "noviembre", "diciembre"]

    fecha_formateada = (
        f"{meses[fecha_utilizada.month - 1]} "
        f"{fecha_utilizada.day} - "
        f"{fecha_utilizada.strftime('%H:%M')}"
    )

    print("Año utilizado:", anio_utilizado)
    print("Fecha utilizada:", fecha_utilizada)
    print("Estaciones disponibles:", len(df_hora))

    # Preparar coordenadas y valores de las estaciones
    puntos = df_hora[
        ["longitud", "latitud"]
    ].values

    valores = df_hora["valor"].values

    # Punto correspondiente al celular
    punto_usuario = [
        [longitud, latitud]
    ]

    # Interpolación espacial lineal
    resultado = griddata(
        puntos,
        valores,
        punto_usuario,
        method="linear"
    )

    # Comprobar si se obtuvo un resultado
    pm25 = resultado[0]

    if np.isnan(pm25):

        return jsonify({
            "error": (
                "La ubicación está fuera "
                "del área de interpolación"
            )
        }), 400


    pm25 = float(pm25)

    # Calcular AQI
    aqi, categoria, color = calcular_aqi_pm25(pm25)

    # 4.11 Respuesta para App Inventor
    return jsonify({
        "pm25": round(pm25, 2),
        "aqi": aqi,
        "categoria": categoria,
        "color": color,
        "fecha": fecha_formateada
    })


# 5. INICIAR SERVIDOR
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )