# E1 — comprobaciones ejecutadas de tiempo y ejecución causal con velas

Documento: IV-E-BARS-001 · Versión: 1 · Evidencia: 2026-11-03 UTC. Traducción del [original canónico inglés](../../en/phase-iv/bar-execution.md).

**La versión exacta NautilusTrader 2.0.0rc7 reproduce una ejecución al mismo cierre después de la señal de la vela cerrada. Añadir 1 ms de latencia desplaza la ejecución de este fixture al cierre de la vela siguiente, no a su apertura. Una pequeña frontera con `bar_execution=False` conserva la secuencia causal en los casos sintéticos probados.** Esto respalda una candidatura offline condicionada, no la selección definitiva del motor ni la admisión financiera.

La [autorización D-052](../../phase-iv/APPROVAL-E1-BARS.es.md) es posterior a `c1d4029`. La [evidencia reproducible](../../phase-iv/technical-results/E-bars/README.md) conserva fixtures congelados, código, configuraciones exactas, callbacks nativos, libros, fills, comprobaciones y recibos. Seis invocaciones técnicas agrupadas ejecutaron **15 contextos nativos y 135 comprobaciones de componentes**; todas pasan, incluida la reproducción deliberada de comportamientos adversos. Una preparación congeló las entradas antes de ejecutar. No fue necesario ningún ciclo correctivo. Superar el control negativo no convierte su configuración en aceptable. No se repitieron M, la batería R de 160 casos, E3-L2, E4 ni LEAN.

## Fixture, relojes y ejecución exacta

Entorno: CPython estándar **3.13.16** existente, **NautilusTrader 2.0.0rc7** exacto, sin instalación ni descarga. Mercado: SYN-USD.SIM inventado, efectivo/netting, saldo inicial 1.000 USD/0 SYN, cantidad 1, incrementos de precio/cantidad 0,01, `MakerTakerFeeModel` maker 0,001/taker 0,002, riesgo nativo activo, L1, consumo de liquidez habilitado, cola de mensajes habilitada, identificadores deterministas y ningún modelo de fills propio. Son parámetros técnicos del fixture, no decisiones económicas E3/E4. Todos los comandos son de compra; aquí no se ha probado la simetría del lado vendedor.

El tiempo utiliza nanosegundos enteros. Sean T0=1.700.000.000.000.000.000, T1=T0+60 segundos y T2=T1+60 segundos. N tiene OHLC 100/101/99/**100,50** y N+1 tiene **110**/125/108/112, ambas con volumen inventado 100. La referencia nativa etiqueta las dos velas al cierre: evento/inicialización/disponibilidad modelada son T1 y T2 respectivamente. El retraso de procesamiento de la decisión es explícitamente cero. No se insertó ningún evento de mercado intermedio para forzar el procesamiento de órdenes en cola. Un `InstrumentStatus.NONE` común, un segundo después de la última entrada, hace avanzar el reloj sin proporcionar un precio; ningún fill observado depende de ese marcador final.

| Variante | Decisión / envío | Llegada nominal | Aceptación y fill nativos | Resultado real |
|---|---|---|---|---|
| Nativa, latencia 0, adaptive false | T1 después del callback de N | T1 | T1, después del envío | 1 @100,50, comisión 0,20 USD |
| Nativa, latencia 0, adaptive true | T1 después del callback de N | T1 | T1, después del envío | Igual |
| Nativa, latencia 1 ms, adaptive false | T1 después del callback de N | T1+1 ms | T2, después del callback de N+1 | 1 @112,00, comisión 0,22 USD |
| Nativa, latencia 1 ms, adaptive true | T1 después del callback de N | T1+1 ms | T2, después del callback de N+1 | Igual |
| Frontera causal, oferta sintética | Decisión T1; envío T1+1 ms | T1+1 ms, latencia de orden cero | T1+1 ms | 1 @110,05, comisión 0,22 USD |
| Disponibilidad de N retrasada, cotización posterior elegible | Decisión T1+10 ms; envío T1+21 ms | T1+21 ms | T1+21 ms | 1 @111,05, comisión 0,22 USD |
| Disponibilidad de N retrasada, sin cotización posterior elegible | Decisión T1+10 ms; sin envío | No procede | Sin aceptación/fill | Efectivo sin cambios |

«Llegada nominal» es el instante de envío más la latencia configurada, **no una llegada observada al exchange**. `OrderAccepted` es una aproximación observada al instante de procesamiento; la traza de la API no expone un evento separado de llegada física. La evidencia conserva individualmente `ts_event`, `ts_init` y el reloj de la estrategia para los eventos de orden y fills.

