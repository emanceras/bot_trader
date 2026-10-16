# Microestructura, ejecución y market making — revisión de Fase I

Fecha de cierre documental: **2026-10-15**. Estado: revisión del corpus local documentada; sin réplica, datos de mercado ni experimentos propios. Lectura inicial de EX-01–02 el 14-10 y cierre de EX-03–05 el 15-10; recuperaciones del 13-10 preservadas en [search-execution.jsonl](search-execution.jsonl). Identidades, versiones, hashes, secciones leídas y cifras se detallan en [evidence-execution.md](evidence-execution.md).

La evidencia disponible muestra predictibilidad de corto plazo y un ensayo maker Bitcoin positivo después de rebates bajo condiciones específicas. **No acredita una ventaja neta robusta y replicada que pueda alcanzar este operador.** En el mismo corpus, los backtests taker de Albers son negativos con tarifa ordinaria; la mayoría de las pruebas restantes describen liquidez, explican precios contemporáneos o simulan ejecución incompleta. Cinco trabajos distintos constituyen la evidencia de este bloque; preprints y versiones editoriales no son pruebas independientes.

## Familia 1 — Microestructura, flujo de órdenes y predicción

El mecanismo propuesto es presión de oferta/demanda observable antes de una decisión y ajuste posterior del precio. Conviene separar dos relaciones:

\[
\Delta m_{(t-h,t]}=\alpha+\beta\,OFI_{(t-h,t]}+\varepsilon_t
\qquad\text{frente a}\qquad
\widehat r_{t,t+h}=f_{\theta}(x_{\le t}).
\]

La primera explica un movimiento y flujo del **mismo intervalo**; es el objeto de Cont (EX-03), con cambios expresados originalmente en ticks. La segunda formula una predicción futura: `x` solo puede contener mensajes recibidos antes de decidir, y θ solo información permitida por la partición temporal. Esta causalidad en el orden de información no demuestra causalidad económica exógena. La entrada realizable llega después del retardo de cálculo/transmisión; el retorno desde un mid anterior a esa entrada no es el retorno negociable. Estas ecuaciones explican la distinción de Fase I, no constituyen un experimento implementado.

| Trabajo | Evidencia favorable | Evidencia adversa o límite decisivo |
|---|---|---|
| **EX-01 Albers et al.**, Bitcoin, arXiv:2108.09750v1; DOI 10.1080/1350486X.2022.2080083 | En 14 mercados, OLS a 500 ms obtiene R² test 0,094–0,289; dos días de test posteriores a seis de entrenamiento en febrero/marzo 2021. Algunas configuraciones taker son positivas al simular la tarifa mínima VIP | Con tarifa ordinaria, todos los PnL2 de tablas 6 y 14 son negativos. PnL1 ya compra al ask/vende al bid: spread incluido; impacto y latencia no resueltos. Los tiers más bajos se asocian a volúmenes institucionales y, a veces, tenencia de token |
| **EX-02 Schnaubelt et al.**, Bitcoin, DOI 10.3390/jrfm12010025 | Describe profundidad, costes de liquidez y recuperación tras trades en tres exchanges, 2017–2018 | No es una estrategia OOS. En Bitfinex, spread medio 0,9663 pb frente a VWAP bilateral 8,3667 pb para USD 100.000 y 39,6270 pb para USD 1M: el mejor precio no describe ejecución a tamaño. Las tarifas históricas no son las actuales |
| **EX-03 Cont et al.**, acciones, arXiv:1011.6402v3; DOI 10.1093/jjfinec/nbt003 | OFI agrega trades, órdenes límite y cancelaciones; asociación lineal contemporánea con impacto inversamente relacionado con profundidad | R² medio alrededor de 65% es ajuste explicativo, no predicción OOS. Los propios autores estudian la tautología parcial de incluir eventos que cambian precios. No hay PnL o evidencia cripto |
| **EX-05 DeepLOB**, acciones, arXiv:1808.03668v6; DOI 10.1109/TSP.2019.2907260 | LSE: seis meses entrenamiento/tres validación/tres test; a 20 eventos, accuracy 70,17%, F1 70,15%, con transferencia a otras acciones | Simulación mid–mid sin costes de transacción. El retraso de cinco eventos no resuelve spread, colas ni fees. La predicción y el PnL bruto estilizado no prueban ventaja neta cripto |

**Datos y viabilidad.** Se necesitan mensajes con orden temporal, secuencias y timestamps de recepción, reconstrucción coherente del libro y precios ejecutables al tamaño previsto. L1 permite ciertas variables OFI; L2 agrega profundidad; ninguno identifica por sí solo prioridad individual. EX-01 usa capturas L2 remuestreadas a 50 ms y EX-02 estados principalmente a un minuto: no se pueden intercambiar sus conclusiones sobre horizontes o fills. Multi-exchange añade sincronización y demora de recepción. En DeepLOB, los horizontes son números de eventos y el forward pass de 0,253 ms reportado no mide latencia completa.

Los costes pertinentes incluyen fees del tier accesible, spread ya incorporado en bid/ask, profundidad consumida, impacto dinámico, financiación si procede y costes operativos. Se evita restar dos veces un coste ya representado en precios ejecutados. Los resultados de Albers son sumas de puntos básicos por operaciones, no retorno sobre patrimonio. No hay capital, acceso a exchanges, licencias de datos, tier, infraestructura o latencia del usuario verificados a fecha de cierre; la viabilidad queda sin determinar.

