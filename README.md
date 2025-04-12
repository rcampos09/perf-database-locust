
# Perf-Test Stack: PostgreSQL Performance Testing

Este proyecto fue creado por **Rodrigo Campos Tapia** ([@dontester_](https://twitter.com/dontester_)) con fines **100% prácticos** para realizar pruebas de rendimiento enfocadas en bases de datos **PostgreSQL**, integrando herramientas modernas de monitoreo, observabilidad y generación de carga.

## 🎯 Objetivo

Diseñar y ejecutar pruebas de rendimiento sobre una base de datos PostgreSQL, monitoreando en tiempo real el comportamiento del sistema mediante Prometheus y Grafana, e inyectando carga con Locust.

---

## 🧱 Stack Tecnológico

| Componente         | Función |
|--------------------|---------|
| **PostgreSQL**     | Motor de base de datos relacional. Contiene la tabla `users` sobre la que se ejecutan consultas de lectura y escritura. |
| **Locust**         | Herramienta de pruebas de carga en Python. Genera múltiples usuarios concurrentes que ejecutan queries sobre PostgreSQL. Contiene un `locustfile.py` personalizado. |
| **Prometheus**     | Sistema de monitoreo que recopila métricas de los componentes del stack. Configurado para recolectar métricas del `postgres-exporter`. |
| **Grafana**        | Dashboard de visualización de métricas en tiempo real. Conectado a Prometheus. |
| **Postgres Exporter** | Exporta métricas del motor PostgreSQL en formato compatible con Prometheus. Expuesto como servicio dentro del namespace `perf-test`. |
| **Kubernetes**     | Orquesta todos los componentes del stack definidos como manifiestos YAML. Se utiliza el `namespace: perf-test` para aislar el entorno. |

---

## 📁 Estructura del proyecto

```bash
.
├── grafana
│   ├── deployment.yaml
│   └── service.yaml
├── locust
│   ├── Dockerfile
│   ├── deployment.yaml
│   ├── locustfile.py
│   ├── requirements.txt
│   └── service.yaml
├── namespace.yaml
├── postgres
│   ├── deployment.yaml
│   ├── pvc.yaml
│   ├── service.yaml
│   └── init.sql
├── postgres-exporter
│   ├── deployment.yaml
│   ├── service.yaml
│   └── serviceMonitor.yaml
└── prometheus
    ├── configmap.yaml
    ├── deployment.yaml
    └── service.yaml
```

---

## 🧾 Base de Datos: Tabla `users`

Agrega el archivo `init.sql` dentro de la carpeta `postgres/` con el siguiente contenido para crear la tabla `users` y poblarla con datos de prueba:

```sql
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Datos mínimos de prueba
INSERT INTO users (name, email) VALUES
('Juan Pérez', 'juan@example.com'),
('Ana Gómez', 'ana@example.com');
```

### 🔧 Cómo montar `init.sql`

Agrega el siguiente volumen en el `deployment.yaml` de PostgreSQL para que se ejecute automáticamente al inicializar la base de datos:

```yaml
volumeMounts:
  - name: init-sql
    mountPath: /docker-entrypoint-initdb.d/init.sql
    subPath: init.sql

volumes:
  - name: init-sql
    configMap:
      name: init-sql-config
```

Luego, crea un `ConfigMap` con el contenido del archivo `init.sql`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: init-sql-config
  namespace: perf-test

data:
  init.sql: |
    (Contenido de tu script aquí)
```

---

## 📌 Puertos expuestos

| Componente         | Puerto | Descripción                        |
|--------------------|--------|------------------------------------|
| PostgreSQL         | 5432   | Acceso a la base de datos          |
| Postgres Exporter  | 9187   | Métricas en formato Prometheus     |
| Prometheus         | 9090   | Interfaz para consultas de métricas|
| Grafana            | 3000   | Dashboards de visualización        |
| Locust             | 8089   | UI para pruebas de carga           |

---

## 🚀 Cómo usar este proyecto

1. **Crear el namespace:**
   ```bash
   kubectl apply -f namespace.yaml
   ```

2. **Desplegar los servicios en este orden:**
   ```bash
   kubectl apply -f postgres/
   kubectl apply -f postgres-exporter/
   kubectl apply -f prometheus/
   kubectl apply -f grafana/
   kubectl apply -f locust/
   ```

3. **Acceder a las interfaces:**
   - **Locust UI**: `http://<NodeIP>:<PortForwarded>:8089`
   - **Grafana UI**: `http://<NodeIP>:<PortForwarded>:3000` (usuario y clave por defecto: admin / admin)

---

## 🧪 ¡Haz tus pruebas!

Con todo desplegado, accede a Locust, inicia la carga, y visualiza el comportamiento del sistema en tiempo real desde Grafana.

---

## 📚 Documentación complementaria

- [📖 PostgreSQL Exporter Docs](https://github.com/prometheus-community/postgres_exporter)
- [📖 Prometheus Docs](https://prometheus.io/docs/introduction/overview/)
- [📖 Grafana Docs](https://grafana.com/docs/)
- [📖 Locust Docs](https://docs.locust.io/en/stable/)
- [📖 Kubernetes Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)

---

## 📢 Autor

**Rodrigo Campos Tapia**

- 🐦 [@dontester_](https://twitter.com/dontester_) – Twitter
- 📷 [@dontester_](https://www.instagram.com/dontester_/) – Instagram
- 💼 [LinkedIn](https://www.linkedin.com/in/rcampostapia/) – Perfil profesional
