# 🦎 08_Cozy_Gecko

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Python](https://img.shields.io/badge/Python-3.14-blue)

**Una pequeña base de IA generativa local, simple, portable y lista para evolucionar.**

Cozy Gecko nace como un laboratorio para explorar cómo construir soluciones de IA que no necesiten empezar siendo enormes para ser útiles.

La idea es sencilla: levantar un modelo local, exponerlo mediante una API propia y construir desde ahí, paso a paso.

Como en toda buena aventura, empezamos con un compañero pequeño y una arquitectura simple. Después veremos hasta dónde puede evolucionar.

## 🎯 Objetivo

Tener una solución de IA generativa que pueda ejecutarse localmente utilizando contenedores y que posteriormente pueda desplegarse en distintos entornos cloud.

```text
Cliente / Swagger
       ↓
FastAPI :8000
       ↓
Docker Network
       ↓
Ollama :11434
       ↓
Llama 3.2 1B
```

## 🧩 Stack

- Docker + Docker Compose
- Ollama
- Llama 3.2 1B
- Python
- FastAPI
- Uvicorn

## 🚀 Cómo ejecutarlo

Requisitos:

- Docker Desktop
- Git

Clonar el proyecto y ejecutar:

```bash
docker compose up -d --build
```

Luego abrir:

```text
http://localhost:8000/docs
```

Desde ahí se puede probar la API mediante Swagger.

### Health Check

```text
GET /health
```

### Generación

```text
POST /generate
```

La API recibe un prompt, consulta el modelo ejecutándose en Ollama y devuelve una respuesta simplificada junto con información básica de ejecución.

## 🌱 Evolución

**v0.1 — Starter**

- Ollama en Docker
- Modelo local
- API con FastAPI
- Docker Compose

**Próximas evoluciones**

- Configuración mediante variables de entorno
- Selección de modelos
- Métricas
- Autenticación
- RAG y conocimiento privado
- GPU
- Deploy en Azure, AWS y GCP

## ✨ Filosofía

Tecnología suficientemente potente para resolver problemas reales, pero suficientemente simple para que siga siendo cercana.

Construir pequeño.  
Entender cada pieza.  
Evolucionar cuando haga falta.

**Cozy Gecko** 🦎  
*Small solutions. Big adventures.*