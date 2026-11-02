# Recuperación E — resultados ejecutados y requisitos pendientes

Documento: IV-E-RECOVERY-001 · Versión: 1 · Fecha: 2026-11-02. Traducción del [original canónico inglés](../../en/phase-iv/engine-recovery.md).

**Nautilus ya se ejecuta, pero ninguno de los motores queda admitido para investigación financiera o producción.** La recuperación acotada aporta evidencia contable, de ejecución y de interrupciones, incluidos resultados adversos. No completa todos los requisitos E originales. La [autorización D-048](../../phase-iv/APPROVAL-E-RECOVERY.es.md) complementa el alcance anterior; los [resultados de 00131bc](technical-results.md) se conservan. No se repitieron M/R ni pruebas concluyentes de LEAN.

## Ejecución efectiva

La wheel aprobada de Nautilus **2.0.0rc7** se instaló en un entorno desechable con **CPython 3.13.16 estándar**, el parche compatible 3.13 más reciente disponible mediante uv 0.12.23. Sin variante free-threaded, Python 3.14, extras ni cambios de producción. La [identidad, procedencia e integridad](../../phase-iv/technical-results/E-recovery/setup-pin.json) se fijaron antes de instalar; importación/ABI y consistencia de dependencias correctas. Archivo del runtime: 35.076.205 bytes, SHA256 `4595c5589fff7bf0cb158d9a88a797e0d791fa33830770fcb7bf3f4b104feeae`. Wheel intacta: 72.042.580 bytes, SHA256 `b3928f37d75d57508030a421dc762186ad1f9ffc5d5420d7daf1d2c6badb8044`.

Se ejercitaron los nueve casos funcionales originales de Nautilus a nivel de componentes, incluida la referencia E5 y tres reconstrucciones interrumpidas, más cuatro configuraciones del diagnóstico de liquidez. **17 procesos nativos**, contando una repetición correctiva de E2 y tres procesos de reconstrucción. En la comparación original de 26 posiciones hay ahora 12 ejercitadas parcialmente (9 Nautilus y 3 LEAN anteriores), 14 sin ejecutar y ninguna certificada frente a todos sus requisitos. E6 permanece bloqueado por los requisitos funcionales; no se genera una clasificación de velocidad.

Se consumió el único ciclo correctivo del harness: el primer E2 falló antes de enviar órdenes al obtener `engine.cache` dentro de un callback durante la ejecución mutable del motor. Capturar la misma caché antes de `run()` corrigió ese acceso. Solo se repitió E2; se conservan su fallo y ambas versiones del código. Sin cambios de expectativas, fixtures, comisiones o motor. **El permiso de corrección está agotado**; las limitaciones posteriores se documentaron sin reparaciones repetidas.

## Evidencia por caso

| Caso | Resultado observado | Interpretación y límites |
|---|---|---|
| E1 | BLOCK, OBSERVE 101 y OBSERVE 99 revisado en los instantes previstos; información retrasada admitida cuando está disponible | Reloj nativo en nanosegundos, regla informativa del harness. No demuestra toda la paridad nativa con los diarios R, prefijos y precisión |
| E2 | Compra 2 a 100, comisión taker 0,40; venta post-only 1 a 102, comisión maker 0,10. Final: **901,50 USD, 1 SYN y 40 USDT**. Rechazos por paso, mínimo y saldo insuficiente | Fills, comisiones, rechazos y conservación contable nativos correctos para estas comprobaciones. Valoración USDT de 39,60 tras la conversión calculada causalmente por el harness; no conversión FX nativa ni certificación de todos los casos parciales |
| E3-L1 | Consumo activado: orden de 4 con solo 1 visible ejecuta **1 a 100 y 3 a 100,01** | Incumple el límite de cantidad visible. El modelo completa el remanente un tick más allá; activar consumo no impone universalmente ese límite |
| E3-L2 | Orden de mercado rechazada con `MARKET_PRICE_UNAVAILABLE`: existe profundidad, pero falta cotización en la ruta de precio del control de riesgo. La limitada ejecuta después 1 a 99 y cancela 2; IOC ejecuta 0 y cancela 2; la orden cancelada antes del fill ejecuta 0 | No se demuestra el recorrido de profundidad por una orden de mercado. Sí se observan efectos nativos de limitada, ejecución parcial y cancelaciones. No equivale a incapacidad general de Nautilus para L2 |
| E4 | Primera orden ejecuta 3 a 100, comisión 0,60. El reenvío directo de la misma identidad deja la orden almacenada DENIED con cantidad ejecutada 0. Segunda estrategia rechazada por saldo libre. Final: 699,40 USD, 3 SYN y **300 USD aún reservados** | Incumple los dos fills distintos esperados y la coherencia del historial. Saldo/posición conservan el fill, pero la orden diverge y quedan reservas con órdenes almacenadas terminales. No observar capital duplicado resulta insuficiente. No se probó reentrega nativa de fill duplicado |
| E5 referencia y tres cortes | Salidas abruptas 71/72/73 tras envío, tras fill y durante cancelación. Reconstrucción con la misma fuente reproduce fills/IDs, órdenes, posiciones, comisiones y saldos; diarios originales intactos | **Recomputación de investigación comprobada a posteriori.** No restauración desde checkpoint ni conciliación antes de nuevas órdenes; tampoco fuente de venue independiente. No supera E5 completo ni demuestra recuperación prospectiva |

