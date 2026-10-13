# Estrategias direccionales, factores, regímenes y carteras

Fecha: 2026-10-13. Estado: **documentado; revisión bibliográfica preliminar pendiente de acceso**. Alcance: Fase I. No se han implementado señales, descargado datos de mercado, ejecutado backtests ni seleccionado parámetros.

## 1. Qué evidencia tenemos realmente

Esta nota distingue tres objetos: mecanismos teóricos que se pueden formular, publicaciones semilla que será necesario leer y evidencia empírica efectivamente consultada. En esta sesión no se ha podido consultar el texto, resumen ni metadatos de las publicaciones enumeradas: los destinos `doi.org` y `www.nber.org` devolvieron `Tunnel connection failed: 403 Forbidden` a través del proxy. Se preservó la verificación TLS; no se intentó eludir esa restricción.

Por tanto, **no atribuimos a estos trabajos resultados positivos, negativos, fuera de muestra o netos de costes**. Los títulos y datos bibliográficos de la tabla son referencias semilla conocidas, pendientes de contrastar con la fuente editorial; no constituyen evidencia extraída ni una revisión exhaustiva. La falta de acceso no es evidencia de ausencia de ventaja. Las condiciones de fracaso descritas abajo son mecanismos y preguntas refutables, no resultados publicados verificados.

## 2. Preguntas científicas transversales

1. ¿Una señal aporta información incremental sobre mantener una exposición pasiva y sobre variar esa exposición mediante una regla sencilla de riesgo?
2. ¿La aparente ventaja procede de predecir retornos, de reducir exposición en caídas, de asumir riesgos omitidos o de seleccionar retrospectivamente activos y periodos?
3. ¿Se conserva después de comisiones, spread, slippage, impacto, financiación y restricciones reales de inversión?
4. ¿Existe evidencia cronológicamente posterior a la especificación del método, además de particiones retrospectivas? ¿Cuántas alternativas se ensayaron antes de publicar?
5. ¿Los resultados dependen de activos desaparecidos excluidos, precios no negociables, timestamps ambiguos o ejecuciones imposibles al mismo precio que genera la señal?
6. ¿Una regla con menos parámetros ofrece resultados económicamente indistinguibles cuando se considera incertidumbre y dependencia temporal?
7. ¿Qué observación falsaría la hipótesis y permitiría detener esa línea sin añadir nuevas condiciones después de ver el resultado?

Notación común: `r(i,t)` es el retorno simple del activo `i` durante el intervalo que termina en `t`; `I_t` es la información disponible al decidir. Una ponderación decidida usando `I_t` se ejecutaría después de observar esa información, con latencia y precios factibles. El retorno posterior de cartera incluiría costes y financiación. Una fórmula de señal no determina por sí sola una política de ejecución o una ventaja negociable.

## 3. Trend following y momentum

### Fundamento y distinciones

El momentum temporal pregunta si el historial de un activo ayuda a determinar su propia exposición. Una formulación de investigación es `m(i,t,L) = sum_{s=t−L+1}^{t} log(1+r(i,s))`, usando solamente observaciones hasta `t`; la exposición posterior depende del signo o magnitud de `m`. El momentum transversal ordena activos por una medida de rendimiento pasado y estudia diferencias posteriores entre grupos. Son hipótesis distintas: una puede reflejar el régimen del mercado y la otra dispersión relativa.

Los mecanismos plausibles incluyen incorporación gradual de información, flujos persistentes y ajustes lentos de posiciones. También pueden producir patrones aparentemente similares una prima por riesgo, burbujas o selección ex post. La continuidad del precio no identifica por sí sola su causa.

Una escala por volatilidad estimada con datos pasados modifica el perfil de riesgo, pero puede confundirse con capacidad predictiva; habrá que separar el efecto de la señal del efecto de esa escala. Para un particular, una versión spot de posiciones largas o efectivo evita supuestos de venta corta; no reproduce automáticamente una estrategia larga/corta publicada.

### Evidencia y contradicción que debemos buscar

