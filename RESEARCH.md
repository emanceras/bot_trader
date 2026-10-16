# Investigación científica — Fase I

**Actualizado:** 2026-10-15 · **Versión:** 0.2 · **Estado:** primer informe con fuentes verificadas y cobertura limitada; Fase I abierta. Sin experimentos propios ni autorización de Fase II.

## 1. Preguntas científicas principales

1. **¿Qué mecanismo produciría la ventaja y quién pagaría por ella?** Diferenciar compensación por riesgo, provisión de liquidez, restricciones de arbitraje y errores de precios. Una prima de riesgo puede ser real y a la vez incompatible con nuestro riesgo tolerable.
2. **¿Existe predictibilidad económicamente utilizable?** Separar predicción de signo/retorno/volatilidad, precisión estadística, beneficio bruto y beneficio neto ejecutable con información disponible entonces.
3. **¿La estrategia aporta algo más que exposición a cripto o a otro factor?** Comparar con efectivo, buy and hold y referencias simples con exposición/riesgo comparables; distinguir alpha de beta, apalancamiento y venta implícita de riesgo de cola.
4. **¿Persiste después de todos los costes y restricciones?** Considerar comisiones alcanzables por un particular, spread, slippage, impacto, préstamos, financiación, funding, rebalanceos, redondeos, transferencias y tamaño mínimo cuando correspondan.
5. **¿Qué evidencia existe fuera del desarrollo original?** Separar OOS temporal verdaderamente sellado, walk-forward con procedimiento congelado, replicación independiente y resultados prospectivos. Un periodo llamado «test» puede haber sido reutilizado.
6. **¿Cuántas decisiones y pruebas condujeron al resultado publicado?** Incluir selección de activos, exchanges, periodos, variables, hiperparámetros, reglas de costes y artículos, no solo la última cuadrícula reportada.
7. **¿Son los datos point-in-time y ejecutables?** Examinar deslistados, cambios de ticker/contrato, timestamps de disponibilidad, volumen artificial, revisiones, interrupciones y profundidad. Una vela agregada no reconstruye una cola de órdenes.
8. **¿La ventaja depende de regímenes conocidos solo retrospectivamente?** Separar resultados condicionados ex post de una política capaz de identificar el estado en tiempo real, descontando cambios de posición y retrasos.
9. **¿Qué pierde la estrategia en situaciones extremas?** Examinar drawdown, colas, liquidación, ampliación de spreads, inversión del funding, ruptura de correlaciones, depeg, insolvencia de contraparte y capital inmovilizado.
10. **¿Se mantiene con pequeñas perturbaciones razonables?** Cambios de periodo, parámetros vecinos, latencia, exchange y estructura de costes. Estabilidad no significa que cada subconjunto deba ganar, pero una única configuración aislada necesita una explicación fuerte.
11. **¿Puede un particular acceder a la prima?** Capital, margen, comisiones, disponibilidad de cortos, datos, infraestructura, restricciones legales y dedicación. Un mecanismo válido puede ser inviable para nosotros.
12. **¿Añade valor la complejidad?** ¿Un modelo no lineal mejora decisiones netas fuera de muestra frente a modelos simples con igual información, riesgo y presupuesto de búsqueda? ¿Compensa operación, mantenimiento e incertidumbre?
13. **¿Diversificar reduce realmente el riesgo?** Distinguir diversificación entre activos de diversificación de mecanismos; medir costes adicionales y correlaciones en estrés, no solo las medias históricas.
14. **¿Qué observación nos haría abandonar cada hipótesis?** Definir falsadores y condiciones de parada antes de elegir parámetros. La falta de significación con baja potencia no prueba inexistencia de ventaja; sí puede impedir justificar capital.

Estas preguntas guían la lectura. Las hipótesis concretas y sus posibles refutaciones están en [HYPOTHESES.md](HYPOTHESES.md).

## 2. Alcance, acceso y límites de esta entrega

El acceso externo funciona para una parte relevante de las fuentes: se recuperaron documentos de NBER, BIS, arXiv, editoriales abiertas y páginas de autores. El bloqueo general observado inicialmente queda superado en esta instancia; persisten denegaciones editoriales concretas y descargas que devuelven HTML en lugar de un PDF. No se requiere una clave de exchange para esta investigación.

Se documentan las trece familias con **28 trabajos con texto completo disponible y fichas de las secciones examinadas**, incluidos trabajos metodológicos y de mercados tradicionales. Esto no significa lectura exhaustiva de todos sus apéndices, réplica de sus resultados ni 28 pruebas de rentabilidad cripto. Las versiones de trabajo y editoriales se agrupan; se declara cuál se leyó. Las fuentes accesibles solo como resumen/metadatos se mantienen aparte.

| Bloque | Textos con ficha de lectura | Síntesis y evidencia verificable |
|---|---:|---|
| Momentum, reversión y factores | 4 | [Síntesis](docs/research/directional.md) · [Fichas DIR](docs/research/evidence-directional.md); otros siete trabajos con acceso parcial |
| Arbitraje estadístico, pares y carry | 3 | [Síntesis](docs/research/relative-value.md) · [Fichas RV](docs/research/evidence-relative-value.md) |
| ML y deep learning | 5 | [Síntesis](docs/research/ml-execution.md) · [Fichas ML](docs/research/evidence-ml.md); incluye dos trabajos metodológicos ajenos a cripto |
| Microestructura y market making | 5 | [Síntesis](docs/research/execution.md) · [Fichas EX](docs/research/evidence-execution.md); dos empíricos Bitcoin y tres de teoría/acciones |
| Volatilidad, regímenes y carteras | 8 | [Síntesis](docs/research/risk-portfolio.md) · [Fichas RP](docs/research/evidence-risk-portfolio.md); incluye teoría y un estudio tradicional |
| Multiplicidad y validación | 3 | [Fichas MET](docs/research/evidence-methodology.md); tres originales adicionales solo identificados por metadatos |

