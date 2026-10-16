# Roadmap del proyecto cuantitativo

Fecha de inicio: 2026-10-13 · Actualización: 2026-10-16 · Versión: 0.2 · Alcance autorizado: **Fase I**.

## Objetivo y estado general

Determinar si existe evidencia suficiente de una ventaja neta, robusta y viable para un operador particular. Una conclusión negativa y reproducible constituye un resultado útil. Ninguna fase posterior está autorizada todavía.

| Fase | Entregable principal | Dependencias | Estado |
|---|---|---|---|
| I. Investigación | Preguntas, protocolo, revisión crítica y mapa de evidencia | Acceso a fuentes primarias | En curso; primer informe con 28 textos y lectura dirigida documentada; lagunas y aceptación pendientes |
| II. Comparación y selección | Matriz con evidencia y candidatos falsables | I aceptada y aprobación explícita | Planificada |
| III. Laboratorio | Arquitectura Python modular y capacidades verificadas | II aceptada; datos y licencias identificados | Planificada |
| IV. Protocolo experimental | Registro prospectivo, particiones, costes y pruebas | II; viabilidad técnica de III; sin resultados de selección | Planificada |
| V. Experimentos | Comparación reproducible, resultados positivos y negativos | III y IV aceptadas | Planificada |
| VI. Sistema y evaluación prospectiva | Arquitectura del bot y paper trading supervisado | Evidencia suficiente en V y nueva aprobación | Planificada y condicionada |
| Operativa real | Decisión independiente del usuario | Paper trading aceptado y autorización explícita separada | No autorizada |

Los estados **documentado**, **implementado**, **probado** y **validado** son distintos. Las casillas marcadas aquí solo acreditan la tarea concreta, no rentabilidad ni finalización de toda una fase.

## Fase I — Investigación científica

### Objetivo

Formular preguntas contrastables y evaluar qué evidencia existe, cuánto se puede confiar en ella y qué condiciones impiden trasladarla a una cuenta particular.

| ID | Tarea | Dependencia | Criterio de aceptación | Estado |
|---|---|---|---|---|
| I.1 | Preguntas científicas y definiciones | Ninguna | Distinguir predicción, ventaja neta y viabilidad; incluir hipótesis nulas | Documentado en RESEARCH |
| I.2 | Protocolo de búsqueda y evaluación | I.1 | Fuentes, consultas, exclusiones, extracción, duplicados y búsqueda contraria explícitos | Documentado |
| I.3 | Acceso a fuentes | Red del entorno | Al menos fuentes primarias relevantes consultables; registrar fallos y nivel de acceso | Comprobado: contenido primario recuperado; persisten bloqueos de algunas fuentes |
| I.4 | Revisión de las 13 familias | I.2–I.3 | Por familia: mecanismo, evidencia positiva/negativa, OOS, costes, datos, sesgos y viabilidad | Documentado para las 13 familias; cobertura empírica desigual, contrastes pendientes |
| I.5 | Auditoría de bibliografía | I.4 | Identidad/versiones verificadas; afirmaciones enlazadas a fuente y ubicación; no contar preprint/publicación dos veces | Auditadas fichas y coherencia de la síntesis; originales inaccesibles y réplicas pendientes |
| I.6 | Primer informe y mapa de lagunas | I.1–I.4 | Conclusiones limitadas a lo observado; prioridades de lectura justificadas | Documentado con fuentes verificadas y lagunas, versión 0.2 |
| I.7 | Revisión y aprobación del usuario | I.5–I.6 | Usuario acepta la cobertura o sus límites y autoriza el siguiente paso | Pendiente |

**Aceptación de la fase completa:** cumplir I.1–I.7. Para cada familia con literatura localizable se buscarán al menos un estudio primario y un contraste independiente, además de un trabajo metodológico cuando corresponda. Esto es un mínimo de cobertura, no una garantía de exhaustividad: si no aparecen estudios o resultados negativos, se registrarán las consultas y la laguna, sin inventar evidencia. Las afirmaciones decisivas requieren lectura de métodos, costes y validación del texto completo. Una revisión con solo referencias semilla no satisface este criterio.

**Condición de cierre de la búsqueda:** dos rondas documentadas de búsqueda hacia atrás/hacia delante sin nueva evidencia material, o límite explícito de acceso/recursos comunicado al usuario. La aceptación de una cobertura limitada exige documentar qué conclusiones quedan abiertas.

