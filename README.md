# Full Stack Banking System Challenge 

Implementar una aplicación que simule el uso de una(s) moneda(s).

Requerimientos.
    - Se debe poder crear una moneda (por ejemplo Peso, Dolar, Bitcoin, etc)
    - Se debe poder enviar dinero entre usuarios (Juan le manda a Pedro 10 pesos)
    - Se debe tener un un registro de las operaciones realizadas.
    - Se debe consultar en cualquier momento el "balance" en una moneda que tiene cada usuario.
    - Tener en cuenta que los usuarios sólo deben hacer operaciones sobre su cuenta.
    - Tener en cuenta la validación de lo datos enviados a la API. (frontside / backside).
    - Tener en cuenta un posible doble gasto u operación concurrente.

La aplicación debe tener un backend con el modelo de datos e implementación de la
lógica de negocios, una API rest que permita realizar las operaciones, y un cliente
web que utilice la API.


Basado en la [plantilla](https://github.com/KartikShrikantHegde/Docker-Flask-Blueprint) de [Kartik](https://github.com/KartikShrikantHegde)

## Iniciando

**Paso 1:** Asegurarse de tener instalado git en su sistema operativo.


**Step 2:** Clone el proyecto en su maquina.

```git clone https://github.com/JhoneM/FSChallenge.git```

### Requisitos

**1. Docker**

Asegurarse de tener docker y docker-compose instalado.

**2. nodejs**

Asegurese de tener nodejs y npm instalado.

### Instalación

**Step 1:** Acceder al directorio donde fue clonado el repo en el paso anterior.

```
cd FSChallenge
```

**Step 3:** Construir e iniciar Backend & APi

```
docker-compose up --build
```
Si ya se ejecuto este comando anteriormente solo se debe ejecutar:

```
docker-compose up
```

**Step 4:** Abrir el navegador en las siguientes ruta.
http://localhost:5000/ => Backend

```
El navegador mostrará la pagina de inicio del sistema.

Credenciales para el backend:
    Usuario: admin
    Password: admin
```
**Step 5:**  Construir e iniciar el cliente web.

```
En una proxima versión se dockerizara todo el proyecto.
Ir al directorio client_web/
```
## Instalacion
```
npm install
```

### Compilar
```
npm run serve
```

http://localhost:8080/ => Cliente Web

El navegador mostrará la pagina de inicio del sistema.

Usuarios de prueba para el cliente web:
    
    Usuario: jmendez
    Password: 1234

    Usuario: martu
    Password: 1234

Pueden registrar mas clientes si así lo desean.

```

El sistema tambien cuenta con un gestor de bases de datos (PhpMyAdmin) alojado en un contenedor, para ingresar se debe ir a la siguiente ruta:
```
http://localhost:8180/
```

## Test

## Deployment

## Construido Con

* [Docker](https://www.docker.com/) -  Contenedores
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web framework
* [Python](https://www.python.org/) - Lenguaje de programación
* [Mysql](mysql.com) - Sistema de gestion de base de datos
* [VueJs](https://vuejs.org/) - Web Framework


## Contribuciones

## Version

## Autores

## Licencia

## Agradecimientos
* KartikShrikantHegde
* jmlcas