E2 conserva la secuencia: la venta llega en offset 320, después de cotización 300 y **antes** de que cotización 500 toque su límite. Nautilus satisface el supuesto congelado; el modelo LEAN previamente probado exige cruce estricto y deja la orden abierta. Ninguna observación determina el resultado de una cola real. No se movió la orden para favorecer el resultado.

El IOC de E3 llega en offset 420, después de que la limitada consumiera la unidad del snapshot 300 y antes del snapshot 500. Su fill cero difiere del ejemplo externo de IOC aislado por un estado informativo distinto. El ejemplo externo no constituye una réplica del proyecto ni justifica introducir liquidez nueva. El recorrido completo de niveles por la orden de mercado sigue sin demostrarse aquí.

## Diagnóstico finito de consumo

Una única observación inicial: bid 99@1 y ask 100@1; dos compras de mercado de una unidad en offsets 120 y 130. Sin actualización intermedia ni posterior de cotización/libro. Un `InstrumentStatus.NONE` terminal permite avanzar el reloj sin pedir cambios de precio o profundidad; los snapshots observados permanecen iguales y no hay fills terminales.

| Libro / consumo | Fill nativo primero / segundo | Presupuesto visible inicial menos fills, derivado | Conclusión |
|---|---|---|---|
| L1 / false | 1 / 1 a 100 | −1 | Reutiliza liquidez visible entre órdenes |
| L1 / true | 1 / 0; segunda rechazada, `No market` | 0 | Distingue las órdenes sucesivas en este ejemplo, aunque E3-L1 exceda el tamaño visible con una orden mayor |
| L2 / false | 0 / 0; ambas denegadas antes del envío | 1 | La falta de precio de referencia impide comparar el matching |
| L2 / true | 0 / 0; mismas denegaciones | 1 | Inconcluyente sobre consumo L2; no es un pase de liquidez |

El libro nativo expuesto mantiene ask size 1 en ambos escenarios L1. No es un contador interno de consumo certificado. Las cantidades derivadas son diagnósticos aritméticos, no afirmaciones sobre liquidez interna restante. Un nivel y dos órdenes no prueban impacto, prioridad de cola ni realismo general. Este diagnóstico complementa E y no sustituye sus fallos.

## Integridad investigadora y recuperación prospectiva

La admisión investigadora sigue exigiendo contabilidad/comisiones correctas, identidades persistentes, ausencia de doble capital/efectos, coherencia entre órdenes y posiciones y entradas causales reproducibles. E4 bloquea por ello la admisión de esta ruta de envío directo también para investigación offline. Requiere una frontera explícita de idempotencia y conciliación, no basta con un saldo aparentemente correcto.

El archivo E5 `venue-fills.jsonl` es un **diario de callbacks nativos**, no un exchange independiente. Cada reconstrucción inicia un simulador aislado nuevo con los mismos bytes de fuente persistida y la misma identidad de ejecución del fixture; el UUID interno del framework puede cambiar. El supervisor compara prefijos después y consolida identidades reales sin sumar dos veces el efecto en el diario de investigación. Suprime 0/1/1 filas repetidas en los tres cortes. Esto respalda la recomputación determinista de una ejecución sintética inmutable; no demuestra un bloqueo de órdenes nuevas hasta conciliar. El requisito original E5 permanece incumplido.

