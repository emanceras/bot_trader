# Verificación técnica de la Fase III

Documento: VERIFY-III-001 · Versión: 1 · Actualizado: 2026-10-21 · Idioma: es (traducción).

Original canónico: [inglés](../en/verification.md), sincronizado con VERIFY-III-001 v1. Este informe aporta evidencia de ejecución para el [registro de aceptación](../phase-iii/acceptance.md), la [solicitud original](../phase-iii/REQUEST.es.md) y el [complemento arquitectónico](architecture/supplement.md). La aceptación técnica no valida una hipótesis financiera.

## Alcance y estado actual

La versión implementada es una plataforma local y modular de investigación con servicios HTTP autenticados, registros persistentes y versionados, datos sintéticos, trabajos técnicos acotados, informes y una interfaz web compilada. Su simulador contable es un instrumento determinista para comprobar software, no un motor financiero admitido para backtesting. Se conservan H-00–H-24 y el corpus científico de 53 trabajos. Los experimentos financieros, entrenamiento financiero, paper trading prospectivo y operaciones reales siguen en **cero**.

**Dictamen: III.A y III.B completadas técnicamente dentro del alcance sintético autorizado**, registrado en D-034 y aceptación. Las comprobaciones esenciales siguientes pasan; no implican validación financiera ni autorización de otra fase.

## Entorno y comprobaciones ejecutadas

Las comprobaciones backend/instalación/unidades se ejecutaron el 2026-10-20, con navegador/arranque predeterminado y conciliación final el 2026-10-21, en el entorno Linux gestionado, desde `/workspace/bot_trader`, con Python **3.12.14**, Node.js **24.19.0**, npm **11.9.0**, `uv.lock`/`web/package-lock.json` congelados y Chromium instalado en `/usr/bin/chromium`. Se necesita el checkout de fuentes; esto no certifica un wheel autónomo, instalación Windows, servidor de producción ni restauración del entorno en una tarea nueva.

Se utilizaron cachés escribibles: `UV_CACHE_DIR=/workspace/.cache/uv` y `NPM_CONFIG_CACHE=/workspace/.cache/npm`. Se conservaron los códigos de salida reales; una compilación o ejecución sin pruebas no se contabilizó como batería de pruebas superada.

| Comprobación | Comando ejecutado / evidencia | Resultado registrado |
|---|---|---|
| Instalación limpia de Python | `UV_PROJECT_ENVIRONMENT=/workspace/.bot-trader-clean-venv uv sync --frozen`, con la caché UV escribible | 36 distribuciones instaladas en un entorno nuevo |
| Batería backend en ese entorno | `UV_PROJECT_ENVIRONMENT=/workspace/.bot-trader-clean-venv uv run --frozen pytest -q` | **110 superadas**, una advertencia, 32,49 segundos; sin omitidas ni fallos esperados comunicados |
| Repetición backend final tras conciliar estados de capacidades | `uv run --frozen pytest -q` | **110 superadas**, la misma advertencia, 2,63 segundos |
| Lint Python | `uv run --frozen ruff check src tests` | Superado |
| Tipado estricto Python | `uv run --frozen mypy src` | Superado, 30 archivos fuente |
| Instalación frontend bloqueada | `npm ci --cache /workspace/.cache/npm --no-audit --no-fund`, desde `web` | 110 paquetes instalados; inventario de 152 resueltos, incluidas variantes opcionales por plataforma |
| TypeScript | `npm run typecheck`, desde `web` | Superado |
| Compilación de producción frontend | `npm run build`, desde `web` | Superada; recursos compilados servidos por la API |
| Unidades/componentes frontend | `npm test`, desde `web` | **7 superadas en 3 archivos**, repetición final 1,53 segundos |
| Navegador real F | `python scripts/browser-check.py --state-dir /workspace/.bot-trader-browser-final3` | **2 superadas en 18,2 segundos**, sin omitidas; API, almacenamiento, worker y Chromium reales, sin simular endpoints |
| Navegador final tras alinear estados | `python scripts/browser-check.py --state-dir /workspace/.bot-trader-browser-release` | **2 aprobadas en 19,5 segundos**, 2026-10-21; procesos propios detenidos después |
| Instalación reutilizable/arranque predeterminado | Script guardado exacto; `bot-trader init` repetido; `serve` y `worker` finito reales | Aprobado: instalación/build/init fijados, credencial privada intacta, lecturas autenticadas de 25 hipótesis/15 módulos, HTML y licencias; sin trabajo financiero en cola |
| Restauración con escritores detenidos | Copiar el estado privado coherente tras detener los procesos propios de API/worker; comprobar registros y artefactos mediante servicios de aplicación | **Superada**: 12 hashes de archivo idénticos; 25 hipótesis, un dataset/24 barras, tres intentos conservados y hashes de informes verificados |