Las fichas registran fuentes públicas, versiones, fechas, páginas/tablas, resultados adversos y límites. Los registros JSONL de la sección 10 conservan consultas, accesos y fallos. Los PDF/textos recuperados se conservan fuera del repositorio, en `/workspace/literature-cache/`; los hashes permiten identificar versiones. No se redistribuyen esos textos en Git.

**Límite de cobertura:** revisión exploratoria estructurada, no revisión sistemática exhaustiva hasta octubre de 2026. No se completaron dos rondas de saturación de citas ni una réplica independiente por familia. Reversión, funding de perpetuos, prima de opciones y combinaciones netas tienen lagunas decisivas. Cerrar esta entrega documental no satisface por sí solo la aceptación completa de Fase I.

**Resultados propios: cero.** No se descargaron series para backtests, no se entrenaron modelos y no se programó el bot. Los números siguientes pertenecen a las fuentes indicadas; no son estimaciones de rentabilidad futura del proyecto.

## 3. Plan de investigación bibliográfica

### 3.1 Pregunta de revisión y unidad de análisis

**Población:** mercados de criptomonedas negociables por particulares, separando spot, futuros con vencimiento, perpetuos y opciones; CEX y DEX no se mezclarán sin modelar su ejecución específica. La primera revisión distinguirá evidencia cripto directa de resultados transferidos desde mercados tradicionales.

**Intervención:** regla de inversión o procedimiento de estimación/selección. **Comparadores:** efectivo definido, exposición pasiva, reglas sencillas y variantes equivalentes en información/riesgo. **Resultados:** P&L neto y riesgo fuera de muestra, replicabilidad y viabilidad operativa.

La unidad será el **estudio y su experimento**, no cada versión del PDF. Preprint, working paper y publicación de un mismo trabajo se agruparán; actualizaciones con datos nuevos se identificarán sin fingir independencia. Varios artículos que reutilizan el mismo dataset tampoco constituyen necesariamente replicaciones independientes.

### 3.2 Fuentes y búsqueda

Orden previsto de consulta:

1. Artículos revisados por pares, páginas editoriales y versiones completas autorizadas de sus autores. Verificar DOI, autores, título, año, versión y, cuando proceda, correcciones/retractaciones.
2. Working papers identificables —por ejemplo NBER/BIS— y preprints arXiv/SSRN. Marcar explícitamente si no hay revisión por pares verificada.
3. Datos y código oficiales asociados a cada estudio, con licencia y versión/commit. Un repositorio de código no sustituye el examen de la metodología.
4. Documentación oficial de exchanges/proveedores para reglas de contratos, tarifas y disponibilidad histórica. Puede establecer mecánica operativa; no demuestra rentabilidad.
5. Afirmaciones comerciales, blogs y backtests promocionales solo como generadores de hipótesis. Identificarlos por separado; no contarlos como confirmación independiente.

Crossref y páginas editoriales sirven para identidad/metadatos; los índices de búsqueda sirven para localizar trabajos, no para adjudicar calidad. La imposibilidad de pagar o acceder a un texto se registra como limitación, no como evidencia negativa.

**Cobertura temporal prevista:** desde los primeros estudios relevantes hasta la fecha efectiva de la búsqueda, con clásicos anteriores para fundamentos. No limitar la lectura a periodos alcistas o a trabajos muy citados. Priorizar actualización y periodos recientes sin confundir novedad con calidad. Registrar fecha de corte efectiva y restricciones lingüísticas; búsqueda inicial en inglés, admitiendo trabajos accesibles en otros idiomas.

### 3.3 Consultas reproducibles por familia

Combinar cada consulta temática con `transaction costs`, `out-of-sample`, `replication`, `robustness`, `survivorship`, `failure`, `no predictability`, `market efficiency` y equivalentes. Son plantillas del protocolo. Los registros JSONL de la sección 10 identifican las consultas efectivamente ejecutadas; no se afirma haber ejecutado todas las combinaciones ni todos los filtros.

