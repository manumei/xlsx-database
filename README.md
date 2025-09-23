# Proyecto iLoveXLSX – Bases de Datos (I312)

Este proyecto contiene el esquema, la carga de datos y un conjunto de consultas SQL 
para el sistema **iLoveXLSX**, desarrollado como parte del Trabajo Práctico.

## Estructura del proyecto

iLoveXLSX/
├── sql/
│   ├── create_ilovexlsx.sql      # Script de creación de tablas (BCNF)
│   ├── load_data.sql             # Script de carga de datos desde los CSV
│   └── consults.sql              # Consultas requeridas (15 en total)
├── data/
│   ├── users.csv
│   ├── spreadsheets.csv
│   ├── features.csv
│   ├── feature_runs.csv
│   └── feature_run_details.csv
└── README.md

## Requisitos

- PostgreSQL 12 o superior (puede ejecutarse en instalación nativa o dockerizada).
- Acceso a un usuario administrador con permisos para crear bases de datos.
- Para generar los datos con los scripts de Python, ver requirements.txt

## Instrucciones de ejecución

1. Crear una nueva base de datos llamada `ilovexlsx`:
   CREATE DATABASE ilovexlsx;
<br>
2. Conectarse a la base de datos:
   \c ilovexlsx
<br>

3. Transferir Archivos de Datos
_Si los archivos de datos no se encuentran en un directorio accessible, sino en uno local separado, se recomienda moverlo desde la consola usando el comando ```docker cp "path_al_archivo_local/archivo" servidor_postgresql:/tmp/archivo.csv``` o a la carpeta que se desee dentro del postgresql dockerizado, para para moverlos a dicho directorio, y luego ejecutar los comandos_
<br>

4. Ejecutar el script de creación del esquema:
   ```\i sql/create_ilovexlsx.sql```
<br>
5. Ejecutar el script de carga de datos.  
   - Si los archivos `.csv` ya están en un directorio accesible por PostgreSQL (ver Paso 3), ajustar las rutas en `sql/load_data.sql` según sea necesario
   - Ejemplo (si los `.csv` están en `/tmp` dentro de un contenedor Docker):
    ```\i sql/load_data.sql``` como lo dejé en la entrega ya deberia funcionar
<br>
6. Ejecutar el conjunto de consultas:
```\i sql/consults.sql```

## Notas

- Los CSV provistos en `data/` contienen datos ficticios generados para el TP con los scripts en src/ 
- El esquema cumple con **Forma Normal de Boyce–Codd (BCNF)**.  
- Las consultas en `consults.sql` cubren selección, proyección, joins, agregaciones, agrupamientos y ordenamientos, según lo requerido.
