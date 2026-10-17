# Auditoría crítica de cobertura científica

**Fecha:** 2026-10-17. **Alcance:** Fase I, después de integrar relaciones entre criptomonedas e interacciones. Auditoría documental interna con revisiones paralelas y criterio independiente de las prioridades previas; no certificación externa ni réplica de los artículos. Ninguna fase posterior queda autorizada.

## Dictamen para revisión

**Recomiendo cerrar la investigación bibliográfica general de Fase I con sus limitaciones expresamente aceptadas.** El corpus es suficiente para una futura comparación razonada de hipótesis, aunque no para afirmar una ventaja operable, seleccionar una estrategia ganadora o iniciar experimentos. No identifico una laguna que obligue a abrir ahora otra familia o una nueva ronda general de literatura.

Sí existen carencias materiales: datos realmente disponibles en cada momento, universo histórico, atribución incremental de señales y contabilidad de ejecución/capital. Pueden impedir evaluar determinados candidatos y deben actuar como condiciones de admisión posteriores. No se resuelven por acumular artículos. Las carencias específicas de on-chain, posicionamiento, liquidaciones y eventos de oferta se detallan abajo; no se consideran oportunidades demostradas ni inexistentes.

**Estado real:** recomendación documentada, aceptación del usuario pendiente. La Fase I no se marca terminada y la Fase II no se inicia. Cerrar una revisión limitada tampoco supone saturación bibliográfica, validación científica de una estrategia ni renuncia a incorporar después una fuente decisiva para una pregunta concreta.

## Alcance, independencia y criterio de materialidad

Se revisaron los seis documentos principales, los 27 Markdown de investigación existentes al iniciar la auditoría y las fichas de los **53 trabajos distintos**. Se contrastaron mecanismo, hipótesis, resultados favorables/adversos, OOS, costes, procedencia y limitaciones. Los 20 registros JSONL se revisaron mediante muestreo y búsqueda de eventos de lectura; la comprobación sintáctica final se hace sobre todos sus registros. No se releyeron íntegramente los 53 originales, no se reabrieron todos sus enlaces externos ni se auditaron sus códigos/datasets. Los cotejos anteriores de PDF conservan su alcance y fecha; no pasan a ser nuevas verificaciones de esta auditoría.

Dos revisiones documentales repartieron los 53 trabajos y otras dos examinaron la materialidad de on-chain y derivados/eventos. Comparten corpus y entorno: esa revisión cruzada reduce errores de integración, pero no equivale a cuatro equipos científicos externos ni elimina sesgos compartidos. La recomendación se apoya en los límites y decisiones que permite el corpus, no en el acuerdo entre revisores.

Antes del contraste adicional se limitó cada bloque de lagunas a **tres consultas bibliográficas de hasta cinco resultados y cuatro recuperaciones de documentación pública**, solo cuando pudieran cambiar una decisión. Son máximos, no objetivos de cantidad. No se descargan series de mercado. Se conservan accesos parciales y fallos; no se busca hasta hallar resultados favorables. Las comprobaciones adicionales y su nivel de acceso se documentan en la [ficha de fuentes de esta auditoría](evidence-coverage-audit.md) y su [registro](search-coverage-audit.jsonl): tres consultas intentadas y seis páginas oficiales recuperadas, de las que solo tres aportaron contenido objetivo. Cero originales académicos nuevos.

Una laguna es **material** si puede cambiar al menos una de estas decisiones: elegibilidad de una hipótesis, validez temporal de la prueba, signo/magnitud del resultado neto, riesgo/capital necesario o viabilidad de conseguir datos. La novedad del indicador, un Sharpe publicado alto o la petición de estudiar un tema no bastan. Se distingue entre:

- Una omisión de mecanismo que impediría una comparación justa: requeriría subsanación bibliográfica acotada antes de cerrar.
- Una condición específica de datos/ejecución: impide admitir o experimentar con ese candidato hasta resolverla, sin mantener abierta toda I.
- Una incertidumbre empírica: corresponde a contraste posterior autorizado, o a posposición si no es identificable con los recursos disponibles.

## Cobertura de mecanismos y evidencia contradictoria

