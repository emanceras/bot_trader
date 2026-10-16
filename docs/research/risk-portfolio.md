# Volatilidad, regímenes y carteras: revisión crítica de Fase I

Fecha de cierre documental local: **2026-10-15**. Estado: revisión de Fase I con cobertura limitada explícita. Ocho PDF disponibles con fichas y alcance de lectura declarado; se cotejaron métodos y resultados de RP-06–08 para cerrar las notas preliminares. No se afirma lectura exhaustiva de cada apéndice. Ningún experimento propio, estrategia implementada o selección de Fase II.

La literatura leída aporta evidencia sobre dinámica del riesgo, valoración de opciones y sensibilidad de asignaciones a supuestos. **No demuestra una ventaja cripto neta, robusta y ejecutable para un particular.** El trabajo de exposición por volatilidad con costes más claro del bloque estudia acciones/divisas; los artículos de opciones estudian cálculo o valoración; el caso de optimización cripto de 2025 ni siquiera muestra mejor Sharpe en su comparación publicada.

## Preguntas y delimitación

1. ¿Prever volatilidad permite controlar exposición con utilidad neta, o solo explicar heterocedasticidad?
2. ¿Una prima de opciones compensa convexidad, saltos y margen después de costes y cobertura?
3. ¿Los regímenes se detectan con información disponible entonces y mejoran decisiones?
4. ¿Una cartera estimada supera referencias simples sin depender de parámetros inestables?

Control de exposición, negociación de volatilidad, clasificación de estados y asignación de capital son hipótesis distintas. Un menor error de previsión o valoración no implica por sí mismo una operación rentable.

## Formalización de los mecanismos

Estas expresiones son marcos conceptuales, no estrategias elegidas o implementadas:

- **Exposición por riesgo:** un objetivo de volatilidad sugiere `w_t = min(w_max, σ_obj / σ̂_t)`, con estimación solo a partir del pasado y unidades temporales compatibles. No es idéntico al peso `c / σ̂_t²` de Moreira–Muir. El factor de escala y los límites deben determinarse sin mirar el periodo evaluado; financiación y rebalanceo cambian el resultado.
- **Volatilidad y opciones:** la volatilidad implícita satisface `V_modelo(σ_IV) = V_observado`. Resolver esa igualdad no predice el payoff. Para un contrato ideal de varianza, el largo recibe `N_var (RV − K_var)`; una prima de venta requiere que el strike compense varianza realizada, costes y colas. Una cartera de opciones discretamente cubierta añade saltos, error de hedge y margen; no replica gratuitamente ese contrato ideal.
- **Regímenes:** un HMM plantea `P(s_t=j | s_(t−1)=i)=A_ij` y retornos condicionados al estado. Operar en t exige probabilidades filtradas `P(s_t | x_1,…,x_t)` y parámetros estimados con información permitida. `P(s_t | x_1,…,x_T)` con T>t usa futuro; Viterbi sobre toda la historia tampoco es una señal disponible entonces. La hipótesis económica es que adaptar exposición añade utilidad neta, no que existan clusters visuales.
- **Carteras:** para pesos w y covarianza Σ, `Var(r_p)=wᵀΣw`. Una formulación media–varianza maximiza `wᵀμ − (λ/2)wᵀΣw` bajo restricciones; μ y Σ estimadas introducen error. La diversificación mejora si las covarianzas y pérdidas conjuntas lo permiten, y la utilidad realizada debe descontar turnover y financiación. Pesos iguales o exposición fija son comparadores necesarios, no garantías de optimalidad.

## Mapa de evidencia disponible

| Línea | Fuentes leídas | Evidencia favorable | Evidencia adversa o insuficiencia | Conclusión limitada |
|---|---|---|---|---|
| Exposición inversa a volatilidad/varianza | RP-01, Moreira–Muir WP 2016 | Señal mensual rezagada; alpha del mercado persiste con costes simulados | No cripto; combinaciones MVE dentro de muestra; resultado más débil en 1956–1985; límites de apalancamiento | Mecanismo documentado, transferencia a BTC/ETH abierta |
| Opciones/volatilidad implícita | RP-02 (2021), RP-03 (2024) | IV no plana, saltos; mejor convergencia numérica o menores errores de valoración/previsión | Fallos cerca del vencimiento; sesgos de moneyness; ninguna cartera de opciones con costes completos | No demuestra prima neta de volatilidad |
| Carteras y eventos raros | RP-04 (2025), RP-05 (2023) | Formalización de diversificación/ambigüedad | MVE menor Sharpe/mayor varianza; fechas/proveedor ausentes; teoría calibrada no es backtest | Superioridad OOS frente a 1/N no establecida |
| Regímenes y dependencia | RP-06 (2026), RP-07 (2025), RP-08 (preprint v1 2026) | Dependencia/heterogeneidad retrospectiva; FIGARCH mejora algunos errores OOS de EGARCH en RP-07 | RP-06 sin OOS; MSGARCH excluido del test en RP-07; HAR/GARCH superan MS en tabla 8 de RP-08, con inconsistencias de reporte | No hay filtro causal o asignación neta validada; complejidad sin superioridad general |

