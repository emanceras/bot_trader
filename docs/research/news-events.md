# Noticias, sentimiento y Event-Driven Trading — línea transversal de Fase I

**Fecha de apertura:** 2026-10-16. **Consolidación:** 2026-10-17. **Estado:** marco, nueve lecturas dirigidas y evaluación documental de fuentes integrados; cobertura acotada y revisión de Fase I abiertas. Es una ampliación paralela de las trece familias existentes, no su sustitución ni una selección de candidatos. No hay código de trading, modelos entrenados, backtests ni experimentos de optimización.

## Preguntas científicas y mecanismo económico

1. ¿Los movimientos responden a la parte inesperada del anuncio, a información difundida antes o a cambios de liquidez/riesgo simultáneos? Un movimiento alrededor de una publicación no prueba causalidad ni beneficio disponible después de recibirla.
2. ¿Noticias macro, regulación, acontecimientos propios de tokens y sentimiento social tienen efectos distintos por activo, mercado, horizonte y régimen? No presumir que «positivo» para la economía es positivo para BTC.
3. ¿El texto añade información a precios, volumen, volatilidad, calendario y exposición de mercado ya conocidos? Separar señal textual de una descripción de un movimiento iniciado.
4. ¿Cuánto efecto queda al tiempo real de entrada de un particular, después de distribución, lectura/modelo, red y ejecución? La fecha editorial no acredita cuándo se recibió un mensaje.
5. ¿Puede el calendario ayudar a gestionar riesgo aun cuando no permita anticipar el signo? Comparar reducción de pérdidas con coste de oportunidad, cambios de exposición y referencia de riesgo equivalente.
6. ¿Una regla que utiliza solo noticias supera a una regla simple, y una combinación mejora incrementalmente a su componente de precio? La mejora contra una referencia débil no basta.
7. ¿Los resultados resisten duplicados, filtraciones, revisiones, noticias falsas, selección de eventos y entrenamiento del modelo con conocimiento posterior? ¿Qué cambia al exigir originales históricos y acceso real a consenso?
8. ¿Compensan la ventaja incremental los costes de datos, inferencia, mantenimiento y ejecución para el capital considerado? El presupuesto y la capacidad del operador siguen pendientes de Fase II.

**Sin techo artificial de rentabilidad.** No se impone una rentabilidad máxima aceptable ni se rechaza un resultado solo por ser alto. Se exige la misma trazabilidad de datos, contabilidad, riesgo, capacidad e incertidumbre para cualquier magnitud. No se recortarán resultados propios para forzar un límite favorable; tampoco se considerará una rentabilidad publicada elevada como prueba de persistencia.

El fundamento económico puede ser incorporación gradual de información, atención limitada, desacuerdo, presión de inventario o compensación por incertidumbre y selección adversa. Las restricciones de arbitraje pueden retrasar ajustes entre activos/venues. Son explicaciones falsables, no causalidad demostrada. Bots, promoción pagada, anticipación y reacción del público a precios también pueden producir correlación entre sentimiento y retornos sin ventaja incremental.

## Tres decisiones distintas

| Uso | Información permitida al decidir | Pregunta económica | Error que invalida la interpretación |
|---|---|---|---|
| Anticipar un anuncio/movimiento | Calendario, consenso y variables realmente disponibles antes del anuncio | ¿Una distribución de sorpresas o riesgo previsible mejora la decisión previa? | Usar la cifra realizada, el consenso revisado o texto posterior para elegir antes del evento |
| Reaccionar a información nueva | Primera versión recibida y estado de mercado disponible antes de enviar la orden | ¿Queda desplazamiento o reversión ejecutable después del retardo total? | Medir el beneficio desde un precio anterior a la recepción/fill, o atribuir al texto una tendencia ya visible |
| Gestionar exposición/riesgo | Calendario conocido o alarma recibida causalmente | ¿Reduce riesgo/pérdidas de forma útil frente a una regla comparable, después de costes y oportunidades perdidas? | Llamar alpha a tener menos exposición, o cerrar antes de un evento imprevisto identificado ex post |

