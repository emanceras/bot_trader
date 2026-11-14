# Cliente público Kraken y diario incremental

Traducción sincronizada. Revisión 1, actualizada 2026-11-14. [English](../../en/integration/kraken-ws-client.md).

Esta entrega continúa `a5e9997`: el cliente real implementado alimenta el recorrido existente `KrakenCaptureService` → `CaptureJournal` → archivo → normalizador → Market Replay. La ejecución sigue limitada a pruebas simuladas. No se ha iniciado ninguna conexión con Kraken, adquisición de mercado, estrategia, backtest financiero ni servicio continuo. El [informe simulado anterior](kraken-ws.md) conserva su carácter de evidencia histórica.

## Fronteras implementadas

`KrakenWebSocketTransport` utiliza el paquete opcional fijado `websockets==17.4`. La biblioteca resuelve WebSocket y TLS; el adaptador solo admite `wss://ws.kraken.com/v2` y las solicitudes públicas existentes de instrumentos, trade y ticker. Se verifican certificado y nombre del servidor. Se desactivan redirecciones, proxies, compresión y métodos privados/de órdenes. El adaptador posee un bucle asyncio privado detrás de la interfaz síncrona existente; importarlo o construirlo no abre una conexión.

Apertura, envío y cierre tienen límites de 10, 2 y 3 segundos respectivamente. Los mensajes se limitan a 1 MiB, con un umbral alto de cola de un frame y control de flujo de la biblioteca. Esto no afirma que todos los buffers de red contengan como máximo un frame. Los sondeos breves sin mensaje no provocan por sí solos una reconexión. Los plazos independientes de handshake e inactividad son de 15 segundos por defecto. La reconexión conserva la política acotada existente, con identidad de sesión nueva y admisión de instrumento/canales en cada intento.

El snapshot inicial debe establecer el par exacto `BTC/EUR` online. Las actualizaciones parciales conservan metadatos omitidos; los cambios explícitos de identidad o un estado no operativo se rechazan. La solicitud ticker usa `event_trigger=bbo`; se registra la ausencia de eco en la confirmación y se rechaza un disparador explícitamente contradictorio. BBO significa cambios de niveles de precio, no flujo completo de órdenes ni todas las actualizaciones de tamaño.

Los tiempos UTC y monotónico se toman inmediatamente después de entregar el mensaje al recolector y antes de parsearlo. Son **tiempos de entrega/extracción de cola de la aplicación**, no de recepción del exchange ni de la NIC. Se conservan bytes del mensaje de aplicación, tiempos exactos de origen e identidades nativas. La disponibilidad basada en recepción no incorpora un retraso de procesamiento medido independientemente. EUR y BTC conservan sus unidades; no se añade conversión implícita a USD.

El resultado del cierre distingue confirmación ordenada de cierre local comprobado con confirmación remota desconocida. Este último puede permitir una sesión nueva sin afirmar que la anterior terminó ordenadamente. Un cierre local no confirmado es un fallo. El trabajo DNS del sistema operativo puede sobrevivir a una cancelación asíncrona; por ello, el comando finito requiere un supervisor externo del proceso para imponer un plazo total.

## Mejora del diario e integridad

El esquema persistido `raw-receipt-journal-v1` no cambia. Un único escritor activo conserva en caché contadores validados, relojes de sesión y la frontera confirmada. Append/checkpoint ya no recorren ni calculan hashes de todo el historial anterior; el trabajo normal es lineal en el número de registros, con trabajo constante por append para mensajes de tamaño acotado.

Se mantiene la verificación completa al abrir, auditar explícitamente, inspeccionar, recuperar o detectar un cambio externo del índice. Cambiar de escritor puede exigir esa auditoría. Entre auditorías se confía en el contenido inmutable ya validado: la corrupción histórica en el mismo fichero se detecta en la siguiente auditoría/reapertura, no en cada append. La corrupción de la última frontera se comprueba inmediatamente. Es una decisión explícita de verificación, no protección frente a un administrador malicioso. Se conservan bloqueo exclusivo de captura, índices append-only, intenciones de escritura pendientes, hashes y recuperación explícita.

Esto elimina la ruta crítica O(N²) demostrada; no acredita rendimiento 24/7, durabilidad nativa de Windows ni retención ilimitada. Continúan las hipótesis POSIX de ficheros/bloqueos.