Las fichas enlazan cada afirmación a páginas/tablas y explican versiones, DOI, hashes y acceso: [evidence-risk-portfolio.md](evidence-risk-portfolio.md). El [registro de búsqueda](search-risk-portfolio.jsonl) conserva solicitudes anteriores y el cierre local; cache fuera del repositorio en `/workspace/literature-cache/risk-portfolio`.

## Volatilidad y control de exposición

Moreira y Muir escalan cada mes por la inversa de la varianza realizada previa. El alpha accionarial del caso base pasa de 4,86% a 3,63% con 14 pb de coste por cambio de exposición; sin apalancamiento, de 2,12% a 1,85% (RP-01, tabla 4, PDF p. 35). Es un resultado publicado bajo supuestos específicos. Las cifras no son rentabilidades cripto ni estimaciones para este proyecto. Los costes se estudian sobre el mercado agregado y no todos los factores; el percentil 99 de exposición del caso base llega a 6,4 veces (p. 14).

El mecanismo puede fallar si la mayor volatilidad anuncia retornos suficientemente superiores, si la exposición tarda en volver tras rebotes, o si rebalanceo y financiación absorben la mejora. Son condiciones de falsación propuestas, no fallos medidos aquí. Menor drawdown por tener menos exposición tampoco basta para afirmar alpha: habría que comparar riesgo, efectivo, apalancamiento y costes equivalentes en una fase autorizada futura. El artículo no proporciona una réplica cripto de esa comparación.

## Opciones: cálculo, valoración y prima son objetos distintos

RP-02 invierte Black–Scholes sobre dos ventanas Deribit de 14 días en 2019/2020. Newton–Raphson suele necesitar menos iteraciones, pero ambos métodos tienen errores cerca del vencimiento (tabla 5, p. 25). El benchmark es IV numérica de la misma relación de precios; no una realización futura ni una posición cubierta. El texto no demuestra que comprar o vender opciones obtenga beneficio.

RP-03 añade saltos y encuentra menores errores para ARJI-EGARCH. Su OOS declarado divide antes/después de diciembre 2019; no informa el día exacto ni un calendario completo de reestimación (pp. 19–20). La tabla 5 da RMSE de 0,194 frente a 0,196/0,198 y MAPE 140,184 incluso para el modelo preferido. La descripción de 10.932 retornos «diarios» entre 2014 y mediados de 2021 requiere aclaración (p. 9). Persiste sesgo para opciones cortas y muy OTM (pp. 21–24).

Ninguno estima una estrategia neta de venta de volatilidad con cobertura, comisiones, spread, financiación, colateral y liquidaciones. Describir bid/ask o hallar un precio distinto del observado no equivale a simular ejecución. Para un particular, los riesgos de saltos, convexidad, margen y acceso a quotes históricos forman parte de la hipótesis económica; la literatura de pricing leída no los resuelve.

## Carteras: diversificación declarada y evidencia de rendimiento

RP-04 publica un ejemplo de cinco activos con «últimos 12 meses» de precios diarios sin proveedor ni fechas (p. 4). Su tabla 3 informa Sharpe **0,0818 MVE frente a 0,0822 MV**, con mayor varianza MVE. Esto limita la conclusión narrativa de mejor rendimiento ajustado por riesgo y protección de colas (p. 9). Tampoco hay rebalanceo OOS, costes o referencia 1/N. Incorporar una penalización de concentración es una idea matemática; el ejemplo no valida protección fuera de muestra.

RP-05 resuelve una elección robusta bajo ambigüedad y eventos raros. La calibración BTC se toma de otro estudio; la nota sobre CoinMarketCap 2017–2021 corresponde a esa procedencia, no a una evaluación propia sobre datos nuevos (pp. 16–19). Variaciones de exposición y bienestar son salidas condicionadas del modelo, no retornos observados. Las dos fuentes dejan abierta la comparación neta frente a ponderación igual, buy and hold o control de riesgo sencillo.

