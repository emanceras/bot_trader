# Instalación y configuración

Idioma canónico: inglés. Revisión: 3. Actualización: 2026-10-20. Original sincronizado: [installation.md](../en/installation.md).

Esta guía instala la plataforma técnica local de Fase III desde el código fuente. No crea conexiones con exchanges, contrata servicios ni descarga históricos de mercado. El estado de verificación figura en [progreso de III](../phase-iii/PROGRESS.md); los comandos describen el procedimiento soportado, no una aceptación independiente.

## Requisitos y dependencias

Utiliza Python 3.12, `uv`, Node.js 24 y npm. La implementación se ha desarrollado en Linux. No se han certificado permisos de Windows, otros sistemas operativos ni despliegues en varios hosts. Python 3.13 queda fuera del requisito actual del paquete. Se necesita el checkout fuente porque migraciones, hipótesis originales, archivos de procedencia y web compilada se cargan desde su raíz.

Desde la raíz del repositorio:

```bash
uv sync --frozen
npm --prefix web ci
npm --prefix web run build
```

`uv.lock` y `web/package-lock.json` fijan las dependencias resueltas. Instalarlas requiere acceso a los registros de paquetes salvo que estén en caché. No sustituyas la instalación congelada por una actualización de dependencias sin revisión. SQLite no requiere servidor de base de datos, Redis ni Docker. PostgreSQL es una alternativa arquitectónica; todavía no existe un adaptador PostgreSQL que configurar.

En un entorno cloud administrado donde las cachés predeterminadas del usuario no sean escribibles, configura cachés dentro del workspace antes de instalar o ejecutar comprobaciones:

```bash
export UV_CACHE_DIR=/workspace/.cache/uv
export NPM_CONFIG_CACHE=/workspace/.cache/npm
uv sync --frozen
npm --prefix web ci
```

Un fallo de permisos de caché no demuestra que el archivo del paquete sea inválido. Conserva la verificación TLS/checksum y comprueba la ubicación de caché antes de reintentar. Estas rutas contienen dependencias de desarrollo, no credenciales de la aplicación. Mantén las variables en las terminales donde ejecutes los comandos siguientes o configúralas en el entorno administrado.

## Inicialización y arranque

```bash
uv run --frozen bot-trader init
uv run --frozen bot-trader fixture --seed 42 --rows 120
uv run --frozen bot-trader serve
```

`init` migra explícitamente los metadatos, crea una credencial privada de administrador una sola vez e importa H-00–H-24 desde `HYPOTHESES.md`. Repetir la inicialización no sustituye la credencial ni borra registros. El comando del fixture crea barras sintéticas con semilla e imprime el identificador del dataset registrado. No ejecuta un experimento financiero.

La API sirve la web compilada en `127.0.0.1`, puerto `8000`. Abre esa dirección en tu navegador local. Si falta la compilación, la página raíz devuelve un error 503 explícito; compila antes de arrancar el servidor. Un esquema de base de datos ausente o incompatible también exige inicialización/migración explícita; el servidor no lo repara silenciosamente.

La inicialización muestra la ruta de la credencial, normalmente `.state/admin.token`. Lee su contenido privadamente en tu equipo e introdúcelo en la pantalla de acceso. Nunca lo copies a una transcripción compartida, incidencia, chat o repositorio. Es autenticación de la aplicación local; no se necesita ninguna clave de exchange.

Arranca otro proceso worker desde el mismo checkout y directorio de estado:

```bash
uv run --frozen bot-trader worker --watch --worker-id local-worker
```

Sin `--watch`, el worker procesa como máximo una tarea técnica pendiente y termina. El servidor no inicia un worker automáticamente. Conserva la identidad que imprime para recuperar interrupciones. Una tarea puede permanecer en cola mientras el worker está detenido; el panel no monitoriza su latido.

## Rutas y configuración