Eventos calendarizados: decisiones de bancos centrales, inflación, empleo y publicaciones económicas. La fecha/hora esperada puede cambiar; se conserva la versión del calendario conocida entonces. Eventos no calendarizados: medidas regulatorias, resoluciones judiciales, aprobación/rechazo de productos, hackeos, insolvencias, depegs, interrupciones y declaraciones públicas. Se distinguen anuncio, filtración/rumor, desmentido y corrección; etiquetas retrospectivas de veracidad no pueden usarse para decidir en el pasado.

## Reloj de información y noticia original

Para cada observación, registrar cuando esté disponible:

| Campo conceptual | Significado y control |
|---|---|
| `scheduled_at_asof` | Hora prevista y fecha de vigencia del calendario; zona/DST originales y conversión UTC |
| `event_at` | Hora del acontecimiento, distinta de la noticia que lo comunica; puede ser incierta |
| `published_at_original` | Hora declarada por fuente original para esa versión, con precisión y significado documentados |
| `source_updated_at` | Actualización o corrección; no sobrescribe la primera versión |
| `vendor_first_seen_at` / `vendor_received_at` | Primera observación/recepción en el proveedor; distinguir captura, rastreo y distribución |
| `local_received_at` | Llegada efectiva al sistema local; necesaria para evaluación prospectiva de latencia |
| `available_at` | Momento a partir del cual todos los campos usados estaban disponibles; si falta el dato, declarar incertidumbre |
| `decision_at`, `order_sent_at`, `accepted_at`, `filled_at` | Procesamiento, envío, aceptación y ejecución; clocks sincronizados y errores conocidos |
| `version_id`, `source_id`, `event_cluster_id` | Versión del mensaje, procedencia y agrupación de republicaciones/correcciones; deduplicar sin información futura |

Para una reacción realizable, la decisión depende de información disponible antes de ella y el fill sucede después. Un historial con `published_at` actual y texto corregido solo demuestra el estado consultado hoy. Si no existe primera versión o timestamp de recepción, se evalúa como limitación de datos; no se inventa una precisión subsegundo.

El retardo relevante es `L_total = L_fuente/distribución + L_ingesta + L_modelo + L_decisión/red + L_ejecución`, con colas, percentiles y fallos, no solo promedio o tiempo de inferencia. La API que respondió rápido hoy no demuestra su latencia histórica. Una vela de un minuto no valida una reacción dentro de ese minuto ni el orden de anuncio, spread y fill. En eventos, spread, impacto y probabilidad de fill pueden empeorar simultáneamente.

## Formalización conceptual y límites

Para publicación macro i en τ, una sorpresa estandarizada puede escribirse como:

\[
z_{i,\tau}=\frac{A^{(0)}_{i,\tau}-C_{i,\tau^-}}{\widehat\sigma_{i,\tau^-}},
\]

donde `A^(0)` es el primer dato publicado, `C` el consenso cuya versión/corte se conocía antes, y la escala usa solo datos de desarrollo disponibles entonces. Un consenso de proveedor, un promedio de encuestas, el precio de futuros que refleja expectativas y la previsión de nuestro modelo son objetos distintos. El dato anterior revisado que acompaña al actual puede ser una segunda sorpresa; no reemplazar retroactivamente el dato original por su última revisión. En FOMC, decisión, trayectoria y comunicación pueden tener componentes distintos; un solo cambio de tipo no identifica todo el shock.

Un estudio de evento puede definir `AR_t = r_t − E[r_t | I_(t−)]` y `CAR_[a,b] = Σ AR_t`. El modelo de retorno esperado, la selección de eventos, el solapamiento de ventanas y las noticias simultáneas condicionan la inferencia. `CAR` desde antes del anuncio mide reacción económica, no P&L accesible al entrar después de recibirlo. Las pruebas de causalidad temporal/Granger no prueban causalidad estructural y un p-valor de evento no acredita una estrategia neta.

Un clasificador produce `s_t = f_θ(textos disponibles hasta t)`; el benchmark de precio podría ser `g(x_≤t)`. La comparación incremental pertinente mantiene universo, periodos, riesgo y ejecución comunes y contrasta `g(x_≤t, s_t)` con `g(x_≤t)`. También debe compararse con calendario/evento sin texto para separar el valor del contenido del simple conocimiento de una publicación. Una mejora de log-loss o F1 no sustituye mejora económica ni informa cuánto volumen puede negociarse.

