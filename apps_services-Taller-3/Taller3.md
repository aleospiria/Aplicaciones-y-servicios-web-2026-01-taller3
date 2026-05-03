# Guía de Trabajo Práctico Experimental — Laboratorio 3

**Desarrollo de servicios web seguros con JWT, scopes y reglas de autorización utilizando FastAPI y PostgreSQL**

---

| Campo | Valor |
|---|---|
| **Código de guía** | 003 |
| **Laboratorio** | Laboratorio DevOps |
| **Tiempo de trabajo práctico estimado** | 4 días |
| **Asignatura** | Aplicaciones y Servicios Web |
| **Programa académico** | Tecnología en Desarrollo de Software |
| **Elaborado por** | Juan Carlos Morales Guerra |
| **Revisado por** | Juan Carlos Morales Guerra |
| **Versión** | 002 |
| **Fecha** | 27-02-2026 |

---

## 1. Competencias, Contenido Temático e Indicador de Logro

| Competencias | Contenido Temático | Indicador de Logro |
|---|---|---|
| Diseñar y desarrollar servicios web seguros utilizando FastAPI, PostgreSQL, JWT y scopes, aplicando reglas de autorización, validación de datos y control de acceso según roles dentro de una mesa de servicios para laboratorios universitarios. | Autenticación con JWT. Autorización basada en scopes. Roles de usuario y permisos. Protección de endpoints en FastAPI. Persistencia de datos con PostgreSQL y SQLAlchemy. Modelado de usuarios, laboratorios, servicios y tickets. Reglas de negocio para flujo de estados del ticket. Validación de acceso según rol, scope y relación con el ticket. Pruebas de endpoints protegidos en Swagger. Trabajo colaborativo con Git y GitHub. | El estudiante implementa una API segura para la gestión de tickets de servicios en laboratorios, utilizando JWT para autenticación, scopes para autorización y PostgreSQL para persistencia, aplicando reglas de negocio que controlan la creación, asignación, actualización, consulta y finalización de tickets según el rol del usuario. |

---

## 2. Fundamento Teórico

El desarrollo de servicios web modernos requiere mecanismos que permitan identificar a los usuarios y controlar las acciones que pueden realizar dentro del sistema. La **autenticación** permite verificar la identidad de un usuario, mientras que la **autorización** define qué operaciones está permitido ejecutar según sus permisos.

**JSON Web Token (JWT)** es un estándar abierto (RFC 7519) utilizado para transmitir información segura entre cliente y servidor mediante un token firmado. Después de iniciar sesión, el servidor genera un token compuesto por tres partes: encabezado (*header*), carga útil (*payload*) y firma (*signature*), codificadas en Base64URL y separadas por puntos. El cliente envía este token en cada solicitud protegida dentro del encabezado HTTP `Authorization: Bearer <token>`. De esta manera, la API puede reconocer al usuario sin mantener una sesión tradicional en el servidor.

Los **scopes** permiten representar permisos específicos dentro del sistema. A diferencia de un rol general (como `admin` o `tecnico`), un scope describe una acción concreta, por ejemplo `tickets:crear` o `tickets:finalizar`. Esto facilita controlar el acceso a los endpoints de forma más precisa y escalable, ya que un mismo rol puede tener múltiples scopes y un scope puede ser compartido entre roles diferentes.

**FastAPI** implementa autenticación y autorización mediante el sistema de dependencias de Python. La clase `OAuth2PasswordBearer` gestiona la extracción del token del encabezado, mientras que `SecurityScopes` permite declarar qué scopes requiere cada endpoint. Combinado con **SQLAlchemy** como ORM y **PostgreSQL** como motor de base de datos, FastAPI permite construir servicios web con persistencia de datos, validación mediante **Pydantic** y separación clara entre modelos, esquemas y lógica de acceso a datos.

En este taller, estos conceptos se aplican al desarrollo de una **mesa de servicios para laboratorios universitarios**. El sistema debe controlar que un usuario pueda crear un ticket; que el responsable técnico lo reciba y asigne a un auxiliar o técnico especializado; que el técnico asignado atienda la solicitud y actualice el estado; y que finalmente el responsable técnico revise y cierre el caso. Este flujo exige combinar autenticación, autorización y reglas de negocio para garantizar que cada usuario solo pueda realizar las acciones permitidas dentro del proceso.

---

## 3. Objetivos

### Objetivo General