## Fase II — Comparación y candidatos

**Objetivo:** seleccionar un conjunto pequeño de hipótesis que merezca el coste de contrastación, sin declarar una ganadora por literatura.

Tareas previstas:

- II.1: concretar moneda de cuenta, residencia/jurisdicción, capital investigable, mercado spot/derivados, exchanges accesibles, horizonte operativo y recursos. No hacen falta claves de cuenta.
- II.2: construir matriz por familia/estudio: calidad, mecanismo, complejidad matemática/técnica, capital y margen, datos, frecuencia, costes, colas, implementación y sobreajuste.
- II.3: aplicar filtros no compensatorios: datos históricos aptos, legalidad/acceso, costes modelables, riesgo asumible y validación reproducible. Una evidencia favorable no compensa datos inservibles o ejecución imposible.
- II.4: fijar referencias comunes —efectivo definido, buy and hold, momentum simple y reversión simple cuando sean aplicables— y ordenar candidatos por razones explícitas. Documentar alternativas descartadas.
- II.5: estimar esfuerzo, disponibilidad de datos y presupuesto de búsqueda para cada candidato. Cualquier ML necesita un benchmark simple con las mismas variables y costes.

**Aceptación:** matriz trazable; requisitos del operador documentados; hipótesis primarias/ secundarias diferenciadas; lista de candidatos y descartes razonada; aprobación del usuario. Ni puntuaciones arbitrarias ni probabilidades de éxito inferidas de etiquetas cualitativas.

## Fase III — Laboratorio cuantitativo

**Objetivo:** disponer de una infraestructura sencilla y verificable para investigar. El diseño y la selección de bibliotecas se realizarán en esta fase, con alternativas y justificación.

Módulos previstos, aún sin implementar:

1. Ingesta y catálogo: fuentes, licencias, timestamps de evento/recepción/publicación, símbolos históricos y acciones de tokens; almacenamiento original inmutable y hashes.
2. Calidad: ausencias, duplicados, husos horarios, datos fuera de orden, revisiones, velas imposibles, unidades, cambios de contrato, exclusiones y activos deslistados.
3. Variables y señales: disponibilidad real, transformaciones ajustadas solo en entrenamiento y contratos explícitos entre módulos.
4. Estrategias y cartera: posiciones objetivo, exposición, capital, rebalanceo y benchmarks comunes.
5. Backtest/ejecución: orden temporal, órdenes/fills, comisiones, spread, slippage, impacto, financiación, margen y liquidaciones cuando apliquen.
6. Riesgos y métricas: resultados comparables, incertidumbre, colas, exposición, capacidad y descomposición del P&L.
7. Experimentos e informes: configuraciones inmutables, versiones de código/datos/entorno, semillas, resultados y fallos; gráficos con datos auditables.

**Aceptación:** instalación reproducible; una validación funcional con datos sintéticos que detecte desfases temporales y contabilidad incorrecta; pruebas relevantes de integridad y ejecución; reconstrucción independiente del P&L; documentación de límites. Los datos sintéticos validan el laboratorio, nunca una ventaja de mercado. No optimizar estrategias durante la construcción del laboratorio.

## Fase IV — Metodología experimental

**Objetivo:** congelar el diseño antes de ejecutar los ensayos que decidirán candidatos. Puede prepararse en paralelo con III, pero debe aprobarse antes de V.

Tareas previstas:

- IV.1: fijar universo point-in-time, fuentes, periodo, moneda de cuenta, elegibilidad por liquidez conocida entonces y tratamiento de desapariciones. Separar exploración autorizada de evaluación final.
- IV.2: particiones cronológicas y walk-forward; intervalos exactos decididos por longitud de muestra, horizonte de señales y suficiencia de regímenes, sin mirar el rendimiento del holdout.
- IV.3: purga de observaciones cuyos intervalos de etiquetas se solapen; embargo definido según horizonte informativo y dependencia cuando proceda. No usar cross-validation aleatoria para series financieras.
- IV.4: sellar holdout final: manifiesto con intervalos y hashes, responsable de acceso, comando/registro de apertura y una sola evaluación confirmatoria del procedimiento congelado. Si se usa para rediseñar, pasa a desarrollo y se necesita un nuevo holdout.
- IV.5: hipótesis, tamaños de efecto económicamente relevantes, criterio primario, métricas secundarias, parámetros/candidatos máximos, reglas de descarte y condiciones de parada.
- IV.6: costes por exchange y nivel alcanzable, escenarios de estrés, disponibilidad de préstamos, funding conocido en su momento y límites de participación. Evitar contar spread, slippage e impacto dos veces.
- IV.7: incertidumbre con bootstrap temporal apropiado; dependencia/colas; múltiples pruebas y selección; Deflated Sharpe Ratio como diagnóstico condicionado a sus supuestos; pruebas de sensibilidad y de regímenes definidos sin futuro.
- IV.8: congelar registro, configuración y criterios; fechar y justificar cualquier enmienda antes de usar datos nuevos.

**Aceptación:** diseño reproducible y aprobado; ninguna decisión dependiente de resultados ocultos; presupuesto de pruebas trazable; holdout inaccesible por defecto; costes y rechazo definidos. No se aceptan umbrales elegidos tras ver qué estrategia pasa.

## Fase V — Experimentación

**Objetivo:** medir si el procedimiento de selección y la estrategia resisten datos nuevos y costes realistas.

Secuencia prevista:

1. Validar referencias y contabilidad sin búsquedas de parámetros.
2. Ejecutar hipótesis sencillas preregistradas; registrar también errores, abandonos y nulos.
3. Comparar candidatos en idéntica moneda, periodos, capital, disponibilidad y límites de riesgo. Informar tanto resultados nativos como comparaciones a riesgo equiparado cuando sean válidas.
4. Revisar sensibilidad a ventanas/umbrales vecinos, retrasos, costes, liquidez, periodos, exchanges y activos, manteniendo el presupuesto de búsqueda.
5. Evaluar variantes complejas solo si aportan una hipótesis incremental justificable y un coste razonable; realizar ablaciones.
6. Congelar el candidato/procedimiento y abrir el holdout una vez. Si no supera las condiciones predefinidas, concluir falta de evidencia o detener esa línea.

Métricas obligatorias cuando estén definidas: rentabilidad neta anualizada, Sharpe y Sortino, máximo drawdown, Calmar, Profit Factor, expectancy, turnover, exposición bruta/neta y tiempo invertido, distribución del P&L, incertidumbre y resultado por régimen. Informar además riesgo de cola, margen/capacidad y descomposición de costes. Especificar frecuencia, anualización, tasa de referencia, objetivo de Sortino y unidad de trade; no ocultar métricas indefinidas ni anualizar ingenuamente observaciones dependientes.

**Aceptación:** ensayos completos y trazables; resultados fuera de muestra con incertidumbre y corrección por selección; estrés/costes superados según el protocolo; evaluación final sin reutilización; informe con evidencia favorable y adversa. Si ningún candidato supera los criterios, se cierra con **evidencia insuficiente para operar**.

## Fase VI — Sistema y paper trading

**Objetivo:** solo después de V, proponer e implementar un sistema operativo controlado y evaluarlo prospectivamente.

Tareas previstas: arquitectura de bot; adaptadores de exchange; gestión de capital/exposición; validación de órdenes y límites de pérdidas; idempotencia y reconciliación; persistencia y recuperación; control de datos obsoletos, desconexiones y reloj; logs/alertas; parada de emergencia; simulación de fallos; paper trading con costes/fills contrastables.

**Aceptación:** evidencia de V suficiente; aprobación nueva; riesgo y arquitectura revisados; pruebas operativas completas; etapa prospectiva con duración/número de observaciones efectivos fijados de antemano, reconciliación e informe de desviaciones frente al backtest. Una simulación favorable no equivale a ejecución real comprobada.

**Puerta adicional:** operar fondos reales requiere autorización explícita separada, límites monetarios y ámbito de órdenes. No forma parte de la autorización actual ni es una consecuencia automática del roadmap.

## Riesgos y decisiones abiertas

