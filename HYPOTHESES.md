# Registro inicial de hipótesis

**Fecha:** 2026-10-13 · **Versión:** 0.1 · **Estado de todas las hipótesis:** propuestas, no probadas ni validadas.

Este documento formula preguntas falsables para guiar la Fase I. No selecciona candidatos ni constituye un preregistro experimental completo. No se han observado datos para elegir estrategias o parámetros.

## Convenciones

- «Mejorar» significa aportar un efecto **neto y económicamente relevante** frente al comparador definido, con riesgo y recursos explícitos; no maximizar un Sharpe retrospectivo.
- La hipótesis nula de ventaja incremental será, cuando proceda, que el efecto neto no supera cero o el mínimo económico que se fije antes de experimentar. Ese mínimo, estimador, intervalo, tamaño muestral y regla de decisión siguen pendientes de II/IV.
- Una hipótesis sobre volatilidad, estacionariedad o precisión no implica rentabilidad. Para operar hará falta una hipótesis económica adicional y validación propia.
- Un resultado no significativo puede deberse a baja potencia. No se confundirá ausencia de evidencia con demostración universal de inexistencia de ventaja.
- Los criterios de retirada siguientes son condiciones conceptuales para investigar; los umbrales y el presupuesto de ensayos deben congelarse antes de usar resultados de selección.

## Hipótesis por mecanismo

| ID | Proposición y fundamento | Comparación/nula a concretar | Observación adversa o condición de retirada | Datos imprescindibles |
|---|---|---|---|---|
| H-01 | Momentum temporal simple puede aprovechar persistencia que no se explica solo por exposición pasiva | Frente a efectivo, buy and hold y referencia de exposición/riesgo; nula: sin mejora neta relevante | Sin valor incremental frente a exposición comparable; resultado dependiente de seleccionar ex post una subida, un umbral aislado o costes irrealizables. Que una regla long/flat gane sobre todo en subidas no basta por sí solo para refutarla | OHLCV ejecutable, liquidez y tarifas históricas; periodos independientes |
| H-02 | Reversión simple puede capturar presión transitoria de liquidez alrededor de una referencia defendible | Frente a no negociar y referencia simple; nula: sin reversión neta utilizable | Efecto explicado por bid-ask bounce, equilibrio inestable, riesgo de caída persistente o coste mayor que ventaja | Trades/cotizaciones según horizonte; señal calculada antes de ejecutar |
| H-03 | Momentum transversal o factores de tamaño/liquidez pueden describir diferencias de retornos | Nula explicativa distinta de nula de cartera neta; comparación con exposición común | Prima desaparece al incluir deslistados/fees, exige tokens ilíquidos o posiciones no disponibles | Universo histórico, cambios de composición, precios/volúmenes y disponibilidad de cortos |
| H-04 | Una cartera residual puede presentar desequilibrios temporales explotables | Frente a exposiciones factoriales y cartera neutral sencilla; nula: sin retorno residual neto | Neutralidad desaparece en estrés, residuo no estable, selección múltiple explica efecto | Series sincronizadas, factores point-in-time, préstamos y margen |
| H-05 | Algunos pares pueden mantener una relación de cointegración estable durante un horizonte negociable | Nula estadística de no cointegración y nula económica de no ventaja, evaluadas por separado | Relación se rompe OOS, selección de pares domina, convergencia demasiado lenta o segunda pata no ejecutable | Precios ajustados por cambios de token, universo de pares, borrow, costes de ambas patas |
| H-06 | Ajustar exposición con volatilidad estimada puede mejorar el perfil de riesgo respecto a exposición fija | Comparador con presupuesto de riesgo/efectivo equivalente; no confundir menor riesgo con alpha | Mejora atribuible solo a menor exposición/apalancamiento oculto, turnover excesivo o riesgo tras saltos | Retornos y estimaciones disponibles entonces; costes de rebalanceo |
| H-07 | Puede existir una prima de volatilidad negociable mediante derivados, compensada por riesgos de cola | Prima neta frente a estrategia sin exposición a convexidad y riesgo de pérdida explícito | Prima insuficiente después de hedge/spread, estrés/margen inaceptable o dependencia de fills irreales | Superficie histórica de opciones, strikes/vencimientos, griegas/margen/cotizaciones |
| H-08 | Funding/basis puede ofrecer rendimiento neto por asumir segmentación y restricciones de capital | Frente a rendimiento accesible del capital/colateral; nula: carry neto no compensa costes y riesgo | Inversión de funding, basis persistente, margen o contraparte hacen inviable el perfil; ingreso bruto no cubre ambas patas | Spot/perpetuo/futuro, funding liquidado y disponibilidad temporal, índices/marca y reglas de colateral |
| H-09 | Order flow disponible a tiempo puede anticipar movimientos ejecutables | Frente a señal simple y no negociar; nula: predicción no produce ventaja tras latencia/spread | Señal caduca antes del fill, solo predice mid, no generaliza entre periodos | Libro secuenciado/trades, timestamps y latencias; calidad de sincronización |
| H-10 | Proveer liquidez puede obtener spread/rebates suficientes para inventario y selección adversa | Frente a no cotizar y regla simple con mismo inventario/límites | Fills/colas optimistas, inventario concentrado en caídas o costes operativos dominan | L2/L3 según simulación, reglas de matching, órdenes/fills parciales y tarifas accesibles |
| H-11 | ML sencillo puede añadir valor condicional frente a reglas/modelos lineales con iguales inputs | Nula: mejora incremental neta nula bajo igual información y presupuesto de selección | Ganancia solo en clasificación o un split; desaparece al cerrar leakage o incorporar costes | Variables point-in-time, pipelines, número total de ensayos y comparadores equivalentes |
| H-12 | DL puede aprovechar estructura temporal que un modelo simple no capture | Frente a modelos simples fuertes y ML con mismos datos; nula incremental | No supera incertidumbre/costes de complejidad, alta sensibilidad a semillas/periodos o muestra efectiva insuficiente | Secuencias temporales auditadas, cómputo y registro de búsquedas/semillas |
| H-13 | Adaptarse a regímenes inferidos con pasado puede mejorar estabilidad | Frente a regla sin cambio de régimen; nula: adaptación no añade valor neto | Mejora solo con estados suavizados usando futuro, clasificación tardía o costes de conmutación altos | Variables disponibles en tiempo real y probabilidades filtradas |
| H-14 | Combinar mecanismos puede reducir concentración y mejorar riesgo neto | Frente a pesos simples y componentes a riesgo comparable; nula incremental | Correlación extrema elimina diversificación o pesos optimizados solo ganan dentro de muestra | P&L sincronizado, exposición agregada y costes/margen conjuntos |