Orden nativo observado sin latencia: preprocesamiento del módulo → callback de N → decisión → envío → submitted → accepted → filled → snapshot del libro expuesto. El libro termina en bid=ask 100,50, tamaño 25 a cada lado, derivado nativamente de la vela inventada, no de un spread observado. Con latencia, submitted ocurre en T1; el preprocesamiento y callback de la vela siguiente ocurren en T2, después accepted/filled y después el snapshot del libro en bid=ask 112,00. El snapshot previo de T1 sigue mostrando 100,50. El resultado observado es compatible con que el comando pendiente se procese después de que la vela siguiente haya actualizado la referencia ejecutable a su cierre. No inspeccionamos cada paso interno de matching OHLC ni afirmamos conocer toda la trayectoria interna.

**Interpretación:** el matching nativo al mismo cierre es incompatible con nuestro contrato, que exige un evento ejecutable posterior y elegible después de la información de la vela cerrada. El orden de callbacks no demuestra por sí mismo look-ahead en la señal, ni esto constituye un defecto universal del motor. Una latencia positiva por sí sola no equivale a un modo de apertura siguiente. La ordenación adaptativa no tuvo efecto en estos resultados de órdenes de mercado; eso no demuestra que sea irrelevante para órdenes en reposo u otros flujos de eventos. No se modificó ningún supuesto para forzar un resultado en apertura/máximo/mínimo/cierre.

## Control negativo de timestamps y precisión

Cuatro contextos nativos dedicados exclusivamente a timestamps entregan una vela completa y no envían órdenes:

| Convención suministrada | Reloj del callback nativo | Hallazgo |
|---|---|---|
| Etiqueta de apertura, `ts_event=T0`, `ts_init=T0` incorrecto | T0 | El OHLC completo llega 60 segundos antes del cierre real: deliberadamente inadmisible |
| Etiqueta de apertura, `ts_event=T0`, `ts_init=T1` corregido | T1 | La vela completa llega en la disponibilidad de cierre modelada |
| Etiqueta de cierre, `ts_event=T1`, `ts_init=T1` | T1 | No se añade un segundo intervalo |
| Etiqueta de apertura con todos los timestamps desplazados 123 ns; init corregido | T1+123 ns | La precisión de evento/init y callback se conserva exactamente |

Por tanto, la ruta rc7 inspeccionada programa la entrega de la vela completa a partir del tiempo de inicialización suministrado; no protege a quien etiqueta incorrectamente la disponibilidad. El contrato real debe usar la disponibilidad efectiva cuando sea posterior al fin del intervalo. `apertura+duración` es la disponibilidad más temprana modelada para la vela completa en este canario idealizado, no una afirmación de retraso cero del proveedor o la red. `ts_init` nativo tampoco conserva por sí solo relojes separados de publicación, recepción y revisión; deben mantenerse en el sobre de procedencia.

El helper de conversión exacta de enteros comprueba segundos/milisegundos/microsegundos/nanosegundos y rechaza floats, booleanos, unidades no admitidas, valores negativos, desbordamiento de entero sin signo de 64 bits y conversiones nanosegundo→microsegundo con pérdida. La conversión exacta a menor resolución sí pasa. **No** se migró `MarketBar` de producción, basado en datetime. Una futura frontera debe conservar la precisión de origen o rechazar explícitamente la precisión no admitida, nunca truncarla silenciosamente.

Se reutilizaron frente a estos helpers hechos seleccionados de los originales **R1** —disponibilidad retrasada—, **R2** —precisión de nanosegundos—, **R3** —vela abierta frente a completa— y **R7** —corrección posterior—. Se incluyen el diario de origen, índices seleccionados, registros esperados y hashes. Es cobertura de predicados seleccionados más los nuevos canarios nativos, no la repetición de todas las comprobaciones R ni una prueba de equivalencia entre producción y motor.

## Alternativa causal mínima e invariancia ante información futura

`bar_execution=False` conserva las velas completas como entradas de señal sin utilizar todo su OHLC para proporcionar precios ejecutables. La frontera retiene la decisión de N y espera un callback de cotización después de que la decisión esté preparada. Comprueba tiempo de evento de la cotización, disponibilidad, antigüedad máxima declarada y cantidad. En esta ruta no se envía ninguna orden desde el callback de la vela completa. Una cotización recibida antes de que la decisión esté preparada no se guarda para reutilizarla después en una ejecución retroactiva.

