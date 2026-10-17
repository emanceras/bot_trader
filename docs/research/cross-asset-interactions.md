# Relaciones entre criptomonedas e interacciones entre variables

**Apertura:** 2026-10-17. **Consolidación:** 2026-10-17. **Estado:** cuatro lecturas dirigidas y síntesis integradas; acceso parcial y límites explícitos, sin saturación. Ampliación acotada de Fase I, integrada en arbitraje estadístico/pares, factores, ML/DL, regímenes y carteras. **No se crea otra familia**, no se seleccionan candidatos y no se ejecutan estrategias, entrenamientos o experimentos. La propuesta del usuario no confiere prioridad ni presunción de rentabilidad.

## Dos preguntas que deben evaluarse por separado

**A. Predicción entre activos:** ¿el pasado disponible de una criptomoneda u otro mercado añade capacidad de predecir el retorno/riesgo futuro de otra, por encima del pasado propio y de factores comunes, y queda valor económico después de recepción, ejecución y costes?

**B. Interacción entre variables:** ¿conocer conjuntamente variables cambia la predicción/decisión de una forma que no puede explicar un modelo aditivo con esas mismas variables? Una variable débil por sí sola puede ser útil como contexto de otra; eso es una posibilidad matemática, no evidencia de que exista en cripto ni de que supere costes.

Combinar variables, combinar pronósticos y mezclar P&L de estrategias son operaciones distintas. Un modelo multivariable no demuestra interacciones; un ensemble puede mejorar por reducción de error de estimación o diversificación sin interacción predictiva. Una cartera de reglas perdedoras tampoco obtiene automáticamente una media positiva por reducir su varianza.

## Alcance y parada definidos antes de la lectura adicional

1. Reutilizar el corpus existente, sin sumar relecturas/versiones: DIR-002, EX-01, RV-E02/03, ML-06/09/11, RP-06, PORT-01–04 y SENT01/02 son antecedentes, no nuevos estudios.
2. Tres bloques paralelos: lead-lag/ejecución; factores comunes/contexto; interacciones/modelos. **Máximo dos trabajos nuevos con lectura dirigida por bloque, seis en total**. Promover una referencia parcial a texto se identifica como tal; no se duplica el estudio.
3. Cada bloque tiene un máximo de seis consultas bibliográficas, hasta ocho resultados por consulta, y doce intentos de recuperación de originales/versiones autorizadas. Buscar resultados contrarios desde el inicio. No es necesario agotar esos máximos. Métodos y tablas prevalecen sobre cantidad de enlaces o mayor rentabilidad reportada.
4. Concluir al completar la tanda o agotar acceso/recursos, conservando lagunas. No ampliar la búsqueda para conseguir confirmación ni afirmar saturación. El cierre de esta ampliación será documental; Fase I y cualquier fase posterior requieren las aceptaciones del roadmap.

Los registros distinguirán consulta, descarga, cribado y lectura efectiva, con versión, URL, hash, páginas y límites. Solo se recupera literatura/documentación pública; no datos para backtesting ni código ejecutable de autores.

## Escala de inferencia: no saltar pasos

| Concepto | Qué permite afirmar | Qué no establece |
|---|---|---|
| Correlación contemporánea/retardada | Asociación bajo muestreo, variables y periodo determinados | Dirección causal ni precio operable posterior |
| Precedencia temporal | Una medición cambia antes que otra según esos relojes | Información nueva: puede haber target obsoleto, reloj desalineado o shock común |
| Granger condicional | Retardos aportan a la predicción respecto al conjunto de controles especificado | Causalidad estructural, estabilidad OOS o beneficio tras costes |
| Dependencia no lineal/transferencia de información | Relación distributiva que un resumen lineal puede omitir | Que la relación sea estimable con suficiente precisión, explotable o causal |
| Cointegración | Una combinación de niveles integrados puede ser estacionaria bajo un modelo | Que exista líder direccional, convergencia dentro del margen disponible o spread rentable |
| Spillover/conectividad | Descomposición de variación o errores de pronóstico dentro del modelo | Shock causal identificado, información incremental de trading o plazo aprovechable |
| Mejora predictiva OOS | Menor pérdida de pronóstico en datos posteriores bajo ese protocolo | Ganancia económica: importa qué decisiones cambian, cuánto cuestan y qué riesgo asumen |
| Beneficio neto ejecutable | Resultado condicionado a datos, órdenes, capital y fricciones reconciliados | Persistencia futura o autorización para operar |