Las trece familias no son trece fuentes independientes de beneficio. ML/DL son estimadores; regímenes son estados/políticas; diversificación puede mejorar riesgo sin crear alpha. Noticias y on-chain son fuentes de información. La cobertura debe juzgarse por el mecanismo y las fricciones que lo hacen accesible.

| Mecanismo y familias relacionadas | Respaldo favorable del corpus | Evidencia adversa o limitación material | Juicio de cobertura para I |
|---|---|---|---|
| Incorporación gradual de información, atención y persistencia de flujos; momentum, noticias | DIR-001: predictibilidad; DIR-006: algunas altcoins positivas OOS; SENT01: simulación social favorable | DIR-006: BTC negativo en test; CTR-01/DIR-010: significación débil y colas; SENT01: costes eliminan beneficio. El mecanismo causal de persistencia no está identificado | Suficiente para formular y comparar; no demuestra persistencia actual |
| Presión transitoria y provisión de liquidez; reversión, order flow, market making | REV-02/03: reversión/proxy de liquidez; EX-01: ensayo maker positivo tras rebates | La reversión se concentra en iliquidez; cortos y fills incompletos. EX-01 taker ordinario negativo y maker dependiente de rebates. Relación contemporánea OFI/precio no prueba pronóstico | Suficiente para reconocer mecanismo y barreras; reversión temporal a una media tiene menos evidencia directa que la transversal |
| Primas por riesgo sistemático, liquidez y colas; factores y volatilidad | DIR-002: factores explicativos; OPT-01: caso con P&L positivo después de sus fees/spreads; OPT-02/03: precios del riesgo | Sustituir cortos cambia significación; costes de cobertura/margen incompletos; resultados sensibles al estimador. Varianza implícita menos realizada no es P&L | Suficiente para separar prima de alpha; no acredita compensación aceptable para el operador |
| Segmentación y restricciones de capital; arbitraje, basis y funding | RV-E01 y FUND-01/02 describen flujos contractuales y carry | Funding puede cambiar de signo; un perpetuo no obliga a converger en una fecha; ampliación de basis, financiación, garantías y quiebra. Captura breve de funding puede no cubrir fees | Mecanismo económico identificable; rendimiento neto y financiación deben demostrarse |
| Ajuste relativo y transmisión entre activos; pares, statarb, H-23 | RV-E02/03: variantes favorables; CX-01/02: precedencia/dependencias | Cointegración no garantiza convergencia negociable; costes, selección de pares y factores compartidos. CF-01 describe contexto, no neutraliza BTC por usarlo como numerario | Suficiente para pregunta condicional; débil como prueba de una relación económica estable |
| Revisión de expectativas y presión de eventos; macro, regulación, noticias de activo | MAC-01/02 y EVT-01/02: respuestas por evento; LLM-01: algunas ablaciones favorables | Coeficientes nulos/cambiantes, movimiento previo, selección de eventos y falta de recepción/fills. Calendario público no equivale a sorpresa | Suficiente en mecanismos; evidencia específica de eventos de oferta de tokens limitada |
| Asignación de riesgo y diversificación; sizing, regímenes, carteras | RP-01: evidencia tradicional de sizing; PORT-03/04: mejoras condicionadas | PORT-01: diferencias pequeñas frente a 1/N; PORT-02: ranking cambia con liquidez; RP-07/08 y PORT-04: complejidad no domina | Suficiente para referencias simples; utilidad/riesgo deben distinguirse de alpha |
| Estimación condicional e interacciones; ML/DL, H-24 | ML-06/09/11 y IX-01: resultados favorables bajo sus diseños | Costes revierten varios resultados; supuestos de ejecución fuertes; IX-01 es acciones y ya incorpora productos en inputs lineales. LLM-02 solo clasifica texto | Cobertura de métodos suficiente; no son un mecanismo económico ni prueba de interacción rentable cripto |

Fuentes, versiones y ubicaciones: [direccionales](evidence-directional.md), [contraste](gap-contrasts.md), [reversión](gap-reversal.md), [valor relativo](evidence-relative-value.md), [funding](gap-funding.md), [opciones](gap-options.md), [ejecución](evidence-execution.md), [riesgo](evidence-risk-portfolio.md), [carteras](gap-portfolios.md), [PORT-04](portfolio-followup.md), [ML](evidence-ml.md), [noticias](news-events.md) y [relaciones/interacciones](cross-asset-interactions.md). Las cifras publicadas y discrepancias permanecen en esas fichas; no se homogeneizan rendimientos de distinto numerario, riesgo, capital o coste.