Desarrollar una API segura para la gestión de tickets de servicios en laboratorios universitarios, utilizando FastAPI, PostgreSQL, JWT y scopes para controlar la autenticación, autorización y flujo de atención de las solicitudes.

### Objetivos Específicos

- Diseñar el modelo de datos para usuarios, laboratorios, servicios y tickets.
- Implementar autenticación de usuarios mediante JWT.
- Definir roles y scopes para controlar el acceso a los endpoints.
- Proteger rutas de la API según los permisos requeridos.
- Implementar reglas de negocio para la creación, recepción, asignación, atención y finalización de tickets.
- Validar la visibilidad de los tickets según el rol y la relación del usuario con la solicitud.
- Probar los endpoints protegidos mediante Swagger o herramienta equivalente.

---

## 4. Recursos Requeridos

### Equipos

- Computador personal o estación de trabajo por estudiante.

### Herramientas de Software

- Sistema operativo Linux o Windows.
- Python 3.10 o superior.
- FastAPI.
- PostgreSQL.
- SQLAlchemy.
- Uvicorn.
- Git.
- Cuenta en GitHub.
- Editor de código (recomendado: Visual Studio Code).

### Dependencias Python del Proyecto

El archivo `requirements.txt` debe incluir como mínimo las siguientes dependencias:

- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `psycopg2-binary`
- `python-jose[cryptography]` — generación y verificación de tokens JWT
- `passlib[bcrypt]` — hashing seguro de contraseñas
- `python-multipart` — requerido por el formulario de login de FastAPI
- `python-dotenv` — manejo de variables de entorno desde archivo `.env`

> **Nota:** Las últimas cuatro dependencias son obligatorias para implementar JWT y autenticación segura. Sin ellas no es posible completar las Actividades 4 y 5.

### Material Bibliográfico y Recursos Digitales

- Documentación oficial de FastAPI: https://fastapi.tiangolo.com
- OAuth2 con scopes en FastAPI: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
- Documentación oficial de Pydantic: https://docs.pydantic.dev
- Documentación oficial de Python: https://docs.python.org
- Documentación de python-jose: https://python-jose.readthedocs.io
- Documentación de passlib: https://passlib.readthedocs.io
- Guías básicas de uso de Git y GitHub.
- Repositorio de clase: https://github.com/Juanmorales177809/apps_services.git

---

## 5. Aspectos de Seguridad

La práctica descrita en esta guía corresponde a una actividad de desarrollo de software, por lo cual no se identifican riesgos físicos o químicos asociados al uso de laboratorios experimentales.

Sin embargo, se recomienda tener en cuenta las siguientes consideraciones:

- Mantener una postura adecuada durante el uso prolongado del computador para evitar fatiga o lesiones musculares.
- Evitar la manipulación inadecuada de cables o conexiones eléctricas de los equipos.
- Realizar copias de seguridad periódicas del código desarrollado para evitar pérdida de información.
- Nunca incluir credenciales sensibles (contraseñas, cadenas de conexión, claves JWT) directamente en el código fuente. Siempre usar variables de entorno mediante un archivo `.env`, el cual debe estar excluido del repositorio mediante `.gitignore`.

---

## 6. Procedimiento o Metodología para el Desarrollo

La práctica se desarrollará en equipos de trabajo conformados por dos a tres estudiantes.

---

### Actividad 1: Configuración Inicial del Proyecto

- Crear repositorio en GitHub.
- Clonar el repositorio en el computador local.
- Crear y activar el entorno virtual.
- Instalar las dependencias listadas en la sección de Recursos Requeridos.
- Generar el archivo `requirements.txt`.
- Crear el archivo `.gitignore` (debe incluir la carpeta del entorno virtual y el archivo `.env`).
- Crear el archivo `.env` para almacenar las variables de entorno sensibles: cadena de conexión a PostgreSQL, `SECRET_KEY`, algoritmo de firma y tiempo de expiración del token.

---

### Actividad 2: Comprensión del Problema y del Modelo de Datos

#### A. Planteamiento del Problema

La universidad requiere una API para gestionar solicitudes de servicios en laboratorios. Una persona podrá crear un ticket seleccionando el laboratorio y el tipo de servicio requerido. El responsable técnico del laboratorio deberá recibir la solicitud, asignarla a un auxiliar o técnico especializado, revisar el avance y finalizar el ticket cuando el servicio haya sido atendido.

El sistema debe controlar el acceso mediante autenticación con JWT y autorización basada en scopes, de modo que cada usuario solo pueda ejecutar las acciones permitidas según su rol.