Un VAR puede tener buen pronóstico de volatilidad y escaso pronóstico de media. Una matriz de correlación dinámica no valida una señal direccional. Se separarán estos objetivos al extraer resultados.

## Formalización de las preguntas y controles

Para predecir `y_(i,t+h)` (retorno o riesgo, elegido previamente), el conjunto restringido `F_t` contiene pasado propio, factores y controles realmente disponibles al decidir. La pregunta A compara:

`E[y_(i,t+h) | F_t, X_(otros,≤t)]` frente a `E[y_(i,t+h) | F_t]`.

La nula de Granger en media es igualdad de ambas esperanzas bajo la especificación; otras pruebas pueden referirse a la distribución completa. Rechazarla en muestra no asegura mejora OOS ni rentabilidad. La nula económica es distinta: el incremento neto no supera el mínimo relevante fijado antes de experimentar. Ese mínimo y el método de inferencia **aún no están definidos**.

Para B, el modelo aditivo `a + Σ f_k(x_k)` se compara con un modelo que permite términos conjuntos, por ejemplo `a + Σ f_k(x_k) + Σ g_kl(x_k,x_l)`. Comparar solo una regresión lineal con una red no aísla interacción: pueden cambiar simultáneamente no linealidad univariable, regularización, información y búsqueda. Un GAM o términos principales no lineales ofrecen un control conceptual adicional, sin seleccionar ahora un estimador.

Como contraejemplo lógico, si dos variables binarias independientes y equiprobables determinan una etiqueta mediante XOR, ninguna por sí sola predice la etiqueta y su pareja sí. **Es una propiedad matemática ilustrativa, sin datos ni simulación ejecutada**, no argumento de rentabilidad cripto. En mercados, el efecto conjunto puede ser pequeño, inestable, colineal o imposible de aprender con el tamaño efectivo disponible.

Para una mezcla estática con pesos no negativos que suman uno de retornos de estrategias comparables, bajo costes aditivos, `E[Σ w_k R_k] = Σ w_k E[R_k]`. Si todas las medias verdaderas son negativas, la mezcla no genera media positiva por simple diversificación. Pesos adaptativos, cambios de capital/costes por neteo, payoff no lineal o un objetivo geométrico/utilidad diferente cambian el problema y necesitan demostración propia. La diversificación puede reducir pérdidas/riesgo o modificar crecimiento geométrico sin crear alpha. No confundir retorno bruto de componentes, coste de asignación y costes internos de su implementación conjunta.

## Factores comunes y relación residual

Los controles deben cubrir pasado propio y, cuando corresponda, BTC/ETH, mercado cripto, liquidez, volumen, volatilidad y condiciones macro conocidas. Debe distinguirse explicación ex post de retornos mediante factores realizados de una predicción usando factores observables antes de la orden. El factor futuro puede ser una etiqueta o control explicativo, **no una entrada disponible en el pasado**.

Un índice que contiene fuertemente al activo objetivo o al supuesto líder puede crear correlación mecánica. Considerar índices excluyendo el objetivo —y análisis excluyendo ambos activos de la pareja—, pesos históricos y estimación solo en desarrollo. PCA y normalización con toda la muestra incorporan futuro. Un numerario común BTC/USDT puede introducir exposición compartida o riesgo de depeg; comparar series en la misma unidad no elimina ese riesgo.

Que una relación desaparezca tras añadir controles reduce el respaldo a información **incremental bajo esos controles**; no demuestra que el canal económico nunca exista. Un control puede absorber un mecanismo mediador real o ser medido con error. La causalidad económica exige supuestos de identificación adicionales; no se decidirá por una red de flechas de Granger.

## Sincronización, ejecución y universo

