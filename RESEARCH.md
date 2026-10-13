# Investigación científica — Fase I

**Fecha:** 2026-10-13 · **Versión:** 0.1 · **Estado:** preguntas y protocolo documentados; informe teórico preliminar; revisión empírica pendiente de acceso.

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

Se cubren conceptualmente las trece familias solicitadas. El trabajo actual **no constituye una revisión bibliográfica exhaustiva ni una actualización verificada a octubre de 2026**.

- El checkout inicial estaba vacío y no contenía datos, estudios ni resultados propios.
- No hay herramienta de navegación/búsqueda académica disponible en esta sesión. Se intentó consultar directamente fuentes primarias por HTTPS con verificación TLS.
- El proxy rechazó NBER, arXiv, Crossref, DOI y otras fuentes académicas con `CONNECT 403` / `Tunnel connection failed: 403 Forbidden`.
- **Artículos recuperados: 0. Textos completos leídos: 0. Resúmenes leídos: 0. Metadatos bibliográficos recuperados: 0. Experimentos propios: 0.** Un intento bloqueado no cuenta como consulta de contenido.
- Los fundamentos matemáticos siguientes son análisis teórico. Las referencias de los apéndices y de la sección 9 son **semillas bibliográficas pendientes de verificación**, no evidencia empírica evaluada.
- Se guardó un borrador con destinos académicos en la configuración del entorno. No modifica por sí solo el acceso de esta máquina ni acredita publicación. Véase [D-003](DECISIONS.md#d-003--acceso-externo-limitado).

No se infieren resultados positivos ni negativos de la inaccesibilidad de los artículos. «Evidencia no evaluada» es distinto de «evidencia de ausencia de rentabilidad».

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

Combinar cada consulta temática con `transaction costs`, `out-of-sample`, `replication`, `robustness`, `survivorship`, `failure`, `no predictability`, `market efficiency` y equivalentes. Son consultas **planificadas**, aún no ejecutadas en un índice bibliográfico.

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

**Parada de búsqueda:** aplicar el criterio de cobertura del roadmap y dos rondas de referencias/citas sin nueva evidencia material, o declarar acceso/recursos insuficientes. La entrega actual está en esta segunda situación y no cierra la revisión.

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

- **No evaluada:** referencia sin lectura suficiente; es el estado empírico actual de todas las familias.
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

## 6. Mapa crítico inicial de las trece familias

La tabla compara **mecanismos y requisitos teóricos** para orientar la lectura. No sustituye la matriz de selección de Fase II. **Estado empírico de todas las filas: no evaluado**, con fuentes semilla en los apéndices. No se han documentado aún resultados positivos, negativos u OOS de publicaciones consultadas.

| Familia | Fundamento y pregunta central | Datos, costes y dificultad para un particular | Objeción decisiva a investigar |
|---|---|---|---|
| 1. Trend/momentum | Persistencia temporal o transversal de retornos; estudiar por separado ambos mecanismos | OHLCV y universo histórico; frecuencia baja limita turnover pero no elimina slippage; spot long/flat relativamente sencillo | ¿Ventaja neta adicional a beta o solo selección de una tendencia alcista? Reversiones y whipsaw |
| 2. Mean reversion | Desviaciones transitorias de equilibrio o presión de liquidez | Referencia de equilibrio defendible; datos más finos a corto plazo; costes pueden consumir el efecto | Una caída no implica infravaloración ni retorno a una media estable; bid-ask bounce puede aparentar señal |
| 3. Statistical arbitrage | Cartera de residuos/spreads con rentabilidad esperada condicionada, no beneficio seguro | Sincronización y múltiples activos/exchanges; cortos, préstamos y financiación; complejidad media/alta | Neutralidad al mercado estimada puede fallar; dependencia/contraparte en estrés |
| 4. Pares/cointegración | Combinación estacionaria de precios integrados y corrección del desequilibrio | Relaciones estimadas solo con pasado, selección múltiple de pares; borrow y dos patas | Correlación no basta; cointegración inestable, costes y no convergencia |
| 5. Factores cripto | Primas comunes y diferencias transversales de retornos | Universo point-in-time amplio; rotación, deslistados y capacidad de pequeños tokens | ¿Prima de riesgo, sesgo de supervivencia o alpha? Exposición observable no garantiza cartera implementable |
| 6. Volatilidad | Separar previsión de volatilidad, control de exposición y prima de opciones | Retornos para sizing; superficies/opciones/griegas/margen para prima; ejecución más exigente | Predecir riesgo no implica beneficio direccional; primas por vender convexidad pueden ocultar pérdidas extremas |
| 7. Funding/basis | Diferencias spot-derivado y transferencias de financiación | Histórico de funding/basis/índice/marca; colateral, dos patas, fees y margen; capital operativo mayor | Funding futuro incierto; perpetuo sin vencimiento; liquidación, basis y contraparte impiden llamarlo libre de riesgo |
| 8. Microestructura/order flow | Desequilibrio de órdenes y formación de precios | Trades/libro secuenciado, timestamps y latencia; señal breve, datos voluminosos | Predictibilidad al mid puede desaparecer al spread o antes del fill de un particular |
| 9. Market making | Captura de spread frente a inventario y selección adversa | Libro L2/L3, simulación de colas, fills parciales, rebates reales y servicio continuo | Fills optimistas o selección adversa pueden convertir el spread aparente en pérdida |
| 10. ML | Relación condicional entre variables disponibles y retorno/riesgo/decisión | Pipelines temporales, pocas variables justificadas, nested selection y costes comunes | Mejor precisión no implica mejor P&L; multiplicidad y no estacionariedad |
| 11. DL/series temporales | Representaciones no lineales y dependencias secuenciales | Muestras efectivas, cómputo/semillas, splits temporales y benchmark simple equivalente | Tamaño bruto de barras no equivale a observaciones independientes; complejidad puede memorizar regímenes |
| 12. Regímenes | Parámetros/exposiciones dependen de un estado latente | Probabilidades filtradas en tiempo real, no suavizadas con futuro; costes de conmutación | Etiquetar después de los hechos no ofrece una política negociable |
| 13. Carteras/combinaciones | Diversificar mecanismos y estimar pesos bajo incertidumbre | Señales sincronizadas, covarianzas solo con pasado, costes y riesgo agregado | Correlaciones cambian en crisis; optimizar pesos añade grados de libertad y puede concentrar riesgos comunes |

Desarrollo matemático y preguntas de falsación:

- [Direccionales, factores, regímenes y carteras](docs/research/directional.md).
- [Valor relativo, cointegración, volatilidad y funding](docs/research/relative-value.md).
- [Microestructura, market making, ML y deep learning](docs/research/ml-execution.md).

Las familias se solapan: un modelo de ML puede implementar momentum, y un filtro de regímenes puede cambiar la exposición de una cartera. No se contarán como trece mecanismos independientes ni se atribuirá al estimador la prima de su señal subyacente.

## 7. Primer informe crítico y prioridades de lectura

**No hay una estrategia ganadora ni evidencia suficiente para operar en este proyecto.** La falta actual es de evaluación y datos, no una refutación empírica de todas las estrategias.

### Lectura inicial: mecanismos simples y contrastables

Momentum/trend y reversión simple permiten formular reglas comprensibles y contrastarlas con efectivo/exposición pasiva. Merecen una lectura temprana porque es más fácil detectar supuestos, costes y riesgo de selección. Esta prioridad se basa en falsabilidad y esfuerzo, **no en una rentabilidad demostrada**. Reversión necesita especial cautela: el «equilibrio» debe justificarse y el efecto observado puede ser una consecuencia del spread.

Los factores sirven primero para preguntar qué exposición explica una rentabilidad. Una cartera que gana tomando más riesgo de mercado o de tokens ilíquidos puede no aportar una ventaja ajustada al riesgo. La literatura transversal requerirá mayor atención a supervivencia, disponibilidad real y tamaño de las posiciones.

### Lectura condicionada: valor relativo, funding y volatilidad

Funding/basis tiene un flujo contractual interpretable, pero necesita analizar capital, margen y riesgo de contraparte. Un perpetuo no garantiza convergencia en una fecha concreta. La neutralidad delta aproximada no elimina pérdidas ni necesidades de liquidez.

Pares y otros spreads permiten hipótesis estadísticas claras, pero seleccionar muchos pares y ventanas puede fabricar relaciones aparentes. Habrá que investigar estabilidad temporal, rupturas y si las operaciones opuestas estaban disponibles al coste declarado.

En volatilidad deben separarse dos investigaciones: ajustar exposición según el riesgo previsto, y negociar una prima de derivados. La primera puede ser accesible; la segunda exige superficies históricas, margen y escenarios de cola que una serie diaria de precios no proporciona.

### Complejidad que debe ganarse su lugar

Microestructura y market making tienen mecanismos económicos definidos, pero el dato y el simulador de ejecución son parte de la hipótesis. Sin colas, latencia y selección adversa, un backtest no decide su viabilidad. Su prioridad práctica dependerá de recursos del operador, todavía desconocidos.

ML y DL son herramientas de estimación. Deben competir con reglas y modelos simples usando la misma información, particiones, costes y presupuesto de investigación. La precisión predictiva no será un criterio sustitutivo de ventaja neta. El acceso a muchos modelos incrementa la necesidad de controlar selección.

Regímenes y combinaciones merecen preguntas incrementales después de entender los componentes. Un régimen observado retrospectivamente puede explicar un fallo, pero no justificar una regla que necesitaba conocerlo de antemano. Una combinación debe mejorar frente a pesos simples sin esconder una nueva búsqueda extensa.

### Qué haría cambiar este orden

Una replicación verificable con costes minoristas, un dataset point-in-time accesible, evidencia adversa convincente o restricciones concretas de capital/mercado pueden cambiar la prioridad. Los criterios se conservarán; se documentará nueva evidencia. La selección formal pertenece a II y requiere aprobación del usuario.

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

## 9. Referencias metodológicas semilla — no consultadas

Las siguientes referencias se identifican a partir de conocimiento previo para organizar la búsqueda. Sus metadatos, versiones y contenido **no han sido verificados externamente en esta sesión**. No se extraen de ellas resultados empíricos para criptomonedas.

| ID | Referencia semilla y enlace | Motivo para leerla | Acceso actual |
|---|---|---|---|
| MET-01 | White, H. (2000), *A Reality Check for Data Snooping*, Econometrica. [DOI](https://doi.org/10.1111/1468-0262.00152) | Inferencia después de comparar reglas; límites bajo dependencia y universo de modelos | No consultada; sin intento individual |
| MET-02 | Hansen, P. R. (2005), *A Test for Superior Predictive Ability*, Journal of Business & Economic Statistics. [DOI](https://doi.org/10.1198/073500105000000063) | Comparación de procedimientos y sensibilidad al conjunto de competidores | No consultada; sin intento individual |
| MET-03 | Bailey, D. H. y López de Prado, M. (2014), *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality*, The Journal of Portfolio Management. [DOI](https://doi.org/10.3905/jpm.2014.40.5.094) | Supuestos y límites de corregir Sharpe por selección y no normalidad | No consultada; sin intento individual |
| MET-04 | Bailey, D. H., Borwein, J. M., López de Prado, M. y Zhu, Q. J. (2017), *The Probability of Backtest Overfitting*, The Journal of Computational Finance. [DOI](https://doi.org/10.21314/JCF.2016.322) | Diagnóstico de selección retrospectiva y límites para series no estacionarias | No consultada; sin intento individual |
| MET-05 | Harvey, C. R., Liu, Y. y Zhu, H. (2016), *… and the Cross-Section of Expected Returns*, The Review of Financial Studies. [DOI](https://doi.org/10.1093/rfs/hhv059) | Multiplicidad en la búsqueda de factores; transferibilidad de sus criterios | No consultada; sin intento individual |
| MET-06 | Lo, A. W. (2002), *The Statistics of Sharpe Ratios*, Financial Analysts Journal. [DOI](https://doi.org/10.2469/faj.v58.n4.2453) | Incertidumbre y anualización de Sharpe bajo dependencia | No consultada; sin intento individual |

Las referencias temáticas se encuentran en los apéndices con IDs DIR, RV y ML. El prefijo identifica la ficha, no una calificación de evidencia.

## 10. Registro de búsqueda inicial y continuidad

| Fecha | Operación efectivamente intentada | Resultado | Qué permite afirmar |
|---|---|---|---|
| 2026-10-13 | GET `https://www.nber.org/papers/w24877` | Proxy CONNECT 403 | No se recuperó el artículo ni su resumen |
| 2026-10-13 | GET `https://arxiv.org/abs/1607.03082` como comprobación de acceso | Proxy CONNECT 403 | Destino inaccesible; el identificador no se incluye como evidencia temática |
| 2026-10-13 | GET `https://api.crossref.org/works?query.title=Common%20Risk%20Factors%20in%20Cryptocurrency&rows=1` | Proxy CONNECT 403 | No se recuperaron metadatos ni resultados de búsqueda |
| 2026-10-13 | Comprobaciones temáticas adicionales a DOI, BIS, NBER y editoriales | Bloqueadas por proxy; detalle en apéndices | Ningún contenido académico recuperado |

**Siguiente paso aprobado por el usuario el 2026-10-13:** completar la lectura crítica dentro de Fase I conforme al marco inicial. Falta habilitar las fuentes en los ajustes del entorno y comprobar el acceso. Después se actualizarán las fichas con evidencia favorable/adversa y se verificará la aceptación de I. Solo con aprobación posterior se iniciará la comparación y selección de II. No hay ensayos ni acciones de trading pendientes de ejecutarse automáticamente.
