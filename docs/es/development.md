# Desarrollo y contratos de extensión

Idioma canónico: inglés. Revisión: 4. Actualización: 2026-10-20. Original sincronizado: [development.md](../en/development.md).

Lee [AGENTS.md](../../AGENTS.md), la [solicitud de III](../phase-iii/REQUEST.es.md) y la [arquitectura](architecture/platform.md) antes de modificar el alcance. El código, comentarios, símbolos y documentación técnica nueva tienen inglés canónico. Conserva el historial científico español y actualiza la traducción técnica emparejada en el mismo cambio.

## Dirección de dependencias

`core` define contratos versionados inmutables, permisos, registro, eventos y puertos. `persistence` implementa metadatos versionados, trabajos y auditoría. `market_data` proporciona catálogo y artefactos sintéticos. `lab` consume esos contratos y registra tareas finitas; `simulation` aporta únicamente contabilidad sintética acotada. `application.py` compone dependencias de confianza. API y CLI adaptan servicios a HTTP y procesos; React consume el contrato HTTP.

Los servicios de dominio no dependen de FastAPI ni de componentes frontend. La base inicial es SQLite en disco local; su interfaz no acredita una implementación PostgreSQL probada. Los adaptadores de artefactos reciben identidades registradas, no rutas elegidas por el cliente. DuckDB opera sobre Arrow verificado con acceso externo y carga de extensiones deshabilitados.

## Tres mecanismos de extensión

| Mecanismo | Procedimiento | Evidencia exigida |
|---|---|---|
| A — añadir módulo | Definir manifiesto, dependencias, estado e interfaces; componerlo explícitamente en la aplicación de confianza | Los servicios existentes siguen funcionando; se rechazan duplicados, dependencias ausentes y ciclos |
| B — añadir capacidad interna | Registrar una capacidad nombrada en un módulo operativo, conservando los contratos | Funciona cuando existe; su ausencia/inactividad falla expresamente sin cambiar comportamientos ajenos |
| C — sustituir implementación | Inyectar en la composición otro adaptador que satisfaga el mismo puerto | Pasa las mismas pruebas de contrato, incluidos fallos y permisos; los consumidores no importan detalles concretos |

`Registry.register`, `Registry.add_capability` y `Registry.call` son puntos de extensión explícitos. `EventBus` es síncrono y local al proceso; no es mensajería distribuida duradera. No existe descubrimiento de plugins no confiables ni endpoint de importación dinámica. Los módulos Python instalados usan los privilegios del proceso; registrarlos no crea aislamiento del sistema operativo.

La sustitución de almacenamiento puede probarse con las implementaciones local y en memoria. Un motor financiero futuro debe entrar detrás de la interfaz de ejecución/contabilidad, con admisión propia por instrumentos y compatibilidad. No conviertas el ledger sintético en un motor de producción indocumentado.

## Datos, trabajos y procedencia inmutable

Utiliza los validadores de contrato para relojes UTC de evento/disponibilidad y cantidades decimales finitas. La disponibilidad desconocida sigue siendo desconocida; no se fabrica desde la hora de observación. Los gráficos convierten valores a coma flotante solo para mostrarlos. La contabilidad emplea decimales e identidad monetaria explícita. USD, USDT y USDC son distintos.

Documentos y auditoría solo admiten adiciones. Cambiar el contenido crea una versión; repetirlo idéntico es idempotente. Configuración y manifiestos de trabajo son inmutables. La adquisición de trabajo es atómica; el cálculo sucede fuera de la transacción y solo puede terminarlo quien todavía posea el intento en ejecución. Conserva fallos, cancelaciones e interrupciones. No reintentes silenciosamente trabajo incierto ni sobrescribas resultados.

Aplica permisos siguiendo la procedencia persistida. Bloquear una ruta de dataset no basta: transformaciones, gráficos, informes, listas de trabajos y workers deben respetar la misma reserva final. La autoridad deriva del registro, no de un indicador `synthetic` o partición recibido del cliente.

La procedencia registra el árbol Python, `pyproject.toml`, `uv.lock`, identidad Git y versiones del entorno. Se comprueba el código cargado frente al disco al enviar/ejecutar y se vuelve a comprobar la identidad antes de publicar el resultado. Reinicia API y todos los workers tras actualizar código ejecutable/dependencias. Es evidencia de reproducibilidad, no certificación firmada de la cadena de suministro. Evita cambios de código/dependencias mientras existan intentos pendientes; envía otro intento si cambia la identidad.

## Alcance del complemento arquitectónico

La [revisión complementaria de cobertura](architecture/supplement.md) y la [evidencia dirigida](architecture/supplement-evidence.md) distinguen invariantes esenciales de funciones aplazadas. Conserva el monolito modular, el historial científico y las prioridades C1–C5. Una plataforma de referencia sirve para comparar, no como autoridad arquitectónica. Restaurar los lockfiles ya aprobados forma parte de la instalación; añadir dependencias requiere la autorización aplicable y una necesidad concreta.

Las referencias inmutables identifican tipo, ID persistente, versión y hash de contenido. Su finalidad es resolver la evidencia exacta utilizada por una ejecución, sin implicar validación científica. Versiones de estrategia/modelo, identidad futura de bot, sesión de despliegue, cuenta y atribución de cartera deben conservarse conceptualmente separadas. No requieren tablas vacías ni servicios nuevos antes de que exista un consumidor que los necesite.

