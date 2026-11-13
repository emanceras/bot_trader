# Captura WebSocket Kraken y Market Replay

Traducción sincronizada. Revisión 1, actualizada 2026-11-13. [English](../../en/integration/kraken-ws.md).

Esta entrega implementa un recorrido finito y simulado de Kraken WebSocket v2 para `BTC/EUR`: transporte inyectado → diario bruto → archivo existente → normalización → Market Replay de datos. Continúa `31c1b59` y `dc859e8`; no reabre la selección de motores. No incluye conexiones reales, adquisición de mercado, órdenes, estrategias, métricas financieras ni dependencias nuevas.

## Implementación y procedencia

| Componente | Responsabilidad implementada | Frontera |
|---|---|---|
| `CaptureJournal` | Bytes originales, relojes de recepción, ordinales inmutables, hashes, identidad de fuente/configuración, almacenamiento acotado y recuperación explícita de escrituras interrumpidas | La integridad local no certifica completitud del proveedor ni veracidad de la fuente |
| `KrakenProtocol` | Preflight público de instrumentos; confirmaciones separadas de `trade` y `ticker`; solicitud explícita `event_trigger=bbo` | Solo transporte inyectado; ningún conector WebSocket real admitido |
| `KrakenWSNormalizer` | Timestamps/números exactos, identidad nativa de operaciones, mapeo explícito, reglas de duplicados/conflictos y procedencia complementaria | Solo el esquema BTC/EUR admitido; entradas desconocidas o ambiguas se rechazan |
| `KrakenCaptureService` | Composición del almacenamiento, permisos, archivo y normalización existentes | Solo partición técnica de desarrollo y configuración simulada |
| `MarketReplay.inspect_capture` | Ordenación informativa según recepción, prefijos deterministas y checkpoints versionados | Sin señales analíticas, motor de ejecución, PnL ni admisión financiera |

Los mensajes brutos se conservan antes de interpretar el protocolo, dentro de los límites de mensaje/almacenamiento. Cada recepción conserva relojes UTC y monotónico; representan entrega a la aplicación, no al exchange ni a la interfaz de red. RFC3339 se convierte exactamente a nanosegundos enteros. Se rechazan floats binarios, precisión inferior al nanosegundo no soportada, identidades de operación conflictivas, timestamps obligatorios ausentes y eventos posteriores a su recepción, sin redondear, inventar ni ajustar relojes. Un retroceso del reloj de recepción bloquea la normalización. La versión `kraken-ws-v2-normalizer-v1` modela disponibilidad en la recepción de la aplicación, sin retraso adicional de decodificación/procesamiento; no es una latencia prospectiva medida. Un mensaje entregado al alcanzar el límite temporal se conserva y después se detienen las entradas; cualquier límite puede finalizar el piloto antes de su duración objetivo.

El mapeo explícito es fuente `BTC/EUR` → interno `BTC-EUR`. La denominación original, lado/tipo de la orden taker, timestamp textual exacto, identidad del mensaje/elemento y condición de snapshot permanecen en la procedencia. Los precios siguen en EUR por BTC y las cantidades en BTC. No hay conversión EUR/USD implícita; la moneda de cuenta científica sigue siendo USD. Las cotizaciones de fixtures llevan `synthetic_explicit`, no liquidez `observed`. Las operaciones no se convierten en observaciones bid/ask.

Un ID nativo repetido con contenido idéntico conserva cada entrega, pero genera un solo evento lógico en su primera recepción. El contenido conflictivo se rechaza. Precios/timestamps iguales con ID distinto permanecen separados. Cada entrega ticker conserva identidad propia porque el esquema examinado no ofrece secuencia/checksum nativo que demuestre duplicidad. Los ordinales locales no son secuencias del proveedor.

Las reconexiones crean una sesión nueva y repiten la admisión de instrumento/canales. Dejan un hueco explícito de cobertura desconocida; el snapshot de las últimas 50 operaciones no demuestra recuperación completa. Los saltos de ID son diagnósticos, no prueba de pérdida. Las escrituras interrumpidas conservan su intención y exigen confirmar que el escritor anterior se detuvo antes de recuperarlas. La recuperación no inventa mensajes ni trunca silenciosamente el historial. Reintentar una captura terminada no abre otro transporte.

