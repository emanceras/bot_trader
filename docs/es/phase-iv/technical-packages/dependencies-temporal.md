# M y R — pruebas acotadas de dependencias y coherencia temporal

Documento: IV-PKG-MR-001 · Versión: 1 · Fecha: 2026-10-28 · Traducción del [original inglés](../../../en/phase-iv/technical-packages/dependencies-temporal.md).

> **Actualización de ejecución, 2026-10-29:** D-046 autorizó posteriormente este alcance exacto. Consultar [resultados reales](../technical-results.md). La propuesta inferior conserva la especificación previa; sus menciones anteriores a permiso pendiente son históricas.

**Propuesta de ejecución, no autorización ni resultado de pruebas.** Los paquetes responden preguntas técnicas distintas. M contrasta una actualización de Arrow con la aplicación existente; R verifica equivalencia causal de información y decisiones mediante un prototipo pequeño y aislado. No implementan un adaptador financiero de producción ni ejecutan hipótesis de trading. E3/E4, Fase V y adquisición de datos de mercado siguen pendientes. Las revisiones de [dependencias](../evolution/dependencies.md) y [tiempo](../evolution/temporal.md) aportan el fundamento; no hace falta otra investigación general.

## Decisiones que permiten tomar y dependencias

| Paquete | Decisión que permite un resultado satisfactorio | Lo que no decide |
|---|---|---|
| M | Si Arrow 26.0.0 puede sustituir a 23.0.1 en la aplicación Python 3.12 actual sin las regresiones semánticas, de persistencia o permisos examinadas | Una actualización de producción, compatibilidad con versiones futuras arbitrarias ni la separación de procesos del motor |
| R | Si una especificación causal congelada produce salidas equivalentes con la misma información disponible en lotes, replay e inyector offline | Equivalencia histórico/directo de un proveedor real, predicción, fills idénticos ni permiso para recoger un stream |

M y R pueden autorizarse conjuntamente, pero sus resultados se interpretan por separado. R usa el lock actual y la biblioteca estándar; no depende de que M pase. [E](engines.md) puede examinar procesos de motores independientes aunque M falle. El candidato activo Nautilus v2 inspeccionado requiere Python 3.13 y no declara PyArrow como dependencia obligatoria: **actualizar solo Arrow no permitiría ejecutar ese motor dentro del entorno Python 3.12 de la aplicación.** M es una opción de compatibilidad de almacenamiento, no un requisito impuesto por una dependencia antigua del motor. M no incluye actualizar Python.

Todo el trabajo futuro queda fuera de producción: exportación explícita del código de la aplicación en el commit del paquete aprobado a un directorio desechable; entornos y estado de prueba separados; sin reconstruir el checkout existente mediante otro worktree. No copiar `.state/admin.token`, credenciales ni archivos reales Q3 de QA. Las credenciales temporales creadas por las pruebas existentes permanecen privadas y no se publican. Conservar código/locks/estado de producción y registrar hashes antes/después de los artefactos seleccionados para lectura.

## M — entorno exacto y alcance finito de instalación

| Elemento | Control | Candidato |
|---|---|---|
| Plataforma | Linux x86_64, host actual; Python **3.12.14**, `uv` **0.12.23** | Mismo host, intérprete e instalador |
| Dependencias | `uv.lock` exacto del repositorio en el commit del alcance aprobado; PyArrow **23.0.1**, DuckDB **1.5.6** | Cambiar solamente PyArrow a **26.0.0** en la copia desechable; fijar todos los demás paquetes a la versión del lock de control, incluido DuckDB **1.5.6** |
| Código y controles | Exportación de aplicación/tests intactos; registrar digest del código | Misma exportación salvo restricción/lock desechables necesarios para admitir Arrow 26; no relajar controles de datos sintéticos o reservados |
| Red | Reutilizar artefactos cacheados y verificados; en su defecto solo paquetes de software exactos del lock | Un intento de resolución candidato y luego wheel exacta y paquetes ya fijados dentro del límite; sin versiones alternativas de Arrow/DuckDB |

El lock candidato se generará y comparará **antes de instalarlo**, como parte del paquete autorizado. Si la resolución exige cambiar otro paquete, registrar el fallo y detener M; no ampliar restricciones ni sustituir versiones silenciosamente. Importar correctamente no basta. Ejecutar la comprobación completa de consistencia de dependencias y conservar locks, wheels/hashes y recibos de instalación. No se ejecutó instalador ni resolución para preparar esta propuesta.