**LLM:** congelar modelo/versión, fecha de entrenamiento conocida o desconocida, prompt, herramientas y fuentes consultadas. Un modelo publicado después del periodo del supuesto test puede conocer los eventos o sus resultados: un split cronológico de las noticias no elimina esa contaminación. Ajuste fino, selección de prompt, etiquetado, embeddings, vocabulario y calibración usan solo desarrollo permitido. La fecha de corte declarada por un proveedor no certifica ausencia de contaminación. Enmascarar nombres/fechas o hacer pruebas de robustez puede diagnosticar problemas, pero no demuestra por sí solo que hayan desaparecido. Si el entrenamiento no es auditable, la limitación se conserva y la evaluación prospectiva adquiere especial importancia.

## Comparaciones e integración con las líneas existentes

Son contrastes **propuestos para diseñar en II/IV**, no experimentos ejecutados ni selección de modelos.

| Familia existente | Integración que merece contraste | Comparador que separa información y complejidad | Riesgo principal |
|---|---|---|---|
| Momentum/trend | Confirmación, cambio de intensidad o identificación de noticia nueva frente a tendencia previa | Misma regla de precio, calendario sin texto, y señal de noticias sola | Texto que describe el movimiento ya sucedido; sumar dos señales redundantes |
| Reversión | Distinguir presión transitoria/rumor de actualización permanente de valor | Reversión sin texto a igual exposición; separar rumor y desmentido disponibles entonces | Promediar pérdidas tras noticia permanente o usar veracidad ex post |
| Arbitraje estadístico/pares/factores | Shock específico de activo frente a shock común; cambios de hedge/residuo | Modelo factorial/pares con iguales datos de precio y restricciones | Correlaciones rotas, cortos inexistentes y atribución narrativa posterior |
| ML/DL | Texto como variable adicional o representación, con ablaciones | Mismos inputs numéricos, presupuesto de búsqueda y referencias léxicas/lineales | Leakage de pretraining/prompts; mejor accuracy sin utilidad neta |
| Volatilidad/regímenes/riesgo | Exposición alrededor del calendario y alarmas de incertidumbre | Control de volatilidad, calendario solo y referencia a riesgo equivalente | Estado retrospectivo; retraso del detector; retirar exposición tras la pérdida |
| Funding/carry | Alertas de contraparte, regulación, depeg y cambio de demanda de apalancamiento | Carry sin noticias con igual margen/capital; separar funding y convergencia | Noticia recibida tras salto/liquidación; garantías inaccesibles |
| Microestructura/market making | Cambiar quotes/inventario o abstenerse tras anuncio recibido | Mismos datos de libro y latencia sin texto; calendario sin contenido | Cola, selección adversa y carreras de cancelación/fill durante eventos |
| Carteras/combinaciones | Asignación entre mecanismos ante shocks, evitando doble exposición | Pesos simples, reglas sin texto y agregación de costes completa | Mucha selección de eventos/pesos y correlaciones extremas comunes |

La futura comparación distinguirá al menos: precio solo, calendario solo, noticias/sentimiento solo, precio+calendario y precio+calendario+texto. Ablaciones separarán cantidad de cobertura, tono, novedad, fuente, entidad y sorpresa numérica. Costes de datos/inferencia se imputarán al capital y actividad pertinentes; no se consideran cero por ser ajenos a una comisión de exchange.

## Sesgos y requisitos para evaluar evidencia