## Hipótesis nula transversal y criterios de evidencia

**H-00:** con la información y ejecución accesibles al operador, ninguna alternativa candidata ofrece una mejora neta suficientemente grande y robusta para justificar riesgo y recursos frente a sus referencias. No se «rechazará H-00» por elegir el máximo entre muchos backtests sin corrección.

Una futura decisión favorable requerirá conjuntamente:

1. Integridad temporal/datos/contabilidad y ejecución verificada.
2. Efecto económico neto y riesgo admisible bajo criterios fijados previamente.
3. Evidencia fuera de muestra con incertidumbre y control de selección adecuados.
4. Sensibilidad y estrés que no contradigan la explicación del mecanismo.
5. Viabilidad operativa/capital y posterior evaluación prospectiva.

La configuración exacta de cada contraste incluirá: instrumento/universo/moneda, señales/horarios, comparador, periodo/particiones, hipótesis primaria/secundaria, métrica/efecto mínimo, costes/margen, parámetros máximos, método estadístico, presupuesto de ensayos, condiciones de descarte, holdout y versión de código/datos. Todos están **pendientes**; no se rellenarán después de ver cuál gana.

## Fuentes y actualizaciones

Los mecanismos se desarrollan en [RESEARCH.md](RESEARCH.md) y sus apéndices. Todas las referencias temáticas están pendientes de consulta; estas hipótesis no se presentan como conclusiones publicadas verificadas.

| Fecha | Cambio | Motivo | Relación con datos/experimentos |
|---|---|---|---|
| 2026-10-13 | Creación H-00 a H-14 | Definir mecanismos y falsadores para Fase I | Ningún dataset ni experimento utilizado |