Para la restauración, el arnés de navegador había detenido su API y worker. Una comprobación Python invocada con `uv run --frozen python` copió `/workspace/.bot-trader-browser-final3` al nuevo directorio separado `/workspace/.bot-trader-restore-check` mediante `shutil.copytree`. Los 12 SHA-256 de archivo coincidían antes de abrir la copia. La comprobación de esquema y `build_services` leyeron las 25 hipótesis restauradas, un dataset con 24 barras y tres intentos: dos completados y uno que conservaba `intentional_fixture_failure`. Cada informe JSON completado coincidía con su digest registrado. No se alteró el original ni se repitió ningún trabajo. Se verifica una restauración local coherente con escritores detenidos, no backup online, recuperación entre hosts ni recuperación sin snapshot utilizable.

Tras superar navegador, el inventario de módulos se ajustó al alcance comprobado: `web` y `charting` son operativos dentro de la plataforma sintética. La repetición backend final, Ruff, Mypy estricto, TypeScript, unidades frontend y compilación de producción pasaron tras ese cambio. La sección de configuración cloud reutilizable registra el guardado confirmado y los límites de publicación/restauración; no se presume una tarea nueva comprobada.

La única advertencia backend procede del cliente de pruebas FastAPI/Starlette sobre su integración actual con `httpx` y una transición futura de dependencias. Las pruebas sí se ejecutaron correctamente. No se ocultó la advertencia ni se añadió una dependencia solo para suprimirla. Las versiones resueltas y las identidades de archivos quedan en los lockfiles.

## Demostraciones obligatorias A–F

| Puerta | Evidencia concreta ejecutada | Interpretación y límites |
|---|---|---|
| A — módulo nuevo | `tests/test_core.py::test_a_add_module_and_b_extend_internal_capability`; `test_registry_rejects_missing_cycles_and_prepared_execution` | Se invoca una extensión explícita sin modificar el consumidor; se rechazan duplicados, dependencias ausentes, ciclos y capacidades inactivas. No se afirma aislamiento de plugins no confiables. |
| B — capacidad interna | La misma prueba añade una capacidad opcional y conserva la existente; `web/src/chart/SeriesChart.test.tsx` comprueba entradas y limpieza del renderer | Funcionan los límites públicos de composición/renderizado. No implica que todos los módulos futuros estén implementados. |
| C — sustitución | `tests/test_market_data.py::test_repeatability_provenance_and_memory_substitution`, `test_memory_store_and_local_store_share_missing_and_format_failures`; `tests/test_simulation.py::test_c_same_ledger_consumer_accepts_execution_and_cost_substitution`; sustitución de transformación en core | Adaptadores reales local/memoria y de ejecución/costes cumplen consumidores y contratos de error comunes. No se certifican PostgreSQL, almacenamiento externo ni motores financieros maduros. |
| D — aislamiento | Pruebas de modos/roles del core; `tests/test_lab.py::test_final_lineage_blocks_submit_reads_reports_and_worker`; partición reservada en datos; rutas ausentes y roles en API | Todos los roles, incluido admin, tienen denegados payloads finales y acciones financieras. Lecturas, transformaciones, informes y workers siguen la procedencia guardada. No se incluyen rutas paper/live/órdenes/importación de mercado/herramientas. No aísla frente al administrador del sistema. |
| E — reproducibilidad | `tests/test_lab.py::test_e_repeated_attempts_same_inputs_have_identical_persisted_results`, parametrizada para calidad, transformación y contabilidad; fallos persistidos, reinicio, deriva y código importado obsoleto | Intentos distintos conservan digests de informe iguales con entradas e identidad congeladas iguales. Una semilla no garantiza equivalencia entre plataformas; se rechazan cambios de fuente/entorno. |
| F — web real | `web/e2e/platform.spec.ts`, arnés real de backend/worker `scripts/browser-check.py` | **Superada.** El recorrido real cubrió 25 hipótesis, fixture/gráfico/atribución, dos trabajos completados y comparación, descarga de informe, fallo intencional conservado, 15 estados de módulos, auditoría, diseño móvil/logout, sesión revocada y denegación de viewer en servidor. |