| Familia | Consulta base orientativa |
|---|---|
| Trend/momentum | `(cryptocurrency OR bitcoin) AND ("time series momentum" OR "cross sectional momentum" OR "trend following")` |
| Reversión | `(cryptocurrency OR bitcoin) AND ("mean reversion" OR "return reversal" OR contrarian)` |
| Statistical arbitrage | `cryptocurrency AND ("statistical arbitrage" OR "relative value" OR "price deviations")` |
| Pares/cointegración | `cryptocurrency AND ("pairs trading" OR cointegration OR "error correction")` |
| Factores | `cryptocurrency AND ("risk factors" OR "factor investing" OR "cross section of returns")` |
| Volatilidad | `(bitcoin OR cryptocurrency) AND ("volatility risk premium" OR "variance risk premium" OR "option strategy" OR "volatility timing")` |
| Funding | `cryptocurrency AND ("funding rate" OR "perpetual futures" OR "cash and carry" OR basis)` |
| Microestructura | `cryptocurrency AND ("order flow" OR "order book imbalance" OR "market microstructure")` |
| Market making | `cryptocurrency AND ("market making" OR "liquidity provision" OR "adverse selection")` |
| ML | `cryptocurrency AND ("machine learning" OR "random forest" OR boosting) AND (trading OR returns)` |
| DL/series temporales | `cryptocurrency AND ("deep learning" OR LSTM OR transformer OR "time series forecasting") AND (trading OR returns)` |
| Regímenes | `cryptocurrency AND ("regime switching" OR "hidden Markov" OR "structural breaks") AND trading` |
| Carteras/combinaciones | `cryptocurrency AND ("portfolio allocation" OR "strategy combination" OR diversification OR ensemble)` |

Buscar también términos que cuestionen el mecanismo concreto: momentum crash, cointegration breakdown, funding reversal, queue position, latency, nonstationarity, fee sensitivity y backtest overfitting. Comparar artículos que usan horizontes y costes similares; diferencias de mercado o fecha pueden explicar resultados opuestos.

### 3.4 Proceso de cribado y contraste

1. Registrar consulta exacta, fuente/índice, fecha, filtros y número de resultados solo si realmente los devuelve el servicio. Conservar errores de acceso.
2. Deduplicar por DOI y por identidad de trabajo; vincular versiones y conjuntos de datos compartidos.
3. Examinar título/resumen para relevancia y después texto completo para métodos. Registrar incluidos, excluidos y pendientes con razones explícitas.
4. Extraer campos de 3.5. Para una conclusión decisiva, una segunda lectura/revisión debe comprobar que la cita soporta exactamente la afirmación y no omite costes o selección.
5. Rastrear referencias anteriores y citas posteriores de cada trabajo clave, incluyendo replicaciones, correcciones y críticas. Buscar de forma deliberada resultados adversos.
6. Sintetizar por familia, distinguiendo evidencia cripto, evidencia de otros mercados y fundamento teórico. No agregar Sharpes incompatibles o sesgados por publicación como si fueran una muestra homogénea.
7. Registrar lagunas y actualizar conclusiones únicamente con evidencia identificada. Comunicar cuándo una familia carece de datos adecuados o de contraste independiente.

**Inclusión:** mecanismos pertinentes y estudios identificables con datos/métodos suficientes para extraer al menos una conclusión delimitada. Teoría sin backtest se admite como teoría, no como rentabilidad empírica.

**Exclusión de la evidencia decisiva de ventaja:** publicidad sin metodología; títulos/abstracts sin validación inspectable; estrategias irreproducibles por falta de especificación; test contaminado o costes incompatibles sin análisis alternativo. No borrar estos trabajos: registrarlos como limitados, contradicciones o pendientes y explicar la razón.

**Parada de búsqueda:** aplicar el criterio de cobertura del roadmap y dos rondas de referencias/citas sin nueva evidencia material, o declarar acceso/recursos insuficientes. Esta entrega se consolida por límite de recursos y con lagunas explícitas; no se alcanzó la saturación y la aceptación de su cobertura sigue pendiente.

### 3.5 Ficha obligatoria por estudio

| Campo | Contenido a registrar |
|---|---|
| Identidad y acceso | ID, título, autores, año, versión, DOI/URL, editor, estado de revisión, fecha y nivel de lectura |
| Mercado y datos | Activos, exchanges, instrumentos, fuentes, frecuencia, fechas, cobertura de deslistados y reglas point-in-time |
| Mecanismo | Hipótesis, nula, señal, formación de cartera, horizonte, supuestos económicos |
| Selección | Parámetros y variables explorados, número de pruebas declarado/desconocido, decisiones tras ver resultados |
| Validación | Entrenamiento/validación/test, walk-forward, purga/embargo cuando procedan, ajuste temporal de transformaciones |
| Ejecución | Decisión/orden/fill, latencia, spread, slippage/impacto, fees, funding, préstamos, margen y liquidación |
| Comparadores | Mismo universo, moneda, riesgo, periodos y costes; efectivo y pasivo bien definidos |
| Resultados | Métricas netas/brutas separadas, intervalos, sensibilidad, regímenes y resultados negativos con página/tabla |
| Reproducción | Código/datos/licencia/versión; diferencias entre replicación por autores e independiente |
| Transferibilidad | Condiciones necesarias para un particular, capital/capacidad, restricciones y riesgos no modelados |
| Juicio | Conclusión que la fuente soporta, objeciones, nivel de evidencia y preguntas abiertas |

Cada afirmación empírica de la síntesis deberá tener ID y ubicación concreta. No rellenar campos desconocidos por inferencia.

## 4. Criterios explícitos de evaluación de evidencia

No se sumarán notas arbitrarias. Para cada dimensión se consignará **suficiente**, **parcial**, **ausente** o **no evaluable**, acompañado de una razón y evidencia. Una dimensión crítica ausente no se compensa con otra favorable.