## Regímenes: descripción retrospectiva y decisión disponible entonces

RP-06 analiza 14 activos CoinGecko, 2022-01-28–2025-07-21, con PCA/K-means/HMM/GARCH y módulos descriptivos. PC1 explica 67,89%, pero el mejor Silhouette es solo 0,096 (p. 10). Estima HMM mediante Baum–Welch y decodifica la secuencia por Viterbi (p. 8); no informa prueba temporal OOS de asignaciones. Las exposiciones propuestas por umbral de estado (p. 20) no se contrastan con P&L neto. Precios estandarizados frente a retornos estandarizados y conteos de observaciones requieren aclaración antes de reproducir.

RP-07 usa cuatro activos Yahoo Finance, 2017-08-11–2024-12-31, con división 80/20 y rolling sin corte calendario ni ventana suficientemente detallados (pp. impresas 127–128). MSGARCH se excluye tras considerar que el test no presenta cambios de régimen relevantes (pp. 136–137). Esa selección condicionada al test impide atribuirle superioridad OOS. FIGARCH mejora RMSE BTC/BNB frente a EGARCH, mientras EGARCH-XRP empeora mucho en test; tasas de convergencia bajas y residuos dependientes limitan la comparación. No hay rendimiento de una regla negociada.

RP-08, preprint v1 no revisado por pares, estudia cinco activos hasta marzo de 2026. Describe ventana creciente con mínimo 756 días, pero tabla 8 presenta un corte 75/25 cuya relación con el calendario anterior no queda explicitada. Su tabla 8 (p. 27) aporta evidencia contraria a superioridad general: **HAR-RV gana QLIKE en tres activos y GARCH en dos; GARCH obtiene menor RMSE en los cinco**. La narrativa de mejor RMSE MS-GARCH-XRP omite el menor error GARCH de la tabla. DM negativo no acredita por sí solo significación en todos los activos; tampoco QLIKE valida por sí solo toda una densidad o su VaR. Hay otras cifras incompatibles entre texto y tabla, detalladas en la ficha. Los datos auxiliares se rellenan parcialmente, se muestran probabilidades suavizadas y no se demuestra trazabilidad causal completa de las salidas. Las reglas operativas se reservan para otro trabajo; el depósito de código/datos se promete tras aceptación, sin paquete verificado aquí.

Un filtro usa información disponible hasta la fecha; el suavizado puede incorporar observaciones posteriores y Viterbi puede decodificar la historia completa. Incluso una recursión de filtrado pierde interpretación en tiempo real si sus parámetros se ajustaron con datos futuros. Ninguna de estas tres fuentes demuestra conjuntamente ese control temporal y una mejora neta de asignación.

Una futura hipótesis negociable necesitaría conocer la probabilidad de estado disponible antes de actuar, tiempo de detección, revisiones, incertidumbre y coste de cambiar exposición. PCA, escalado, selección de estados y parámetros deben estimarse solo con pasado. Son requisitos conceptuales de interpretación; no se ha desarrollado ni probado ningún filtro o backtest en esta entrega.

## Viabilidad y lagunas

| Aspecto | Lo que se puede sostener con esta lectura | Lo que queda abierto |
|---|---|---|
| Datos spot y sizing | Hay métodos formulados y factores tradicionales identificados | Serie cripto point-in-time, exchanges, exclusiones, costes y control de riesgo comparables |
| Opciones | Deribit se identifica y hay ventanas históricas descritas | Quotes ejecutables/versionados, licencias, tick/contract changes, cobertura y colateral |
| Carteras | Sensibilidad a media/covarianza y ambigüedad relevante | Superioridad incremental de modelos complejos frente a 1/N, estabilidad y turnover |
| Regímenes | Estados retrospectivos y previsión OOS declarada, con resultados adversos frente a modelos simples | Reconciliar splits/tablas, filtro causal, latencia, selección congelada y prueba económica neta |
| Contraste independiente | Fuentes diferentes no se cuentan como réplica de la misma hipótesis | Réplicas netas y evidencia negativa independiente en cripto; críticas de sizing a texto completo |

Este cierre usa exclusivamente los ocho documentos cacheados, sin nuevas búsquedas ni descargas. Los fallos previos de acceso y los metadatos pendientes siguen registrados. No hubo dos rondas completas de saturación y no se afirma exhaustividad ni cobertura universal hasta octubre de 2026. La revisión permite mantener preguntas falsables y documentar evidencia insuficiente; no selecciona candidatos de Fase II ni autoriza implementaciones.