- Evidencia consultada en esta sesión: ninguna. DIR-001, DIR-002 y DIR-003 son semillas; DIR-003 corresponde a mercados tradicionales y no demostraría transferibilidad a criptomonedas.
- Pregunta favorable: ¿se repite la persistencia en periodos y mercados independientes con reglas sencillas fijadas previamente?
- Pregunta contraria: ¿desaparece al controlar exposición al mercado, costes y publicación del hallazgo? ¿Los cambios bruscos de tendencia o recuperaciones rápidas concentran pérdidas? Un promedio positivo puede coexistir con pérdidas extremas incompatibles con el capital disponible.
- Fuera de muestra pendiente: fechas de formación y prueba, frecuencia con que se modificó la regla, universo disponible en cada fecha, independencia entre versiones del artículo y continuidad posterior a su publicación.

### Costes, datos e infraestructura

Datos de precios negociables y volumen por venue, calendario 24/7, reglas de listado y baja, eventos de tokens y una convención temporal inequívoca. En pruebas transversales se necesita universo histórico punto en el tiempo. El turnover aumenta con cambios frecuentes de clasificación y rebalanceos; los costes pueden ser mayores precisamente cuando cambia una señal. Las variantes cortas exigen disponibilidad de préstamos o contratos, financiación, restricciones y riesgo de liquidación. La viabilidad técnica minorista de una regla spot de baja frecuencia es plausible; su rentabilidad sigue sin establecerse.

### Condiciones de descarte

Detener una especificación si su aparente ventaja depende de ejecuciones contemporáneas imposibles, exclusión de activos fallidos, un único episodio o parámetros estrechos sin soporte fuera de muestra. No rescatarla ajustando el horizonte después de abrir el holdout. Si no supera de forma robusta una referencia pasiva comparable tras costes, no hay base para aumentar su complejidad.

## 4. Mean reversion

### Fundamento y distinciones

La hipótesis requiere una desviación respecto de una referencia económicamente o estadísticamente justificable y una fuerza de corrección. Una señal descriptiva es `z_t = (x_t - mu_t) / sigma_t`, donde las estimaciones de referencia utilizan exclusivamente información disponible. **Que `z_t` sea extremo no implica que el precio vaya a volver a la media.** Un modelo ilustrativo `x(t+1) - mu = phi * (x(t)-mu) + epsilon(t+1)`, con `abs(phi)<1`, describe estacionariedad en el modelo; no demuestra que un precio de criptomoneda siga ese proceso.

Debe distinguirse reversión de retornos tras movimientos extremos, reversión de una variable estacionaria y reversión de un spread entre activos. La tercera pertenece a la revisión de arbitraje estadístico y pares. Sobreprecios temporales por demanda de liquidez o inventarios son mecanismos posibles; noticias permanentes y cambios de valor fundamental explican por qué una desviación puede no corregirse.

### Evidencia y contradicción que debemos buscar

No se ha consultado un estudio primario de reversión en criptomonedas en esta sesión. La bibliografía específica es una brecha de cobertura; no se extrapolan automáticamente conclusiones de pares o de acciones.

Se buscarán estudios que distingan bid–ask bounce de reversión económica: retornos calculados alternando compras y ventas pueden inducir autocorrelación negativa sin margen capturable. También se exigirán análisis de precios medios frente a precios ejecutables, tendencias persistentes, saltos, activos ilíquidos y bajas. Un patrón significativo antes de costes no basta.

### Costes, datos e infraestructura

A baja frecuencia podrían bastar inicialmente precios y volumen, más spreads observables para evaluar factibilidad. A frecuencias altas se necesitan operaciones con timestamps consistentes, cotizaciones bid/ask y, según el mecanismo, libro y simulación de fills. Una orden límite no garantiza ejecución; condicionarla a ser ejecutada introduce selección adversa. La expectativa del beneficio bruto debe superar la expectativa de los costes completos, considerando la distribución de ganancias y pérdidas, fills parciales y periodos de espera; no se exige que cada operación individual sea rentable. Promediar pérdidas sin límite no resuelve la incertidumbre sobre reversión.

Para un particular, una regla sencilla spot puede ser técnicamente accesible. La reversión intradía que depende de prioridad de cola o datos muy finos exige infraestructura muy diferente y no se presume viable.

### Condiciones de descarte