#### B. Roles del Sistema

| Rol | Descripción |
|---|---|
| `solicitante` | Crea tickets y consulta sus propias solicitudes. |
| `responsable_tecnico` | Recibe, asigna y finaliza tickets. |
| `auxiliar` | Atiende tickets asignados a él; actualiza el estado según el flujo permitido. |
| `tecnico_especializado` | Igual que auxiliar; atiende tickets de mayor complejidad técnica. |
| `admin` | Acceso total al sistema. Puede ver y gestionar cualquier recurso. |

#### C. Scopes del Sistema

Los scopes representan los permisos concretos que se incluyen en el payload del token JWT. Cada rol recibe un conjunto predefinido de scopes al iniciar sesión. La siguiente tabla debe servir como referencia para la implementación de toda la lógica de autorización.

| Scope | Descripción | Roles que lo poseen |
|---|---|---|
| `tickets:crear` | Crear nuevos tickets | solicitante, admin |
| `tickets:ver_propios` | Ver los tickets propios (como solicitante o asignado) | solicitante, auxiliar, tecnico_especializado, responsable_tecnico, admin |
| `tickets:recibir` | Cambiar estado de `solicitado` a `recibido` | responsable_tecnico, admin |
| `tickets:asignar` | Asignar ticket a un auxiliar o técnico | responsable_tecnico, admin |
| `tickets:atender` | Cambiar estado a `en_proceso` o `en_revision` | auxiliar, tecnico_especializado, admin |
| `tickets:finalizar` | Cambiar estado a `terminado` | responsable_tecnico, admin |
| `tickets:ver_todos` | Ver todos los tickets del sistema | admin |
| `usuarios:gestionar` | Crear, listar y consultar usuarios | admin |

#### D. Flujo de Estados del Ticket

El estado de un ticket sigue un flujo estrictamente controlado. Solo se permiten las transiciones indicadas. Cualquier intento de transición fuera de esta tabla debe ser rechazado.

| Estado actual | Estado siguiente | Quién puede realizar la transición | Scope requerido |
|---|---|---|---|
| `solicitado` | `recibido` | responsable_tecnico, admin | `tickets:recibir` |
| `recibido` | `asignado` | responsable_tecnico, admin | `tickets:asignar` |
| `asignado` | `en_proceso` | auxiliar o tecnico_especializado **asignado al ticket**, admin | `tickets:atender` |
| `en_proceso` | `en_revision` | auxiliar o tecnico_especializado **asignado al ticket**, admin | `tickets:atender` |
| `en_revision` | `terminado` | responsable_tecnico, admin | `tickets:finalizar` |

#### E. Modelo de Datos

El sistema se desarrollará a partir de cuatro tablas principales.

##### Tabla `usuarios`