| Dimensión | Evidencia que aumenta la confianza | Lo que impide una conclusión fuerte |
|---|---|---|
| Identidad/independencia | Fuente primaria identificada; versión y revisión verificadas; réplica independiente | Marketing, versiones duplicadas, conflictos/selección no transparentes |
| Mecanismo económico | Hipótesis falsable y explicación de quién absorbe riesgo/coste | Relato construido después de ver retornos |
| Datos | Universo histórico, disponibilidad temporal y datos ejecutables auditables | Supervivientes, futuro filtrado, precios teóricos, historial reconstruido sin control |
| OOS | Cronología real; selección cerrada antes del test; procedimiento walk-forward completo | Split aleatorio, reutilización del test, normalización/modelo ajustados con futuro |
| Ejecución/costes | Costes alcanzables, sensibilidad, órdenes/fills y margen coherentes | Cero costes, fills al mid garantizados, shorts o margen supuestos gratuitos |
| Selección/multiplicidad | Historial de búsqueda y controles adecuados a la dependencia | Solo mejor modelo presentado; ensayos omitidos; optimización fuera del registro |
| Incertidumbre | Intervalos/procedimientos adecuados a dependencia y colas; magnitud económica | Solo p-value/Sharpe puntual; anualización que presupone independencia inexistente |
| Robustez | Perturbaciones razonables, épocas/exchanges y resultados adversos explicados | Un activo/periodo/parámetro aislado sin explicación |
| Reproducibilidad | Código/datos/versiones y especificación suficiente; replicación | Dependencias/datos inaccesibles o métodos insuficientes |
| Viabilidad/riesgo | Capital/capacidad, margen y pérdidas extremas; entorno operativo accesible | Liquidaciones/contraparte omitidas o infraestructura inalcanzable |

### Vocabulario para las conclusiones

- **No evaluada:** referencia o dimensión sin lectura suficiente; se aplica a las lagunas identificadas, no a todo el corpus.
- **Mecanismo plausible:** análisis económico/matemático coherente; no demuestra una prima o beneficio.
- **Indicio empírico:** resultados inspeccionados con limitaciones identificadas; no implica replicación ni operabilidad.
- **Evidencia retrospectiva más sólida:** fuentes primarias con OOS y costes creíbles, corrección de selección y contraste independiente; requiere detalle, no una etiqueta automática.
- **Evidencia prospectiva:** procedimiento congelado observado en datos posteriores; aún sujeto a tamaño de muestra y costes/fills reales.

Estos estados no son probabilidades ni una clasificación de estrategias. La revisión por pares ayuda a evaluar procedencia, pero no garantiza reproducibilidad, corrección o persistencia actual.

**Resultados positivos y negativos:** «positivo» requiere especificar resultado, periodo, mercado, benchmark y costes. Un resultado que se vuelve negativo con costes es adverso para su implementación, aunque la predicción sea significativa. «No significativo» con poca potencia no se traduce en «no existe efecto». Un fallo de datos/ejecución no prueba que el mecanismo económico sea falso.

## 5. Marco económico común

Para una cartera sencilla sin flujos externos, una aproximación de un periodo es:

\[
r^{neto}_{t+1} \approx w_t^\top r_{t+1} +(1-\mathbf{1}^\top w_t)r^{caja}_{t+1}
- C_{t+1}+F_{t+1}-B_{t+1}.
\]

Las ponderaciones se deciden con información disponible en \(t\). \(C\) son costes de negociación como fracción del patrimonio; \(F\) es funding **firmado**, positivo si se recibe; \(B\) es financiación/préstamo. Esta expresión es conceptual: derivados, colateral, apalancamiento, liquidaciones y posiciones intraperiodo requieren contabilidad de flujos exacta. No permite asumir fills al mismo cierre que genera la señal ni volver a sumar costes ya incluidos en precios ejecutados.

El efectivo debe definirse en una moneda y un instrumento concretos. Una stablecoin tiene riesgo de emisor/depeg y una cuenta remunerada tiene sus propias condiciones. Buy and hold también incurre en costes de entrada/salida y custodia según la comparación.

Una prima neta no es necesariamente alpha: puede ser compensación por exposición de mercado, iliquidez, financiación o riesgo extremo. La pregunta no será solo «¿gana?», sino «¿qué riesgo y recursos exige frente a una alternativa accesible?».

## 6. Mapa crítico de las trece familias

Esta tabla reúne evidencia y límites para orientar la investigación. No es la matriz de selección de Fase II ni una puntuación de probabilidad de éxito. Los identificadores remiten a las fichas de la sección 2; allí constan páginas y tablas. OOS significa evaluación fuera de la muestra de ajuste declarada por el estudio, sin presumir que su selección estuviera sellada.

