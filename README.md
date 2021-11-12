# Proyecto de Software - Trabajo Integrador

Aplicación para el trabajo integrador para la materia de Proyecto de Software de la Facultad de Informática de la UNLP.

## Usuarios para logearse

- Usuario administrador:
  - Email: admin@gmail.com
  - Contraseña: Admin123
- Usuario operador:
  - Email: ron@gmail.com
  - Contraseña: Operador123


## APIs:

- Zonas Inundables:    
----------
  **/api/zonas-inundables**  
 
  @param: **pagina** -> int  
  @param: **por_pagina** -> int

  Ejemplos:

  * [localhost/servidor]/api/zonas-inundables
  * [localhost/servidor]/api/zonas-inundables?pagina=2
  * [localhost/servidor]/api/zonas-inundables?por_pagina=15
  * [localhost/servidor]/api/zonas-inundables?pagina=5&por_pagina=6  
  *Ver mas ejemplos en el archivo /request/flood_zones/get_all_paginated.rest*

----------
      
  **/api/zonas-inundables/:id**  
 
  Ejemplos:

  * [localhost/servidor]/api/zonas-inundables/6
  * [localhost/servidor]/api/zonas-inundables/6a
  *Ver mas ejemplos en el archivo /request/flood_zones/get_by_id.rest*
 
-----------

- Denuncias:    

----------
  **/api/denuncias**

  * [localhost/servidor]/api/denuncias/

  Realiza la creación de una denuncia en base a los parámetros recibidos por post.

  *Ver ejemplos en el archivo /request/complaints/create.rest*

## Iniciar ambiente

### Requisitos

- python3
- virtualenv

### Ejecución

```bash
$ virtualenv -p python3 venv
# Para iniciar el entorno virtual
$ . venv/bin/activate
# Instalar las dependencias dentro del entorno virtual
$ pip install -r requirements.txt
# En el directorio raiz
$ FLASK_ENV=development python run.py
```

Para salir del entorno virutal, ejecutar:

```bash
$ deactivate
```

## Estructura de carpetas del proyecto

```bash
config            # Módulo de donde se obtienen las variables de configuración
helpers           # Módulo donde se colocan funciones auxiliares para varias partes del código
models            # Módulo con la lógica de negocio de la aplicación y la conexión a la base de datos
resources         # Módulo con los controladores de la aplicación (parte web)
templates         # Módulo con los templates
db.py             # Instancia de base de datos
__init__.py       # Instancia de la aplicación y ruteo
```