Almacena la información de las personas que interactúan con el sistema.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_usuario` | Integer (PK) | Identificador único |
| `nombre` | String | Nombre completo |
| `correo` | String (unique) | Correo electrónico — usado para iniciar sesión |
| `password_hash` | String | Contraseña almacenada como hash bcrypt |
| `rol` | String | Uno de los roles definidos en la sección B |
| `activo` | Boolean | Indica si el usuario puede iniciar sesión |

##### Tabla `laboratorios`

| Campo | Tipo | Descripción |
|---|---|---|
| `id_laboratorio` | Integer (PK) | Identificador único |
| `nombre` | String | Nombre del laboratorio |
| `ubicacion` | String | Ubicación física |
| `activo` | Boolean | Indica si está operativo |

##### Tabla `servicios`

| Campo | Tipo | Descripción |
|---|---|---|
| `id_servicio` | Integer (PK) | Identificador único |
| `nombre` | String | Nombre del servicio |
| `descripcion` | String | Descripción del tipo de soporte |
| `activo` | Boolean | Indica si está disponible |

##### Tabla `tickets`

| Campo | Tipo | Descripción |
|---|---|---|
| `id_ticket` | Integer (PK) | Identificador único |
| `id_solicitante` | FK → usuarios | Quien crea el ticket |
| `id_laboratorio` | FK → laboratorios | Laboratorio donde se requiere el servicio |
| `id_servicio` | FK → servicios | Tipo de servicio solicitado |
| `id_responsable` | FK → usuarios (nullable) | Responsable técnico que gestiona el ticket |
| `id_asignado` | FK → usuarios (nullable) | Auxiliar o técnico asignado para ejecutar |
| `titulo` | String | Título breve de la solicitud |
| `descripcion` | String | Descripción detallada del problema |
| `estado` | String | Estado actual según el flujo definido |
| `prioridad` | String | baja / media / alta |
| `observacion_responsable` | String (nullable) | Comentario del responsable técnico |
| `observacion_tecnico` | String (nullable) | Comentario del técnico asignado |
| `fecha_creacion` | DateTime | Timestamp de creación |
| `fecha_actualizacion` | DateTime | Timestamp de última modificación |
| `fecha_finalizacion` | DateTime (nullable) | Timestamp de cierre |

**Relaciones principales:**

- `usuarios` 1:N `tickets` (como solicitante)
- `usuarios` 1:N `tickets` (como responsable)
- `usuarios` 1:N `tickets` (como asignado)
- `laboratorios` 1:N `tickets`
- `servicios` 1:N `tickets`

---

### Actividad 3: Configuración de la Base de Datos y Modelos

**Propósito:** Configurar la conexión con PostgreSQL y desarrollar la estructura base de la API mediante modelos SQLAlchemy, esquemas Pydantic y endpoints iniciales.

**Descripción:** El equipo deberá crear las tablas del sistema dentro del schema de PostgreSQL asignado por el docente, configurar la conexión desde FastAPI y desarrollar los componentes iniciales para gestionar usuarios, laboratorios, servicios y tickets.

> **Nota:** No deben crearse tablas en el schema `public` ni en otro que no haya sido asignado.

**Acciones a realizar:**

1. Configurar la conexión a PostgreSQL usando la variable `DATABASE_URL` definida en el `.env`.
2. Crear los modelos SQLAlchemy para las cuatro tablas.
3. Definir claves primarias, claves foráneas y relaciones entre las tablas.
4. Crear los esquemas Pydantic para validar datos de entrada y salida.
5. Implementar endpoints base para crear, listar y consultar registros.
6. Verificar el funcionamiento desde Swagger.

**Endpoints mínimos:**

```
POST   /usuarios/
GET    /usuarios/
GET    /usuarios/{id_usuario}

POST   /laboratorios/
GET    /laboratorios/
GET    /laboratorios/{id_laboratorio}

POST   /servicios/
GET    /servicios/
GET    /servicios/{id_servicio}

