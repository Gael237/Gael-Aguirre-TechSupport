# Sistema de Soporte Técnico

**Equipo: ** Gael Aguirre
**Dominio:** Sistema de Soporte Técnico
**Fecha:** Abril 2026

---

## ¿Qué problema resuelve?

Este sistema permite a los clientes reportar problemas técnicos mediante tickets, los cuales pueden ser gestionados por el equipo de soporte hasta su resolución. Facilita el seguimiento de incidencias, priorización de tareas y asignación de técnicos.

---

## Arquitectura

El sistema está construido bajo una arquitectura de **microservicios**:

* **Servicio A (Frontend + API):**

  * Maneja la interfaz HTML
  * Procesa las solicitudes del usuario
  * Se conecta a la base de datos (RDS MySQL)
  * Llama al servicio B para tareas pesadas

* **Servicio B (Worker):**

  * Ejecuta tareas pesadas simuladas (`time.sleep(5)`)
  * No expone interfaz al usuario
  * Solo responde a llamadas internas

Ambos servicios corren en contenedores Docker usando **Docker Compose**.

---

## Estructura de la Base de Datos

| Tabla    | Descripción                 | Relación                 |
| -------- | --------------------------- | ------------------------ |
| clientes | Información de los clientes | Se relaciona con tickets |
| tecnicos | Información de técnicos     | Se relaciona con tickets |
| tickets  | Tickets de soporte          | FK a clientes y técnicos |

---

## Rutas de la API

| Método | Ruta          | Descripción                                       |
| ------ | ------------- | ------------------------------------------------- |
| GET    | /             | Interfaz principal (formulario HTML)              |
| POST   | /crear_ticket | Crea un nuevo ticket                              |
| GET    | /tickets      | Muestra todos los tickets ordenados por prioridad |
| POST   | /estado       | Actualiza el estado de un ticket                  |
| POST   | /asignar      | Asigna un técnico a un ticket                     |

---

## ¿Cuál es la tarea pesada y por qué bloquea el sistema?

La tarea pesada se encuentra en el **Servicio B**, donde se utiliza `time.sleep(5)` para simular un proceso costoso como el envío de notificaciones o procesamiento de datos.

Cuando se crea un ticket, el Servicio A realiza una llamada al Servicio B. Si múltiples usuarios realizan solicitudes al mismo tiempo, estas tareas pueden acumularse y generar retrasos, simulando un escenario real de carga en el sistema.

---

## Cómo levantar el proyecto

```bash
# 1. Clonar el repositorio
git clone [URL_DEL_REPO]

cd equipo-techsupport/microservicios

# 2. Crear las tablas en RDS
mysql -h ENDPOINT_RDS -u admin -p < ../schema.sql

# 3. Construir y levantar contenedores
docker-compose up --build

# 4. Acceder desde navegador
http://IP_EC2:5000
```

---

## Variables de entorno

Estas variables se definen en `docker-compose.yml`:

* DB_HOST = Endpoint de RDS
* DB_USER = Usuario de MySQL (admin)
* DB_PASSWORD = Contraseña
* DB_NAME = Nombre de la base de datos

---

## Decisiones técnicas

Se decidió utilizar una arquitectura de microservicios para separar la lógica del sistema en componentes independientes, permitiendo mayor escalabilidad y mantenibilidad.

El Servicio A se encarga de la interacción con el usuario y la base de datos, mientras que el Servicio B maneja procesos pesados, evitando bloquear la experiencia del usuario.

Se implementó manejo de errores con `try/except` y cierre de conexiones en bloques `finally` para asegurar estabilidad. Además, se utilizaron consultas parametrizadas para prevenir inyección SQL.

---


## Puntos Extra — Microservicios

El sistema cumple con los criterios de microservicios:

Separación de responsabilidades entre servicios
Comunicación interna mediante hostname (servicio_b)
Servicio B no expone puertos
Resiliencia: el sistema sigue funcionando aunque B falle

---