El estado se guarda por defecto en `.state/`, ignorado por Git. Incluye `metadata.sqlite3`, artefactos inmutables y credenciales privadas por rol. La base de datos y los artefactos forman un único registro lógico; conservar solo una parte no basta para restaurarlo.

El argumento global `--state-dir` debe aparecer **antes** del subcomando. Usa el mismo valor para todos los procesos:

```bash
uv run --frozen bot-trader --state-dir /workspace/bot-trader-state init
uv run --frozen bot-trader --state-dir /workspace/bot-trader-state serve
uv run --frozen bot-trader --state-dir /workspace/bot-trader-state worker --watch --worker-id local-worker
```

Mantén los directorios personalizados fuera de los archivos versionados y accesibles únicamente para el operador local. `.gitignore` protege la ruta predeterminada; no puede proteger cualquier ruta arbitraria que se elija.

La configuración admite variables con prefijo `BOT_TRADER_`. `Settings` **no carga automáticamente** archivos `.env`; configura expresamente el entorno del proceso. Valores principales:

| Variable | Predeterminado | Significado |
|---|---|---|
| `BOT_TRADER_REPOSITORY_ROOT` | Directorio actual | Raíz de código, migraciones, hipótesis y `web/dist` |
| `BOT_TRADER_DATA_DIR` | `.state` | Directorio de estado, relativo al repositorio salvo ruta absoluta |
| `BOT_TRADER_MODE` | `technical` | Único modo admitido; no puede habilitar trading |
| `BOT_TRADER_ENVIRONMENT` | `development` | Configuración del despliegue, no permiso financiero |
| `BOT_TRADER_ALLOWED_HOSTS` | `["localhost","127.0.0.1"]` | Hosts HTTP aceptados explícitamente, sin comodín |
| `BOT_TRADER_ALLOWED_ORIGINS` | Orígenes HTTP locales en puerto 8000 | Orígenes explícitos obligatorios para mutaciones, incluido login |
| `BOT_TRADER_SECURE_COOKIES` | `false` | HTTP local; configuración de producción exige true y orígenes HTTPS |
| `BOT_TRADER_SESSION_TTL_SECONDS` | `3600` | Duración de sesión, entre 60 y 86.400 segundos |
| `BOT_TRADER_MAX_DATASET_ROWS` | `10000` | Límite de filas sintéticas |
| `BOT_TRADER_MAX_QUEUED_RUNS` | `100` | Límite de cola |

Las variables de tipo lista usan JSON. Cada origen debe corresponder a un host permitido. `BOT_TRADER_ADMIN_TOKEN` puede sustituir la credencial de administrador dentro de un entorno de proceso controlado, pero el archivo privado creado por `init` evita introducir secretos en el historial de comandos. No escribas tokens directamente en comandos del shell.

## Actualización y resolución de problemas

Detén API y workers; crea una copia privada coherente antes de cambiar código o esquema. Instala los lockfiles revisados, recompila la web y ejecuta:

```bash
uv run --frozen bot-trader migrate
```

Las migraciones son actualizaciones explícitas. No se ofrece un procedimiento destructivo de downgrade. Reinicia **la API y todos los workers** después de cambiar código ejecutable o dependencias, y solo cuando pase la comprobación del esquema. Los procesos Python conservan código importado: la plataforma compara su identidad con los archivos en disco y rechaza cambios para no atribuir código antiguo a archivos nuevos. También vuelve a comprobarla al terminar el cálculo. Las tareas pendientes congelan la identidad del código y entorno; si cambió, el worker registra un fallo en lugar de ejecutar silenciosamente código nuevo bajo un manifiesto antiguo. Cuando corresponda, envía un intento nuevo conservando el fallo anterior.

Si el acceso falla, comprueba directorio de estado, permisos privados de la credencial y host/origen utilizado. Reiniciar el servidor invalida las sesiones. Si una tarea sigue en cola, revisa el worker separado. Si queda `running` tras una caída confirmada, utiliza [seguridad y operación](security.md). No edites filas SQLite para forzar un éxito.