La política versionada **D052-OHLC-synthetic-v1** declara spread completo de 0,10 USD, slippage adicional cero, latencia de orden cero, cantidad visible 2, cantidad máxima enviada 1 y antigüedad máxima de cotización de 1 ms. La primera oferta utiliza únicamente el valor independiente de apertura de N+1, 110: bid 109,95/ask 110,05, evento T1 y entrega T1+1 ms. En ese callback la estrategia no recibe máximo, mínimo ni cierre de N+1; la vela N+1 completa llega en T2. El fill nativo es 1@110,05; la frontera no fabrica ni inyecta fills.

Esta cotización es **información de ejecución inventada**, no bid/ask histórico reconstruido. Supone que la oferta derivada de la apertura sigue siendo ejecutable al recibirse y que la latencia adicional de orden cero es admisible en este escenario sintético. La igualdad entre tiempo de evento y frontera de decisión solo se admite con el orden de callbacks declarado y la recepción posterior; los empates reales ambiguos requieren secuenciación de origen o exclusión conservadora. OHLC no demuestra ni que la apertura sea ejecutable ni que la oferta persista. El límite de una unidad mantiene esta prueba por debajo de la cantidad visible inventada; no corrige ni elimina el hallazgo anterior de sobre-ejecución L1.

Cuando N llega 10 ms tarde, se omite la oferta de apertura de +1 ms. Una cotización inventada separada, mid 111/evento +20 ms/entrega +21 ms, permite una compra nativa a 111,05. Sin ella no se produce orden ni fill, incluso cuando llega la vela N+1 completa. Por tanto, la apertura no puede recuperarse retrospectivamente solo porque su precio figure en una vela almacenada. El cambio de precio y el resultado sin ejecución son consecuencias deliberadas de la política causal.

Cuatro perturbaciones congeladas por separado dejan todo el prefijo de la traza nativa hasta T1+25 ms idéntico a la referencia causal:

- Máximo de N+1 de 125→135, sin modificar el resto del OHLC.
- Mínimo de N+1 de 108→106, sin modificar el resto del OHLC.
- Cierre de N+1 de 112→113, sin modificar el resto del OHLC.
- Una revisión adicional de N, cierre 100,50→99,75, con evento antiguo T1 pero disponibilidad T1+30 ms. Se observó realmente su callback posterior de vela; no fue descartada silenciosamente.

Todas las velas mantienen coherencia OHLC. El prefijo de decisión/orden/fill ya ejecutado permanece intacto, incluidas las identidades deterministas y la contabilidad. Las cuatro comparaciones corresponden a la ruta causal; los resultados nativos con latencia no se reclasificaron como invariantes. Es un canario acotado de una sola intención, no una implementación completa de indicadores recursivos, revisiones persistentes o historial de estrategias.

## Contrato para un primer runner offline futuro

El contrato se restringe a **spot largo/efectivo, velas cerradas confirmadas y órdenes de mercado**. La frontera técnica es una prueba desechable, no ese runner. Esta evidencia no admite stops/límites en reposo cuyo matching dependa de un orden intravela desconocido.

| Invariante requerido | Implementación/evidencia actual | Pendiente antes del uso financiero dependiente |
|---|---|---|
| Conocimiento de la señal | Control de cierre/fin/disponibilidad, helpers exactos de nanosegundos, traza de decisión | Sobre de procedencia de producción, convenciones/retrasos del proveedor, revisiones y persistencia; modelo de latencia de decisión |
| Primera elegibilidad de la orden | Decisión retenida; cotización posterior elegible; sin apertura en caché usada retroactivamente | Retraso de procesamiento/transporte y política de empates versionados e integrados con los datos reales |
| Formación del precio | Matching nativo contra cotización explícitamente sintética, sin HLC futuro en la apertura | Elegir y predeclarar aproximación solo OHLC frente a quotes/trades históricos admitidos; procedencia y conversiones exactas |
| Costes/capacidad | Spread del fixture, comisiones/redondeo, slippage/latencia adicionales cero y límites de tamaño versionados | Sensibilidad a comisiones, spread, slippage, retraso, impacto y capacidad específicos de fuente/producto; sin afirmar que costes cero sean adecuados |
| Rechazo/parcial/cancelación | Esta tanda registra resultados nativos de órdenes; sin nuevo caso parcial/de rechazo. Se reutilizan observaciones D-051 sin repetirlas | Implementar/revisar la política del ciclo de vida en el runner futuro; distinguir intención, aceptación, fills parciales, rechazo y cancelación confirmada |
| Tratamiento de remanentes | La política indica cancelar y confirmar en la siguiente oportunidad de procesamiento; **no está implementada** en este harness | Bloquear exposición nueva hasta confirmar el resultado; nunca presumir continuación automática ni reserva de efectivo; marcar explícitamente estados terminales sin resolver/desconocidos |
| Conciliación independiente | Pasan comprobaciones Decimal de efectivo BUY/USD, comisiones, inventario, libre+reservado y posición | Validar venta/ida y vuelta e integración parcial/cancelación antes de admitirlas; siguen pendientes identidad, asignación de financiación y recuperación |