Los metadatos PyPI [M-S1] identifican `pyarrow-26.0.0-cp312-cp312-manylinux_2_28_x86_64.whl`, **53.931.932 bytes**, SHA256 `6a628922ba20705fa964ca73e4ef959c2fb2f14b9bbec5589a6a1e68e6257c85`, requisito Python `>=3.11`. No se ha adquirido su contenido. Si esa wheel exacta no está disponible o la plataforma es incompatible, parar en vez de compilar Arrow desde código fuente. Reutilizar cache también exige comprobar identidad/hash. El commit exportado y digest del lock de control intacto se fijarán en el recibo de ejecución; elegir ese commit no autoriza cambios futuros fuera del alcance.

## M — casos y aceptación

Preparar tres conjuntos sintéticos pequeños bajo el escritor de control: receta v1 existente con **120 filas, semilla 42**; conjunto de límites Decimal/null/esquema de **32 filas**; y **32 eventos** de precisión con ticks enteros de nanosegundos, metadatos de unidad y timestamps de visualización separados. Son tamaños de pruebas de software, no horizontes de estrategia ni supuestos de suficiencia muestral. Los dos últimos examinan interoperabilidad propuesta fuera de v1; no presentarlos como contratos de mercado ya soportados en producción. Congelar entradas exactas y salidas esperadas antes de ejecutar el candidato.

Si la aplicación local ya contiene artefactos sintéticos v1 elegibles, inventariar sus identificadores/digests sin modificarlos e incluir copias de solo lectura de hasta tres versiones distintas de esquema/escritor, elegidas por versión e identificador, no por resultados. Excluir objetos reales, de procedencia desconocida o con secretos. Si no existen artefactos antiguos elegibles, explicitarlo: generar con el escritor de control verifica el formato antiguo, pero no objetos históricos ausentes. Las copias opcionales añaden como máximo seis comprobaciones de lectura, no una búsqueda de ejemplos que pasen.

| Grupo | Comprobaciones finitas | Aceptación obligatoria |
|---|---|---|
| M1 — regresión de aplicación y controles | Suite pytest existente de backend una vez por entorno, con estado desechable; importaciones y consistencia de dependencias una vez por entorno | Control y candidato cumplen las aserciones existentes. Un fallo del control invalida la atribución; conservarlo y detener la comparación dependiente. No hace falta repetir frontend/navegador ni integrar mercado |
| M2 — interoperabilidad antigua/nueva | Tres conjuntos × dos escritores × dos lectores = **12 casos**. En cada uno examinar valores/metadatos Parquet/IPC y proyección DuckDB correspondiente; escritores de control/candidato, nunca modificaciones de originales | Valores Decimal declarados, nulls, IDs, unidades, orden y disponibilidad exactos; v1 anterior legible por candidato y salida candidata legible por control cuando lo promete el esquema admitido. Conservar hashes originales; una serialización nueva diferente crea artefactos inmutables nuevos |
| M3 — corrupción y acceso | Digest alterado, partición reservada y etiqueta de datos reales rechazados en ambos entornos = **6 casos** | Rechazo antes del acceso analítico. Resultados favorables no justifican eludir o cambiar controles |
| M4 — interrupción de publicación | Una interrupción controlada de escritor por entorno = **2 casos**, con artefacto temporal incompleto y referencia original conservada | Ningún objeto parcial pasa a resultado admitido; artefacto/manifiesto original sobrevive y se restaura coherentemente. Verifica el límite de artefactos, no recuperación de órdenes |

M contiene **20 casos propios**, hasta seis lecturas de artefactos antiguos registradas y dos invocaciones de la suite existente. Generación, instalación/importación/consistencia y mediciones también consumen su presupuesto de recursos. Cada caso propio se ejecuta una vez; repetir exige defecto de harness identificado, conservar el resultado original y cumplir la regla de corrección siguiente.

La pérdida conocida de precisión zonificada en nanosegundos de DuckDB es un **control negativo**, no un resultado que eliminar. Una conversión nativa insegura se rechazará o declarará con pérdida; la ruta canónica admitida debe conservar ticks/unidades y valores exactos. Truncar la visualización puede ser explícito, pero no convertirla en clave de orden/join. Ninguna tolerancia ocultará cambios contables, de disponibilidad o precisión. Separar comparación semántica y bytes serializados. Puede concluirse «Arrow compatible con v1 examinado, ruta futura de precisión bloqueada»; no declara universalmente segura ninguna versión.

## R — una especificación congelada y cinco rutas de entrega

Usar Python **3.12.14**, el lock intacto cuando sea necesario y bibliotecas estándar `decimal`, `json`, `hashlib` y `zoneinfo`. R no instala paquetes nuevos. Crea solo un módulo de pruebas aislado y fixtures escritos a mano; sin migración de producción, conector, scheduler, servicio ni framework general de agregación. v1 permanece intacto.

El formato común contiene enteros `event_ns`, `available_ns`, ordinal de recepción, ID/secuencia de fuente, revisión padre, unidad temporal explícita, identificadores de instrumento/moneda y cadenas Decimal. Disponibilidad desconocida se representa expresamente; no se deduce del fichero final. E puede reutilizar estos controles de tiempo/identidad; compartir formato no implica que todos los motores soporten toda precisión o producto.