- Distinguir mismo activo entre exchanges, activos diferentes dentro de un exchange y activos diferentes entre exchanges. El descubrimiento de precio de BTC entre venues no demuestra que BTC anticipe altcoins.
- Registrar reloj del exchange y recepción, secuencia, cierre/inicio de barra, agregación, zona horaria y disponibilidad de cada campo. Una barra termina después de empezar; su volumen final no puede usarse al abrirla. Funding anunciado/estimado y funding liquidado son variables diferentes.
- Cotizaciones/trades obsoletos, bid-ask bounce, diferencias de frecuencia y precios arrastrados pueden aparentar liderazgo. No interpolar con observaciones futuras. Comparar sincronizaciones causales y sensibilidad a muestreo/frescura; reconocer que sincronizar mejor puede cambiar el mecanismo detectado.
- Todo predictor debe existir antes de decidir; la orden/fill ocurre después de recepción, procesamiento y red. Un retardo de una barra no es el mismo tiempo físico en todas las frecuencias. Predicción del mid no significa beneficio comprando ask y vendiendo bid.
- Definir posteriormente un universo **dinámico y point-in-time**, sin imponer ahora un número de monedas: disponibilidad histórica de instrumentos en venues accesibles, liquidez/profundidad/spread observados antes, antigüedad suficiente para la ventana y acceso a cortos cuando sean necesarios. Los umbrales se justificarán por estimación y capacidad del operador, sin elegirlos mirando beneficios.
- Conservar entradas, bajas, suspensiones, cambios de ticker/contrato y retornos terminales; no exigir supervivencia durante todo el test ni mantener precios planos ficticios para evitar pérdidas. Registrar monedas elegibles sin historial suficiente y la consecuencia de excluirlas.
- Distinguir stablecoins, activos envueltos, tokens apalancados y duplicados económicos según la pregunta. Estratificar por liquidez/edad/tamaño/función cuando esté justificado; no elegir solo grandes supervivientes ni atribuir representatividad por abarcar muchos símbolos.
- Universo de investigación y universo operable pueden diferir. Documentar ambas coberturas y cómo cambian resultados; no trasladar beneficios de tokens ilíquidos a una cuenta particular.

## Propuesta de evaluación para futuras fases — no ejecutada

| Pregunta | Comparaciones necesarias | Ablación/contraste que evita atribuciones indebidas |
|---|---|---|
| A: información entre monedas | Pasado propio → propio+factores → propio+factores+otros activos | Retirar grupos de activos/variables; mercado excluyendo objetivo; mismo activo entre venues por separado; mantener periodo común de evaluación |
| B: información conjunta | Variables individuales, aditivo lineal, aditivo no lineal y términos de interacción | Conservar variables y presupuesto; comparar incremento sobre modelo aditivo, no solo sobre variable débil |
| Modelos complejos | AR/VAR o regularizados y controles simples frente a árboles/boosting/redes | Igual información permitida, horizonte, restricciones y presupuesto de selección; intervalos/semillas donde proceda |
| Contexto | Modelo fijo frente a interacción con liquidez/volatilidad o régimen inferido con pasado | Estado filtrado, no suavizado con futuro; estimación en desarrollo; no escoger crisis/activos tras ver resultado |
| Información frente a cartera | Mejor pronóstico → misma regla de decisión → costes/riesgo comunes | Separar error predictivo, exposure timing y beneficio neto; añadir coste de cada pata y neteo realista |
| Noticias con mercado | Modelos anteriores con y sin información textual causalmente disponible | Precio/calendario/texto, disponibilidad y conocimiento del LLM según la ampliación de noticias existente |

Las comparaciones son anidadas conceptualmente, no una autorización de explorar todas sus combinaciones. Antes de V se fijarán hipótesis primarias, variantes máximas, presupuesto y correcciones; parejas dirigidas crecen como `N(N−1)` antes de añadir retardos, ventanas y modelos. Elegir la mejor pareja dentro de toda la muestra y luego llamar OOS a su backtest invalida la selección.

Walk-forward debe repetir **dentro del entrenamiento** selección del universo/modelo/grafo, factores, lags y transformaciones. Separar validación de holdout final; bloquear fechas compartidas entre activos para que entrenar con otra moneda en el mismo futuro no eluda el corte temporal. Controlar solapamiento de etiquetas con purga/embargo cuando corresponda. Bloques temporales compartidos preservan dependencia transversal en inferencia; millones de filas activo×tiempo no equivalen a millones de shocks independientes.