Para todos los fills reales de esta prueba, el oráculo Decimal independiente comprueba redondeo de comisiones a céntimos USD, cargo de efectivo e incremento de unidades base, y después concilia saldos nativos, libre+reservado y posiciones. El estado final causal de referencia es 889,73 USD/1 SYN; el de la cotización posterior retrasada, 888,73 USD/1 SYN; sin evento, 1.000 USD/0 SYN. Es contabilidad de transacciones sintéticas ejecutadas, no evidencia de rentabilidad de estrategia ni certificación de un libro contable financiero general.

La política de remanentes propuesta utiliza primitivas nativas de cancelación ya observadas en D-051: una orden de mercado de 6 contra profundidad 4 dejó 2 sin ejecutar y sin reservar; la cancelación explícita funcionó, pero un snapshot posterior no la completó automáticamente. Esos hallazgos y la ausencia del segundo fill de E4 siguen siendo adversos o limitados. Una cancelación pendiente no es confirmación. Ante incertidumbre, debe bloquearse exposición adicional y fallar la conciliación del run offline, en lugar de inventar un fill o una liberación. Aquí no se añade ninguna política operativa de cierre de emergencia.

Con **solo OHLC**, las cotizaciones derivadas de la apertura, spread, liquidez y retraso de ejecución siguen siendo supuestos. Si los datos de velas cerradas no hacen disponible la apertura cuando el modelo la utiliza, esa ruta necesita un modelo explícito y justificado de construcción de eventos o debe esperar; el HLC futuro completo debe permanecer inaccesible. Con **quotes/trades históricos**, hay que conservar evento/recepción/disponibilidad reales y huecos; un trade no equivale automáticamente a bid/ask disponible simultáneamente ni garantiza capacidad. L2 no es universal, pero ninguna de las dos opciones de datos justifica fills perfectos. Costes y robustez deberán reflejar posteriormente la resolución realmente admitida.

## Recursos, auditoría y conclusión técnica

Los recibos del guard registran **9,712751 segundos de tiempo activo de máquina** incluyendo preparación, **6,404959 segundos de CPU**, máximo RSS muestreado del grupo de procesos de **82.489.344 bytes** (~78,7 MiB), afinidad de cuatro núcleos, cero descargas nuevas y cero servicios contratados. El índice de resultados registra los bytes temporales adicionales finales —menos de 1 MiB, frente a 512 MiB—. Las seis invocaciones de prueba agrupadas se distinguen de los quince procesos hijos nativos secuenciales; no hubo ejecución exploratoria del motor ni corrección sin registrar. No es necesario gastar los slots sin usar.

El RSS muestreado cada 100 ms puede omitir picos breves y no constituye una certificación de límite duro de memoria mediante cgroup. El guard offline existente deniega IPv4/IPv6; Landlock no está disponible en este host. Los recursos son medidas de estas pequeñas pruebas sintéticas, no un dimensionamiento de producción. El tiempo de ingeniería/documentación no está incluido en el tiempo de máquina vigilado. Las comprobaciones de preservación confirman **73 archivos de runtime/configuración y 4.630 archivos regulares del venv de producción sin cambios**, ninguna incorporación, rutas científicas protegidas intactas y hash del registro de descargas de software sin cambios.

Se recomienda conservar Nautilus como **candidato offline condicionado a una frontera causal explícita de datos/órdenes**, sin confiar en `bar_execution=True` nativo ni en una latencia positiva pequeña como garantía de apertura siguiente. Esta incertidumbre concreta queda resuelta para los casos exactos; no se necesita otra revisión general de frameworks para interpretarlos. El primer runner financiero sigue necesitando integración temporal de producción, supuestos de ejecución justificados y la admisión aplicable de ciclo de vida/contabilidad. Esta tanda no cubre equivalencia histórica/directo general, recuperación prospectiva segura, todos los tipos de orden nativos ni la admisión E completa.

E1 designa aquí el caso técnico del motor, distinto de la decisión científica E1 aprobada. **E3/E4 económicos siguen pendientes**; las **26 especificaciones**, los compromisos científicos E1/E2, las prioridades C1–C5, T/D/U/V/F y las mejoras UX futuras permanecen intactos. La Fase IV sigue abierta de forma condicionada. No hubo cambios de dependencias/código de producción, nuevos datos financieros, experimentos financieros, Fase V ni ejecución paper/live, ni estos resultados los autorizan.