- **Disponibilidad temporal:** primera versión, recepción, granularidad, revisiones, DST y calendarios actualizados. Unir por `available_at`, no solo fecha del evento. Sin información histórica suficiente, no afirmar ejecución causal.
- **Dependencia y duplicados:** agrupar republicaciones, traducciones, hilos, comunicados y noticias que describen el mismo evento. No repartir copias entre entrenamiento y test ni contarlas como eventos independientes. Una actualización posterior no puede decidir retrospectivamente cómo agrupar una noticia recibida antes.
- **Selección:** incluir eventos sin movimiento, publicaciones de signo contrario, noticias no difundidas y fallos de feed; no elegir solo grandes crashes o mensajes virales conocidos después. No usar número final de likes/retuits como variable inicial.
- **Texto y etiquetas:** separación entre sentimiento humano, información de riesgo y dirección del precio. Una etiqueta construida con retornos posteriores es un objetivo supervisado, no información disponible al operar. Purga/embargo cuando intervalos de etiquetas se solapen; todo ajuste se realiza dentro del desarrollo.
- **OOS:** división temporal por grupos de eventos y disponibilidad; sensibilidad entre fuentes, periodos/activos y regímenes, sin tuning del test. Conservar test final y futura evaluación prospectiva. En eventos escasos, miles de titulares no equivalen a miles de shocks independientes.
- **Multiplicidad:** registrar fuentes, ventanas, horizontes, modelos, prompts, filtros, activos, regímenes y variantes. Los resultados fallidos cuentan. No aplicar una corrección elegida después de ver cuál permite rechazar la nula.
- **Ejecución y estrés:** retrasos plausibles y escenarios de feed lento/caído, spread/impacto/fees, funding, préstamo, fills parciales, margen y news falsas/corregidas. El retraso debe evaluarse junto al estado de mercado; no prometer fills por tocar un precio.
- **Valor incremental:** igualar información no textual, capital, restricciones, presupuesto de selección y fechas; informar efecto económico e incertidumbre. Modelos complejos deben justificar aportación y coste; una comparación positiva en acciones no prueba transferencia cripto.

## Evidencia y datos

Se añaden **nueve trabajos distintos con texto completo disponible y lectura dirigida**, no nueve pruebas de rentabilidad: dos macro/regulación, dos sentimiento, tres NLP/LLM y dos estudios de eventos. Uno de los tres NLP/LLM estudia acciones y otro clasifica etiquetas sin evaluar retornos. Versiones editoriales/preprints del mismo estudio no se suman; las fichas precisan qué versión se leyó. Hay publicaciones académicas, preprints e informes institucionales, identificados por separado.

| Bloque y fuentes | Evidencia favorable examinada | Evidencia adversa, OOS y costes | Consecuencia para investigar |
|---|---|---|---|
| [Macro/regulación: MAC-01/02](evidence-news-macro.md) — Benigno–Rosa y Auer–Claessens | CPI subyacente y factor Path asociados a BTC en algunas especificaciones; categorías regulatorias con respuestas distintas | NFP/Target nulos en especificaciones base; CPI deja de ser significativo al retirar 2022; advertencias/CBDC sin efecto significativo en aquella muestra. Ventanas incluyen movimiento previo; sin estrategia OOS ni costes | Estudiar sorpresa, tipo de evento y régimen; no comprar/vender mecánicamente por nivel macro o tono positivo |
| [Sentimiento: SENT01/02](evidence-news-sentiment.md) — García–Schweitzer; Kraaijeveld–De Smedt | Simulación retrospectiva BTC en 2014 favorable a combinación social; Granger significativo para algunos activos/contrastes | La primera pierde rentabilidad con comisión por intercambio superior a 0,25% bajo su modelo; la segunda carece de prueba OOS y costes, con múltiples activos nulos. Agregación diaria y reacción del texto a precios dificultan disponibilidad | Comparar sentimiento contra precio, actividad y calendario; no equiparar causalidad de Granger a causalidad económica o beneficio |
| [NLP/LLM: LLM-01–03](evidence-news-llm.md) — CryptoTrade, Roumeliotis et al., Glasserman–Lin | CryptoTrade muestra algunos resultados y ablación textual favorables; GPT ajustado mejora clasificación; anonimizar cambia resultados en acciones | CryptoTrade frecuentemente pierde ante buy and hold/SLMA; tasa de comisión no localizada y ablación con activo/cifra discordantes. Clasificación no evalúa P&L. Contraste en acciones omite costes y no es cripto. Preentrenamiento/versiones impiden certificar test limpio | Exigir NLP sencillo, misma información y riesgo, congelación del modelo y evaluación posterior a su conocimiento; no inferir superioridad por tamaño |
| [Eventos/ejecución: EVT-01/02](evidence-news-execution.md) — Ante; Mehdian et al. | Reacciones intradía y actividad ante algunas publicaciones/episodios; diferencias entre activos y ventanas | Seis eventos elegidos en el WP de Ante y dos episodios ETF en el otro estudio; movimientos previos, negativos y nulos. El estudio ETF mezcla aprobación/debut/apertura y contiene discrepancias de tabla/prosa. Ninguno mide P&L desde recepción retrasada, OOS o costes | La velocidad aprovechable no está determinada. CAR significativo no significa retorno restante tras clasificación y fill |