Ablaciones fuera de muestra deben tener su propia selección interna. Permutar columnas indiscriminadamente rompe dependencia y puede fabricar inputs imposibles; controles temporales/grupales o condicionales deben justificarse. SHAP/importancia, una arista estimada o atención de una red no prueban contribución causal ni ganancia incremental OOS. Se fijarán pérdida predictiva, efecto económico, incertidumbre y costes antes de observar resultados; no se aplicarán tests sucesivos hasta obtener uno favorable.

La viabilidad requerirá fees alcanzables, spread, slippage/impacto, fills/capacidad, préstamos/funding/margen, rebalanceo y distribución de demora. Informar resultado por horizonte/venue/régimen sin convertir cada corte ex post en una nueva estrategia. El efecto que desaparece con una demora razonable puede ser información estadística interesante y una línea operativa descartable.

## Evidencia integrada y juicio

La tanda incorpora **cuatro trabajos con lectura dirigida**, dentro del máximo de seis: tres empíricos descriptivos de criptomonedas y un estudio metodológico/empírico en acciones. No son cuatro estrategias netas ni cuatro pruebas independientes de una misma hipótesis. Se mantienen las referencias anteriores y sus conclusiones.

| Fuente y nivel | Qué respalda el texto examinado | Contraste adverso y límite decisivo |
|---|---|---|
| [CX-01: Anderson 2023](evidence-cross-leadlag.md), artículo editorial | Lead-lag estimado BTC–ADA en trades HitBTC de 2019–2021; duraciones mensuales 16–118 segundos | Duración variable y decreciente; selección de retardo por significación. No controles completos de mercado, OOS predictivo, precios ejecutables ni costes. El promedio 56,5 s no es una ventana garantizada para operar |
| [CX-02: Schnoering–Inzirillo, arXiv v2 2022](evidence-cross-leadlag.md), preprint | Información mutua retardada entre 69 activos Binance; Bonferroni por matriz; representación multiescala | Enlaces típicos caen rápidamente con lag y abundan ceros; concentración en fuertes caídas. Grafos bivariantes sin factores, simetrizados; autoencoder reconstruye grafos, no pronostica retornos OOS. No cartera ni costes |
| [CF-01: Drożdż et al. 2020](evidence-cross-factors.md), artículo editorial | Dependencia/redes de 128 series X/BTC cambia con escala, amplitud y contexto | Escala temporal no es lead-lag; cotizar en BTC no equivale a neutralizar su factor. Ventanas solapadas y eventos únicos; sin predicción OOS o P&L. No demuestra desaparición de una señal tras controles completos |
| [IX-01: Gu–Kelly–Xiu, WP revisado 2019](evidence-variable-interactions.md), acciones estadounidenses | Comparación recursiva de modelos lineales, splines, árboles y redes; algunas mejoras puntuales predictivas/económicas brutas | Los inputs lineales ya incluyen productos macro×característica. Muchas diferencias pierden significación con corrección; redes no dominan árboles de forma significativa; mayor profundidad no siempre mejora. Turnover alto y costes completos ausentes; no transferencia cripto demostrada |

**Antecedentes reutilizados, sin contarlos de nuevo.** [DIR-002](evidence-directional.md) respalda controlar exposición común y advierte de primas que pierden significación al sustituir cortos, pero no prueba desaparición de un lead-lag concreto tras residualizarlo. [RV-E02/03](evidence-relative-value.md) muestran resultados heterogéneos de pares y erosión por costes; cointegración no basta. [EX-01](evidence-execution.md) aporta límites de fees/latencia para el mismo BTC entre venues, sin convertirse en una prueba crosscoin. [ML-06/09/11](evidence-ml.md) contienen evaluaciones multivariables y carteras con resultados favorables/adversos; usar múltiples inputs o combinar pronósticos no identifica por sí solo una interacción marginalmente débil. [PORT-04](portfolio-followup.md) encuentra fallos de estimación de medias con DL frente a 1/N y mejoras de mínimo riesgo bajo supuestos: asignación de riesgo y predicción de retorno son problemas distintos. [SENT01/02](evidence-news-sentiment.md) recuerdan retroalimentación, sensibilidad a contraste y costes; no se alteran sus conclusiones.