## Familia 2 — Market making e inventario

El ingreso potencial depende de los fills de las quotes; mantener dos precios visibles no asegura comprar y vender con beneficio. Para una representación contable simple de un activo lineal, con `Δq_j>0` para compras, precio ejecutado `p_j` y costes explícitos acumulados `C_t` netos de rebates:

\[
q_t=q_0+\sum_{j\le t}\Delta q_j,\qquad
X_t=X_0-\sum_{j\le t}p_j\Delta q_j-C_t,\qquad
W_t=X_t+q_t m_t.
\]

`X` es efectivo, `q` inventario y `W` riqueza marcada al mid. El resultado requiere comparar riqueza inicial/final, valorar inventario y contemplar su liquidación ejecutable. Esta identidad no describe sin adaptación contratos inversos, margen o funding. La selección adversa aparece en el movimiento del precio después de un fill; si ya está reflejada en el PnL, no se resta de nuevo como un cargo adicional.

**Fundamento y límite teórico.** Avellaneda–Stoikov (EX-04; DOI 10.1080/14697680701381228) deriva, bajo precio browniano e intensidades Poisson exponenciales, un precio de reserva `r=s−qγσ²(T−t)` y quotes dependientes de riesgo de inventario. Sus 1.000 simulaciones de tabla 1 producen menor desviación del beneficio (6,6 frente a 12,7) y del inventario final (2,9 frente a 8,4), pero también menor beneficio medio (65,0 frente a 68,4) que un benchmark simétrico. No son cifras de rentabilidad real, porcentaje o criptomonedas. Quotes actualizables gratuitamente y valoración terminal al mid omiten elementos materiales de ejecución.

**Evidencia real condicionada.** Albers sí describe un ensayo maker con órdenes reales en Bybit BTC durante julio de 2021. Para metaMM publica −4,4749 pb por roundtrip antes de rebates y **+0,5251 pb por roundtrip tras 5 pb de rebates**. Las órdenes fueron de USD 2.000 y el turnover USD 1,537 millones: este último es volumen ejecutado, no capital invertido. El benchmark ingenuo queda en −1,8184 pb con el mismo rebate, pero operó en fechas distintas y con órdenes de USD 100; no identifica un efecto causal con condiciones iguales.

El ensayo utilizó AWS Singapur en la región del exchange, latencia declarada inferior a 1 ms, cálculo 0–2 ms y decisiones aproximadamente cada 5–10 ms. La mediana entre fills opuestos fue 328 s: una predicción de un segundo no elimina exposición de inventario durante minutos. El umbral maker usó entrenamiento y test anteriores combinados y otra condición se escogió por ensayo/error; julio es posterior, pero no consta un protocolo preregistrado inmutable. El resultado es un ensayo publicado por los autores, **no replicado por el proyecto ni de forma independiente en este corpus**.

No se ha comprobado una conciliación completa de capital, margen, funding, infraestructura y liquidación terminal en esa cuenta. El margen de +0,5251 pb puede cambiar de signo con gastos omitidos o cambio de rebate; el texto no justifica generalizarlo a un particular en 2026. Tampoco respalda afirmar que todo market making sea inviable: delimita las condiciones bajo las cuales se observó ese resultado.

**Datos, colas y costes.** El backtest maker necesita demostrar cuándo una orden era aceptada, su prioridad, cancelaciones delante/detrás, fills parciales, rechazos y carrera entre fill y cancelación. Snapshots L2 no identifican estos hechos; EX-01 lo señala expresamente. Un toque del precio no garantiza fill y llenar toda orden tocada sesga el resultado. Datos de órdenes individuales y reglas del venue pueden mejorar la identificación, pero su disponibilidad, licencias y calidad no están verificadas aquí. Fills y retornos posteriores son dependientes: ignorar esa selección convierte el spread visible en ingreso ficticio. A esto se añaden inventario, hedging o cierre agresivo, financiación y cambios de liquidez documentados por EX-02.

## Cobertura, exclusiones y conclusión de Fase I

Se incluyen dos trabajos empíricos Bitcoin (EX-01–02) y tres mecanismos/estudios de acciones (EX-03–05). No se cuentan los últimos como validación cripto ni como réplicas del ensayo de Albers. La falta de réplica comparable, costes completos y condiciones alcanzables por el usuario impide concluir ventaja neta robusta. Los hallazgos justifican estudiar los riesgos y la diferencia entre predicción y ejecución; no seleccionan una estrategia ni autorizan Fase II.

**Exclusión de identidad:** `crypto_microstructure.pdf` es Markus Zeggel, *The Bounded Isomorphism Conjecture for Spaces of Graphs with Large Girth*, arXiv:2108.09700v1, matemáticas. Se conserva el archivo y su registro; se excluye como evidencia financiera (EX-X01). Albers corresponde a arXiv:2108.09750, un documento distinto.

El bloque se cierra con el corpus ya recuperado, por límite de recursos e instrucción de consolidación, **sin nuevas búsquedas o descargas**. No equivale a búsqueda exhaustiva hasta octubre de 2026 ni a dos rondas de rastreo de citas. Quedan abiertas literatura posterior, replicación independiente y acceso actual a datos/venues/costes; no se simula que esas comprobaciones se hayan realizado. Estado final: documentación de cinco estudios y una exclusión; ninguna estrategia implementada, probada o validada.