## Aprobación, comando y límites del piloto

`capture-pilot` produce por defecto un plan local con `network_contacted=false`. Ejecutar exige un registro separado de aprobación vinculado a identidad de captura, hash exacto de configuración, alojamiento, referencia de derechos y ventana temporal. La [plantilla](../../integration/kraken-ws-client/approval.template.json) conserva `approved=false` y una ventana vencida. No es una autorización. El registro es una declaración trazable del operador local, no una prueba criptográfica de aprobación del usuario.

Sustituir `PRIVATE` por un directorio privado dedicado fuera de Git. Este comando solo prepara el plan:

```bash
.venv/bin/python -m bot_trader.cli --state-dir PRIVATE capture-pilot \
  --capture-id kraken-btc-eur-001 \
  --config docs/integration/kraken-ws-client/pilot.json
```

Antes de un piloto autorizado, preparar la dependencia opcional fijada en el entorno aislado elegido con `uv sync --frozen --extra capture`; inicializar allí los metadatos con `bot-trader --state-dir PRIVATE migrate` cuando corresponda. Esta entrega instaló el extra únicamente en `/workspace/kraken-ws-real-dev/deps` para pruebas. No se sustituyeron las dependencias instaladas de la plataforma; el extra opcional y sus hashes están en `pyproject.toml`/`uv.lock` y en [el recibo de dependencia](../../integration/kraken-ws-client/dependency.json).

La [configuración](../../integration/kraken-ws-client/pilot.json) propone 300 segundos; también se admiten 600 tras fijar nueva configuración y aprobación. Se detiene al alcanzar el primer límite aplicable:

| Límite | Valor inicial |
|---|---:|
| Duración de recepción | 300–600 segundos |
| Mensajes brutos / registros del diario | 10.000 / 20.000 |
| Tamaño de mensaje | 1 MiB |
| Imputación conservadora del diario | 64 MiB |
| Reserva de disco libre durante escrituras del diario | 128 MiB |
| Umbral de parada de filas de mercado | 8.000 |
| Tamaño de artefacto de normalización/replay | 32 MiB por artefacto |
| Reconexiones | 2 |

No se trunca un mensaje para cumplir el umbral de filas: el último mensaje indivisible puede contener hasta 1.000 filas. Siguen vigentes los techos del normalizador/replay. Los límites pueden detener la adquisición antes de cinco minutos; sería una duración incompleta, no cumplimiento de la ventana objetivo. Diario y derivados acotados caben en una envolvente lógica conservadora inferior a 256 MiB para este recorrido finito; no es una cuota del sistema de ficheros ni un límite sobre otros usuarios concurrentes del disco. Supervisar el espacio libre real y conservar las salidas en privado.

**Comando futuro únicamente, después de aprobación separada y comprobaciones de alojamiento/derechos:**

```bash
timeout --signal=TERM --kill-after=5s 320s \
  .venv/bin/python -m bot_trader.cli --state-dir PRIVATE capture-pilot \
  --capture-id kraken-btc-eur-001 \
  --config docs/integration/kraken-ws-client/pilot.json \
  --approval PRIVATE/approved-pilot.json --execute
```

Usar un supervisor externo de 620 segundos para una configuración de 600 segundos. Comprobar el comportamiento de GNU `timeout` en el alojamiento real antes de activar. SIGINT/SIGTERM solicitan parada controlada; una terminación forzada puede dejar una intención pendiente, que no debe descartarse silenciosamente.

Añadir `--inspect` al comando de plan realiza inspección offline de integridad/normalización/replay. `--recover-stopped-writer` recupera únicamente el diario offline, después de confirmar expresamente que el escritor anterior está detenido. La recuperación offline no requiere renovar la ventana de ejecución y no reconecta. Iniciar o reanudar adquisición sigue exigiendo aprobación vigente. Conservar configuración y aprobaciones con la evidencia privada. El hash de aprobación se registra de forma duradera antes de recibir datos; los reintentos terminales no añaden nueva autorización ni mensajes.

## Verificación y preparación