**Respuesta A.** Existe evidencia publicada de dependencia y precedencia entre ciertas criptomonedas, con contexto y muestreo determinantes. Esta tanda **no establece una señal cruzada incremental, estable OOS y negociable después de todas las fricciones**. Tampoco permite negar universalmente que pueda existir. Justifica conservar un contraste condicional y sencillo dentro de arbitraje estadístico/factores/ML; no concede prioridad sobre momentum simple, exposición o las demás hipótesis. La lectura de redes no obliga a construir un sistema de grafos.

**Respuesta B.** Es posible que una variable útil solo en determinados estados tenga escasa señal marginal. IX-01 y los antecedentes permiten formular ese contraste, pero **no hemos demostrado en cripto que variables individualmente no rentables produzcan juntas una ventaja neta robusta**. Un efecto puede venir de regularización, más información, distinta exposición o neteo de costes, sin interacción predictiva. La evidencia debe separar estas explicaciones. Añadir variables también empeora estimación: OLS completo de IX-01 tiene R² OOS negativo y sus redes más profundas no mejoran monótonamente. Promediar predicciones aumenta algunas métricas sin dominar todas las carteras.

**Lagunas deliberadamente conservadas.** Los originales sobre correlación parcial de Shen et al. y predicción cripto de Filippou et al. solo fueron accesibles como resumen/metadatos; Stosic et al. quedó en metadatos. No acreditan los controles/resultados que interesa buscar. No se documentó una prueba completa de desaparición de un lead-lag específico al introducir BTC/ETH/mercado/liquidez, ni una ablación cripto limpia de individual→aditivo→interacción con costes. Funding/volumen/liquidez son variables candidatas justificables por mecanismos y antecedentes, pero esta tanda no valida interacciones rentables entre ellas. Las lagunas no se convierten en hallazgos negativos.

## Disposición crítica y condiciones de cierre

| Línea dentro de las familias existentes | Disposición en Fase I | Qué justificaría reconsiderarla o retirarla después |
|---|---|---|
| Predicción cruzada condicional sencilla | Mantener como pregunta falsable, sin preferencia ni candidato seleccionado | Exigir incremento sobre pasado propio/factores, datos disponibles y costes alcanzables; posponer si falta sincronización o universo histórico |
| Lead-lag rápido como estrategia operativa | **Posponer** su diseño operativo; el desfase significativo no basta | Retirar una variante si se extingue antes de un fill razonable, depende de precios obsoletos o el coste absorbe el efecto |
| Redes profundas de dependencia | **Posponer** complejidad; representación descriptiva no justifica inversión de ingeniería | Solo reconsiderar con comparación predictiva incremental frente a referencias simples y presupuesto equivalente |
| Interacciones entre variables | Mantener contraste limitado dentro de H-11/H-12/H-14, con nula explícita | Descartar variantes sin mejora OOS sobre un aditivo comparable, sensibles a búsqueda o que amplifiquen pérdidas/costes |
| Mezcla automática de reglas con media neta negativa | **Descartar como premisa justificativa** | Neteo, pesos adaptativos o distinto objetivo requieren hipótesis y contabilidad nuevas; no basta alegar diversificación |

La alternativa metodológica más relevante antes de aumentar complejidad es **comprobar sincronización y exposición común con referencias simples**. Puede explicar por qué parece existir una señal y reducir falsos descubrimientos; no es una nueva familia ni una promesa de rentabilidad. Su implementación pertenece al laboratorio/protocolo autorizados posteriormente.

**Cierre de la ampliación:** se documentan las dos preguntas, fuentes favorables/adversas, niveles de inferencia, hipótesis nulas, criterios de universo y evaluación futura con ablaciones. La entrega queda acotada a lo leído y a sus límites de acceso/recursos; no se continuó hasta encontrar un ganador ni se afirma saturación. Corpus total: **49 + 4 = 53** trabajos con lectura dirigida. Las fuentes de metadatos/resumen, relecturas y versiones no se suman. Fase I sigue abierta para revisión del usuario; no se inicia II ni se ejecuta experimento alguno.