Los contratos actuales de `Signal`, órdenes y cartera sirven al banco técnico acotado. Un objetivo de cantidad no es una predicción general ni una política completa de cartera multibot. Antes de admitir un adaptador de estrategia real, hay que concretar cómo se combinan sus señales, objetivos de cartera, decisiones de riesgo e intenciones de orden, preservando entradas/salidas cohesionadas cuando una secuencia rígida distorsionase la estrategia. No debe suponerse que la posición neta de la cuenta coincide con la propiedad virtual de cada bot. Son requisitos futuros de admisión del adaptador, no asignación de capital implementada ni autorización para operar.

Evaluación científica, preparación técnica, permiso de prueba, estado de ejecución y elegibilidad para recibir capital son dimensiones distintas. Ninguna etiqueta de ciclo de vida, reconsideración de una estrategia retirada, propuesta de IA almacenada o revisión humana concede por sí misma permisos de ejecución. Los futuros servicios de revisión, archivo y conciliación reutilizarán registros versionados y fronteras explícitas de política cuando sus flujos admitidos lo necesiten; no son dependencias de las tareas sintéticas actuales.

## Comprobaciones locales

Instala las dependencias congeladas según [instalación](installation.md) y ejecuta desde la raíz:

```bash
uv run --frozen pytest
uv run --frozen ruff check src tests
uv run --frozen mypy src
npm --prefix web run typecheck
npm --prefix web test
npm --prefix web run build
```

El tipado Python estricto se configura en `pyproject.toml`. Las pruebas emplean datos sintéticos y estado temporal. Incluye fronteras reales entre servicios, persistencia tras reinicio, adquisiciones concurrentes, bloqueo de finalizaciones tardías, cambios de código/entorno, alteración de registros, causalidad temporal, conservación de efectivo/inventario sintético, permisos y rutas de artefactos. No descargues históricos de mercado para aparentar más realismo técnico.

La integración de navegador debe usar API real, estado temporal inicializado y worker efectivo cuando haya trabajos. Comprueba acceso, denegaciones, vacío/error, datos y gráficos sintéticos, transiciones e informes. Los mocks de componentes no satisfacen por sí solos la aceptación integral. Registra comando, entorno y resultado reales; compilar correctamente no demuestra que el navegador funcione.

Para la aceptación en navegador, reserva el puerto loopback 8000 para una API de prueba y utiliza un directorio privado de estado separado. No dirijas estas comprobaciones al estado de investigación personal. Tras compilar la web, inicializa el directorio y arranca la API desde la raíz del repositorio en una terminal:

```bash
uv run --frozen bot-trader --state-dir /workspace/.bot-trader-browser init
uv run --frozen bot-trader --state-dir /workspace/.bot-trader-browser credential viewer
uv run --frozen bot-trader --state-dir /workspace/.bot-trader-browser serve
```

En una segunda terminal, arranca su worker:

```bash
uv run --frozen bot-trader --state-dir /workspace/.bot-trader-browser worker --watch --worker-id browser-worker
```

En una tercera terminal, ejecuta la suite de navegador con esa misma ruta de estado:

```bash
BOT_TRADER_E2E_STATE=/workspace/.bot-trader-browser npm --prefix web run test:e2e
```

La configuración de navegador utiliza Chromium instalado; el entorno Linux administrado dispone de `/usr/bin/chromium`. El runner lee la credencial privada de prueba desde el directorio de estado sin incluir su valor en un comando. Conserva informes, capturas y estado privados; no registres la credencial de acceso. API y worker deben mantener el mismo código/entorno congelado durante la ejecución. Detén ambos procesos de prueba al terminar. Documentar un comando no significa haberlo superado: consulta la verificación para conocer el resultado ejecutado y los requisitos pendientes.

Como alternativa, tras compilar, el helper del repositorio inicializa un estado aislado (admin y viewer), arranca su API y worker, ejecuta Chromium y detiene únicamente esos procesos hijos:

```bash
python scripts/browser-check.py --state-dir /workspace/.bot-trader-browser-check
```

La [lista de aceptación](../phase-iii/acceptance.md) relaciona los requisitos arquitectónicos y de implementación, incluidos D separación de ejecución, E repetibilidad y F web real. Su evidencia determina el cierre; un recuento de tests unitarios no basta.

## Cambios, migraciones y licencias

Añade revisiones Alembic explícitas al cambiar el esquema; no uses `create_all` al arrancar ni edites silenciosamente una revisión desplegada. Conserva invariantes inmutables y compatibilidad. Prueba actualizaciones sobre una copia del estado previo y documenta recuperación antes de publicar. La CLI permite actualización explícita, no downgrade destructivo.

Revisa actualizaciones con lockfiles, compatibilidad y licencias de [stack](architecture/stack.md), [motores](architecture/engines.md) y [herramientas](architecture/research-tools.md). El inventario Python resuelto está en [python-dependencies.json](../licenses/python-dependencies.json); las licencias de terceros no asignan una licencia al código propio del proyecto. Conserva licencia, NOTICE y atribución/enlace visibles de Lightweight Charts con la aplicación; el contrato de datos del gráfico es distinto de la licencia del renderer. Añadir una dependencia no contrata datos ni servicios.

Termina con un commit coherente revisado y actualiza progreso, decisiones y traducciones. Informa del alcance implementado/probado, fallos y límites reales. La validación técnica nunca debe registrarse en `EXPERIMENTS.md` como experimento financiero exitoso.