Descartar una especificación cuyo resultado desaparezca con precios ejecutables, dependa de ventanas escogidas a posteriori, falle al introducir latencia razonable o concentre las pérdidas en tendencias que no puede financiar. Una estimación de vida media inestable o sin precisión útil impide justificar el horizonte de una estrategia de spread.

## 5. Factor investing en criptomonedas

### Fundamento y distinciones

Un modelo como `r(i,t) = alpha_i + beta_i' f_t + epsilon(i,t)` describe covariación con factores. Explicar retornos realizados no equivale a predecirlos ni a construir una cartera negociable. Debe distinguirse un factor estadístico contemporáneo de una característica observable antes de decidir, y la prima económica de su réplica ejecutable.

Candidatos conceptuales: exposición al mercado, tamaño, momentum, liquidez y medidas de actividad de la red. Una prima puede compensar iliquidez, riesgo de cola, concentración o limitaciones de arbitraje; no sería necesariamente una ineficiencia. Capitalización depende de oferta circulante y precio; revisiones de oferta, tokens bloqueados y liquidez real complican la interpretación.

### Evidencia y contradicción que debemos buscar

DIR-002 y DIR-001 son semillas, no estudios consultados. La revisión deberá comprobar qué factores se definen, si explican retornos dentro de muestra o predicen fuera de ella y si existen carteras netas de costes implementables.

La evidencia contraria relevante incluye pérdida del efecto al conservar activos desaparecidos, al usar capitalización históricamente disponible, al excluir precios sin liquidez o al contabilizar costes de rotación. Muchos tokens comparten mercado, tecnología, plataforma o tokenomics; no son observaciones independientes. Una prima de microcapitalización no implica facilidad de ejecución para cuentas pequeñas.

### Costes, datos e infraestructura

Universo histórico punto en el tiempo, identificadores estables, listado y baja por venue, oferta circulante tal como era conocida, precios, volumen y liquidez. Datos on-chain deben registrar retrasos de publicación y revisiones. Una clasificación larga/corta exige acceso real a instrumentos cortos; las carteras con solo largos deben evaluarse por separado. Los grupos de pequeña capitalización pueden tener spreads, impacto y riesgo de manipulación elevados. El capital necesario depende de número de posiciones, mínimos de orden y liquidez; no puede fijarse una cifra con la literatura aún sin consultar.

### Condiciones de descarte

No avanzar un factor si solo se puede construir con datos revisados, si la cartera es inviable por costes/restricciones, si su premio depende de activos no negociables o si solo describe retornos simultáneos sin aportar una decisión de inversión. Conservar factores útiles para explicar riesgos aunque no produzcan una estrategia.

## 6. Detección de regímenes

### Fundamento y distinciones

Un modelo de estados latentes puede escribir `r_t | S_t=s ~ F_s` y `P(S_t=s | S_(t-1)=j) = p_js`. El número de estados, las distribuciones y las transiciones son elecciones de modelado, no hechos observados. También se pueden definir estados mediante reglas observables sencillas de tendencia y volatilidad.

Para una decisión en `t` es admisible una probabilidad filtrada `P(S_t | I_t)`; una probabilidad suavizada usando observaciones futuras contiene información que no estaba disponible. Etiquetar retrospectivamente periodos como alcistas o bajistas puede servir para describir resultados, pero no para simular una política ejecutable que conocía esas etiquetas.

### Evidencia y contradicción que debemos buscar

DIR-004 es una semilla metodológica de econometría, no evidencia de ventaja en trading cripto. Faltan estudios primarios específicos y replicaciones con evaluación temporal.

La pregunta favorable es si ajustar exposición mediante estados mejora utilidad o riesgo después de costes frente a reglas observables simples. La contraria es si el modelo identifica tarde las transiciones, cambia de significado al reestimar o añade suficiente rotación para eliminar su utilidad. Clasificar regímenes con precisión retrospectiva no responde a esas preguntas.

### Costes, datos e infraestructura

Precios y variables observables con su timestamp de disponibilidad; si hay datos macro, versiones históricas publicadas. Hay que conservar el estado estimado en cada momento y la versión del modelo. La incertidumbre de clasificación importa: una etiqueta dura puede dar una falsa sensación de certeza. Los cambios de asignación producen turnover y pueden ocurrir durante crisis de liquidez.

