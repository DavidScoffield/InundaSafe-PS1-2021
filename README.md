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

---

**/api/zonas-inundables**

@param: **pagina** -> int  
 @param: **por_pagina** -> int

Ejemplos:

- [localhost/servidor]/api/zonas-inundables
- [localhost/servidor]/api/zonas-inundables?pagina=2
- [localhost/servidor]/api/zonas-inundables?por_pagina=15
- [localhost/servidor]/api/zonas-inundables?pagina=5&por*pagina=6  
  \_Ver mas ejemplos en el archivo /request/flood_zones/get_all_paginated.rest*

---

**/api/zonas-inundables/:id**

Ejemplos:

- [localhost/servidor]/api/zonas-inundables/6
- [localhost/servidor]/api/zonas-inundables/6a
  _Ver mas ejemplos en el archivo /request/flood_zones/get_by_id.rest_

---

- Denuncias:

---

**/api/denuncias**

- [localhost/servidor]/api/denuncias/

Realiza la creación de una denuncia en base a los parámetros recibidos por post.

_Ver ejemplos en el archivo /request/complaints/create.md_

## Comentarios sobre Mapa

- Hemos encontrado un bug en los **mapas de zonas inundables**, en donde en algunos telefonos celulares el mismo no se muestra, mientras que en otros si. En base a la informacion recolectada, concluimos que sea algun tipo de bug con el pluggin `Draw de Leaflet` incorporado para la implementacion del mismo. En navegadores web por su parte, en cualquier tipo de resolucion el mismo funciona correctamente.

#### Resoluciones

Probando en un celular con resolucion 375 x 667 el mapa no se veia, pero por ejemplo en un celcular de 5,5" el mismo si podia verse. Intentanto con distintos modelos con distintas resoluciones, en algunos se veia mientras que en otros no.

A continuacion se encuentra el acceso a la issue perteneciente a este problema.
https://gitlab.catedras.linti.unlp.edu.ar/proyecto2021/proyectos/grupo24/-/issues/83

## Validación CSRF

Detectamos un bug a la hora de realizar las validaciones de los formularios de la aplicación privada del sistema, el cuál provoca que dicha validación falle informando "The CSRF token is invalid". Este bug ocurre de forma aparentemente "aleatoria" al enviar un formulario al servidor. La función donde se arroja la excepción es llamada "[`validate_csrf`](https://flask-unchained.readthedocs.io/en/latest/_modules/flask_wtf/csrf.html)" (perteneciente a la librería [`Flask-WTF`](https://flask-wtf.readthedocs.io/en/0.15.x/)).

Intentamos solucionar el problema renderizando los campos del formulario uno a uno (en lugar de de utilizar la función "render_form"), actualizando el archivo de requirements, borrando librerías que podrían llegar a tener conflictos entre sí, aumentando el tiempo de expiración del token CSRF, renderizando el token de distintas maneras (invocando los métodos "csrf_token" y "hidden_tag" del formulario, e invocando a la función "csrf_token"), pero no tuvimos éxito. Siguiendo los pasos de la [`documentación oficial`](https://flask-wtf.readthedocs.io/en/0.15.x/csrf/) tampoco pudimos solucionar el problema.

Issue perteneciente a este problema: [`#87`](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2021/proyectos/grupo24/-/issues/87).

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

## TESTING

- Tener creada la base de datos "_grupo24tests_" (las credenciales se encuentran especificadas en el archivo “config.py”, en la definición de la clase “[`TestingConfig`](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2021/proyectos/grupo24/-/blob/master/config.py#L66)“)
- Ejecutar siguiente comando desde la raíz del proyecto para correr los tests:

  ```
  python -m unittest -v
  ```