Fills externos desconocidos, órdenes pendientes en exchange, atribución de broker y reanudación operativa segura siguen siendo requisitos futuros. No hace falta implementarlos ahora para comprobar integridad offline. La recuperación no autoriza esa infraestructura y una futura admisión offline tampoco concedería permisos paper/live.

## Recursos y preservación

Los [recibos reproducibles](../../phase-iv/technical-results/E-recovery/README.md) conservan observaciones, hashes, corrección, comandos y negativos. Solo se eliminan de la publicación las consultas firmadas de redirecciones públicas de descargas, registrando hashes originales/publicados y la redacción. Sin binarios ni datasets financieros en Git.

| Medición | Incremento / medición de recuperación | Acumulado M/R/E |
|---|---|---|
| Tiempo activo registrado de instalación/pruebas/descargas | **21,244048 s** | **219,708965 s** de 7 h conjuntas; E 175,554503 s de 4 h |
| CPU vigilada | 10,281705 s | 369,067488 s |
| Transferencia de software contabilizada | **107.247.021 bytes** | **438.885.198 bytes**, 418,55 MiB de 2,5 GiB; E 384.953.266 bytes de 2 GiB |
| Incremento / total de almacenamiento temporal actual | 594.733.238 bytes | **3.085.496.951 bytes**, 2,874 GiB de 12 GiB; E 1.839.633.750 bytes de 8 GiB |
| Máximo RSS muestreado del grupo de procesos | 94.113.792 bytes en recuperación | 1.674.530.816 bytes en instalación anterior, por debajo de 8 GiB |

Trabajos secuenciales y máximo cuatro núcleos. Sin paradas por recursos ni servicios contratados. Las mediciones excluyen ingeniería/revisión no medida e interrupciones por créditos; ejecuciones breves pueden quedar entre muestras RSS de 100 ms, por lo que no certifican picos exactos. Afinidad CPU, bloqueo de red y vigilancia muestreada no proporcionan confinamiento de escritura frente a código hostil en este entorno.

La [verificación de preservación](../../phase-iv/technical-results/E-recovery/preservation.json) compara 73 archivos de ejecución/configuración y 4.630 archivos regulares del entorno estable: sin cambios, adiciones ni modificaciones de fuentes científicas protegidas. No audita destinos de enlaces simbólicos ni estado privado. Contadores financieros en cero; decisiones metodológicas E3/E4, Fase V y paper/live pendientes. C1–C5, 26 especificaciones, compromisos científicos E1/E2, T/D/U/V/F y UX futura intactos.

## Recomendación y siguiente alcance concreto

Mantener **Nautilus como candidato técnicamente plausible**, sin seleccionarlo aún: ahora existen pruebas nativas de contabilidad, rechazos y orden causal, y un efecto medido del interruptor de consumo. Son materiales su condición de RC, la inconsistencia de orden duplicada y la ruta L2 sin precio de referencia. LEAN conserva su candidatura, con otro supuesto de fill y una integración de ciclo de vida incompleta. No hay comparación completa de rendimiento ni ganador de sistema.

El siguiente trabajo útil sería una comprobación offline acotada con autorización separada: obtener la cotización de referencia **causalmente del mismo snapshot L2**, sin inventar liquidez ni desactivar riesgo; rechazar IDs de comando duplicados antes de reenviar conservando el estado nativo; comprobar identidad de fills duplicados y reservas terminales; y, si el runner investigador lo necesita, conciliar la misma ejecución durable antes de permitir nuevas órdenes. También queda incompleta la cobertura de paridad temporal nativa. Se propone como nuevo alcance porque el ciclo correctivo actual se agotó; no se ha ejecutado ocultamente en esta entrega. No exige otra revisión general de proveedores, datasets de mercado, entrenamiento ni adaptador live completo.

No imponer L2 universalmente: los mecanismos dependientes de profundidad, cola o reacción rápida necesitan pruebas más exigentes; investigación con velas de menor frecuencia podría utilizar un contrato conservador de ejecución justificado por separado. La selección no debe depender de un supuesto sintético favorable de ejecución al tocar el precio. La Fase IV sigue condicionada.