| Familia | Mecanismo y evidencia observada | Límite decisivo: OOS, ejecución y riesgo | Datos e infraestructura; viabilidad particular |
|---|---|---|---|
| 1. Trend/momentum | Persistencia temporal/transversal. DIR-001 encuentra predictibilidad; DIR-006 presenta resultados OOS distintos por activo; DIR-010 no encuentra momentum bruto significativo en toda su muestra | Correcciones de incertidumbre debilitan algunas señales; BTC pierde en el test de 2018 de DIR-006. Riesgo de reversión/crash y selección de reglas; ventaja neta actual no establecida | OHLCV y universo histórico; long/flat de baja frecuencia relativamente sencillo. Cortos transversales añaden préstamo, margen y capacidad |
| 2. Mean reversion | Presión transitoria de liquidez o corrección de desviaciones. DIR-007/008/013 sugieren dependencia del horizonte/tamaño, pero solo se leyeron resúmenes | Falta auditar métodos, costes y OOS de esos originales. Bid-ask bounce no equivale a retorno capturable; la referencia de equilibrio puede romperse | Quotes/trades para horizonte corto; OHLCV solo si basta para la hipótesis. Regla simple viable de investigar, evidencia negociable insuficiente |
| 3. Statistical arbitrage | Retorno residual respecto a factores o spreads; RV-E02/03 aportan casos de valor relativo | La cobertura se concentra en pares, sin demostrar neutralidad robusta de carteras residuales amplias. Dependencia común, selección múltiple y posiciones cortas | Precios sincronizados, universo point-in-time, factores, borrow/margen; dificultad media/alta |
| 4. Pares/cointegración | Corrección de un spread estimado. RV-E02: distancia supera cointegración intradía; RV-E03: algunas cópulas son positivas tras fees | RV-E02 excluye activos sin historia continua y omite coste de cortos; RV-E03 deja funding/slippage sin modelar. Varias referencias cambian de signo con fees; pérdidas teóricas inferiores a −100% requieren auditoría de solvencia | Dos patas ejecutables, formación solo con pasado, costes y colateral conjuntos; viabilidad condicionada |
| 5. Factores cripto | Mercado, tamaño y momentum explican diferencias de retornos en DIR-002 | Explicación factorial no prueba alpha neto. En el WP, varios momentums dejan de ser significativos al sustituir cortos de perdedores por BTC; universo y liquidez importan | Amplio universo histórico con deslistados y características disponibles entonces. Útiles como controles; cartera implementable por demostrar |
| 6. Volatilidad | Separar previsión, exposición por riesgo y prima de opciones. RP-01 respalda un mecanismo de escalado en mercados tradicionales; RP-02/03 estudian IV/valoración | Transferencia cripto sin verificar; valoración más precisa no es P&L. Sin evidencia consultada de prima de opciones neta con hedge, margen y colas completos | Retornos para sizing; superficies bid/ask, vencimientos y colateral para opciones. Control simple más accesible que negociación de convexidad |
| 7. Funding/basis | Segmentación y demanda de apalancamiento. RV-E01 encuentra carry de futuros con vencimiento bajo supuestos de financiación | Su Sharpe 0,59 es anterior a costes de transacción y spreads de financiación. No demuestra estrategia de funding de perpetuos; margen, contraparte y convergencia son distintos | Spot/derivado, índice/marca, funding liquidado y disponible entonces, financiación y capital de ambas patas; complejidad operativa media/alta |
| 8. Microestructura/order flow | Presión de órdenes y formación de precios. EX-01 predice a corto plazo; EX-03 relaciona OFI y precio contemporáneos | Cont no demuestra predicción futura ni causalidad exógena. Taker de EX-01 negativo con tarifa ordinaria; spread, latencia y profundidad consumen señal | Libro secuenciado y timestamps de recepción; multivenue sincronizado. Exigencia técnica alta para un particular |
| 9. Market making | Spread/rebates frente a inventario y selección adversa. EX-04 formaliza control de inventario; EX-01 informa un ensayo maker real positivo tras rebates | Resultado muy pequeño y condicionado a rebates/latencia, sin réplica comparable ni costes completos. Simulación de quotes no identifica prioridad/fill | Datos de órdenes/colas, fills parciales, servicio continuo, inventario y riesgo de desconexión. Viabilidad sin determinar |
| 10. ML | Estimar relaciones condicionales. ML-06 encuentra algunos resultados OOS positivos y fuerte sensibilidad a fees; ML-09 compara boosting/LSTM | Efecto depende de activo/modelo, costes incompletos y búsqueda de especificaciones. Falta demostrar incremento neto replicado frente a referencias equivalentes | Variables disponibles entonces y pipelines temporales; ML sencillo técnicamente accesible. Mantenimiento y multiplicidad son costes de investigación |
| 11. DL/series temporales | Representaciones secuenciales/no lineales. ML-11 comunica grandes ganancias simuladas; EX-05 predice libros de acciones | ML-11 supone ejecución inmediata sin slippage/impacto; EX-05 usa simulación mid–mid sin costes. ML-08 muestra competencia de modelos lineales en otros datos, sin demostrar superioridad universal | Más cómputo, semillas y muestras efectivas. Complejidad solo justificable si añade mejora neta fuera de muestra |
| 12. Regímenes | Estados latentes con distintas dinámicas. RP-06 describe estados; RP-07/08 comparan previsión de volatilidad | Clasificación retrospectiva, splits poco claros y modelos simples competitivos/superiores. Filtrado con parámetros futuros o suavizado no está disponible para operar entonces | Probabilidades filtradas, estimación causal, demora de detección y costes de conmutación; beneficio de asignación no demostrado |
| 13. Combinaciones/carteras | Diversificar mecanismos y controlar concentración. RP-04/05 formalizan optimización/ambigüedad; ML-06 estudia ensembles | RP-04 no mejora Sharpe en su propia tabla; RP-05 es teoría calibrada. Falta comparación neta independiente contra pesos simples, con estrés y turnover | P&L sincronizado, covarianzas pasadas, costes/margen agregados. Pesos simples accesibles; optimización añade inestabilidad y selección |