**Fundamento verificable no significa ventaja verificada.** Los pagos contractuales, balance de inventario, restricciones de financiación y exposición a convexidad permiten explicar de dónde procede el P&L y quién soporta riesgo. El mecanismo de atención, persistencia o presión de venta es plausible, pero requiere identificación y evidencia adicional. Cointegración, Granger, importancia de variables, grafos o estados ajustados describen relaciones bajo un modelo; no identifican por sí solos quién pagaría un beneficio persistente. No es necesario demostrar causalidad estructural de toda señal para medir valor predictivo, pero tampoco se debe atribuir causalidad a ese valor.

## Lagunas materiales: alcance y decisión recomendada

| Área | Cobertura real e integración existente | Carencia que puede cambiar una decisión | Disposición para esta auditoría |
|---|---|---|---|
| Actividad on-chain, flujos y cohortes | ML-06 incluye variables de red; LLM-01 combina on-chain/precio/texto. Encaja en factores, ML, regímenes y eventos; H-03/11/13/20/24 | Semántica y disponibilidad: direcciones no son usuarios; transferencias no son compras/ventas; etiquetas y agregación de entidades pueden revisarse. Falta atribución incremental limpia neta OOS | **No abrir una familia ni otra ronda general.** Posponer afirmaciones de alpha on-chain. Para admitir una hipótesis concreta: versiones/recepción/confirmación y comparación precio+volumen frente a añadir la variable |
| Posicionamiento en derivados: OI, ratios, basis y opciones | RV-E01 usa OI, posiciones y liquidaciones; FUND/OPT cubren carry y riesgo. H-07/08/09/13/24 | OI mide contratos abiertos, no una dirección neta: cada contrato tiene contrapartes. Ratios de cuentas no equivalen a nominal; coberturas cruzadas y unidades alteran interpretación. Faltan timestamps, cobertura y prueba incremental | **Conservar como posible variable dentro de líneas existentes**, sin prioridad. Su mecanismo no exige ahora más literatura; elegibilidad dependerá de especificación y datos históricos |
| Liquidaciones y flujos forzados | Riesgo de margen en RV-E01/FUND-02; presión/ejecución en EX; H-02/08/09/19/23 | El feed puede ser parcial o representar órdenes y no ejecuciones; información llega durante/después del movimiento. Un mapa de liquidaciones estimadas no es el libro de cuentas reales | **Posponer la estrategia reactiva rápida.** Exigir alcance/censura y latencia del feed antes de considerarla; modelar liquidación propia será obligatorio para cualquier candidato con margen |
| Unlocks, vesting, emisiones/burns, listings/bajas, migraciones, hacks y upgrades | Eventos H-17/19/20/21, universo/cambios de contrato y factores H-03/04/24 | No hay en el corpus una prueba específica neta y reproducible de estos eventos. Fecha prevista ≠ anuncio ≠ ejecución ≠ recepción; oferta desbloqueada ≠ venta. Calendarios reconstruidos y selección de supervivientes pueden introducir futuro | **Separar integridad de datos de alpha.** Historial de bajas/migraciones/cambios de unidades es necesario para el universo; una estrategia de evento requiere una pregunta acotada, calendario versionado y evidencia propia posterior. No abrir ahora una búsqueda general de eventos |

Las señales solicitadas no reciben trato preferente. On-chain tiene antecedentes favorables y adversos multivariables, pero no una atribución aislada concluyente. Posicionamiento y liquidaciones están más cubiertos como explicación/riesgo que como señal ejecutable. Para eventos específicos de oferta no se verificó aquí una muestra suficiente con rentabilidad neta OOS; **no se inventa un estudio negativo para cubrir esa ausencia**. La falta de demostración es incertidumbre, no prueba de inexistencia ni motivo para investigar hasta encontrar beneficios.

