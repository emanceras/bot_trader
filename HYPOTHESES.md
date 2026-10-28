# Registro inicial de hipótesis

**Estado de plataforma al 2026-10-28:** III aceptada; E1/E2 de IV aprobadas condicionalmente. D-044 registra la [admisión metodológica por etapas aprobada](docs/es/phase-iv/staged-amendment.md); D-045 propone [pruebas M/E/R](docs/es/phase-iv/technical-packages.md), todavía sin permiso de ejecución. E3/E4 y admisión financiera pendientes. No cambian filas, nulas, falsadores, prioridades ni las 26 especificaciones. No hay resultados financieros ni autorización de V.

**Creación:** 2026-10-13 · **Actualización:** 2026-10-18 · **Versión:** 0.8 · **Estado de todas las hipótesis:** propuestas, no probadas ni validadas.

Este documento conserva las preguntas falsables de Fase I y añade su disposición provisional en la Fase II autorizada. No constituye un preregistro experimental completo. No se han utilizado datasets propios para elegir estrategias o parámetros; la lectura de resultados publicados sí informa las preguntas y deberá declararse en un futuro preregistro. Las notas fechadas que indicaban «no seleccionadas» describen las entregas históricas; el mapa actual del final no modifica sus proposiciones, nulas ni falsadores.

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

Los mecanismos se desarrollan en [RESEARCH.md](RESEARCH.md) y sus apéndices. Las fichas enlazadas distinguen textos con secciones examinadas, resúmenes y referencias pendientes. La evidencia publicada informa las hipótesis; no prueba ni valida ninguna para este proyecto.

| Fecha | Cambio | Motivo | Relación con datos/experimentos |
|---|---|---|---|
| 2026-10-13 | Creación H-00 a H-14 | Definir mecanismos y falsadores para Fase I | Ningún dataset ni experimento utilizado |
| 2026-10-15 | Añadidas implicaciones de literatura, sin cambiar H-00–H-14 ni sus falsadores | Incorporar evidencia favorable y contraria trazable | Lectura documental; cero ensayos propios |

## Implicaciones de la lectura — no validación experimental

| Hipótesis | Evidencia que orienta la siguiente pregunta | Estado/limitación |
|---|---|---|
| H-01/H-03 | DIR-001/002: predictibilidad y factores; DIR-006: BTC OOS negativo y altcoins positivas; DIR-010: momentum no significativo en toda la muestra y colas severas | Propuestas; separar temporal/transversal, costes y disponibilidad de cortos |
| H-02 | REV-02 amplía DIR-008: reversión en pequeñas/ilíquidas frente a momentum grande/líquido; REV-03 predice un proxy de provisión de liquidez | Propuesta; costes/cortos y selección impiden afirmar ventaja neta; DIR-007/013 siguen parciales |
| H-04/H-05 | RV-E02/03 muestran diferencias entre métodos y deterioro por fees; selección, supervivencia y financiación limitan transferencia | Propuestas; cointegración estadística no basta para negociar un spread |
| H-06/H-07 | RP-01 estudia exposición tradicional; OPT-01 añade estrategia con cobertura y costes parciales; OPT-02/03 estiman primas/kernels | Propuestas; no confundir varianza con P&L; funding, margen, colas y selección siguen abiertos |
| H-08 | RV-E01 documenta futuros; FUND-01/02 añaden perpetuos, funding/convergencia y deterioro por régimen; captura breve puede no cubrir fees | Propuesta; costes completos, timestamps, capital total y liquidaciones sin validar |
| H-09/H-10 | EX-01 aporta predicción y maker real condicionado a rebates; taker ordinario negativo; EX-03/04/05 delimitan teoría/predicción | Propuestas; latencia, colas, capital y gastos completos pendientes |
| H-11/H-12 | ML-06 mezcla éxitos y pérdidas con costes; ML-09/11 tienen grandes resultados simulados y supuestos fuertes; ML-08 ofrece baselines ajenos a cripto | Propuestas; ninguna superioridad general de ML/DL establecida |
| H-13/H-14 | RP-04/07/08 cuestionan complejidad; PORT-01 compara con 1/N y costes, PORT-02 muestra fragilidad por liquidez y PORT-03 mejoras condicionadas de factores | Propuestas; no equivalencia universal de 1/N; causalidad, selección y costes internos pendientes |

