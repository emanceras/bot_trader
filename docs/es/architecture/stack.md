# Stack de la plataforma y revisión acotada de alternativas

Idioma canónico: inglés. Revisión: 2. Evaluación original: 2026-10-18. Recuperación de evidencia: 2026-10-19. Original sincronizado: [stack.md](../../en/architecture/stack.md). Registro de evidencia: [stack-sources.jsonl](../../architecture/stack-sources.jsonl).

Esta es una decisión arquitectónica para III, no evidencia de implementación, rendimiento ni ventaja financiera. La implementación autorizada utiliza fixtures sintéticos. IV–VI y la simulación prospectiva/operativa conectada a mercados conservan sus puertas independientes. Las versiones instaladas y comprobaciones ejecutables corresponden a los lockfiles y al informe de verificación.

## Decisión y alternativas

| Frontera | Base seleccionada | Alternativa y contrapartida | Condición de reconsideración |
|---|---|---|---|
| API HTTP y contratos | Python, FastAPI, Pydantic 2, esquemas explícitos versionados | Un framework web mayor integra administración/autenticación, pero aumenta el acoplamiento a su modelo. La validación de Pydantic complementa el tipado estático; ninguno demuestra veracidad ni disponibilidad causal de datos. | Identidad organizativa, administración o compatibilidad externa que lo justifiquen |
| Transacciones de metadatos | Repositorios SQLAlchemy 2, migraciones Alembic, SQLite en disco local persistente inicialmente | PostgreSQL es la opción prevista de servidor. Añade servicio, credenciales, copias y operación, pero encaja mejor con varios hosts y escritores concurrentes. Portabilidad diseñada no significa adaptador PostgreSQL probado. | Contención medida, varios hosts/usuarios, acceso por red u otras exigencias de despliegue |
| Artefactos tabulares y análisis | Parquet inmutable versionado, PyArrow para materializarlo y DuckDB para lecturas analíticas acotadas | Guardar todas las series en filas transaccionales mezcla análisis con estados/tareas. No se elige DuckDB como único almacén de metadatos. Un lago distribuido añade infraestructura sin requisito actual. | Tamaño, actualizaciones o concurrencia justifican otro adaptador con contratos equivalentes |
| Cliente web | React, TypeScript, Vite; compilación estática servida con la API en el mismo origen | Next.js permite alojamiento propio, exportación estática y renderizado en servidor; no exige proveedor de pago. Renderizado/caché en servidor añadirían otro modelo de ejecución sin necesidad actual. | Páginas públicas indexables, renderizado en servidor o carga de datos del framework compensan su mantenimiento |
| Tareas técnicas prolongadas | Proceso worker dedicado, estado duradero en base de datos y registro de tareas permitido | RQ requiere Redis/Valkey; Celery añade broker y primitivas potentes de encaminamiento, programación, reintentos y monitorización. Ambos pueden integrarse después. Tareas HTTP en segundo plano o colas en memoria no satisfacen durabilidad. | Varios workers/hosts, encaminamiento, programación o volumen superan el worker local probado |
| Programación periódica | Envío explícito de ejecuciones técnicas finitas; futuro planificador usa la misma interfaz | Un temporizador en cada proceso API arriesga duplicación. Ni cron ni un planificador proporcionan por sí solos semántica duradera de tareas. | Trabajo recurrente autorizado con propietario, idempotencia, zona horaria y política de ejecuciones omitidas |

Se elige un monolito porque estas capacidades comparten identidades, permisos y registros científicos. API y worker se ejecutan en procesos distintos cuando procede; esto no exige microservicios, llamadas de red entre todos los módulos ni un bus distribuido.

## Evidencia y consecuencias de ingeniería

### API y contratos

FastAPI distingue procesos API, arranque, reinicio y replicación de memoria [ST-01]. El cálculo intensivo no debe ejecutarse dentro de peticiones API ni depender de memoria del proceso para compartir estados. Las migraciones se ejecutan explícitamente una vez antes de servir tráfico, no dentro de cada worker API.

Pydantic documenta esquemas derivados del tipado, JSON Schema, validadores y modos estricto/conversor [ST-02]. Los esquemas públicos deben rechazar campos desconocidos cuando corresponda, validar números finitos, precisar zona/precisión y separar DTO versionado de objetos ORM. La validación estricta se decide por campo: las fechas JSON necesitan análisis. Superar un esquema no acredita timestamp fiable, licencia ni aptitud de un dataset.

