import asyncio
import aiohttp
import pandas as pd
from pandas import json_normalize

# Inicializar un DataFrame vacío
df_principal = pd.DataFrame()

# Limitar el número de conexiones concurrentes
semaphore = asyncio.Semaphore(1000)  # Ajusta este número según sea necesario

# Función asíncrona para realizar la solicitud y procesar los datos
async def obtener_datos(session, documento):
    async with semaphore:
        url = f"https://signomedico.dyndns.org:933/api/Afiliados?docId={documento}"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                df_temp = json_normalize(
                    data['data'],
                    'domicilios',
                    [
                        'benId', 'benGrId', 'documento', 'cuil', 'numeroAfiliado',
                        'nombreAfiliado', 'sexo', 'estado', 'convenio', 'plan',
                        'fechaNacimiento', 'legajo', 'email', 'agenteCuenta',
                        'parentesco', 'observaciones', 'medicoCabecera', 'coberturas'
                    ],
                    sep='_',
                    record_prefix='domicilio_'
                )
                return df_temp
            return pd.DataFrame()

# Función principal asíncrona
async def main():
    global df_principal
    async with aiohttp.ClientSession() as session:
        tasks = [obtener_datos(session, doc) for doc in range(33605892, 33705892)]
        results = await asyncio.gather(*tasks)
        df_principal = pd.concat(results, ignore_index=True)

# Ejecutar la función principal
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# Guardar el DataFrame principal en un archivo Excel
df_principal.to_excel("lote_gecros.xlsx", index=False)