**Informe crítico.** Hay mecanismos interesantes en sorpresas macro, novedades específicas de activo, desacuerdo/atención social y riesgo alrededor del calendario. La revisión no establece todavía una ventaja neta robusta y accesible. Una asociación puede proceder del movimiento ya iniciado, de selección de eventos o de cambios de exposición. Tampoco demuestra que las noticias sean inútiles: los nulos dependen de muestra, potencia y objetivo. La siguiente lectura debe buscar replicaciones, periodos recientes y evaluación incremental con disponibilidad verificable, incluidos resultados negativos.

La distinción entre noticias solas e híbridas es central. Los híbridos pueden aprovechar contexto de precio o limitar exposición durante eventos, pero añaden decisiones de selección. Se proponen comparaciones de precio solo, calendario solo, texto solo, precio+calendario y precio+calendario+texto, con igual información permitida, capital, riesgo y presupuesto de búsqueda. También se compararán lexicones/modelos lineales con NLP/LLM sobre los mismos textos. Son requisitos para futuras fases, sin elegir ni implementar candidatos ahora.

La [matriz de fuentes de datos](news-data-sources.md) examina BLS, Fed, ALFRED, Trading Economics, GDELT, NewsAPI, X y Reddit; Benzinga permanece pendiente. Son 22 páginas oficiales leídas en secciones relevantes, **fuera del recuento de estudios académicos**. Ningún feed, histórico point-in-time o SLA fue validado mediante cuenta/dataset. Los archivos oficiales ayudan con primeras publicaciones/revisiones; el consenso previo y la recepción necesitan evidencia adicional. NewsAPI no entrega texto completo y su modalidad gratuita retrasa noticias 24 horas; las prestaciones de pago no acreditan por sí solas ejecución rápida.

**Continuidad paralela:** [PORT-04](portfolio-followup.md) añade una cuarta lectura dirigida de carteras frente a 1/N, con mejoras de mínimo riesgo y resultados adversos a estimar medias mediante DL, costes y ambigüedades contables preservados. No reemplaza ninguna familia ni selecciona pesos. El corpus general pasa de 39 a **49** trabajos con lectura dirigida: 9 de esta línea más 1 de carteras.

**Lagunas y cierre de tanda:** Mai/SENT03 sigue en resumen/metadatos; el estudio IMF del ciclo cripto no se recuperó completo; otros bancos centrales, noticias de hackeos/depeg/insolvencia y réplicas con latencias realistas no tienen cobertura suficiente. No se midió cuánto tarda el mercado en incorporar cada tipo de noticia, no se probaron proveedores y no se completaron dos rondas de saturación. Esta entrega se consolida por presupuesto y acceso, conservando preguntas pendientes, sin cerrar Fase I ni bajar los criterios de evidencia.

## Criterio de aceptación de esta ampliación

Documentar mecanismos y fuentes primarias de macro/regulación, sentimiento/NLP/LLM y reacción intradía; preservar resultados positivos y nulos/adversos; evaluar OOS, latencia y costes por estudio; mapear fuentes de noticias/consenso con versiones históricas, restricciones y coste verificable; integrar hipótesis y comparadores sin elegir ganadores. Las carencias de acceso o de evidencia se declaran por dimensión. No cerrar la línea solo por contar artículos ni exigir encontrar una estrategia rentable. La aceptación de Fase I y cualquier avance a II siguen siendo decisiones posteriores del usuario.