**Contraste acotado de datos:** AUD-D01 documenta por qué direcciones activas no son usuarios y pueden incluir movimientos no económicos; AUD-D02 diferencia observación y finalidad; AUD-D03 limita el histórico de OI de un endpoint al último mes y documenta huecos. Son hechos de documentación, sin prueba de un feed. Las rutas intentadas de Glassnode y liquidaciones no dieron el contenido objetivo: revisiones de etiquetas y censura del feed siguen siendo requisitos por verificar, no características certificadas de esos proveedores. Dos resúmenes académicos de dilución/unlocks quedaron como fuentes parciales, sin cifras aceptadas ni nuevos estudios completos en el corpus.

### Condiciones de datos que una etiqueta temática no resuelve

- **On-chain:** distinguir hora del bloque, observación por nodo/proveedor, confirmación/finalidad y cálculo/publicación de la métrica. Registrar reorganizaciones, revisiones de etiquetas, metodología y cadena; actividad de contratos, batching, cambios internos de custodia y transferencias entre redes pueden alterar un indicador sin cambiar demanda inversora. Una métrica reconstruible hoy puede no ser la disponible entonces. Las características se exigen solo cuando sean pertinentes a la cadena/variable seleccionada.
- **Derivados:** separar instrumentos lineales/inversos, nominal en contratos/monedas/USD, marca/índice/último precio, funding estimado/anunciado/liquidado, OI y volumen. La subida del OI en USD puede deberse al precio. La publicación de una posición agregada tiene retraso y población propia; no atribuirla a todo el mercado. Dos posiciones opuestas pueden ser una cobertura, no desacuerdo direccional.
- **Liquidaciones:** conocer qué cuenta el proveedor, muestreo, deduplicación, cortes y cambios de cobertura. Ningún volumen reconstruido debe darse por censo completo sin comprobarlo. El impacto observado puede preceder a recepción y el precio de marca que activa margen puede diferir del negociado. Continuación y reversión requieren preguntas distintas.
- **Eventos de token:** conservar calendario tal como se conocía, correcciones, denominador de oferta, beneficiarios si se conocen, moneda/unidades, transacción efectiva y primera comunicación. Una liberación prevista puede estar descontada; capacidad de vender depende de custodia, préstamos y liquidez. Bajas o hacks no deben desaparecer del universo por falta de cotizaciones posteriores. No atribuir rentabilidad a participar en ventas/airdrops sin incluir elegibilidad y capital/costes reales.

### Límites de alcance que no justifican expansión automática

El corpus se concentra en CEX, spot y derivados; no cubre suficientemente ejecución DEX/AMM, MEV, staking o préstamo DeFi. Sus mecanismos se relacionan con liquidez, segmentación, servicios y riesgo de capital, pero **sus reglas específicas no quedan validadas por analogía** con un libro centralizado. Recompensas en tokens, fees de protocolo o una tasa anunciada no prueban rendimiento neto en la moneda de cuenta.

Recomiendo dejarlos **pospuestos en esta entrega**, sin afirmar inviabilidad universal. Solo sería material reabrir un bloque acotado si el alcance autorizado del operador y un candidato concreto requieren esas reglas, acceso y riesgos. No se propone otro catálogo de estrategias. La misma regla vale para nuevas métricas de stablecoins, ETF, actividad de desarrolladores o volumen social: fuente nueva no implica mecanismo nuevo ni mejora incremental. Su ausencia no bloquea el cierre limitado actual.

## Barreras que sí pueden impedir experimentos rigurosos

