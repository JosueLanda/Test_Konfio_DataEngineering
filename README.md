# Test Konfío
## Data Engineering

## Librerías

Las librerías y frameworks usados se enlistan a continuación : 

| Librería                                 | Detalle                                |
| ---------------------------------------- | -------------------------------------- |
| datapipeline_konfio-0.1-py3-none-any.whl | Archivo wheel de extractor de datos    |
| requests                                 | Libería para realizar solicitudes HTTP |


## Instalación / Ejecución

Para poder ejecutar el programa , se deben seguir los siguientes pasos

1.- Generar el archivo .env , para la ruta que se utilizará posteriormente para el docker

```sh
PATH_LOCAL_USER="PERSONAL_PATH"/Test_Konfio_DataEngineering/
```

2.- Ejecutar

```sh
source Launcher.sh
```
3.- Darle click al url , que se genera una vez levantado el docker:

```sh
http://127.0.0.1:8888/lab?token="generado_por_el_contenedor"
```

4.- Correr el notebook :

```sh
develop_datapipeline.ipynb (abriendo el notebook y corriendolo)
```

## Link Diagrama De Plan De Scalabilidad

https://excalidraw.com/#json=hO3S0jApp5zQ4W1atV6h8,4TUvqz2pI0T7dgpEtQPvYw

## Deudas tecnicas

- 1.-La API , bajo el registro demo; no permitio el intervalo definido en el test, pero se probo con : (2025, 3, 1) al (2025,3,30) a manera de continuar con el test.
- 2.-Data Analysis
- 3.-Testing

## License

MIT

**Free Software**