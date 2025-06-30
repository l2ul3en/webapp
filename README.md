# 🕸️ WebApp NOC

Aplicación web desarrollada en Django para concentrar diferentes WebApps, ademas de visualizar reportes personalizados.

---

## 🚀 Requisitos

- Python >= 3.11
- Podman y Podman Compose
- Git

---

## 📦 Instalación manual (modo local sin Podman)

### 1. Clonar el repositorio

```bash
git clone https://github.com/l2ul3en/webapp.git
cd webapp
```
### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4. Configurar variables de entorno
Crear un archivo <mark>.env</mark>:
```bash
SECRET_KEY=tu_clave_secreta
ZABBIX_URL=https://zabbix.ejemplo.com/api_jsonrpc.php
ZABBIX_TOKEN=token_de_acceso

DB_HOST=localhost
DB_PORT=5432
DB_NAME=webapp_db
DB_USER=webapp_user
DB_PASSWORD=webapp_pass

DJANGO_ENV=development
```
### 5. Ejecutar migraciones y servidor
```bash
python manage.py migrate --settings=config.settings.development
python manage.py runserver
```
---
## 🐳 Uso con Podman y Podman Compose
### 1. Crear archivo <mark>.env</mark>
```bash
cp .env.example .env
```
Edita <mark>.env</mark> con tus valores reales.
### 2. Construir e iniciar el contenedor (modo QA)
```bash
docker compose up --build
```
Esto levanta:
-  PostgreSQL en <mark>localhost:5432</mark>
- Django en <mark>localhost:8080</mark>
- El entorno se define con <mark>DJANGO_ENV=development</mark> o <mark>production</mark> en tu <mark>.env</mark>

### 📁 Estructura del proyecto
```bash
webapp/
├── config/                         # Configuración por entorno (dev/prod)
├── reports/                        # App principal de reportes
├── templates/                      # Plantillas HTML
├── static/                         # Archivos estáticos
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── .env.example
└── manage.py
```

### 🔧 Comportamiento del contenedor
El script <mark>entrypoint.sh</mark> ejecuta lo siguiente al levantar el contenedor:

> 1. Espera a que PostgreSQL esté disponible.
> 2. Aplica automáticamente <mark>python manage.py migrate</mark>.
> 3. Lanza el servidor Django con la configuración adecuada (development o production).
