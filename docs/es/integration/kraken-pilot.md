# Piloto acotado de Kraken y validación de Market Replay

Traducción sincronizada del original inglés. Revisión 1, actualizada el 2026-11-16. [English](../../en/integration/kraken-pilot.md).

**Validado dentro de la primera versión acotada de QA de datos:** terminó una captura real de cinco minutos y pasaron los 20 controles offline, incluida la comparación con el resultado original tras reiniciar. La entrega continúa `2316029`; D-061 registra el permiso explícito para un feed público acotado. No autoriza experimentos financieros, órdenes, captura permanente ni Fase V.

## Alcance e implementación

Se conserva el recorrido: Kraken WebSocket v2 → `KrakenCaptureService` → `CaptureJournal` → archivo local → normalización exacta → Market Replay. Las únicas suscripciones de mercado son BTC/EUR, `trade` y `ticker` con `event_trigger=bbo`. El snapshot público de instrumentos comprueba su disponibilidad. Market Replay ordena información disponible; no cruza órdenes financieras.

El entorno rechazó la apertura TCP directa. Un diagnóstico breve completó el handshake TLS/WebSocket verificado mediante su proxy configurado, sin suscripciones. El cliente admite ahora una ruta **explícita** `HTTPS_PROXY` solo cuando el hash de su URL exacta está vinculado a la configuración inmutable y a la aprobación. Rechaza URLs con credenciales; conserva verificación de certificado/hostname y prohibición de redirecciones. El modo directo sigue siendo el predeterminado e ignora los proxies del entorno. La omisión de los campos opcionales conserva los hashes anteriores. No cambian dependencias ni contratos centrales.

El mecanismo existente `PilotApproval` registra la instrucción del usuario, el host real, configuración, uso privado y ventana finita. Es una declaración del operador, no una certificación jurídica independiente ni una firma criptográfica del usuario. Tras la interrupción entre el 15 y el 16 de noviembre se registró una vinculación nueva al host y horario bajo el permiso existente; se conservaron los registros previos. No se repitió investigación de licencias. Mensajes originales, extractos y artefactos normalizados permanecen fuera de Git, en el espacio privado.

El comando devuelve ahora error cuando falla la aceptación del piloto, aunque permita inspeccionar un archivo parcial válido. El supervisor conserva la denegación de red offline por defecto; su modo público explícito admite únicamente el comando existente de captura finita. El límite externo reserva cinco segundos para cierre controlado dentro del plazo total. Se corrigió una carrera del muestreo de disco: tolera nombres temporales desaparecidos por escrituras atómicas; un fallo inesperado de supervisión termina el proceso hijo y conserva un recibo negativo sin texto privado de la excepción.

## Intentos y fallos conservados

| Intento | Resultado observado | Interpretación |
|---|---|---|
| `pilot-live-01`, 15 de noviembre | Tres aperturas directas rechazadas; cero mensajes; límite de reconexiones | Conexión realmente intentada, sin captura de mercado. El código de salida 0 original era equívoco; la aceptación ya era negativa y se conserva. |
| `pilot-live-02`, 16 de noviembre | 3.465 mensajes originales; 3.288 eventos de mercado; unos 214 segundos de cobertura por canal | Incompleto. El supervisor original produjo `FileNotFoundError` al medir `pending.json` mientras desaparecía. El hijo informó `storage_failure` y cierre local confirmado, con acuse remoto desconocido. No se conservó el errno original de almacenamiento: no está demostrada la relación causal entre ambos errores. |
| `pilot-live-03`, 16 de noviembre | Duración objetivo alcanzada; 2.449 mensajes originales / 2.175 eventos de mercado; aceptación correcta | Misma configuración de datos/ruta e identidad nueva tras probar la corrección del supervisor. Cierre local confirmado; acuse remoto desconocido. |

La primera inspección concurrente del intento 02 falló y se conserva. La inspección offline tras el cierre verifica su prefijo comprometido, hashes originales, timestamps exactos, fronteras causales y determinismo tras reiniciar. Sigue sin superar la admisión del piloto por falta de duración/cierre terminal. No se modificó ni eliminó ningún registro original. No se encontraron intenciones de escritura pendientes ni registros comprometidos corruptos. La recuperación offline explícita del escritor parcial confirmado como detenido no encontró intenciones pendientes ni reconectó. El servicio corregido registra tipo/errno de futuros errores de almacenamiento sin rutas ni contenido.

El supervisor fallido no escribió su recibo de recursos. Se conservan su referencia Git de fuentes y la salida del comando; el recibo reconstruido marca CPU/RSS/disco desconocidos y carga conservadoramente los 320 segundos completos. Esa carga no es una duración medida.

## Verificación y limitaciones

El intento final se detuvo automáticamente tras el objetivo de 300 segundos de recepción. Conservó **1.284.814 bytes de mensajes originales**, 168 observaciones de trades y 2.007 de BBO. La cobertura observada por canal fue de 297,010 s (trade) y 298,899 s (ticker); el handshake y un tramo sin operaciones no son cobertura de mercado. No se registraron reconexiones, entregas duplicadas de trades, registros comprometidos corruptos ni intenciones pendientes en este intento final. Esos ceros no demuestran completitud upstream. El [informe offline conserva los 20 controles correctos](../../integration/kraken-pilot/final-qa.json).