Las pruebas frontend también cubren estados vacíos sin datos inventados, controles de viewer, metadatos reservados sin abrir gráficos, representación segura de texto no confiable, versiones inmutables seleccionadas, CSRF y errores seguros de autorización. Complementan F y no la sustituyen.

## Evidencia de persistencia, integridad temporal y seguridad

- **Persistencia y recuperación:** `tests/test_persistence.py` comprueba migración explícita desde cero, rechazo de esquema incompatible, invariantes de conexión, historial append-only/versionado, idempotencia, reclamación atómica concurrente, colas acotadas, cancelación y bloqueo de finalización obsoleta tras recuperación. `test_recovery_during_publication_fences_late_worker` rechaza publicaciones tardías. Reiniciar no borra intentos fallidos ni completados. No es sustitución automática de un worker caído.
- **Identidad del contenido:** se recalculan hashes al leer documentos; los artefactos ausentes, modificados o no registrados y los intentos de traversal/enlace simbólico/exceso de tamaño se rechazan. La integridad no demuestra veracidad de la fuente ni conciliación contable externa.
- **Causalidad:** las pruebas de datos conservan disponibilidad de transformaciones anteriores y comprueban invariancia de prefijos/perturbación futura en la transformación de ventana finita. `tests/test_temporal.py` comprueba particiones cronológicas, disponibilidad de etiquetas, solapamiento/purga/embargo, planes inmutables y un intervalo final intacto. No certifican un dataset de mercado no disponible ni detectan todas las formas de leakage.
- **Contabilidad sintética:** `tests/test_simulation.py` comprueba conservación de efectivo/inventario/comisiones, adaptadores de ejecución/costes/riesgo, rechazo atómico, duplicados, cronología, compatibilidad de fills y prohibición de ventas cortas. No modela prioridad de cola, impacto, margen, liquidación, conciliación de fills parciales ni capacidad de mercado.
- **Autenticación y autoridad:** `tests/test_auth.py` y `tests/test_api.py` comprueban creación privada e idempotente de credenciales, rechazo de enlaces simbólicos, expiración/revocación, login acotado, roles derivados del servidor, Host/Origin/CSRF, cuerpos acotados, errores seguros y ausencia de rutas de ejecución. Reiniciar revoca las sesiones. Es una evaluación de aplicación local confiable, no un pentest independiente ni certificación multiusuario hostil.
- **Límite de IA:** `test_agent_proposals_are_inert_and_budget_is_transactional` verifica cuotas persistidas finitas, rechazo de escalada y ausencia de creación de trabajos. Las propuestas no son ejecutables ni autorizan recursos. No se ejecutaron llamadas a modelos, agentes RAG ni bucles autónomos.

## Entregables originales y disposición del complemento

El [registro de aceptación](../phase-iii/acceptance.md) conserva los **19 criterios III.A** y **20 III.B**. Su relación con implementación/evidencia es:

| Entregables originales | Material y verificación |
|---|---|
| III.A 1–3, 6–10 | Diagnóstico, requisitos, diagramas, límites de dominios, contratos, modelo de datos y diseño web/backend en [arquitectura](architecture/platform.md), conciliados con `core`, `application.py`, persistencia y API |
| III.A 4–5, 11, 15 | [Stack](architecture/stack.md), [motores](architecture/engines.md), [herramientas de investigación/gráficos](architecture/research-tools.md); recibos de fuentes oficiales, inventarios de licencias, instalaciones bloqueadas y pruebas de adaptadores |
| III.A 12–14 | Laboratorio sintético persistente; diseño paper de primera clase e inactivo; registros/permisos inertes de IA y puertas futuras |
| III.A 16–19 | Seguridad, clases de costes, D-031–D-033 y plan por dependencias/aceptación; sin gastos ni activación de fases posteriores |
| III.B 1–4 | Repositorio único, registro explícito, configuración validada y contratos tipados congelados; core A–D |
| III.B 5–8 | API autenticada real, migraciones explícitas, datos sintéticos Parquet/Arrow/DuckDB, hipótesis conservadas e intentos duraderos/versionados; pruebas API/datos/persistencia/hipótesis |
| III.B 9–11 | Laboratorio finito, informes/comparación persistidos, contratos sustituibles de modelo/estrategia/ejecución y arnés contable; E y pruebas contables |
| III.B 12–14 | Web compilada de seis secciones, gráfico reutilizable y registro real de 15 módulos; frontend y **F superada** |
| III.B 15–18 | Errores seguros/correlación/auditoría, pruebas estáticas y automatizadas, A–E, instalación limpia y API/worker explícitos; evidencia de navegador real y restauración con escritores detenidos según lo anterior |
| III.B 19–20 | Documentación técnica EN/ES, [política de traducción](../TRANSLATIONS.md), roadmap y autorización de fase siguiente explícita; ciencia histórica conservada, sin traducción/sustitución silenciosa |

La [matriz complementaria](architecture/supplement.md) relaciona las 28 secciones solicitadas, 21 capacidades, ocho escenarios de identidad y catorce disposiciones de pruebas. Su ampliación mínima implementada es `VersionedReference` y referencias opcionales a versiones exactas de hipótesis en trabajos técnicos. `test_supplement_hypothesis_version_change_preserves_historical_association` demuestra que una versión nueva no reescribe un trabajo anterior, que un hash incorrecto se rechaza y que las referencias duplicadas son inválidas. No valida la hipótesis ni prueba aislamiento de identidades de bots.

Las pruebas complementarias 4, 5, 7, 10, 11, 13 y 14 tienen la evidencia técnica acotada descrita en esa matriz. La 12 queda cubierta por la ejecución real de F. La 9 cubre únicamente riesgo sintético inyectado y modos denegados; la prioridad global/cuenta/cartera queda pendiente. Las 1–3, 6 y 8 necesitan servicios futuros de instancias/capital/señales/autorizaciones/confirmación y no se consideran superadas por analogía. No se añadieron tablas vacías ni servicios operativos para aparentar cobertura completa.

## Fallos, correcciones y revisión independiente

Se conservan estos resultados junto al resumen de comprobaciones superadas:

1. La instalación npm inicial encontró una caché predeterminada no escribible y advertencias engañosas de archivos/integridad. Una caché en workspace resolvió la instalación; se verificó la identidad del archivo de origen relevante. No se debilitaron ni omitieron TLS, checksums ni valores esperados de integridad.
2. La prueba frontend inicial descubrió cero tests y fallaron tres suites por no habilitar los globales de Vitest. Se corrigió la configuración explícita; la repetición sí ejecutó y superó las siete pruebas.
3. Una revisión interna independiente del backend detectó atribución de código importado obsoleto y omisión de disponibilidad de una transformación previa. Ahora se vincula la identidad del código cargado, se exige reinicio tras cambios de fuente/dependencias y se propaga la disponibilidad. Las regresiones pasaron. También se añadieron verificación de hashes de documentos e invariancia causal ante prefijos/perturbación futura. Esta revisión es análisis interno de código, no réplica científica ni certificación externa.
4. La primera ejecución real de navegador tuvo una prueba superada y otra fallida. El selector obtenía el ID del texto visible, que incluía la versión. Se corrigió el arnés para tomar el ID de la respuesta POST real y esperar a cada trabajo completado. Una segunda ejecución siguió fallando una prueba porque el localizador de etiqueta exacta no seleccionaba el control esperado; ahora se utiliza su rol/nombre accesible de combobox y se comprueba el ID devuelto. La ejecución corregida superó las dos pruebas. No se eludió ni simuló el producto para resolver estos defectos de localizadores; los fallos originales se conservan.