Un bloqueo de captura rechaza recolectores/inspectores concurrentes con la misma identidad. La configuración inmutable completa se almacena bajo su hash; los informes vinculan checkpoint del diario, manifiesto archivado, normalización y replay. La completitud del proveedor permanece expresamente desconocida.

El replay reutiliza los contratos v2 y la lógica común de ordenación/identidad. Tiene checkpoint propio versionado y vinculación a la clase de datos. La ruta QA histórica de OHLC/operaciones sigue rechazando cotizaciones. Los cortes por recepción y la reconstrucción del prefijo permiten comprobar información anterior con independencia de entregas posteriores; es coherencia informativa, no garantía de ejecución de mercado.

## Estado de verificación

Ejecutadas: **70 pruebas focalizadas correctas**, incluida la revisión final del código; **260 regresiones backend correctas** (incluyen las focalizadas, no se suman). No se repitieron pruebas de motores nativos. Mypy estricto pasa sobre 42 archivos tras corregir cinco errores de anotación; se conservan snapshot fallido, salida y diff. El backend emitió un aviso de deprecación existente de Starlette/httpx; no se cambió ninguna dependencia. Un aviso preparatorio Ruff de longitud de línea en el nuevo verificador se corrigió antes de su comprobación final.

Las comprobaciones finales y recibos de recursos están en [la evidencia](../../integration/kraken-ws/evidence/ws/). El [nuevo presupuesto técnico](../../integration/kraken-ws/budget.json) es un techo interno de esta entrega, no una renovación de permisos M/R/E ya consumados. Ocho comandos vigilados consumieron 18,57 s de reloj / 14,25 s CPU; máximos muestreados 187,8 MiB RAM y 4,74 MiB temporales (el muestreo no certifica un pico absoluto). La ingeniería activa se estima en 55 min entre sesiones interrumpidas, sin instrumentación exacta. Descargas, conexiones reales y experimentos financieros: cero. [Resumen de recursos](../../integration/kraken-ws/resources.json). Exportar evidencia y publicar Git añade una pequeña huella fuera de esas muestras.

Para reproducir las pruebas focalizadas en el entorno bloqueado existente, sin capturar ni instalar dependencias:

```bash
.venv/bin/pytest -q tests/test_capture_archive.py tests/test_capture_service.py tests/test_capture_replay.py tests/test_kraken_ws.py
```

La composición de la plataforma expone `services.capture`; su única entrada de captura es `run_simulated`, con transporte finito y reloj inyectados. `inspect` reconstruye archivo/normalización/replay y puede verificar un `CaptureReplayCheckpoint` anterior. No hay comando real ni interruptor de captura en el dashboard. Las pruebas ejercitan la composición con el almacenamiento existente y los componentes aislados. Ruff pasa para src/tests y herramientas modificadas; el chequeo más amplio conserva dos avisos previos de make_fixtures.py/verify_delivery.py. No se reescribieron esos archivos históricos. La preservación verifica 4.630 archivos del entorno estable, contratos centrales/científicos y evidencias anteriores sin cambios; los prefijos publicados de DECISIONS/EXPERIMENTS siguen exactos.

## Limitaciones conocidas

Transporte y reloj son interfaces inyectadas de confianza, no un aislamiento de código hostil. No se entrega ni admite un conector real; no existe un comando soportado para activar una captura real. Los timeouts y la confirmación de cierre de un futuro cliente requieren admisión independiente. La durabilidad local utiliza primitivas POSIX de ficheros/bloqueo; no se ha demostrado durabilidad nativa en Windows.

El diario acotado verifica el contenido bruto previo al añadir registros, con trabajo acumulado de lectura O(N²). Es aceptable para este alcance sintético pequeño, no evidencia de rendimiento 24/7. Normalización/replay operan sobre prefijos acotados, no sobre flujos ilimitados. La imputación por registro es un límite local conservador, no una tasa de tráfico medida ni una previsión completa de todos los derivados. Un capturador continuo necesitará dimensionamiento medido, segmentación, ciclo de almacenamiento y pruebas de recuperación/carga antes de desplegarse. La propuesta anterior de 24 horas conserva su carácter de diseño histórico, sin implementación ni operación autorizada.

## Procedimiento condicionado para una futura captura supervisada de 5–10 minutos

