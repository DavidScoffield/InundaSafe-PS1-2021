### Datos que debe recibir el servicio `POST /api/denuncias/`:

| Parámetro | Tipo |
|----------|:-------------:|
| categoria_id |  int |
| coordenadas |    string   |
| apellido_denunciante | string |
| email_denunciante |    string   |
| titulo |    string   |
| descripcion |    string   |

### Restricciones:

- `categoria_id` debe ser un entero que se corresponda con el id de alguna categoría existente
- `coordenadas` no pueden contener letras
- `titulo`, `apellido_denunciante`, `nombre_denunciante` solo pueden contener letras
- `descripcion` no puede tener caracteres especiales
- `telcel_denunciante` solo puede contener números
- `email_denunciante` debe tener un formato de emáil válido
- Todos los campos son obligatorios

### Ejemplo de datos correctos:

```json
{
  "categoria_id":1,
  "coordenadas": "41.40338, 2.17403",
  "apellido_denunciante": "Perez",
  "nombre_denunciante": "Juan",
  "telcel_denunciante": "2218436754",
  "email_denunciante": "juan.perez@gmail.com",
  "titulo": "Alcantarilla tapada",
  "descripcion": "Hay una alcantarilla tapada"
}
```

Como resultado se crea la denuncia con los datos recibidos y retorna el siguiente resultado:

```json
{
  "atributos": {
    "apellido_denunciante": "Perez",
    "email_denunciante": "juan.perez@gmail.com",
    "telcel_denunciante": "2218436754",
    "coordenadas": "41.40338, 2.17403",
    "nombre_denunciante": "Juan",
    "titulo": "Alcantarilla tapada",
    "descripcion": "Hay una alcantarilla tapada",
    "categoria_id": 1
  }
}
```

### Ejemplo de datos incorrectos:

```json
{
  "categoria_id": "1",
  "coordenadas": "4a1.40338, 2.17403",
  "apellido_denunciante": "Perez!",
  "nombre_denunciante": "Juan|",
  "telcel_denunciante": 2218436754,
  "email_denunciante": "juan.perezgmail.com",
  "titulo": "Alcantarilla tapada",
  "descripcion": "Hay una alcantarilla tapada"
}
```
No cumple con las restricciones (retorna 400 Bad Request)

```json

  "coordenadas": a,
  "apellido_denunciante": "Perez!",
  "nombre_denunciante": "Juan|",
  "telcel_denunciante": "2218436754",
  "email_denunciante": "juan.perezgmail.com",
  "titulo": "Alcantarilla tapada",
  "descripcion": "Hay una alcantarilla tapada"
}
```
No es un formato json válido (retorna 400 Bad Request)