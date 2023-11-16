# Test 3B
## Data Engineering

## Página Scrappeada

https://www.worldometers.info/world-population/population-by-country/

## Librerías

Las librerías y frameworks usados se enlistan a continuación : 

| Librería                                   | Detalle                                        |
| ------------------------------------------ | ---------------------------------------------- |
| tools_datapipeline_3b-0.1-py3-none-any.whl | Archivo wheel , de herramientas propias de ETL |
| requests                                   | Libería para realizar peticiones               |
| beautifulsoup4                             | Librería para realizar el Web Scraping         |
| lxml                                       | Complemento de beautifulsoup4                  |
| delta-spark==2.4.0                         | Librería para construccion del Data Lake       |


## Instalación / Ejecución

Para poder ejecutar el programa , se deben seguir los siguientes pasos

1.- Generar el archivo .env , para la ruta que se utilizará posteriormente para el docker

```sh
PATH_LOCAL_USER="PERSONAL_PATH"/Test_3B_DataEngineering/notebooks
```

2.- Ejecutar

```sh
source Launcher.sh
```
3.- Darle click al url , que se genera una vez levantado el docker:

```sh
http://127.0.0.1:8888/lab?token="generado_por_el_contenedor"
```

4.- Se puede correr el notebook :

```sh
develop_datapipeline.ipynb (abriendo el notebook y corriendolo)
```

o el .py , ejecutando en linea de comandos

```sh
python prod_datapipeline.py
```

## Link Doc - Preguntas Estrategia

https://docs.google.com/document/d/1ukQJ_v3UbQCwjPOCWXNI3PXGifgPp73b6tu3bf6C7_M/edit

## Link Doc - Diagrama De Arquitectura

https://app.diagrams.net/#G13Avo3FfVeTAIuVsC2cP2-DbaP8WdzR9w

## Deudas tecnicas

- 1.-#TODO: Completar tipos de ingesta (incremental,por intervalo , re-proceso)
- 2.-#TODO: Orquestación de datos

## License

MIT

**Free Software**