Este procedimiento **no se ejecuta ni queda autorizado por esta entrega**. Depende de un conector público admitido y de aprobación separada de fuente, derechos, alojamiento y recursos finitos. No se activa cambiando la etiqueta sintética de un fixture.

1. Revisar las condiciones Kraken aplicables a la conservación privada del feed desde el alojamiento/jurisdicción reales. Preservar versión y conclusión acotada; el acceso público no concede una licencia general de almacenamiento o redistribución. Resolver ambigüedades materiales antes de adquirir datos. No hacen falta claves ni cuentas financiadas.
2. Implementar/admitir por separado el conector mínimo: verificación TLS, timeout/tamaño acotados, timestamps UTC/monotónico inmediatos, confirmación de cierre y desconexión recuperable. Conservar mensajes en privado. Verificar sincronización del reloj, disco persistente y apagado del proceso; un piloto supervisado no exige contratar alojamiento 24/7.
3. Fijar antes de activar una duración, 300 o 600 segundos, y techos de mensajes, registros, disco/espacio libre y reconexiones. Los valores simulados actuales son 1.000 mensajes, 2.000 registros, 1 MiB/mensaje y 64 MiB de imputación conservadora del diario; son límites iniciales que evaluar, no prueba de que quepan diez minutos. Detenerse al alcanzar el primer límite. Aprobar un techo total privado que cubra bruto, metadatos y derivados, no solo el diario. Usar las tasas medidas del piloto para dimensionar después; no hay cuotas de servicios/cloud cotizadas ni autorizadas.
4. Realizar el preflight público v2 desde ese alojamiento. Exigir el par exacto `BTC/EUR` online con metadatos BTC/EUR de base/cotización y confirmar por separado `trade` y `ticker`. Conservar la solicitud `event_trigger=bbo`. Una respuesta explícita contradictoria se rechaza; la confirmación documentada no garantiza repetir ese parámetro, por lo que su ausencia se registra sin inventar confirmación.
5. Supervisar la captura finita. Registrar relojes, hashes, transiciones de sesión, confirmaciones, mensajes no soportados, desconexiones y paradas. `bbo` describe cambios de **niveles de precio** de mejor bid/ask, no cada actualización de tamaño ni flujo completo de órdenes. No reparar huecos desconocidos por inferencia ni mediante descargas REST no autorizadas.
6. Detener entradas, confirmar cierre del transporte, persistir metadatos y conservar intenciones pendientes. Verificar hashes y reconstrucción del checkpoint tras reinicio. Normalizar con una declaración de datos reales distinta y procedencia observada de cotizaciones, no con el modo del servicio simulado. Mantener contenido de mercado privado; publicar solo agregados técnicos aprobados. Evaluar relojes, cobertura, recursos y recuperación, sin estrategias, PnL ni estadísticas financieras.

Un despliegue posterior 24/7 requiere proceso supervisado permanente, TLS saliente fiable, relojes sincronizados, disco persistente, retención explícita, alertas de disco/reloj/conectividad y recuperación medida. Un ordenador personal puede suspenderse o perder conexión; una VM añade costes y dependencias operativas. No se selecciona ninguno aquí.

## Fuentes y límites científicos

Se reutilizan los hallazgos oficiales dirigidos y sus hashes del [registro de fuentes](../../integration/kraken/sources.json), examinados el 2026-11-11, y la [especificación histórica](../../integration/kraken/capture-spec.json). No es necesaria otra investigación general. Originales pertinentes: [ticker](https://docs.kraken.com/api/docs/websocket-v2/ticker/), [trade](https://docs.kraken.com/api/docs/websocket-v2/trade/), [instrument](https://docs.kraken.com/api/docs/websocket-v2/instrument/), [introducción WebSocket](https://docs.kraken.com/api/docs/guides/spot-ws-intro/) y [condiciones EEE](https://www.kraken.com/legal/eea-terms). La cotización spot previamente observada en REST no demuestra una suscripción v2 correcta ni acceso desde el alojamiento futuro.

E3/E4 económicos siguen pendientes. C1/C3, C2, reservas C4/C5, las 26 especificaciones, T/D/U/V/F y las restricciones del holdout no cambian. Fase V, paper/live y entrenamiento financiero permanecen sin autorización.