OpenAPI es la fuente del contrato API, contra la cual se comprueba el contrato frontend. Los servicios de dominio/aplicación no dependen de objetos de petición FastAPI ni sesiones concretas de almacenamiento. La API de tareas no expone rutas arbitrarias de importación Python, SQL, rutas de archivos ni funciones ejecutables.

### Metadatos y artefactos

SQLite admite muchos lectores pero un solo escritor simultáneo; recomienda servidor para muchos escritores o acceso directo desde varios hosts y advierte sobre bloqueos en sistemas de archivos de red [ST-06]. Los metadatos iniciales permanecen en disco local persistente, con transacciones breves, esperas de bloqueo acotadas y reclamación concurrente de tareas probada. El cálculo largo ocurre fuera de transacciones de escritura. SQLite es una opción de despliegue con condición de ampliación, no una aplicación provisional que sustituir.

SQLAlchemy describe el comportamiento transaccional heredado de `sqlite3`, las implicaciones para DDL/savepoints y la configuración de claves foráneas [ST-03]. Deben configurarse y probarse explícitamente; un ORM no lo resuelve automáticamente. Alembic proporciona migraciones para SQLAlchemy [ST-11]. Revisarlas, actualizar almacenes existentes y comprobar copias/restauración sigue siendo responsabilidad de la aplicación. No se anunciará soporte PostgreSQL probado hasta verificar allí migraciones, invariantes, reclamaciones de tareas y fallos.

Parquet contiene datos; los metadatos contienen identidades, versiones de esquema, hashes, procedencia, permisos de partición y referencias. Se publican artefactos inmutables atómicamente y luego se registran. Deben tratarse publicaciones interrumpidas y artefactos huérfanos: un hash acredita integridad, no permiso para abrir una partición reservada. Las copias deben ser coherentes entre ambos almacenes.

DuckDB permite consultas Parquet directas y proyección/filtrado durante su lectura [ST-12b]. Su modo embebido permite un proceso lector/escritor o varios procesos de solo lectura; los hilos escritores tienen semántica de conflictos [ST-08b]. La documentación actual también describe Quack y DuckLake: sería incorrecto afirmar que DuckDB carece universalmente de opciones multiproceso. III elige conexiones analíticas embebidas aisladas sobre archivos inmutables aprobados, sin adoptar esas alternativas distribuidas. No se permiten rutas remotas, SQL ni carga de extensiones arbitrarios desde clientes no confiables; que la biblioteca pueda leer Parquet HTTP no autoriza descargarlo.

### Elección del frontend

La propia documentación React recomienda frameworks en muchos casos y advierte que una aplicación basada solo en herramientas de compilación debe aportar navegación, obtención de datos y estados de carga/error [ST-04]. Documenta Vite como opción React/TypeScript. Nuestra decisión se limita a un dashboard autenticado cuya lógica y datos ya residen en Python. Debe tener navegación estable, acceso API reutilizable, cancelación/errores, estados vacíos reales y gráficos independientes, sin improvisar otro backend en el cliente.

Next.js es una alternativa válida; no se rechaza por ser inherentemente caro o propietario. Su guía oficial contempla proxy inverso, cachés y coordinación entre instancias [ST-05]. La exportación estática evita servidor Node, pero no aporta ventaja inmediata para estos requisitos frente a la SPA elegida. Se evita duplicar autenticación, lógica de negocio o cálculo científico en servidor JavaScript. La compilación Vite exige entorno de construcción compatible; no exige su servidor de desarrollo en producción.

### Tareas, recuperación y propiedad

Celery documenta workers dedicados, mensajes mediante broker, reintentos, encaminamiento y monitorización [ST-09]. RQ es más sencillo, pero también exige Redis o Valkey y un worker [ST-10]. III necesita verificaciones sintéticas finitas: un worker duradero específico evita otro servicio sin atribuirse orquestación general equivalente.

El worker debe persistir estados en cola/en ejecución/completado/fallido, configuración e intentos; reclamar tareas atómicamente; registrar propietario/progreso y permitir recuperación explícita tras perder el proceso. Si se implementan concesiones temporales/reintentos, un propietario antiguo no debe sobrescribir un intento nuevo. No se presupone ejecución exactamente una vez. El trabajo repetido será idempotente o conservará un intento distinto. Se persisten errores estructurados seguros y se mantiene la API disponible. El registro selecciona tareas instaladas confiables, nunca código enviado por el usuario. Un planificador futuro no autoriza investigación continua.