| Asunto | Impacto | Resolución prevista |
|---|---|---|
| Acceso parcial y cobertura limitada | Algunos originales siguen inaccesibles; no todas las familias tienen contraste neto independiente | Versiones autorizadas, rastreo de citas y límites explícitos en RESEARCH §10 |
| Capital, jurisdicción, exchange y horizonte desconocidos | Viabilidad minorista solo cualitativa | Concretar en II, antes de elegir candidatos |
| Datos point-in-time y deslistados | Sesgo de supervivencia y selección | Auditar proveedores antes de aprobar III/IV |
| Cambios de microestructura y costes | Evidencia antigua puede no generalizar | Replicación temporal y pruebas prospectivas |
| Múltiples decisiones de investigación | Inflación de resultados | Registro integral y presupuesto de búsqueda |

## Registro de progreso

- **2026-10-13:** repositorio inicialmente vacío; creados documentos de gobernanza y planificación de Fase I. Consultas académicas bloqueadas por proxy 403. Guardado un borrador de acceso a dominios académicos; no demuestra acceso aplicado ni publicación. No hay código de trading, datasets de mercado, backtests ni optimizaciones. Fase I permanece abierta.
- **2026-10-13:** revisión independiente de los nueve documentos; incorporadas precisiones sobre expectativa neta, deriva de ponderaciones, financiación y falsación de momentum. Comprobados archivos requeridos y destinos de enlaces locales. Esta auditoría valida coherencia documental, no referencias externas ni hipótesis de mercado.
- **2026-10-13:** el usuario aprueba continuar la revisión de Fase I con el marco inicial. Pendiente habilitar acceso académico; el borrador conserva 14 dominios. La aceptación final de I y el inicio de II siguen pendientes y son decisiones distintas.

- **2026-10-15:** integradas recuperaciones y lecturas del 13–15 de octubre: 28 trabajos distintos con PDF disponible y lectura de secciones registrada, además de fuentes parciales. El bloqueo general inicial está superado; siguen fallos específicos. Creadas seis fichas de evidencia por bloques, cinco síntesis temáticas y seis registros JSONL. Las versiones de un mismo trabajo no cuentan como réplicas.
- **2026-10-15:** auditoría documental independiente de las fichas/síntesis confirma coherencia de costes, OOS, versiones y recuento; no es una réplica ni una validación de los cálculos publicados. Conservados resultados adversos, contradicciones y una exclusión por identidad incorrecta. Cero experimentos propios.

- **2026-10-16:** reanudación desde los archivos existentes, sin repetir búsquedas. Comprobados 17 Markdown, 48 destinos locales de enlaces, 180 registros en seis JSONL y los 38 hashes registrados en fichas frente al cache; sin errores. `git diff --check` correcto. Son comprobaciones documentales, no experimentos financieros. Consolidación guardada en un commit local para continuidad.

## Punto de reanudación — 2026-10-16

**Entregado:** preguntas científicas; protocolo reproducible de revisión; criterios no numéricos; desarrollo de las 13 familias; primer informe basado en fuentes y límites; roadmap completo. Leer [RESEARCH.md](RESEARCH.md), especialmente §§2, 7 y 10, y las fichas antes de buscar de nuevo.

**Auditoría de aceptación de I:** I.1/I.2 documentadas; I.3 comprobada con acceso parcial; I.4 parcial por las lagunas empíricas; I.5 comprobada dentro del corpus disponible, sin réplica; I.6 documentada; I.7 pendiente de revisión de esta entrega. No se cumplieron dos rondas de saturación ni el contraste independiente por familia. **Fase I permanece abierta.** No se reescriben sus criterios para declarar un cierre artificial.

**Próximo trabajo propuesto:** completar reversión/liquidez a texto completo y funding de perpetuos; buscar evidencia negociable de opciones y combinaciones; contrastes independientes y rastreo de citas. La alternativa es aceptar explícitamente una cobertura limitada para una futura comparación, dejando fuera conclusiones no sustentadas. Esa aceptación y la autorización de II siguen pendientes; no hay selección, implementación ni experimento autorizado por defecto.

**Archivos reutilizables:** fichas `docs/research/evidence-*.md`, registros `docs/research/search-*.jsonl` y cache local `/workspace/literature-cache/` con PDF/textos y hashes. La documentación en Git es el punto de continuidad; el cache es auxiliar y puede no acompañar a un nuevo entorno. Si falta un archivo, recuperar solo la versión necesaria y comprobar identidad/hash. No reiniciar la revisión entera por una interrupción.