La última regresión completa de plataforma pasó **352 pruebas**. Tras ajustar el diagnóstico de almacenamiento/parser pasaron 61 comprobaciones afectadas; una comprobación final de compatibilidad de serialización conserva el rango de dependencias declarado y las identidades de configuración anteriores. Pasaron las pruebas unitarias web (7), integración de navegador (2), tipos/compilación web, tipado estricto Python (45 archivos) y lint del alcance modificado. Se corrigieron y conservaron los hallazgos iniciales de lint; permanece el aviso previo de deprecación Starlette/httpx. Se excluyen las campañas opcionales de motores/estrategias y órdenes nativas de este encargo de QA de datos. Su evidencia anterior permanece intacta.

El verificador offline compara el informe original de captura con un proceso CLI nuevo y un servicio reconstruido. Comprueba cadena de mensajes/sobres/índices, vinculación de configuración/aprobación, timestamps originales exactos, EUR nativo, procedencia hasta la normalización, duplicados de trades, origen observado del BBO y checkpoints intactos. Prueba las fronteras primera/intermedia/última de disponibilidad y continúa el replay desde esos checkpoints. No imprime valores de mercado. Un flujo parcial o vacío no puede superar la aceptación solo por tener un hash determinista.

El piloto completo consumió **306,72 s de tiempo transcurrido / 11,04 s de CPU hija**, con **133,2 MiB de RSS hija muestreada**. Los [recursos de campaña](../../integration/kraken-pilot/resources.json) distinguen comandos medidos, la carga conservadora de 320 segundos del supervisor fallido y dos diagnósticos breves de conexión. El pico medido de RSS de campaña fue de 663,1 MiB (regresión de navegador); el almacenamiento temporal rondó 55 MiB antes de exportar. Se desconocen los picos del intento fallido y el coste del supervisor: no son máximos certificados de toda la campaña. No se descargó software ni se utilizó un servicio de pago.

Las edades observadas de actualizaciones entre origen y recepción en aplicación tuvieron medianas muestrales de 74,25 ms (trade) y 113,05 ms (ticker), y máximos de 203,86 ms y 5,644 s. Son observaciones técnicas, no una garantía de latencia de ejecución; no se identifican por separado tránsito de red, cola local o desviación de reloj. Las 50 observaciones del snapshot de trades eran anteriores, hasta 91,03 segundos, y solo se admitieron al recibirlas.

La completitud del proveedor sigue siendo desconocida: no hay secuencia global ni feed independiente que demuestre la llegada de todos los eventos upstream. El ticker BBO disparado por precios no es un libro completo ni garantiza actualizaciones solo de tamaño. La antigüedad entre timestamp de origen y recepción en aplicación no es latencia de red; los snapshots pueden contener eventos antiguos. El kernel indicó sincronización del reloj, sin una comprobación independiente de desviación/error UTC. La disponibilidad utiliza la convención existente de recepción en aplicación, no llegada a NIC ni retraso de transformación medido.

Fallos/reconexiones/duplicados/corrupción ausentes del flujo real final deben identificarse como cobertura sintética. La validación de primera versión no certifica servicio 24/7, durabilidad nativa Windows, carga en crisis, calidad de ejecución ni mérito financiero. La retención privada depende de este workspace; no se activó alojamiento de pago ni copia externa.

## Reproducción y punto de parada

Se reutiliza el runtime opcional fijado `websockets==17.4`. `capture-pilot` por defecto solo presenta el plan y no abre sockets. Una captura futura sigue necesitando su propio alcance aplicable y una aprobación acotada; esta campaña terminada no inicia un servicio continuo.

La inspección offline utiliza la configuración privada conservada y la identidad de captura:

```bash
python -m bot_trader.cli --state-dir PRIVATE capture-pilot \
  --capture-id CAPTURE_ID --config PRIVATE/config.json --inspect
python tools/integration/verify_pilot.py --state-dir PRIVATE \
  --capture-id CAPTURE_ID --config PRIVATE/config.json \
  --capture-report PRIVATE/original-command.log --output PRIVATE/new-qa.json
```

Para un escritor confirmado como detenido, `--recover-stopped-writer` utiliza la recuperación existente sin reconectar. Nunca recuperar con otro escritor activo. Las evidencias contienen hashes de código/configuración, diffs compactos y referencias Git inmutables, sin copias de datos de mercado. [Presupuesto](../../integration/kraken-pilot/budget.json) y [evidencias](../../integration/kraken-pilot/evidence/pilot/) conservan éxitos y fallos ejecutados.

Tras esta entrega se detiene la ampliación de infraestructura. El siguiente objetivo son las decisiones económicas E3/E4, todavía pendientes. Se conservan las 26 especificaciones, C1/C3, C2, C4/C5, admisión por etapas y holdout final. No se ejecutaron Fase V, paper/live ni experimentos financieros.