Los desarrollos matemáticos se encuentran en las cinco síntesis temáticas de la sección 2. Las familias se solapan: un modelo ML puede implementar momentum y un filtro de estados puede modificar una cartera. No son trece mecanismos independientes.

## 7. Primer informe crítico basado en fuentes

**Hay fundamentos suficientes para investigar varias líneas; no hay evidencia suficiente en este proyecto para operar ni para declarar una ganadora.** El corpus contiene resultados favorables y contrarios. La limitación no es solo acceso: muchas evaluaciones publicadas no representan conjuntamente tarifas alcanzables, disponibilidad de cortos, margen, selección y estabilidad temporal.

### Momentum y factores: hipótesis claras, evidencia heterogénea

El [WP de Liu y Tsyvinski de 2018](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf) aporta predictibilidad y una evaluación temporal de umbrales (DIR-001, §4.1). Pero algunas significaciones cambian al corregir incertidumbre: el estadístico diario ordinario 2,96 pasa a 1,22 con su bootstrap. No es evidencia suficiente de rentabilidad neta.

[Hudson y Urquhart](https://link.springer.com/content/pdf/10.1007/s10479-019-03357-1.pdf), DIR-006, evalúan muchas reglas y un test enero–junio de 2018: las mejores reglas de las dos series BTC presentan retornos/Sharpe/Sortino negativos, mientras LTC/XRP/ETH conservan resultados positivos (§6.5, tabla 9). Sus costes de equilibrio no equivalen a fills reales con todas las fricciones. [Grobys et al. 2025](https://link.springer.com/content/pdf/10.1007/s11408-025-00474-9.pdf), DIR-010, no encuentran momentum bruto significativo en toda la muestra 2016–2023 y documentan colas severas. Escalar por volatilidad no elimina ese riesgo.

Por ello, momentum temporal sencillo merece atención por su falsabilidad y menor esfuerzo de implementación, no porque la literatura haya probado su persistencia. Los factores sirven para explicar exposición antes de atribuir alpha. En el [WP de Liu, Tsyvinski y Wu](https://www.nber.org/system/files/working_papers/w25882/w25882.pdf), DIR-002, los momentums de una, dos y cuatro semanas dejan de ser significativos al sustituir la pata corta de perdedores por BTC (§5.1). La implementabilidad forma parte del resultado.

Reversión sigue siendo una pregunta interesante, especialmente su relación con liquidez, tamaño y horizonte, pero la evidencia directa consultada es insuficiente: resúmenes de DIR-007/008/013 no permiten resolver cuánto efecto queda después del spread y la selección. No se le asigna el mismo respaldo que a métodos examinados a texto completo.

### Valor relativo y carry: mecanismos interpretables con riesgos concretos

[Crypto carry, BIS WP1087 de 2023](https://www.bis.org/publications/working-paper-1087-crypto-carry.pdf), RV-E01, relaciona la base de futuros con segmentación y demanda de apalancamiento. La estrategia de la tabla 5 presenta Sharpe anualizado 0,59 antes de costes de transacción y spreads de financiación. No es una prueba de funding de perpetuos, cuyo pago futuro y ausencia de vencimiento requieren otra hipótesis. Una posición aproximadamente neutral al precio puede exigir liquidez adicional o liquidarse antes de converger.

En pares, [Fil y Kristoufek](https://doi.org/10.1109/ACCESS.2020.3024619), RV-E02, muestran distancia más competitiva que cointegración intradía; también advierten costes/shorts y un universo limitado a historias continuas. [Tadi y Witzany](https://link.springer.com/content/pdf/10.1186/s40854-024-00702-7.pdf), RV-E03, aportan evaluación semanal móvil y resultados favorables de algunas cópulas tras fees, junto a pérdidas enormes de referencias con mayor rotación. Funding, slippage y restricciones de margen no están resueltos por esa deducción de comisiones. El contraste merece lectura adicional; escoger el Sharpe mayor del artículo sería una selección prematura.

### ML/DL: hay resultados, sin superioridad general demostrada

[Sebastião y Godinho](https://link.springer.com/content/pdf/10.1186/s40854-020-00217-x.pdf), ML-06, separan entrenamiento/validación/test. Para Ensemble 5, la rentabilidad anualizada ETH del test pasa de 44,65% bruta a 9,622% con 0,5% por roundtrip; BTC pasa de 5,868% a −23,66% (tabla 7). Otros modelos se comportan de otra manera. El coste escalar no demuestra ejecución completa, y el Sharpe bruto no debe rotularse como neto.

Alessandretti et al. (ML-09) y Jiang et al. (ML-11) comunican grandes ganancias en BTC como unidad de cuenta, con simplificaciones importantes. [Jiang et al., arXiv v2](https://arxiv.org/abs/1706.10059v2), asumen expresamente ejecución inmediata sin slippage ni impacto (§2.4); esas cifras no son retornos anualizados en dólares ni una evaluación prospectiva. El trabajo de Zeng et al. (ML-08) aporta un motivo metodológico para exigir referencias lineales fuertes, pero usa otras series y no demuestra que un modelo lineal gane siempre en trading.

ML es una herramienta cuyo valor incremental sigue abierto. DL necesita justificar el coste de complejidad contra modelos sencillos con iguales datos y presupuesto de búsqueda.

### Microestructura y market making: la ejecución decide

[Albers et al., arXiv v1](https://arxiv.org/abs/2108.09750v1), EX-01, encuentran resultados taker negativos con tarifa ordinaria en las tablas 6/14 y algunos positivos con condiciones VIP. También realizaron un ensayo maker real: −4,4749 pb por roundtrip antes de rebates y +0,5251 pb tras ellos. No se debe ocultar este resultado favorable ni generalizarlo: utiliza condiciones de latencia muy bajas, rebates históricos y un benchmark de fechas/tamaños distintos, sin conciliación verificada de todos los gastos y riesgos de capital. No es una réplica propia.

Cont, Avellaneda–Stoikov y DeepLOB (EX-03–05) permiten entender formación de precios, inventario y predicción. Estudian teoría/acciones y no acreditan por sí mismos rentabilidad neta cripto. Estas líneas requieren un nivel de datos y ejecución que aún no sabemos si está al alcance del operador.

### Volatilidad, regímenes y carteras: separar riesgo de alpha

Moreira–Muir (RP-01) respaldan el mecanismo de ajustar exposición usando volatilidad pasada en mercados tradicionales; no es una prueba cripto. Los artículos de opciones RP-02/03 aportan cálculo/valoración, no una prima negociada con costes de cobertura y margen. Esto deja abierta la hipótesis, sin convertir menor error numérico en rentabilidad.

Los estudios de estados y carteras también contienen evidencia contraria útil: RP-04 informa menor Sharpe de su extensión que del comparador; RP-07 retira MSGARCH del OOS después de caracterizar el test; en la tabla 8 de RP-08, GARCH tiene menor RMSE en los cinco activos, pese a parte de la narrativa. RP-08 es un preprint, no un resultado revisado por pares. Estos hallazgos aconsejan investigar controles de riesgo y combinaciones simples antes de atribuir valor a la adaptación compleja.

### Prioridad de investigación y condiciones para cambiarla

La prioridad provisional de lectura se basa en mecanismo falsable, comparadores sencillos, costes identificables y viabilidad de los datos. Momentum temporal y control simple de exposición merecen contraste; reversión necesita mejor soporte documental; carry/pares merecen examen condicionado a financiación, costes y colas. Factores son útiles como controles. ML, estados y optimización deberán demostrar aportación incremental. Microestructura, market making y opciones requieren primero resolver sus datos y restricciones operativas.

Esto no selecciona candidatos ni descarta universalmente familias. Una réplica independiente con costes alcanzables, datos point-in-time o restricciones concretas del operador puede modificar la prioridad. La selección formal pertenece a Fase II y requiere aprobación.

## 8. Control metodológico que deberá extraerse de los estudios

Esta sección define preguntas de lectura y requisitos a diseñar en IV; **no es un protocolo experimental cerrado ni ejecutado**.

| Sesgo/problema | Qué comprobar en la literatura y exigir después |
|---|---|
| Look-ahead | Momento de publicación/recepción de cada variable y posibilidad de ejecutar después de la señal |
| Leakage | Escalado, selección de variables, imputación y estimación ajustados solo en entrenamiento; etiquetas solapadas controladas |
| Supervivencia | Activos y exchanges desaparecidos, elegibilidad histórica y pérdidas al salir del universo |
| Selección de datos | Periodos/activos/venues elegidos por resultados; benchmark con igual información disponible |
| Overfitting/data snooping | Registro de todos los intentos y alternativas; presupuesto de búsqueda; validación del procedimiento completo |
| Multiplicidad | Hipótesis primarias/secundarias, dependencia entre pruebas, correcciones apropiadas y recuentos desconocidos declarados |
| Optimización | Selección dentro de ventanas de desarrollo; modelos hiperparametrizados no consultan test; mismo presupuesto de búsqueda |
| Incertidumbre temporal | Bootstrap por bloques/estacionario u otro estimador justificado; sensibilidad a dependencia y colas; tamaño efectivo |
| Regímenes | Diferenciar clasificación ex post de variables/estados disponibles ex ante |
| Holdout final | Una apertura confirmatoria del procedimiento congelado; registro de acceso; no reutilizarlo tras rediseñar |

Purged CV/embargo se justifican cuando hay intervalos de etiquetas o información solapada; no son una receta universal ni corrigen datos ya contaminados. Walk-forward valida un procedimiento móvil solo si cada refit/selección utiliza pasado. El Deflated Sharpe Ratio no subsana un historial de ensayos oculto ni demuestra persistencia; revisar supuestos de momentos, dependencia y número efectivo de intentos. Los intervalos estrechos bajo un proceso histórico no eliminan riesgo de cambio estructural.

Para futuras pruebas múltiples se compararán métodos adecuados a la pregunta: correcciones de hipótesis primarias, Reality Check/SPA y diagnósticos de selección/Sharpe. No se acumularán tests hasta encontrar uno favorable. El método, su familia de hipótesis y nivel de error deben quedar fijados antes de V.

## 9. Evidencia metodológica consultada

Las [fichas metodológicas](docs/research/evidence-methodology.md) identifican versión, páginas, supuestos y límites. Ninguno de estos trabajos constituye evidencia de una estrategia cripto rentable.

| ID | Fuente | Nivel y consecuencia de lectura |
|---|---|---|
| MET-01 | White (2000), [Reality Check](https://doi.org/10.1111/1468-0262.00152) | Identidad verificada por metadatos; original bloqueado. No se adjudican supuestos detallados sin leerlo |
| MET-02 | Hansen (2005), [SPA](https://doi.org/10.1198/073500105000000063) | Metadatos; original bloqueado. Pendiente lectura antes de decidir aplicación |
| MET-03 | Bailey–López de Prado, [DSR, manuscrito 2014](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf) | Secciones examinadas: requiere historial de búsqueda, dispersión de Sharpes, momentos y número efectivo de ensayos. Su probabilidad no significa probabilidad de ganar en el futuro |
| MET-04 | Bailey et al., [PBO, manuscrito 2015](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf) | Diagnóstico de posición relativa OOS de la selección IS; no probabilidad de pérdida. CSCV no sustituye walk-forward causal ni holdout final |
| MET-05 | Harvey–Liu–Zhu, [NBER WP20592, 2014](https://www.nber.org/system/files/working_papers/w20592/w20592.pdf) | Selección/multiplicidad de factores, FWER frente a FDR. Un umbral t contextual no es regla universal ni transportable automáticamente a cripto |
| MET-06 | Lo (2002), [Statistics of Sharpe Ratios](https://doi.org/10.2469/faj.v58.n4.2453) | Metadatos; original bloqueado. Lectura de detalles pendiente |

La consecuencia práctica es conservar todos los intentos y definir el contraste antes de observar resultados de selección. No se ha elegido ni ejecutado todavía una prueba estadística para este proyecto.

## 10. Registro de búsqueda, lagunas y continuidad

| Fecha | Operación efectivamente intentada | Resultado | Qué permite afirmar |
|---|---|---|---|
| 2026-10-13 | GET `https://www.nber.org/papers/w24877` | Proxy CONNECT 403 | No se recuperó el artículo ni su resumen |
| 2026-10-13 | GET `https://arxiv.org/abs/1607.03082` como comprobación de acceso | Proxy CONNECT 403 | Destino inaccesible; el identificador no se incluye como evidencia temática |
| 2026-10-13 | GET `https://api.crossref.org/works?query.title=Common%20Risk%20Factors%20in%20Cryptocurrency&rows=1` | Proxy CONNECT 403 | No se recuperaron metadatos ni resultados de búsqueda |
| 2026-10-13 | Comprobaciones temáticas adicionales a DOI, BIS, NBER y editoriales | Bloqueadas por proxy; detalle en apéndices | Ningún contenido académico recuperado |

Los fallos anteriores son históricos. Las recuperaciones posteriores demostraron acceso efectivo a contenido académico, sin que ello acredite acceso universal o publicación de la configuración del entorno. La trazabilidad actual está en:

- [Direccionales](docs/research/search-directional.jsonl).
- [Valor relativo/carry](docs/research/search-relative-value.jsonl).
- [ML/DL](docs/research/search-ml.jsonl).
- [Ejecución](docs/research/search-execution.jsonl).
- [Riesgo/carteras](docs/research/search-risk-portfolio.jsonl).
- [Metodología](docs/research/search-methodology.jsonl).

Estos registros son heterogéneos por proveedor; no equivalen a un diagrama PRISMA ni a un recuento universal de publicaciones. Se preservan accesos fallidos, respuestas HTML y la exclusión EX-X01: arXiv:2108.09700 era un artículo de matemáticas, distinto del estudio financiero arXiv:2108.09750. Un HTTP 200 no verifica identidad ni contenido.

### Lagunas que impiden cerrar toda la Fase I

| Pendiente | Por qué afecta a las conclusiones | Siguiente trabajo de investigación propuesto |
|---|---|---|
| Reversión y liquidez a texto completo | No permite distinguir anomalía ejecutable de spread/selección | Obtener versión autorizada de DIR-013 y un contraste independiente; auditar horizonte, universo, costes y OOS |
| Funding de perpetuos | El carry de futuros con vencimiento no responde a esa hipótesis | Localizar estudio con pagos históricos conocidos entonces, ambas patas, margen y comisiones alcanzables |
| Volatilidad/opciones y combinaciones cripto | Cálculo/valoración/teoría no demuestra ventaja neta | Buscar estrategia neta con cobertura/colas y asignación OOS contra pesos simples, incluyendo resultados adversos |
| Réplicas y literatura posterior | Fuentes distintas pueden compartir datos; la cobertura no está saturada | Rastreo hacia atrás/delante de trabajos decisivos y búsqueda explícita de refutaciones; registrar resultados y límites |
| Reproducibilidad y métodos | No se ejecutó código de autores ni se auditaron paquetes/licencias; MET-01/02/06 pendientes | Inspección documental de datos/código y originales accesibles antes de diseñar la metodología experimental |

**Estado de aceptación:** preguntas, protocolo y primer informe documentados; acceso primario comprobado; trece familias cubiertas a distinto nivel. No todas tienen un estudio de trading y contraste independiente con métodos/costes/OOS examinados. Dos rondas de saturación pendientes. No se declara terminada Fase I ni se inicia II.

**Continuidad:** este cierre del 15 de octubre integra archivos y fuentes recuperados los días 13–15. Tras una interrupción, leer primero roadmap/decisiones, fichas, registros y cache; retomar tareas pendientes sin repetir búsquedas ya resueltas. El próximo paso requiere revisar este informe y acordar el tratamiento de las lagunas. Ningún experimento ni acción de trading queda programado para ejecutarse automáticamente.