Una transición pura aplica las mismas reglas en todas las rutas: orden de recepción; entradas disponibles en el corte actual; deduplicación por identidad con ámbito; revisiones solo tras recepción; invalidar estado ante un gap hasta el resnapshot previsto; cerrar vela solo mediante el evento explícito del fixture. La decisión técnica es `OBSERVE` o `BLOCK`, con motivo, IDs elegibles, ID de última vela completa y digest de estado. No es orden, estrategia, retorno ni objetivo de cartera. Comprobaciones Decimal/conteos y un diario esperado calculado a mano forman un oráculo independiente; dos rutas igualmente defectuosas no pasan por coincidir.

Ejecutar ocho diarios fijos, cada uno de **4–256 eventos**, mediante: lotes de **1**, **7** y **64** eventos; replay individual; e **inyector offline en memoria con cola** y llegadas prescritas. No hace falta socket, conexión a exchange, espera de reloj real ni captura prospectiva. Todas las rutas usan el mismo orden de llegada y reloj lógico. Repetir cada una con tres cortes de prefijo —tras evento 1, en `floor(N/2)` y antes de evento N— además del diario completo: **8 × 5 × 4 = 160 ejecuciones acotadas**. Sin búsqueda aleatoria ni semilla estocástica. El lote impar cruza deliberadamente cierres/revisiones; los tamaños prueban transporte, no intervalos financieros aprobados.

| Caso | Contraejemplo y comportamiento esperado |
|---|---|
| R1 — disponibilidad y desacuerdo de relojes | Tiempo efectivo programado, publicación anterior, recepción tardía, igualdad con el corte y disponibilidad desconocida. Entra solo la versión disponible declarada; no imponer cadena monótona de relojes económicos |
| R2 — precisión e identidad | Dos eventos dentro de un microsegundo, unidades ms/us/ns explícitas, valores iguales con IDs diferentes y entregas duplicadas. Conservar orden/identidad o rechazar representación no soportada; nunca adivinar unidad por magnitud |
| R3 — velas abiertas/cerradas y agregación | Eventos de frontera, velas provisionales/finales/corregidas, agregación directa frente a fina-gruesa con anclas alineadas y deliberadamente incompatibles. Valores finales esperan al cierre; solo rutas compatibles deben coincidir |
| R4 — gaps y llegadas de recuperación | Salto de secuencia, recuperación duplicada, snapshot ausente y resnapshot posterior válido. Bloquear decisiones dependientes mientras sea inválido; datos recuperados no reescriben decisiones anteriores |
| R5 — frontera de calendario | Hora repetida/inexistente por DST en Nueva York, cierre anticipado inventado y sesión nocturna. Hora ambigua exige fold/offset explícito; hora inexistente se rechaza; fecha de sesión y UTC difieren cuando corresponde |
| R6 — join causal multientrada | Dos instrumentos inventados y observación de conversión tardía/obsoleta. Join as-of por disponibilidad y antigüedad fijada en fixture; ausencia de conversión bloquea observación dependiente. Etiquetas de stablecoin no se convierten silenciosamente en USD |
| R7 — revisiones y estabilidad de prefijos | Corrección posterior, backfill, publicación externa retrasada y warm-up insuficiente. Añadir futuro sin cambiar decisiones emitidas; etiquetar aparte la vista histórica corregida |
| R8 — continuación y mapeo de fuente | Restaurar pequeño checkpoint sintético de transformación con última identidad procesada; entregar duplicado y siguiente evento. Coincidir exactamente con diario sin interrupción. Conservar significado maker/taker nativo con mapeo explícito del fixture, sin presentar un adaptador live inexistente |

En R5 reutilizar el TZif existente `America/New_York`, etiqueta de tzdata del sistema **2026b**, SHA256 `e9ed07d7bee0c76a9d442d091ef1f01668fee7c4f26014c0a868b19fe6c18a95` [M-S2]. Cargar una copia aislada de solo lectura con `ZoneInfo.from_file`, no la base de zonas que resulte ser actual después. Fija una dependencia de prueba; no afirma última versión IANA ni certifica calendarios bursátiles. La tabla de cierre anticipado/sesión es inventada. Si falta el snapshot, conservar el caso de calendario bloqueado, sin instalar otra base de zonas ni cambiar silenciosamente el hash.

R pasa solo si todas las rutas admitidas coinciden con el diario esperado independiente y el prefijo correspondiente de la ejecución completa, con IDs, disponibilidad, motivos, Decimal y estado canónico exactos. Contenido diferente o fuente indisponible/con pérdida debe producir el bloqueo/diferencia explícitos esperados, no igualdad forzada. Verifica una invariante del prototipo concreto. Captura/replay real, conciliación de proveedor y equivalencia de una estrategia científica son trabajos posteriores con otro alcance. No promete fills idénticos entre simulación y directo.