## Licencias, seguridad y costes operativos

| Componente | Declaración primaria comprobada | Consecuencia dentro de esta revisión |
|---|---|---|
| FastAPI; Pydantic; React; Vite; Next.js; DuckDB | Texto MIT, LIC-01–06 | Uso privado permisivo; conservar avisos de copyright/permiso aplicables al redistribuir |
| SQLAlchemy; Alembic | Pie documental SQLAlchemy, ST-03; licencia Alembic, LIC-09 | MIT; las herramientas no sustituyen obligaciones de migración de la aplicación |
| SQLite | Declaración de dominio público, LIC-08 | El núcleo no necesita licencia; herramientas incorporadas pueden tener condiciones propias |
| PostgreSQL | PostgreSQL Licence, ST-07 | Uso, copia, modificación y distribución permisivos con conservación de avisos |
| Apache Arrow / PyArrow | Términos principales Apache-2.0 y alcance de componentes incorporados, LIC-07 | Conservar licencia/NOTICE y avisos aplicables; revisar distribución realmente instalada |
| Celery; RQ | Texto BSD-3-Clause LIC-10; página RQ declara BSD, ST-10 | Alternativas no adoptadas; licencias de broker y dependencias necesitan comprobación propia |

Son instantáneas upstream, no una auditoría completa de dependencias resueltas, asesoramiento jurídico ni derechos sobre datos de exchanges/noticias. Las URL de licencias siguen ramas móviles; los hashes conservan qué se examinó. No se auditó exhaustivamente el apéndice de terceros de Arrow ni la variante exacta BSD de RQ. Durante implementación deben conservarse inventario y avisos de versiones instaladas; no inferir licencias transitivas de la principal.

Los proyectos tienen documentación oficial accesible e interfaces de integración establecidas. Esto acredita capacidades disponibles, no una garantía medida de seguridad, rendimiento o mantenimiento. Fijar/probar versiones, revisar actualizaciones de seguridad y registrar entorno; este documento no ejecutó benchmarks ni auditoría de vulnerabilidades.

Los términos revisados no exigen tarifas iniciales de licencia para los componentes abiertos seleccionados. Hardware, electricidad, almacenamiento, copias, ingeniería y mantenimiento sí cuestan recursos. API/worker/base/cliente local permiten evitar servicios de pago ahora; servidor, PostgreSQL gestionado o broker son alternativas si un requisito concreto justifica su coste. Esta decisión no autoriza compras cloud, credenciales ni licencias de pago.

El despliegue predeterminado es local y autenticado, con roles explícitos, configuración fuera de Git y sin claves de exchanges. Un despliegue remoto futuro necesita TLS, configuración de proxy fiable, identidad/sesiones seguras, límites de recursos y copias. Un mismo origen reduce configuración CORS, pero no constituye autenticación ni control CSRF. El monolito modular no aísla plugins Python maliciosos: solo ejecuta módulos instalados confiables; el investigador autónomo futuro necesitará restricciones separadas de procesos/herramientas.

## Verificación exigida a la implementación

Ejecutar comprobaciones de instalación/arranque, migraciones/persistencia, esquemas/API, compilación/tipado/unidades/integración frontend, permisos y fallos. Demostrar módulo añadido, capacidad interna opcional y sustitución de implementación sin cambiar dominios ajenos. Verificar reproducibilidad técnica e imposibilidad de enviar una orden real. Probar recuperación de tareas y conservar intentos fallidos. El informe distinguirá comprobaciones superadas de capacidades propuestas; esta revisión no marca ninguna como superada.

## Alcance de fuentes

La evaluación original estaba fechada el 2026-10-18. No se recuperaron su registro ni el cache del stack, por lo que aquí no se afirma su historial exacto de descargas. Una recuperación acotada del 2026-10-19 descargó y calculó hashes de doce páginas oficiales sustantivas y diez instantáneas de licencia/declaración. Cuatro solicitudes adicionales devolvieron redirecciones HTML, no documentación; los destinos canónicos `/docs/current/` de ST-08b/ST-12b aportaron el contenido de DuckDB. Las 26 solicitudes de recuperación devolvieron HTTP 200, que por sí solo no acredita contenido sustantivo. Se inspeccionaron secciones pertinentes, no todos los enlaces. El registro separa nuevas recuperaciones y lectura dirigida, sin inventar eventos anteriores. No se añaden estudios académicos, datasets financieros, experimentos de rendimiento ni tareas de investigación continua.