| Barrera | Consecuencia | Momento de resolución y regla de retirada |
|---|---|---|
| Universo histórico, bajas, contratos y datos por venue | Supervivencia, selección y precios no ejecutables | Antes de admitir un diseño en III/IV; limitar justificadamente el universo o posponer si no puede reconstruirse sin mirar resultados |
| Tiempo real de disponibilidad y revisiones | Leakage incluso con split cronológico | Antes de construir variables; excluir datos contaminados, usar demora justificable o recoger datos prospectivos tras autorización. Un embargo no sanea un dato futuro |
| Cobertura/licencia/coste de fuentes | Imposibilidad de reproducir o coste fijo superior al valor esperado para el capital disponible | Filtro documental de II, validación específica antes de III/IV. PDF abierto y endpoint actual no garantizan histórico apto |
| Tarifas, bid/ask, fills, cortos, funding, margen y capital completo | El beneficio cambia de signo o la cartera deja de ser solvente | Contabilidad y capacidad obligatorias antes de V; posponer variantes cuyo mecanismo no sobreviva a supuestos alcanzables |
| Selección de variables/activos/ventanas/modelos y ensayo repetido | Falsos descubrimientos; test reutilizado | Presupuesto finito y procedimiento íntegro congelado en IV. Ningún DSR/PBO corrige decisiones no registradas o fills imposibles |
| Pocos eventos, periodos/venues compartidos, dependencia y colas | Potencia insuficiente, intervalos engañosos y baja generalización | Justificar tamaño efectivo y bloques; un resultado inconcluso puede impedir asignar capital sin negar el mecanismo |
| Riesgo/exposición y numerario distintos entre comparadores | Atribuir a alpha menor exposición, carry, apalancamiento o beta | Comparadores y sizing causales, benchmarks accesibles y P&L reconciliado. No equiparar riesgos usando resultados completos del test |
| Conocimiento previo de LLM y cambios de modelos/proveedores | El test histórico puede estar contaminado aunque los precios estén separados | Snapshot/conocimiento declarados; alternativas simples y futura evaluación prospectiva. No confundir precisión de sentimiento con rendimiento |

Capital, jurisdicción, moneda de cuenta, productos/exchanges accesibles, horizonte, tolerancia a pérdidas y presupuesto de datos siguen desconocidos. **No impiden este dictamen bibliográfico**, pero sí una selección concreta de candidatos. Se resolverán si el usuario autoriza II; no se necesitan claves ni cuentas financiadas.

## Auditoría de hipótesis y calidad de evidencia

H-00–H-24 siguen siendo **propuestas no probadas**, no un preregistro. No se añade H-25 ni se cambian nulas para hacer encajar nuevas fuentes. Se conserva su evidencia favorable/adversa y se precisan cuatro interpretaciones para las fases futuras:

1. H-00 es una regla global de decisión sobre el conjunto finito efectivamente evaluado, no un test que pueda demostrar que ninguna oportunidad cripto existe. La familia de contrastes y su inferencia quedan por definir.
2. H-06/07/14/19 pueden mejorar riesgo/utilidad sin alpha. Riesgo de cola, exposición, costes y oportunidad perdida deben formar parte del comparador; un Sharpe mayor no basta.
3. H-23 exige incremento sobre pasado propio/factores con relojes coherentes. No se exige leer indefinidamente hasta hallar un artículo que haya aplicado exactamente esos controles; tampoco se afirma que la relación desaparecerá al aplicarlos.
4. H-24 prueba mejora relativa a un aditivo concreto, información, regularización y soporte muestral. Aun si lo supera, no identifica necesariamente una interacción estructural ni causal. Ablación reentrenada y presupuesto común serán necesarios, sin asumir beneficio por mezclar reglas perdedoras.

La calidad es desigual. Hay working papers, preprints, artículos editoriales, teoría y estudios ajenos a cripto. Las versiones no son réplicas. Varios trabajos comparten proveedores, activos y épocas; el corpus accesible y la búsqueda principalmente en inglés introducen selección. No hay metaanálisis homogéneo, saturación en dos rondas ni validación actual de todas las reglas de mercado. Las inconsistencias de RP-04/07/08, las ambigüedades de PORT-03/04 y los límites de ejecución de RV-E03/ML-11 impiden darles el mismo peso que una comparación temporal trazable por el mero hecho de estar publicados. Eso no permite acusar de errores a códigos no examinados.

Las fuentes parciales —por ejemplo MET-01/02/06, Cederburg, Mai, ciertos estudios de factores/ML— siguen siendo parciales. Solo requieren recuperación selectiva si una decisión concreta depende de su resultado o método. No hace falta convertir toda referencia identificada en una tarea obligatoria. Si se adopta un procedimiento estadístico en IV, sus supuestos deberán verificarse entonces; mencionarlo en una revisión no autoriza aplicarlo.

## Correcciones documentales y criterios de cierre