## Recursos, parada y alcance de ejecución solicitado

Son **estimaciones de planificación técnica y techos de autorización**, no mediciones, presupuestos financieros ni requisitos obligatorios del ordenador personal. Ejecución secuencial; los límites evitan convertir una prueba pequeña en ingeniería indefinida. CPU/RAM/disco aplican al árbol de subprocesos, no solo al intérprete principal. Usar el host existente no contrata un servicio nuevo; no se presume coste cero de electricidad, personal o facturación del proveedor.

| Paquete | Estimación de planificación | Límite de ejecución propuesto |
|---|---|---|
| M | 20–60 minutos de cómputo de preparación/pruebas; 0,5–1,5 jornadas-persona para preparar/revisar harness; aproximadamente 0,5–2 GiB RAM y 0,5–2 GiB temporales si existen wheels compatibles | **2 vCPU, 4 GiB RAM, 3 GiB temporales, 512 MiB de software transferido, 2 horas activas acumuladas de preparación/build/tests**. Wheel Arrow exacta ~51,4 MiB; margen para paquetes ya fijados si cache incompleta. Sin compilación desde fuente |
| R | Menos de 10 minutos de cómputo; 1–2 jornadas-persona para implementar/revisar harness pequeño; diarios menores de 1 MiB antes de informes | **1 vCPU, 1 GiB RAM, 0,5 GiB temporales, sin red, 1 hora activa acumulada de tests**. Copia de zona local y software existente |

Registrar tiempo de pared/CPU, RAM máxima del árbol de procesos, máximo de almacenamiento temporal, bytes de software y esfuerzo humano por separado. Estimaciones humanas no son promesas de entrega. Superar un límite produce `blocked_resource_limit`; no contratar capacidad, ampliar versiones, eliminar casos ni rebajar aceptación. Crash, timeout o fixture ausente no es éxito. Segundos de smoke test no estiman el coste de las 26 especificaciones financieras.

Permitir un ciclo documentado de corrección por paquete solo ante defecto demostrado de harness/transcripción del fixture, dentro del mismo techo y reglas congeladas sin criterios financieros; conservar evidencia original. Una limitación del producto, incompatibilidad del control, precisión no soportada o cambio de aceptación no es ese tipo de defecto. Parar por red/mercado imprevistos, secretos expuestos, escritura en producción, hash incorrecto, deriva de dependencias, recursos agotados o invariante obligatoria incumplida. Distinguir pasado, fallido, bloqueado y no ejecutado; no pasar eliminando un caso.

La autorización futura solicitada queda limitada a: adquisición/instalación verificada de software para M en las versiones/bytes exactos; exportaciones desechables y código local de harness; casos sintéticos anteriores; copias de solo lectura de artefactos sintéticos y zona identificados; publicación de código/recibos/resultados pequeños sin secretos ni series reales. R no necesita instalación nueva. **No se ha instalado ni ejecutado nada de estos paquetes ahora.** Aprobarlos o superarlos no actualiza producción, implementa adaptadores financieros, añade fuentes/datasets, optimiza estrategias, entrena modelos ni autoriza paper/live o Fase V. Un M satisfactorio permite revisar por separado una futura migración de producción; no la realiza.

El techo correctivo es explícito: M repite como máximo una vez cada caso/lectura directamente afectado (52 intentos como máximo, incluidas lecturas opcionales de artefactos anteriores) y cada invocación de suite por entorno (máximo cuatro). R permite una sola repetición de cada caso de ruta/prefijo afectado, máximo 320 ejecuciones incluidas las 160 iniciales. Se consumen los techos originales; no hay segundo ciclo correctivo.

## Evidencia reutilizada y comprobaciones nuevas

- **M-S1 / PKG-M-01:** [metadatos PyPI de PyArrow 26.0.0](https://pypi.org/pypi/pyarrow/26.0.0/json), recuperados anteriormente el 2026-10-27 y reutilizados desde cache: versión/requisito Python, nombre, tamaño y SHA256 de wheel CPython 3.12 Linux. Solo metadatos; wheel no descargada ni importada.
- **M-S2:** etiqueta de versión y hash del TZif local, junto con identidades de lock/código del repositorio, leídos el 2026-10-27. Los [recibos de versiones](../../../phase-iv/technical-packages/dependency-version-sources.jsonl) separan inspección local y ejecución de paquetes. Las propiedades de bibliotecas y limitaciones conocidas de precisión siguen en la revisión enlazada.
- Tamaños, casos y límites de recursos son decisiones explícitas para comprobaciones de software acotadas. No estiman comportamiento de mercado, suficiencia de datos, materialidad de retorno ni riesgo financiero aceptable.