POST   /tickets/
GET    /tickets/
GET    /tickets/{id_ticket}
PATCH  /tickets/{id_ticket}/estado
```

---

### Actividad 4: Autenticación con JWT y Gestión de Usuarios

**Propósito:** Implementar el inicio de sesión de usuarios y la generación de tokens JWT para proteger el acceso a la API.

**Descripción:** Los usuarios registrados deberán iniciar sesión con su correo y contraseña. Si las credenciales son válidas, la API genera un token JWT que el cliente envía en las solicitudes protegidas.

**Acciones a realizar:**

1. Agregar almacenamiento seguro de contraseñas usando hash bcrypt.
2. Implementar el endpoint de inicio de sesión `POST /auth/token`.
3. Validar las credenciales del usuario contra la base de datos.
4. Generar un token JWT que incluya como mínimo en el payload:
   - `sub`: correo del usuario
   - `id_usuario`: identificador
   - `rol`: rol del usuario
   - `scopes`: lista de scopes correspondientes al rol (ver tabla de la Actividad 2)
   - `exp`: tiempo de expiración
5. Crear una dependencia para obtener el usuario autenticado a partir del token.
6. Proteger al menos un endpoint usando autenticación JWT.

**Probar desde Swagger el flujo completo:**

1. Crear usuario mediante `POST /usuarios/`.
2. Iniciar sesión mediante `POST /auth/token` con correo y contraseña.
3. Copiar el `access_token` de la respuesta.
4. Hacer clic en el botón **Authorize** en Swagger e ingresar `Bearer <token>`.
5. Consultar un endpoint protegido y verificar que responde correctamente.
6. Intentar acceder sin token y verificar que la respuesta es `HTTP 401`.

**Producto esperado:** El sistema permite autenticar usuarios mediante correo y contraseña, genera un token JWT válido con los scopes del rol y protege endpoints que solo puedan ser accedidos por usuarios autenticados.

---

### Actividad 5: Autorización con Scopes y Reglas de Acceso

**Propósito:** Proteger los endpoints según los scopes requeridos y aplicar reglas de negocio adicionales basadas en la relación del usuario con el ticket.

**Descripción:** No basta con que el usuario esté autenticado. Cada endpoint debe validar dos condiciones de forma independiente:

1. **Verificación de scope:** el token del usuario debe incluir el scope requerido por el endpoint. Si no lo tiene, la API responde con `HTTP 403`.
2. **Verificación de regla de negocio:** incluso con el scope correcto, el usuario debe cumplir la condición de negocio asociada a la acción (por ejemplo, que solo el técnico asignado pueda cambiar el estado de su propio ticket, o que el responsable solo pueda finalizar tickets en estado `en_revision`).

Para implementar esto, se debe crear una dependencia que use `SecurityScopes` de FastAPI, de modo que cada endpoint declare explícitamente qué scopes requiere. Esta dependencia debe extraer los scopes del payload del token y compararlos con los requeridos antes de permitir el acceso.

**Acciones a realizar:**

1. Implementar la dependencia de verificación de scopes usando `SecurityScopes`.
2. Actualizar todos los endpoints de tickets para declarar el scope que requieren.
3. Implementar la lógica de validación de transiciones de estado según la tabla de la Actividad 2.
4. Implementar la validación de relación usuario-ticket: para cambios de estado a `en_proceso` y `en_revision`, verificar que `id_asignado` coincide con el usuario autenticado.
5. Implementar la validación de visibilidad: un solicitante solo puede ver sus propios tickets; un responsable y un asignado pueden ver los tickets en los que participan; el admin puede ver todos.
6. Probar todos los casos de la tabla de evidencias.

> **Criterio clave:** No basta con que el endpoint funcione para el caso positivo. Deben demostrarse dos condiciones:
> 1. Que el usuario **sin scope** recibe `HTTP 403`.
> 2. Que el usuario **con scope** también debe cumplir la regla de negocio. Ejemplo: un responsable técnico tiene el scope `tickets:finalizar`, pero no debe poder pasar un ticket directamente de `solicitado` a `terminado`.

**Evidencias de funcionamiento requeridas:**

El equipo debe realizar las siguientes pruebas con usuarios de diferentes roles y registrar los resultados con capturas de pantalla:

| # | Usuario | Acción | Resultado esperado |
|---|---|---|---|
| 1 | solicitante | Crear ticket | Permitido (200) |
| 2 | solicitante | Asignar ticket | Denegado (403) |
| 3 | responsable_tecnico | Recibir ticket (`solicitado` → `recibido`) | Permitido |
| 4 | responsable_tecnico | Asignar ticket (`recibido` → `asignado`) | Permitido |
| 5 | auxiliar | Cambiar ticket a `en_proceso` | Permitido solo si está asignado a él |
| 6 | auxiliar | Finalizar ticket como `terminado` | Denegado (403) |
| 7 | tecnico_especializado | Cambiar ticket a `en_revision` | Permitido solo si está asignado a él |
| 8 | responsable_tecnico | Finalizar ticket (`en_revision` → `terminado`) | Permitido |
| 9 | solicitante | Ver tickets de otros usuarios | Denegado (403) |
| 10 | admin | Ver todos los tickets | Permitido |

---

### Actividad 6: Trabajo Colaborativo

El equipo deberá evidenciar el trabajo colaborativo mediante el uso de Git y GitHub.

**Requisitos mínimos:**

- Cada integrante debe tener commits identificables con mensajes descriptivos.
- El historial del repositorio debe reflejar la participación de todos los miembros del equipo.
- El README del repositorio debe incluir la descripción del aporte de cada integrante.

---

## 7. Resultado Esperado del Taller

Al finalizar el taller, cada equipo deberá entregar una API funcional desarrollada con FastAPI y PostgreSQL para gestionar tickets de servicios en laboratorios universitarios.

La API debe:

- Implementar autenticación mediante JWT con hashing bcrypt de contraseñas.
- Generar tokens con los scopes del rol del usuario autenticado.
- Proteger endpoints según los scopes definidos en la tabla de la Actividad 2.
- Controlar el flujo de estados del ticket según la tabla de transiciones de la Actividad 2.
- Permitir crear usuarios, laboratorios, servicios y tickets.
- Asignar tickets a auxiliares o técnicos especializados.
- Finalizar tickets únicamente por parte del responsable técnico o administrador.
- Rechazar con `HTTP 403` cualquier acción para la que el usuario no tenga el scope requerido.
- Rechazar con `HTTP 403` o `HTTP 422` las transiciones de estado no permitidas.

La entrega debe incluir el código fuente en el repositorio, la base de datos configurada en el schema asignado, los modelos SQLAlchemy, los esquemas Pydantic, los endpoints funcionales y las evidencias de prueba en Swagger o herramienta equivalente.

---

## 8. Parámetros para Elaboración del Informe

El informe del taller deberá presentarse en formato **README.md** dentro del repositorio del proyecto en GitHub. No se aceptarán informes en formatos externos (PDF, Word, etc.). Toda la documentación debe estar incluida dentro del repositorio.

### Contenido del README.md

#### 1. Información General

- Nombre del proyecto.
- Integrantes del equipo.
- Asignatura.
- Fecha.

#### 2. Descripción del Sistema

- Descripción general del sistema desarrollado.
- Entidades implementadas: Usuarios, Laboratorios, Servicios y Tickets.
- Descripción de la arquitectura utilizada.

#### 3. Configuración del Entorno

- Creación y activación del entorno virtual.
- Instalación de dependencias.
- Uso del archivo `requirements.txt`.
- Configuración del archivo `.env` (describir las variables necesarias sin incluir valores reales).

#### 4. Configuración de la Base de Datos

- Descripción de la conexión a PostgreSQL.
- Schema asignado (sin incluir credenciales sensibles).

#### 5. Endpoints Implementados

Listado completo de endpoints con: método HTTP, ruta, descripción, scope requerido y rol(es) autorizados.

#### 6. Evidencias de Funcionamiento

**Autenticación con JWT:**

- Login exitoso con token generado.
- Uso del botón Authorize en Swagger con Bearer Token.
- Consulta de endpoint protegido con token válido.
- Intento de acceso sin token recibiendo `HTTP 401`.

**Autorización con scopes:**

- Usuario con scope ejecutando acción permitida (captura de pantalla con respuesta HTTP).
- Usuario sin scope recibiendo error `HTTP 403` (captura de pantalla con respuesta HTTP).
- Ejemplo de endpoint protegido por scope.

**Reglas de negocio del ticket:**

- Ticket creado en estado `solicitado`.
- Responsable técnico recibe el ticket (`solicitado` → `recibido`).
- Responsable técnico asigna el ticket a un auxiliar o técnico.
- Auxiliar o técnico cambia estado a `en_proceso`.
- Auxiliar o técnico cambia estado a `en_revision`.
- Responsable técnico finaliza el ticket (`en_revision` → `terminado`).

**Evidencia de restricciones:**

- Solicitante intentando asignar un ticket → error.
- Auxiliar intentando finalizar un ticket → error.
- Usuario intentando modificar un ticket no asignado a él → error.
- Responsable intentando finalizar un ticket que no está en `en_revision` → error.

#### 7. Control de Versiones

- Enlace al repositorio en GitHub.
- Evidencia de commits realizados por cada integrante.
- Descripción breve del aporte de cada miembro.

#### 8. Conclusiones

- Principales aprendizajes.
- Dificultades encontradas.
- Soluciones aplicadas.

> **Nota:** El README debe permitir que cualquier persona pueda clonar el repositorio y ejecutar el proyecto sin necesidad de información adicional fuera del archivo.

### Requisitos del Repositorio

El repositorio debe:

- Contener el código fuente completo organizado según la arquitectura trabajada en clase.
- Incluir el archivo `README.md` correctamente estructurado.
- Incluir el archivo `requirements.txt`.
- Incluir el archivo `.gitignore`.
- No incluir el archivo `.env` con credenciales reales.

---

## 9. Disposición de Residuos

La actividad descrita en esta guía no genera residuos físicos o químicos. En consecuencia, no se requiere un procedimiento específico de disposición de residuos para esta práctica.

---

## 10. Bibliografía

- FastAPI. (2024). *FastAPI Documentation*. https://fastapi.tiangolo.com
- FastAPI. (2024). *OAuth2 with scopes*. https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
- Pydantic. (2024). *Pydantic Documentation*. https://docs.pydantic.dev
- Python Software Foundation. (2024). *Python Documentation*. https://docs.python.org
- python-jose. (2024). *Python JOSE Documentation*. https://python-jose.readthedocs.io
- passlib. (2024). *Passlib Documentation*. https://passlib.readthedocs.io
- Chacon, S., & Straub, B. (2014). *Pro Git*. Apress.
- Fielding, R. (2000). *Architectural Styles and the Design of Network-based Software Architectures*. University of California, Irvine.