**Ejecutadas:** 127 pruebas focalizadas correctas sobre la revisión funcional final; la regresión backend anterior pasó 311 pruebas antes de añadir los seis últimos casos focalizados y sus correcciones. Las suites se solapan y no se suman. Mypy estricto pasa sobre 45 archivos y Ruff pasa para código/pruebas y herramientas modificadas. Se conservan dos comprobaciones de tipos fallidas: seis incidencias iniciales y ocho después de una corrección incompleta de anotaciones. No se relajaron expectativas funcionales. Persiste el aviso previo Starlette/httpx; no se cambió ninguna versión existente.

Las pruebas incluyen la clase de transporte real integrada de extremo a extremo con interlocutores asíncronos inventados; no hubo servidor real, negociación TCP/TLS ni suscripción Kraken. Duplicar la carga del diario de 20 a 40 registros mantiene las lecturas de artefactos por debajo de 2,2 veces y no escanea el directorio por cada append; la auditoría completa sigue verificando cada registro. Se cubren corrupción, cambio de escritor, escrituras interrumpidas, reinicio, permisos, límites de filas/tiempo, desconexiones, rechazo de solicitudes privadas y replay causal. Los reintentos terminales conservan la aceptación; cancelar durante la apertura impide suscribir; recuperar offline no exige renovar permisos de red. Un rechazo TLS/de apertura se registra sin afirmar falsamente que se recibió un mensaje bruto; los fallos de decodificación conservan sus bytes originales.

[Evidencia reproducible](../../integration/kraken-ws-client/evidence/client/), [recursos](../../integration/kraken-ws-client/resources.json) y [nuevo presupuesto acotado](../../integration/kraken-ws-client/budget.json): nueve comandos vigilados, **30,98 s de reloj / 23,19 s CPU**, máximos muestreados de **222,2 MiB RAM / 7,09 MiB temporales**. La ingeniería se estima en 45 minutos activos entre sesiones interrumpidas, sin instrumentación exacta. Los procesos de prueba tenían sockets IPv4/IPv6 bloqueados. El wheel opcional se instaló antes en el destino aislado; los recibos describen la ejecución offline de cada comprobación, no toda la adquisición de software de la entrega. Cero datasets financieros, conexiones Kraken o experimentos financieros. El registro distingue muestreo y coste adicional de exportación/Git.

La auditoría confirma las 36 dependencias previas del lock, 4.630 archivos del entorno instalado, contratos centrales, ciencia y evidencia anterior sin cambios. Los prefijos publicados de decisiones/experimentos siguen exactos. Solo se añadió el extra opcional del cliente.

Reproducir las pruebas focalizadas después de instalar el extra fijado en un entorno de desarrollo aislado:

```bash
.venv/bin/pytest -q tests/test_capture_archive.py tests/test_kraken_ws.py \
  tests/test_capture_service.py tests/test_capture_replay.py tests/test_public_capture.py \
  tests/test_capture_cli.py tests/test_kraken_transport.py
```


El informe de aceptación técnica comprueba por separado integridad del archivo/replay, observaciones de trade y ticker, cumplimiento de duración objetivo y cierre local confirmado. `technical_qa` no equivale por sí solo a piloto completado: un prefijo vacío válido tras un handshake fallido no cumple esos criterios. Desconexiones, cobertura ausente y completitud desconocida del proveedor siguen explícitas; el determinismo del replay no las repara. No se evalúan rentabilidades ni admisión financiera.

La implementación superó la validación simulada autorizada y está técnicamente preparada para solicitar el primer piloto supervisado. No queda identificado un bloqueo material de código dentro del alcance probado; esto no concede permiso ni demuestra conectividad real. Antes de ejecutar siguen pendientes los derechos de conservación privada, sincronización del reloj y almacenamiento del alojamiento real, runtime fijado, watchdog eficaz y aprobación explícita. La negociación TLS, acceso desde ese alojamiento, esquema/tráfico real del proveedor y latencia observada solo podrán comprobarse durante el piloto autorizado. No ejecutar mientras esos requisitos no estén concretados: la plantilla distribuida impide deliberadamente autorizar una conexión.

E3/E4 económicos, las 26 especificaciones, C1/C3, C2, C4/C5, T/D/U/V/F y restricciones del holdout no cambian. Fase V, paper/live y experimentos financieros continúan sin autorización.
