# 🦎 08_cozy_gecko

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Version](https://img.shields.io/badge/version-0.2.0-5c7cfa)

**Una pequeña base de IA generativa local, portable y lista para evolucionar.**

Cozy Gecko permite levantar un modelo de lenguaje local y utilizarlo mediante una API propia, sin depender de servicios externos ni modificar el código para cada entorno.

Como en toda buena aventura, empezamos con un compañero pequeño, entendemos cada pieza y evolucionamos solamente cuando hace falta.

## Objetivo

Ofrecer una solución open source que cualquier persona pueda clonar y ejecutar en una computadora compatible con Docker.

```text
Cliente / Swagger
        |
        v
FastAPI :8000
        |
        v
Docker Network
        |
        v
Ollama :11434
        |
        v
Modelo configurable
```

Docker Compose también incluye un inicializador llamado `model-loader`, encargado de descargar automáticamente el modelo configurado antes de iniciar la API.

## Stack

* Docker y Docker Compose
* Ollama 0.32.14
* Llama 3.2 1B
* Python 3.14
* FastAPI
* Uvicorn
* Requests

## Inicio rápido

Requisitos:

* Docker Desktop o Docker Engine con Compose
* Git
* Memoria suficiente para ejecutar el modelo seleccionado

Clonar el repositorio:

```bash
git clone https://github.com/fquirosledesma/08_cozy_gecko.git
cd 08_cozy_gecko
```

Levantar la solución:

```bash
docker compose up -d --build
```

La primera ejecución puede tardar algunos minutos porque Docker descarga la imagen de Ollama y `model-loader` prepara el modelo automáticamente.

Abrir Swagger:

```text
http://localhost:8000/docs
```

Comprobar los servicios:

```bash
docker compose ps -a
```

El estado esperado es:

* `ollama`: healthy
* `model-loader`: exited con código 0
* `api`: healthy

`model-loader` debe finalizar después de preparar el modelo; no es un servicio permanente.

## Configuración

La solución funciona con valores predeterminados, sin necesidad de crear archivos adicionales.

Para personalizarla, copiar `.env.example` como `.env`:

```powershell
Copy-Item .env.example .env
```

En Linux o macOS:

```bash
cp .env.example .env
```

Variables disponibles:

| Variable                  | Valor predeterminado | Descripción                                              |
| ------------------------- | -------------------: | -------------------------------------------------------- |
| `MODEL`                   |        `llama3.2:1b` | Modelo descargado y utilizado por Ollama                 |
| `REQUEST_TIMEOUT_SECONDS` |                `120` | Tiempo máximo de una generación                          |
| `MAX_PROMPT_LENGTH`       |               `4000` | Longitud máxima aceptada para el prompt                  |
| `OLLAMA_URL`              |     Según el entorno | Dirección de Ollama para ejecución local, Docker o cloud |

La API utiliza `localhost:11434` cuando se ejecuta localmente y `ollama:11434` dentro de Docker Compose.

## API

### Estado de FastAPI

```text
GET /health
```

Confirma que la API está funcionando e informa su versión.

### Disponibilidad completa

```text
GET /ready
```

Comprueba que Ollama responde y que el modelo configurado está disponible.

### Generación

```text
POST /generate
```

Request:

```json
{
  "prompt": "Explica qué es Docker en una sola frase."
}
```

Response:

```json
{
  "model": "llama3.2:1b",
  "response": "Docker es una plataforma para ejecutar aplicaciones dentro de contenedores.",
  "duration_ms": 5638
}
```

Ejemplo en PowerShell:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/generate -Method Post -ContentType "application/json; charset=utf-8" -Body (@{prompt="Explica qué es Docker en una sola frase."} | ConvertTo-Json)
```

## Prueba rápida

Con los contenedores levantados, ejecutar:

```bash
python tests/smoke_test.py

## Resiliencia básica

Cozy Gecko incluye:

* Validación del cuerpo JSON.
* Límite configurable para el prompt.
* Timeout de generación.
* Errores claros cuando Ollama no está disponible.
* Health checks para FastAPI y Ollama.
* Verificación de disponibilidad del modelo.
* Volumen persistente para evitar descargas repetidas.
* Ejecución de FastAPI con un usuario sin privilegios.
* Codificación UTF-8 explícita.

## Comandos útiles

Ver logs de la API:

```bash
docker compose logs api
```

Ver logs del inicializador:

```bash
docker compose logs model-loader
```

Detener la solución sin eliminar el modelo:

```bash
docker compose down
```

## Evolución

### v0.1 — Starter

* Ollama y FastAPI en Docker.
* Modelo local.
* API básica de generación.
* Docker Compose.

### v0.2 — Portable

* Configuración mediante variables de entorno.
* Contratos de request y response.
* Health y readiness checks.
* Manejo de errores y timeouts.
* Descarga automática del modelo.
* Dependencias e imágenes controladas.
* Contenedor de API sin privilegios.
* Experiencia reproducible con un único comando.
* Smoke test portable con Python.

### v0.3 — Azure

* Azure Container Registry.
* Despliegue de la API y el motor de inferencia.
* Microsoft Entra ID.
* Azure API Management.
* Logs, métricas y alertas.
* Custom Connector para Power Apps.

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

## Filosofía

Tecnología suficientemente potente para resolver problemas reales, pero suficientemente simple para que siga siendo cercana.

Construir pequeño.
Entender cada pieza.
Evolucionar cuando haga falta.

**Cozy Gecko** 🦎
*Small solutions. Big adventures.*