Un esquema descriptivo sencillo es viable para investigación minorista. Un sistema adaptativo exige mayor vigilancia y solo se justificaría con valor incremental. Los regímenes sirven primero para preguntar dónde falla una hipótesis, sin convertirse automáticamente en señales.

### Condiciones de descarte

Descartar una ventaja que use estados suavizados con datos futuros, cambie etiquetas o número de estados después de ver resultados, carezca de suficientes transiciones independientes o no supere reglas sencillas bajo la misma información y costes.

## 7. Combinaciones de estrategias y carteras

### Fundamento y distinciones

Para retornos de estrategias `g_t` y pesos `w_t`, la varianza condicional de cartera se aproxima por `w_t' Sigma_t w_t`. La diversificación depende de dependencia conjunta futura, incertidumbre de `Sigma_t`, concentración y colas; correlaciones históricas bajas no garantizan protección en crisis.

Pesos iguales, asignaciones por riesgo y optimización media–varianza son alternativas conceptuales con distintos supuestos. La última es particularmente sensible a estimaciones de retorno y covarianza. Una combinación de señales aumenta el número de decisiones de selección: elegir componentes, pesos, restricciones y ventanas constituye búsqueda adicional. Mezclar muchas estrategias similares no equivale a tener muchas fuentes independientes de evidencia.

### Evidencia y contradicción que debemos buscar

No hay evidencia primaria consultada en esta sesión sobre carteras de estrategias cripto. La relación matemática entre pesos y varianza no demuestra una mejora futura de la rentabilidad ajustada al riesgo.

Buscar estudios que contabilicen componentes fracasados y selección del conjunto, comparen reglas sencillas con optimizadores y evalúen costes y dependencia en crisis. Comprobar si la mejora aparente procede solo de reducir exposición, de netear órdenes opuestas o de asumir nuevas fuentes de riesgo. Un peso elegido retrospectivamente puede ocultar estrategias sin mérito propio.

### Costes, datos e infraestructura

Series sincronizadas de cada componente generadas bajo supuestos compatibles, posiciones, operaciones y un libro agregado de costes/exposición. El neteo puede reducir operaciones, pero debe simularse sobre las posiciones efectivamente ejecutadas: sumar curvas netas calculadas por separado puede contabilizar costes incorrectamente. Instrumentos, colateral y venues distintos añaden restricciones de financiación y riesgo operacional.

Una combinación de pocos componentes transparentes sería técnicamente accesible; el beneficio económico requiere demostración propia. No se fija capital mínimo sin conocer liquidez, tamaños mínimos y reglas de riesgo.

### Condiciones de descarte

Rechazar una combinación cuya mejora dependa de pesos inestables, cuyas pérdidas extremas excedan límites predefinidos o que no añada valor respecto de asignaciones sencillas comparables. Una cartera no convierte automáticamente resultados débiles de muchas estrategias en evidencia fuerte.

## 8. Bibliografía semilla y trazabilidad de acceso