5. El formato de la descripción final de estado incumplió brevemente la longitud de línea de Ruff; dividirla conservó el comportamiento y pasaron los controles estáticos/backend completos. La comprobación separada de arranque predeterminado esperaba inicialmente HTTP 201 en login, pero el endpoint declarado devuelve 200; se corrigió la aserción y pasó el recorrido autenticado. Ninguna corrección cambió un criterio de aceptación ni un permiso del producto.

## Configuración cloud reutilizable

Se aplicó `cloud-environment-onboarding:setup`. El 2026-10-21 la herramienta confirmó **saved** para `install_script` y `start_skill`, borrador `019aa6d4-0bc4-451f-a76d-4710c22ef91b~cecfgdraft_6ad82485ac748192a28b7e07eb9e777a`, con `requires_publish=true`. No se modificaron repositorios, política de red ni requisitos de secretos. El script comprobado es:

```bash
set -euo pipefail
cd /workspace/bot_trader
export UV_CACHE_DIR=/workspace/.cache/uv
export NPM_CONFIG_CACHE=/workspace/.cache/npm
uv sync --frozen
npm --prefix web ci --no-audit --no-fund
npm --prefix web run build
uv run --frozen bot-trader init
```

Las instrucciones guardadas especifican checkout, API/worker, comprobaciones de proceso frente a disponibilidad autenticada, credenciales privadas, helper de navegador aislado y límites de reinicio/recuperación. No crean una previsualización cloud para el usuario. La instancia actual está verificada; publicar el entorno requiere revisar/guardar su configuración y publicarlo desde la interfaz de entornos. Guardar el borrador no publica el entorno ni acredita restauración en una tarea cloud nueva. Los procesos de prueba se detuvieron al terminar.

El código de esta entrega es `70761ad` (web/gráficos, tras backend `eabbd8e` y núcleo `2cf79b4`). Las pruebas utilizaron el mismo código ejecutable con cambios documentales locales; los manifiestos conservan su identidad Git/dirty real. El cierre documental se versiona aparte. La publicación utiliza push normal autorizado y comprobación del HEAD remoto, sin force push.

## Licencias, límites y siguiente puerta

El [inventario Python](../licenses/python-dependencies.json) registra 36 distribuciones instaladas, incluido el proyecto; el [inventario npm](../licenses/npm-dependencies.json) registra 152 paquetes resueltos, distinguiendo los opcionales no instalados aquí. Son inventarios de metadatos, no certificación legal ni análisis de vulnerabilidades. Las licencias de dependencias no asignan licencia al código propio del proyecto.

Las licencias/notices del frontend se reúnen en `web/public/THIRD_PARTY_NOTICES.txt`, servido por una ruta fija de la aplicación. Se conservan LICENSE/NOTICE de Lightweight Charts y atribución/enlace visible a TradingView. El archivo de licencia ausente en el paquete `fancy-canvas` se recuperó del commit de su etiqueta oficial; `web/licenses/fancy-canvas/provenance.json` registra origen e identidad. El complemento arquitectónico no añadió dependencias.

Persisten los límites: SQLite en un host, un proceso API con sesiones en memoria, tareas sintéticas finitas, recuperación explícita de workers interrumpidos, sin conector de datos reales, motor financiero de producción, asignador de capital multibot, conciliación externa ni monitorización continua. Un módulo futuro necesita sus propias pruebas significativas de contratos, ejecución, tiempo y permisos. Un hash no demuestra eventos externos completos/correctos ni resistencia frente a un administrador malicioso.

La Fase IV necesita aprobación explícita independiente. Definiría protocolos financieros prerregistrados, admisión/licencias de datos, compatibilidad del motor, costes, incertidumbre, presupuesto finito de búsqueda y gobierno del holdout para las candidatas aceptadas. Esta versión de software no autoriza ni implica esa evaluación financiera. Se mantienen C1/C3 prioritarias, C2 secundaria y C4/C5 condicionadas; ninguna estrategia se declara rentable.