No se rechaza H-00 con esta revisión. Los resultados publicados no sustituyen contabilidad, datos, control de selección y evidencia propia fuera de muestra. Los IDs y sus páginas/tablas se encuentran en los enlaces de [RESEARCH §2](RESEARCH.md#2-alcance-acceso-y-límites-de-esta-entrega). Toda hipótesis nueva surgida al observar literatura deberá fecharse, sin fingir que se registró antes de esos hallazgos.

## Actualización bibliográfica del 2026-10-16

H-00–H-14 conservan sus proposiciones y falsadores; no se ajustaron retrospectivamente para favorecer ningún resultado. Las once lecturas adicionales elevan el corpus a 39 textos con secciones examinadas, sin ensayos propios. CTR-01/DIR-005 añade momentum no significativo al 5% en una muestra antigua; esto limita extrapolación, no prueba nulidad universal. Las nuevas fichas separan resultado neto de costes supuestos y beneficio neto integral, y contraste de autores distintos frente a réplica exacta. Ninguna hipótesis cambia a probada/validada ni se rechaza H-00.

## Ampliación del 2026-10-17 — noticias, sentimiento y eventos

H-15–H-22 son **propuestas no probadas**, formuladas después de leer los estudios de esta ampliación. No constituyen preregistro, selección de candidatos ni autorización experimental. H-00–H-14 conservan sus criterios. Fundamentos, fuentes y disponibilidad se enlazan en [noticias/eventos](docs/research/news-events.md); PORT-04 añade contraste a H-12/H-14 sin validarlas.

| ID | Proposición y fundamento | Comparador/nula a concretar | Evidencia adversa o retirada | Datos imprescindibles |
|---|---|---|---|---|
| H-15 | La sorpresa macro puede aportar información condicional sobre retorno o riesgo distinta del nivel anunciado | Precio/volatilidad y calendario sin sorpresa; contrastes de dirección y riesgo separados | Efecto dependiente de una época, consenso revisado, noticia simultánea o retorno anterior a disponer del dato; no persiste OOS | Primera publicación, consenso anterior versionado, revisiones, calendario, precios ejecutables y régimen conocido entonces |
| H-16 | Sentimiento/atención social puede añadir información a precios y actividad | Mismo modelo con precios/volumen, con actividad textual sin tono y con tono; nula de incremento neto | Texto solo sigue al precio; bots/duplicados/engagement final explican resultado; nulos entre activos, costes o retrasos consumen efecto | Corpus con tiempos/versiones y cobertura, etiquetas disponibles, actividad contemporánea, costes/derechos |
| H-17 | Puede quedar ajuste o reversión tras recibir una noticia no programada | Entrada causal retrasada frente a no negociar y señal de precio equivalente | Todo efecto ocurre antes del fill; eventos elegidos por impacto; fuentes falsas/corregidas o costes eliminan beneficio | Mensajes originales y actualizaciones, recepción, clasificación, cotizaciones/fills y distribución de demora total |
| H-18 | Noticias combinadas con momentum/reversión pueden mejorar a cada componente | Precio solo, texto solo, calendario y combinaciones bajo igual riesgo/información/búsqueda | Redundancia, más exposición, más selección o una ventana aislada explican mejora; neto OOS no incremental | Datos sincronizados por disponibilidad; reglas/variantes y costes conjuntos; no usar hindsight para clasificar shocks permanentes |
| H-19 | Calendario/alarma de evento puede mejorar gestión de pérdidas sin predecir signo | Control de volatilidad simple, calendario solo y exposición equivalente; incluir oportunidad perdida | Menor riesgo se explica solo por menor exposición; salida posterior a pérdida, mayor cola residual o retorno perdido no compensa | Calendario conocido antes, alertas recibidas entonces, exposición y riesgos comparables; eventos sin movimiento |
| H-20 | Noticias específicas de activo pueden informar residuales, pares y riesgo de ruptura de cartera | Modelo factorial/pares o pesos simples sin texto, mismas restricciones | Shock común ya explicado, neutralidad rota, falta de préstamo/margen o texto futuro genera supuesto alpha | Entidades/eventos agrupados, universo histórico, factores y costes de todas las patas, riesgos de correlación |
| H-21 | Novedad y procedencia pueden ser más útiles que tono agregado o cantidad de titulares | Cantidad, tono y primera aparición, con/sin agrupación causal; nula de valor adicional | Republicaciones cuentan como shocks; autenticidad/veracidad se etiqueta con futuro; fuente/idioma/periodo decide resultado | Primera versión, cadenas de republicación, credibilidad conocida entonces, rumores y desmentidos con su propia hora |
| H-22 | NLP/LLM puede mejorar decisiones frente a léxico/lineal con los mismos textos | Modelos simples fuertes, mismo corpus y numerarios, ablar precio/calendario/texto; incluir coste/latencia de inferencia | Solo mejora etiquetas; test dentro del conocimiento del modelo; resultado sensible a prompts/semillas; coste total o complejidad supera incremento | Modelo/snapshot, fecha de conocimiento conocida o desconocida, prompts/herramientas, corpus versionado y evaluación temporal/prospectiva limpia |

Para H-15, el efecto contemporáneo no valida anticipación ni una reacción negociable; para H-19, menor riesgo no demuestra alpha. MAC-01/02 y EVT-01/02 orientan impacto/cronología; SENT01/02, valor social y nulos; LLM-01–03, incremento textual y contaminación. La evidencia de clasificación o de acciones no prueba ventaja cripto.

Todas deberán fijar horizonte, efecto mínimo relevante, tamaño efectivo por eventos independientes, métricas, costes, incertidumbre y presupuesto de búsqueda antes de experimentar. **No existe un límite máximo artificial de rentabilidad admisible**; un retorno alto tampoco exime de integridad y evidencia. Fallos de datos pueden impedir evaluar una hipótesis sin demostrar que el mecanismo no exista. Todos los contadores experimentales siguen en cero.

## Ampliación del 2026-10-17 — relaciones entre activos e interacciones

**H-23/H-24: propuestas, no probadas ni seleccionadas.** Se formulan después de la lectura bibliográfica y no constituyen preregistro. H-00–H-22 se conservan; ninguna conclusión previa se modifica para acomodar la propuesta. Se integran en familias existentes, sin añadir otra. Fuentes y diseño conceptual: [relaciones e interacciones](docs/research/cross-asset-interactions.md).

| ID y relación | Proposición y fundamento | Nulas y comparadores a fijar | Refutación/retirada o motivo para posponer | Datos necesarios |
|---|---|---|---|---|
| H-23; H-03/04/05/09/11/13 | Retardos de otros activos podrían aportar información condicional al pasado propio y factores comunes, con efecto dependiente de horizonte/liquidez | Nula predictiva: no mejora OOS sobre propio+factores; nula económica separada: incremento neto no supera el mínimo relevante predefinido. Comparar propio, propio+factores y +otros activos con igual periodo/información | Señal desaparece al sincronizar, controlar factores o usar precios frescos; falla en nuevas ventanas o vive menos que demora/fill; fees/capacidad consumen efecto. Datos insuficientes implican posponer, no probar inexistencia universal | Universo histórico dinámico, clocks/recepción, quotes/trades, factores estimados con pasado, liquidez/costes, funding disponible y acceso a cortos si aplica |
| H-24; H-11/12/14 y H-18/20/22 | Variables débiles individualmente podrían modificar la utilidad de otras según contexto y mejorar una decisión conjunta | Nula de interacción: modelo con términos conjuntos no mejora OOS sobre aditivo comparable con los mismos inputs. Nula económica: no hay incremento neto relevante a riesgo/capital/costes comunes. Separar individual, lineal regularizado, aditivo no lineal e interacción | Aparente mejora explicada por más datos/búsqueda/exposición, desaparece al reentrenar ablaciones, depende de test reutilizado o aumenta costes/pérdidas. No confundir mejores etiquetas/error con beneficio | Variables con disponibilidad real, contexto inferido usando pasado, registro de selección/prompts/modelos cuando aplique y contabilidad conjunta de patas/turnover |

No se afirma que las variables débiles o una mezcla de estrategias perdedoras contengan alpha. La diversificación reduce varianza bajo ciertas covarianzas, pero una mezcla estática con pesos no negativos que suman uno, de medias netas verdaderamente negativas, sigue teniendo media negativa si los costes son aditivos. Neteo y pesos adaptativos cambian supuestos y requieren hipótesis/contabilidad explícitas.

Antes de cualquier experimento se fijarán target (retorno/riesgo), horizonte, información restringida, factores y posibles interacciones primarias, universo/particiones, efecto mínimo, inferencia bajo dependencia temporal/transversal, presupuesto y holdout. Comparar grafos aprendidos exige reestimar selección dentro de cada ventana. Las sensibilidades por regímenes no autorizan elegirlos ex post. H-00 sigue sin rechazarse.

## Auditoría de cobertura del 2026-10-17 — precisiones sin nuevas hipótesis

La [auditoría](docs/research/coverage-audit.md) no añade una familia ni H-25, no selecciona candidatos y conserva H-00–H-24 y sus falsadores. Las siguientes fuentes pueden integrarse, si posteriormente se justifican y autorizan, en las preguntas existentes:

| Fuente/estado | Hipótesis relacionadas | Condición previa para considerar su evaluación |
|---|---|---|
| Actividad/flujos on-chain | H-03/11/13/20/24 | Significado de variable, cadena/entidades, versión, disponibilidad/confirmación y comparación incremental frente a precio/volumen; transferencia no equivale a venta |
| Posicionamiento/OI de derivados | H-07/08/09/13/24 | Contrato, unidades/población y publicación; OI no identifica dirección neta; distinguir cobertura de apuesta direccional |
| Liquidaciones/flujos forzados | H-02/08/09/19/23 | Cobertura/censura del feed, orden frente a fill, recepción y demora; efecto después de recibirlo; margen propio separado de señal de terceros |
| Eventos de oferta, listados/bajas, contratos y seguridad | H-03/04/17/19/20/21/24 | Calendario/primera comunicación disponibles entonces, evento esperado frente a sorpresa, bajas y cambios de unidades; unlock no equivale a venta efectiva |

Estas asignaciones no demuestran evidencia específica ni conceden prioridad. El histórico de bajas/migraciones es requisito de integridad aunque nunca se utilice como señal. Los demás inputs son opcionales y deben justificar su coste/incremento; no se probarán todas sus combinaciones.

**Interpretaciones para el protocolo futuro:** H-00 es una regla global sobre las alternativas efectivamente evaluadas, no una prueba universal de inexistencia de oportunidades. H-06/07/14/19 pueden referirse a riesgo/utilidad sin alpha; el comparador deberá incorporar exposición, colas y oportunidad perdida. H-24 mide incremento frente a un aditivo especificado con el mismo soporte, información y presupuesto, no identifica necesariamente interacción estructural o causal. Ninguna de estas precisiones cambia retrospectivamente un umbral ni un resultado: no hay experimentos y los parámetros siguen pendientes de II/IV.

## Propuesta final de disposición de Fase II — 2026-10-18, revisión 2

El cierre limitado de I fue aceptado y II autorizada en D-025. La [matriz comparativa](docs/phase-ii/COMPARISON.md) cubre H-00–H-24 y conserva evidencia favorable/adversa y motivos de aplazamiento. El [informe de selección](docs/phase-ii/SELECTION.md) propone dos preguntas primarias y una comparación secundaria de riesgo; dos alternativas quedan condicionadas a recursos concretos. **No son cinco estrategias aprobadas para ejecutar.** D-028 incorpora preferencias; D-029/D-030 presentan proceso y propuesta final para revisión. USD/España están confirmados; capital, riesgo, venue y presupuesto definitivos pueden esperar a sus puertas de dependencia. La aceptación final de II sigue pendiente; todas las hipótesis permanecen propuestas, no probadas ni validadas, y H-00 no se rechaza.

| Candidata y papel provisional | Hipótesis | Pregunta delimitada y condición |
|---|---|---|
| C1 — individual, primaria | H-01 | Momentum temporal simple frente a efectivo, buy and hold y exposición/riesgo comparable, con datos y costes accesibles; su rentabilidad sigue desconocida |
| C2 — comparación secundaria de riesgo | H-06 | Exposición ajustada por volatilidad frente a referencias de riesgo/efectivo equivalentes; no es una promesa separada de alpha ni autoriza apalancamiento |
| C3 — información combinada, primaria condicionada a recursos | H-11/H-24 y sus referencias | C3-I: combinación aditiva frente a referencias individuales; C3-X: interacción frente a aditivo no lineal con iguales inputs. Soporte, riesgo, costes y presupuesto comparables; datos/muestra/esfuerzo antes de admisión experimental |
| C4 — alternativa condicionada | H-23 | Otros activos frente a pasado propio y factores; supeditada a universo histórico, sincronización, disponibilidad y coste de investigar dependencias |
| C5 — alternativa condicionada | H-08 | Carry de funding/basis con capital y garantías completos; supeditada a productos accesibles, margen, costes y capacidad operativa |

La [evaluación de viabilidad](docs/phase-ii/FEASIBILITY.md) distingue preferencias confirmadas de escenarios hipotéticos. La recomendación puede cambiar por evidencia material, recursos o acceso, sin favorecer una intuición ni observar el holdout. C3 no exige éxito previo de C1 ni rentabilidad marginal positiva de sus inputs. C3-I puede justificar una referencia combinada sencilla sin rechazar H-11/H-24, que conservan comparación a igual información. H-24 exige incremento frente al aditivo comparable; una mejora predictiva sola no satisface su nula económica. Un resultado adverso de interacciones no invalida una combinación aditiva útil. No se crean dos candidatas ni pruebas ilimitadas; la mezcla de P&L sigue siendo otra pregunta.

[Horizontes](docs/phase-ii/HORIZONS.md) documenta las escalas por mecanismo y su selección prospectiva; segundos a semanas o más permanecen posibles, sin extrapolar evidencia ni adoptar una parrilla indiscriminada. [Acceso](docs/phase-ii/ACCESS.md) distingue investigar de operar: USD, España y escenarios de capital no alteran nulas ni prueban viabilidad. Condiciones para promover reservas, detener construcciones sin fundamento y resolver dependencias antes de ingeniería/experimentos se conservan en selección.

Las restantes H-02–H-05, H-07, H-09/H-10, H-12–H-22 y H-14 como combinación de estrategias se conservan con su disposición trazable en la matriz; no admitirlas en la lista inicial no equivale a refutarlas. H-03 puede servir como control de factores sin aprobar una cartera factorial; una referencia sencilla de reversión tampoco convierte H-02 en candidata primaria. Parejas, fuentes nuevas, redes neuronales, boosting o variantes de estimador no permiten ampliar libremente el número de pruebas: toda incorporación necesita necesidad incremental y presupuesto de búsqueda definidos antes de experimentar.

No se cambian H-00–H-24, sus nulas, falsadores ni resultados publicados. No se crean H-25 ni nuevos umbrales tras resultados. Laboratorio, datasets de backtesting, entrenamientos y experimentos continúan sin autorización.