| ID | Referencia semilla y vínculo | Nivel de acceso el 2026-10-13 | Preguntas de extracción pendientes |
|---|---|---|---|
| DIR-001 | Liu, Y.; Tsyvinski, A. *Risks and Returns of Cryptocurrency*. [DOI: 10.1093/rfs/hhaa113](https://doi.org/10.1093/rfs/hhaa113). Versión de trabajo: [NBER w24877](https://www.nber.org/papers/w24877). | **No consultada**. Intento al DOI bloqueado por proxy 403. No contar publicación y working paper como dos estudios. | Confirmar versión, activos, fechas y variables; separar explicación y predicción; extraer definición de momentum, cronología de prueba, costes y resultados contrarios. |
| DIR-002 | Liu, Y.; Tsyvinski, A.; Wu, X. *Common Risk Factors in Cryptocurrency*. [DOI: 10.1111/jofi.13119](https://doi.org/10.1111/jofi.13119). Versión de trabajo: [NBER w25882](https://www.nber.org/papers/w25882). | **No consultada**. Intentos al DOI y NBER bloqueados por proxy 403. | Confirmar factores, universo histórico, disponibilidad de cortos, reglas de formación, retornos netos y pruebas temporales; distinguir factor explicativo de prima capturable. |
| DIR-003 | Moskowitz, T. J.; Ooi, Y. H.; Pedersen, L. H. *Time Series Momentum*. [DOI: 10.1016/j.jfineco.2011.11.003](https://doi.org/10.1016/j.jfineco.2011.11.003). | **No consultada**. Intento al DOI bloqueado por proxy 403. Transferibilidad desde mercados tradicionales pendiente. | Confirmar instrumentos, ajustes de riesgo, formación/prueba, coste, selección de parámetros y vulnerabilidades; no transferir cifras a cripto. |
| DIR-004 | Hamilton, J. D. *A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle*. [DOI: 10.2307/1912559](https://doi.org/10.2307/1912559). | **No consultada; sin intento individual**. Referencia metodológica pendiente, sin evidencia cripto atribuida. | Extraer supuestos, estimación de estados y distinción filtrado/suavizado; identificar después estudios cripto con decisión verdaderamente fuera de muestra. |

No se han usado afirmaciones comerciales como evidencia. No se infieren magnitudes, significación estadística, rentabilidad o robustez a partir de los títulos. Tampoco se afirma cobertura de la literatura hasta octubre de 2026: la fecha identifica esta nota y los intentos de acceso, no una búsqueda actualizada concluida.

## 9. Plan específico de búsqueda y extracción

Consultas iniciales a ampliar cuando exista acceso: `cryptocurrency time series momentum out of sample transaction costs`; `cryptocurrency cross sectional momentum reversal survivorship`; `cryptocurrency mean reversion bid ask bounce`; `cryptocurrency factors delisting liquidity short selling`; `cryptocurrency regime switching filtered out of sample`; `cryptocurrency portfolio strategies transaction costs estimation error`. Buscar activamente términos `replication`, `fails`, `post publication`, `data snooping`, `crash`, `negative results` y `liquidity`, sin excluir artículos por resultados desfavorables.

Priorizar versiones editoriales y repositorios de los autores; rastrear bibliografía y citas posteriores de cada estudio. Registrar cada consulta, fecha, repositorio, filtros y resultado; deduplicar versiones. Una búsqueda por palabras favorables solamente sesgaría la muestra bibliográfica. Las conclusiones de mercados tradicionales se catalogarán por separado de la evidencia cripto. En literatura de carteras, una comparación de optimizadores sin costes o sin prueba temporal no sustituye una evaluación ejecutable.

Para cada artículo: ficha de identidad y versión; pregunta; mecanismo; activos y venues; periodo; disponibilidad histórica de datos; señal y reloj de decisión; referencia; particiones temporales; búsqueda de parámetros; costes y financiación; métricas con incertidumbre; resultados adversos; código y licencia; diferencias entre afirmaciones y tablas; replicaciones y conflictos de interés. Distinguir explícitamente ausencia de reporte, omisión confirmada y dato realmente medido. El resumen puede acreditar una afirmación de los autores, pero no verificar detalles metodológicos ausentes del resumen.

## 10. Lectura provisional para el proyecto

Por transparencia, parsimonia y viabilidad técnica, el momentum temporal spot de baja frecuencia y una regla sencilla de reversión justifican **preguntas de investigación iniciales**, junto con efectivo y buy and hold como referencias futuras. Esto no establece su prioridad definitiva en Fase II ni evidencia de superioridad. Los factores justifican investigación como herramienta para separar primas y riesgos; una cartera negociable requeriría datos históricos e instrumentos adecuados. Los regímenes son inicialmente una herramienta de diagnóstico; su uso para adaptar señales es una hipótesis adicional. La combinación de estrategias solo debe considerarse con costes consistentes, control del número de ensayos y comparación con reglas simples.

La decisión actual es completar y contrastar fuentes, especialmente evidencia contraria y detalles de implementación. Ninguna de estas familias está empíricamente validada para este proyecto. El siguiente paso continúa sujeto a revisión del usuario; no se inicia la Fase II ni se ejecutan experimentos.