La auditoría detectó desincronización entre algunas fichas y sus registros: estados históricos de descarga sin evento posterior de lectura. Se añadieron **once conciliaciones fechadas basadas en las fichas existentes**: DIR-001/002/006/010, RV-E01–03 y ML-06/08/09/10. Identifican estudio y alcance declarado. No se reescriben registros originales, no se simula una lectura actual de PDF y no aumenta el corpus. RP dispone de un cierre agregado que conserva sus lecturas; MET y ML-11 tienen eventos explícitos, por lo que no se les imputa la misma carencia. El detalle y las comprobaciones finales quedan en DECISIONS y los logs afectados.

Las afirmaciones históricas de fichas parciales que mantenían abierta I describen aquella entrega. Esta evaluación global posterior recomienda aceptar sus límites; no las convierte retrospectivamente en revisiones exhaustivas ni elimina los pendientes. La ausencia inicial de comparadores de cartera frente a 1/N se redujo con PORT-01–04; la ausencia de ventaja neta replicada permanece. Son lagunas diferentes.

| Criterio del roadmap | Resultado de auditoría |
|---|---|
| I.1–I.2: preguntas y protocolo | Documentados; distinciones de predicción/riesgo/economía adecuadas; parametrización experimental aún pendiente |
| I.3: acceso primario | Acreditado parcialmente; originales inaccesibles y límites conservados |
| I.4: familias, ampliaciones y contrastes | Cobertura suficiente de mecanismos para comparación futura; desigual en evidencia cripto neta. No se declara una réplica ni dos pruebas independientes completas por cada sublínea |
| I.5: identidad, versiones y trazabilidad | Fichas y fuentes documentadas; conciliaciones de logs y límites de esta auditoría explícitos. No certificación integral de originales/datos/código |
| I.6: informe crítico y lagunas | Esta entrega distingue lagunas decisivas, requisitos posteriores y líneas pospuestas; sin nuevas familias ni ganador |
| Regla de parada | Se utiliza la alternativa ya prevista de límite de alcance/acceso/recursos. No se afirma haber alcanzado las dos rondas de saturación |
| I.7, I.N5 e I.X4: aceptación | **Pendiente del usuario**. La recomendación de cierre no sustituye aprobación ni inicia II |

**Asuntos pendientes acotados:** aceptar o no este cierre limitado; si después se autoriza II, concretar restricciones del operador y decidir qué hipótesis merecen el coste de comprobar sus datos. Posteriormente III/IV deberán resolver los requisitos exclusivos de las seleccionadas, fijar umbrales económicos, presupuestos, particiones y contabilidad antes de cualquier ensayo. Ninguna lectura adicional general se considera imprescindible para solicitar ahora esa decisión.

**Regla de reapertura recomendada:** una lectura adicional deberá indicar la decisión que podría cambiar, la fuente exacta y un límite de búsqueda. Procede ante contradicción material, problema de reproducibilidad decisivo o necesidad concreta de un candidato; no por existir otro indicador o para conseguir un resultado positivo. Si no se resuelve con el esfuerzo acotado, se conserva la incertidumbre y se pospone o descarta la variante, sin prolongar toda la fase.

## Inventario de estudios cubiertos por la auditoría documental

| Bloque y fichas | Trabajos distintos revisados a través de sus fichas |
|---|---|
| Direccionales y ampliaciones | DIR-001/002/006/010; CTR-01 = DIR-005; REV-02 = DIR-008; REV-03 — **7** |
| Valor relativo y perpetuos | RV-E01–03; FUND-01/02 — **5** |
| Ejecución | EX-01–05 — **5** |
| Riesgo, opciones y carteras | RP-01–08; OPT-01–03; PORT-01–04 — **15** |
| ML y metodología | ML-06/08/09/10/11; MET-03/04/05 — **8** |
| Noticias y eventos | MAC-01/02; SENT01/02; LLM-01–03; EVT-01/02 — **9** |
| Relaciones e interacciones | CX-01/02; CF-01; IX-01 — **4** |

**Total: 53.** Fuentes parciales, versiones, documentación de proveedores y conciliaciones de logs no añaden estudios. No se ejecutaron backtests, entrenamientos, optimizaciones, código de autores ni pruebas sobre series de mercado. Todos los contadores experimentales permanecen en cero.
