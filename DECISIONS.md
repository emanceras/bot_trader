# Registro de decisiones

Las entradas son fechadas y conservan su justificación. Una propuesta no equivale a una decisión experimental aprobada. No se reescribirá el pasado para favorecer resultados.

## D-001 — Alcance inicial

- **Fecha:** 2026-10-13. **Estado:** adoptada; instrucción del usuario.
- **Decisión:** trabajar exclusivamente en Fase I y crear los seis documentos iniciales y el roadmap completo. El usuario revisará las conclusiones antes del siguiente paso.
- **Alternativas:** empezar por un bot o seleccionar un modelo antes de revisar evidencia. Descartadas porque anticipan la decisión e incumplen el encargo.
- **Consecuencia:** no programar estrategias, descargar series para backtests, optimizar ni conectar una cuenta en esta entrega. El diseño detallado del laboratorio y la elección de librerías quedan en III.

## D-002 — Evidencia y trazabilidad

- **Fecha:** 2026-10-13. **Estado:** adoptada.
- **Decisión:** separar teoría, referencias semilla, lectura verificada, evidencia empírica y resultados propios; exigir trazabilidad de afirmaciones decisivas a métodos/resultados consultados.
- **Alternativas:** resumir artículos de memoria como si se hubieran leído; usar resúmenes comerciales como prueba de rentabilidad. Descartadas por falta de verificabilidad.
- **Consecuencia:** no se atribuyen rentabilidades ni validaciones OOS a artículos inaccesibles. Un enlace o un DOI conocido no acredita consulta, revisión por pares ni replicación.

## D-003 — Acceso externo limitado

- **Fecha:** 2026-10-13. **Estado:** limitación observada; corrección propuesta en borrador.
- **Hecho:** solicitudes HTTPS a NBER, arXiv y Crossref fallaron con `Tunnel connection failed: 403 Forbidden`. Las comprobaciones adicionales de DOI/BIS/editoriales tampoco permitieron lectura. No hubo respuesta de artículo ni resultados bibliográficos recuperados.
- **Decisión:** continuar trabajo teórico y diseño de revisión, con estado de lectura pendiente. No llamar «exhaustiva» ni «actualizada hasta 2026» a la revisión inicial.
- **Configuración:** guardado `network.allowed_domains` con `www.nber.org`, `arxiv.org`, `export.arxiv.org`, `api.crossref.org`, `doi.org`, `academic.oup.com`, `www.bis.org`, `papers.ssrn.com`, `www.sciencedirect.com`, `link.springer.com`, `onlinelibrary.wiley.com`, `www.tandfonline.com`, `financialinnovation.springeropen.com`, `www.math.nyu.edu`. La lista custom original estaba vacía; al ampliar el borrador se conservaron sus entradas y los presets existentes. No se cambiaron scripts, secretos ni repositorios.
- **Estado real:** el backend confirmó borrador guardado y `requires_publish: true`; guardar un borrador no aplica conectividad ni publica. El usuario puede revisar y guardar los cambios en ajustes del entorno y publicar; después se deben repetir las consultas afectadas. Dominios de redirección adicionales se documentarán si hacen falta.
- **Alternativas:** sortear restricciones mediante proxies externos o desactivar TLS. Descartadas. No se han solicitado credenciales para leer literatura.

## D-004 — Orden inicial de lectura, sin seleccionar estrategias

- **Fecha:** 2026-10-13. **Estado:** propuesta para revisión del usuario.
- **Criterios:** mecanismo económico falsable, comparador sencillo, trazabilidad temporal de los datos y posibilidad de modelar costes de un particular. Son criterios de eficiencia de investigación, no estimaciones de éxito.
- **Propuesta:** empezar a leer momentum/trend, reversión simple y exposición a factores; profundizar en funding/basis y cointegración por sus riesgos identificables; tratar carteras/regímenes como hipótesis incrementales; exigir datos específicos antes de priorizar microestructura, market making y volatilidad de opciones; evaluar ML/DL frente a referencias equivalentes.
- **Alternativa:** priorizar el algoritmo más sofisticado o el mayor Sharpe publicado. Descartada porque confunde complejidad y selección retrospectiva con evidencia.
- **Consecuencia:** no hay ganadora, ranking cuantitativo ni lista de candidatos aprobada. La selección pertenece a II.

## D-005 — Reproducibilidad y control de versiones

- **Fecha:** 2026-10-13. **Estado:** adoptada.
- **Decisión:** conservar documentación en Markdown en el checkout existente, con apéndices de investigación por bloques y un protocolo explícito de búsqueda. Mantener registros completos de decisiones y resultados, incluidos nulos y fallos.
- **Alternativas:** mantener el conocimiento solo en chat, introducir ahora un framework o crear otro worktree. Descartadas por pérdida de continuidad o trabajo prematuro.
- **Consecuencia:** solo documentación en esta fase; ningún lockfile, paquete de trading o dependencia añadida. No se publican ni envían cambios remotos automáticamente.

## D-006 — Puertas de aceptación y criterios estadísticos

- **Fecha:** 2026-10-13. **Estado:** principio adoptado; parámetros experimentales aún por definir.
- **Decisión:** completar y verificar criterios por fase. Congelar antes de los experimentos universo, particiones, costes, efecto mínimo relevante, pruebas, presupuesto de búsqueda y holdout final.
- **Alternativas:** elegir primero el mejor backtest y redactar luego el criterio; abrir repetidamente el test final. Descartadas por selección y fuga de información.
- **Consecuencia:** las hipótesis iniciales son propuestas falsables, no preregistros completos ni autorizaciones de ejecución. No hay umbrales numéricos de aceptación elegidos con datos ni experimentos realizados.

## D-007 — Parámetros del operador pendientes

- **Fecha:** 2026-10-13. **Estado:** pendiente de decisión en II.
- **Asuntos:** capital, moneda de cuenta, jurisdicción, acceso a mercados, horizonte, tolerancia al drawdown, contraparte, presupuesto de datos y dedicación operativa.
- **Alternativas relevantes:** spot long/flat con menor complejidad de financiación; derivados/carry con mayor necesidad de margen y supervisión; alta frecuencia con datos/infraestructura más exigentes.
- **Consecuencia:** no se presupone acceso a cortos, comisiones institucionales, apalancamiento, préstamo gratuito ni stablecoins sin riesgo. La investigación de mecanismos puede continuar sin resolver estas preferencias.

## D-008 — Aprobación para continuar la investigación

- **Fecha:** 2026-10-13. **Estado:** aprobada explícitamente por el usuario.
- **Instrucción recibida:** «Sí, vamos a seguir, doy el visto bueno»; solicita instrucciones para habilitar las fuentes.
- **Decisión:** continuar la revisión bibliográfica dentro de Fase I conforme al marco inicial. No es necesario volver a pedir aprobación para esa lectura.
- **Límite:** no implica aceptación de la Fase I completa ni autorización de Fase II, experimentos o trading.
- **Acceso:** lectura del borrador confirma 14 dominios académicos guardados, con política restringida. Su aplicación al entorno sigue sin confirmarse; el usuario necesita revisar/guardar y publicar la configuración antes de comprobar nuevamente las consultas afectadas.


## D-009 — Acceso primario recuperado y evidencia versionada

- **Fecha de consolidación:** 2026-10-15; consultas/lecturas del 13–15 de octubre. **Estado:** comprobado en la instancia actual.
- **Hecho:** se recuperaron PDF y contenido bibliográfico de NBER, BIS, arXiv, editoriales abiertas y autores; ya no existe el bloqueo general descrito en D-003. Persisten denegaciones puntuales, rate limits y respuestas HTML que no son el texto solicitado.
- **Decisión:** utilizar contenido efectivamente obtenido, conservar errores y separar texto disponible, secciones examinadas, resumen y metadatos. Las fechas/versiones y hashes están en fichas/registros. Un WP y su publicación posterior son el mismo estudio salvo cambios que deban identificarse.
- **Alternativas:** inferir contenido a partir de un DOI/resumen o tratar HTTP 200 como PDF válido. Descartadas; EX-X01 documenta además un identificador que correspondía a matemáticas y se excluyó del corpus financiero.
- **Límite de configuración:** la conectividad observada no prueba por sí sola cómo se publicó el borrador ni que se haya validado un entorno futuro. No se guardó nueva configuración de red/scripts/secretos en esta consolidación.

## D-010 — Entrega bibliográfica acotada, sin declarar ganadora

- **Fecha:** 2026-10-15. **Estado:** informe documentado; aceptación de cobertura pendiente.
- **Decisión:** integrar 28 trabajos con lectura dirigida de secciones de PDF completos y los registros de fuentes parciales en un primer informe de las 13 familias. No proclamar exhaustividad ni finalización de toda Fase I.
- **Fundamento:** evidencia heterogénea; costes, shorts, colas, unidades de cuenta y periodo pueden cambiar la interpretación. Deducir fees no equivale a resultado neto de todas las fricciones. Predicción/valoración no equivale a estrategia y teoría calibrada no es test empírico.
- **Alternativas para el siguiente paso:** (a) completar lagunas de reversión, funding perpetuo, opciones/combinaciones y contrastes; (b) aceptar expresamente el alcance limitado antes de una futura comparación. La primera conserva la cobertura prevista; la segunda reduce alcance con incertidumbres explícitas. Ninguna permite inferir ventaja no demostrada.
- **Consecuencia:** I permanece abierta. II y ensayos no iniciados. H-00–H-14 mantienen sus criterios y estado no probado; se añaden implicaciones bibliográficas sin cambiar falsadores retrospectivamente.

## D-011 — Recuperación tras interrupciones y conservación del trabajo

- **Fecha:** 2026-10-15. **Estado:** adoptada dentro del alcance documental autorizado.
- **Decisión:** continuar desde documentos, logs y cache existentes; cerrar primero notas incompletas y actualizar el punto de reanudación. Conservar versiones locales en Git; no enviar cambios remotos sin autorización.
- **Alternativas:** repetir la investigación desde cero o depender del historial del chat. Descartadas por coste, pérdida de trazabilidad y riesgo de mezclar versiones.
- **Consecuencia:** el registro permite distinguir búsquedas completadas y pendientes. Un cache local puede no persistir en una máquina nueva: si falta, se recuperará solo lo necesario con identidad/hash, sin afirmar que toda la continuidad depende de procesos en ejecución.

## D-012 — Auditoría de coherencia y límites de verificación

- **Fecha:** 2026-10-15. **Estado:** revisión documental realizada.
- **Comprobación:** un revisor independiente dentro del equipo cotejó las seis fichas y cinco síntesis, sin nueva consulta de PDF, red ni ejecución de cálculos. Confirmó 4 DIR + 5 ML + 3 RV + 5 EX + 8 RP + 3 MET = 28 trabajos, sin contar versiones ni referencias parciales como textos adicionales. No encontró contradicciones materiales de costes, OOS o versiones.
- **Alcance:** valida consistencia de esta documentación; no verifica de nuevo cada tabla original, reproduce resultados ni demuestra ventaja financiera. Las lecturas de fuentes y sus ubicaciones están registradas por separado.
- **Comprobación operativa del 2026-10-16:** 17 Markdown; 48 destinos locales de enlaces existentes; seis JSONL con 180 registros válidos; 38 hashes de las fichas encontrados en el cache. `git diff --check` sin incidencias. Estas verificaciones no acreditan disponibilidad futura de enlaces externos ni reproducibilidad de los resultados financieros.


## D-013 — Publicación autorizada y continuación de Fase I

- **Fecha:** 2026-10-16. **Estado:** autorización explícita recibida y envío inicial comprobado.
- **Instrucciones:** el usuario respondió «Sí, envíalo» al envío del avance a `emanceras/bot_trader`. Se publicó `b468369` en `main`; el remoto confirmó el mismo hash. Después, ante la propuesta de cerrar lagunas de investigación, respondió «Adelante, revisa lo que necesites».
- **Decisión:** continuar la investigación y actualizar la documentación del repositorio autorizado, conservando versiones y verificando los envíos normales. No implica autorizar Fase II, experimentos, una cuenta financiada ni trading.
- **Consecuencia:** los cambios documentales de esta ampliación se preparan para revisión en GitHub; no se necesita volver a solicitar el acceso o envío ya autorizado en la sesión.

## D-014 — Ampliación dirigida y condición de parada explícita

- **Fecha:** 2026-10-16. **Estado:** lectura completada; aceptación de cobertura pendiente.
- **Decisión:** añadir once trabajos con secciones examinadas: REV-02/03, FUND-01/02, OPT-01–03, PORT-01–03 y CTR-01. Total 39; las versiones e identidades compartidas no se cuentan dos veces. Dos referencias antes parciales se amplían, no se convierten en estudios independientes nuevos.
- **Alternativas:** seguir acumulando artículos sin un entregable integrado, o presentar como exhaustiva una búsqueda incompleta. Se opta por una tanda acotada de dos o tres textos por laguna y un contraste, seguida de integración, con originales/replicaciones pendientes explícitos.
- **Fundamento:** se ha reducido la ausencia de métodos de reversión y perpetuos y se añadieron una estrategia de opciones con costes parciales y comparaciones de carteras con 1/N. Ninguna aportación resuelve conjuntamente todos los sesgos, costes, capital y ejecución. La ausencia de un ganador no obliga a buscar hasta encontrar uno.
- **Cierre:** se comunican límites de acceso/recursos, sin afirmar dos rondas de saturación. Esta alternativa ya constaba en el roadmap; aceptarla como cierre de la Fase I corresponde al usuario. No se rebajan retrospectivamente criterios de éxito de una estrategia ni se inicia II.

## D-015 — Costes, identidades y resultados adversos preservados

- **Fecha:** 2026-10-16. **Estado:** adoptada al integrar nueva evidencia.
- **Decisión:** mantener separados funding y convergencia, exceso sobre Treasury y financiación real, varianza implícita/realizada y P&L negociado, costes de asignar a un factor y costes internos de replicarlo. Un Sharpe alto sin capital/margen completo no decide viabilidad.
- **Correcciones trazables:** versión institucional DIR-008/REV-02 identifica autor único; He/FUND-01 no recibe el DOI de Ackerer citado en su ruta de descubrimiento; el nombre del archivo de Farag no fecha su publicación; dos descargas de opciones con extensión PDF eran HTML y quedan excluidas. Los registros originales se conservan y se añaden aclaraciones.
- **Contrastes:** la evidencia no favorece uniformemente complejidad: resultados de reversión ligados a iliquidez, costes que erosionan opciones/funding, diferencias pequeñas entre optimización y 1/N, y cambio de ranking con liquidez. Los resultados favorables también se conservan con sus supuestos. No se concluye que ningún modelo complejo pueda funcionar.

## D-016 — Auditoría de la ampliación y continuidad

- **Fecha:** 2026-10-16. **Estado:** comprobación de fuentes realizada en alcance acotado.
- **Evidencia:** revisión adicional cotejó afirmaciones decisivas de REV-02/03, FUND-01/02 y CTR-01 con PDFs locales: signos, cifras, tablas, tarifas, capital y uso del OOS. Confirmó cinco hashes y las discrepancias de reporte documentadas; no encontró errores materiales nuevos en esas comprobaciones.
- **Límite:** no es auditoría exhaustiva de 39 artículos ni réplica de resultados. Las fichas OPT/PORT declaran sus lecturas y controles por separado. Los logs que terminaban en «descargado, sin leer» recibieron eventos posteriores de lectura y cribado, sin borrar el pasado.
- **Continuidad:** se reanudaron fichas incompletas desde cache y registros tras interrupciones, sin repetir búsquedas terminadas. Ningún experimento, orden o código de trading se ejecutó.
- **Verificación documental final:** 22 archivos Markdown; 79 destinos locales de enlaces existentes; 267 registros válidos en 11 JSONL; los 55 hashes citados en fichas y ampliaciones coinciden con artefactos del cache. `git diff --check` sin errores. Los hashes incluyen textos y metadatos: no son un recuento de estudios ni una validación de rentabilidad.

## D-017 — Ampliación paralela de noticias, sentimiento y eventos

- **Solicitud:** ampliación explícita del usuario durante Fase I; **consolidación:** 2026-10-17. **Estado:** documentada, sin selección/implementación.
- **Decisión:** añadir la línea transversal a las trece familias y continuar su investigación; PORT-04 amplía carteras en paralelo. Nueve lecturas de noticias más una de carteras elevan el corpus de 39 a 49, sin sumar versiones, accesos parciales o documentación comercial.
- **Alternativas:** sustituir las familias anteriores por un bot de noticias o avanzar a II bajo aprobaciones antiguas. Incompatibles con el alcance solicitado. Se conserva el roadmap y sus puertas de aceptación.
- **Rentabilidad:** el usuario exige no imponer techo artificial. Se adopta como regla; magnitud alta o baja se evalúa con igual integridad, incertidumbre, riesgo y capacidad. Esto no elimina futuros límites de pérdida/exposición.

## D-018 — Disponibilidad temporal y valor incremental

- **Fecha:** 2026-10-17. **Estado:** criterio de investigación adoptado; protocolo experimental pendiente.
- **Decisión:** separar anticipación, reacción y riesgo; noticia original/recepción/revisiones; primera publicación macro y consenso anterior; duplicados y conocimiento del modelo. Un CAR, correlación, Granger o accuracy favorable no acredita beneficio tras recepción.
- **Alternativas:** ordenar solo por fecha editorial, usar el texto revisado actual o dar por limpio un LLM por separar precios cronológicamente. Descartadas por posible información futura.
- **Comparación propuesta:** precio, calendario, texto y combinaciones; NLP sencillo y LLM con información/riesgo/búsqueda comparables. Costes de órdenes, feed/inferencia y demora total. No se elige candidato ni se ejecuta comparación ahora.

## D-019 — Fuentes de datos: documentación frente a aptitud comprobada

- **Fecha de fuentes:** 2026-10-16; **integración:** 2026-10-17. **Estado:** evaluación documental, sin contratos ni feeds probados.
- **Decisión:** distinguir ocho fuentes con secciones oficiales examinadas y Benzinga pendiente. Las 22 páginas leídas no son estudios académicos ni evidencia de rendimiento. Tarifas y prestaciones son declaraciones fechadas de proveedor.
- **Hallazgos:** archivos BLS/Fed ayudan con publicaciones; ALFRED ofrece vintages por fecha, no recepción intradía; Trading Economics documenta consenso pero el ejemplo no prueba todos sus cortes históricos; NewsAPI no entrega texto completo y Developer demora 24 h. X tiene costes por recurso; Reddit impone condiciones de acceso/borrado. Falta validar cobertura, derechos y disponibilidad temporal de muestras concretas.
- **Alternativas:** asumir datos gratuitos equivalentes a terminales usadas por autores, o comprar un feed antes de fijar necesidad/capital. No se adoptan. No se solicitaron credenciales ni hicieron compras.

## D-020 — Consolidación, auditoría y límites de la ampliación

- **Fecha:** 2026-10-17. **Estado:** revisión documental integrada; Fase I abierta.
- **Recuento:** MAC-01/02, SENT01/02, LLM-01–03, EVT-01/02 y PORT-04. LLM-02 clasifica texto sin retorno y LLM-03 estudia acciones; no son diez evidencias de rentabilidad cripto. Mai/IMF y otras fuentes parciales siguen fuera del recuento.
- **Auditoría:** cotejo adicional de títulos/versiones y diez hashes PDF; cuatro verificaciones dirigidas de afirmaciones de SENT01, LLM-01, MAC-01 y EVT-02. Sin contradicciones materiales nuevas en ese alcance. No es auditoría exhaustiva ni réplica; cronología externa de los eventos ETF no reconstruida.
- **Límites:** macro entregó dos textos frente al presupuesto inicial de tres/cuatro por acceso/recursos. No se alcanzó saturación ni validación neta OOS de noticias con latencia realista. Se preservan los resultados favorables, nulos y adversos y discrepancias de tablas/prosa. Cerrar esta tanda no significa completar Fase I.
- **Continuidad:** fichas/cache recuperados tras interrupciones; se añaden eventos de lectura sin borrar descargas/fallos. Actualizados los seis documentos principales. La aprobación de Fase II y cualquier experimento siguen pendientes; cero órdenes y experimentos propios.

- **Verificación documental del 2026-10-17:** 29 Markdown, 116 enlaces locales (incluidas dos anclas), 17 JSONL con 393 registros válidos y 68 hashes citados en Markdown encontrados en el cache. Además se cotejaron los hashes de las 22 páginas oficiales al registrar su lectura. Sin errores detectados en estas comprobaciones; no validan resultados financieros ni disponibilidad futura de las fuentes.

## D-021 — Relaciones entre activos e interacciones: alcance acotado

- **Fecha:** 2026-10-17. **Estado:** ampliación de Fase I autorizada expresamente por el usuario; marco de revisión documentado antes de completar nuevas lecturas.
- **Decisión:** separar dos preguntas: información predictiva entre criptomonedas y mejora incremental por interacciones entre variables. Integrarlas en arbitraje estadístico/pares, factores, ML/DL, regímenes y carteras; no crear otra familia ni otorgar prioridad por el origen de la propuesta.
- **Presupuesto:** reutilizar corpus; máximo seis textos nuevos, dos por bloque de lead-lag, factores/contexto e interacciones. Por bloque: hasta seis consultas bibliográficas con ocho resultados por consulta y doce intentos de recuperar originales. Parar con la tanda o límite de acceso/recursos, sin buscar hasta confirmar una hipótesis ni afirmar saturación.
- **Alternativas:** equiparar correlación/Granger con causalidad o retorno, mezclar estrategias perdedoras esperando beneficio automático, o expandir indefinidamente universo y combinaciones. Descartadas como premisas. Los hallazgos pueden justificar posponer o descartar una línea.
- **Límites:** solo literatura pública y documentación; sin datos de backtesting, código de estrategias, entrenamiento, experimentos ni Fase II. Las puertas de aprobación previas permanecen vigentes.

## D-022 — Resultado acotado y disposición de las dos preguntas

- **Fecha:** 2026-10-17. **Estado:** cuatro lecturas dirigidas completadas e integradas; corpus 53, Fase I abierta.
- **Evidencia:** CX-01/02 sobre precedencia/redes cripto; CF-01 sobre contexto y dependencia; IX-01 sobre interacciones en acciones. No son cuatro pruebas de rentabilidad. Factores comunes, correlación condicionada y comparación OOS son cuestiones separadas; cotizar en BTC no neutraliza automáticamente su factor.
- **Límites:** referencias completas de correlación parcial y predicción cripto con ML no accesibles; resumen/metadatos no permiten certificar desaparición tras factores ni rentabilidad incremental. Se cierra con cuatro textos de un máximo de seis por acceso/recursos y pertinencia, sin afirmar saturación. Interrupciones se resolvieron desde cache, conservando búsquedas/fallos.
- **Disposición:** mantener H-23/H-24 como preguntas dentro de familias existentes, sin elegir candidatos. Posponer diseño operativo de lead-lag rápido y grafos profundos hasta demostrar información incremental y ejecución. Descartar la premisa de que mezclar reglas con media neta negativa genera beneficio automáticamente; cambios de coste/pesos/objetivo requieren otra prueba.
- **Alternativa razonada:** controles simples de sincronización, pasado propio y factores antes de añadir complejidad; mayor relevancia metodológica para distinguir señal de artefacto. No se incorpora una familia nueva ni se implementa ahora.
- **Evaluación futura:** comparaciones anidadas, aditivo no lineal, interacción preespecificada, ablaciones reentrenadas y mismo presupuesto; universo dinámico sin número arbitrario, dependencia transversal, costes/demora/capacidad. No se descargaron datasets, entrenaron modelos o ejecutaron experimentos; Fase II sigue pendiente de autorización.

- **Auditoría del 2026-10-17, relaciones/interacciones:** revisión adicional de coherencia de síntesis, hipótesis, roadmap y decisiones contra las tres fichas, y cotejo dirigido de identidad/hash, tablas, Bonferroni y objetivo de reconstrucción de CX-02. Sin errores materiales en ese alcance; precisado que los pesos de la mezcla estática suman uno. CX-01 también cotejado localmente en ecuación 2 y tablas 1–4. No fue auditoría exhaustiva ni réplica financiera.

- **Comprobación documental de esta entrega:** 33 Markdown, 144 enlaces locales (tres con ancla), 20 JSONL con 435 registros válidos y 76 hashes citados encontrados en el cache; sin incidencias. Comprobación de integridad documental, no validación económica ni verificación futura de los enlaces externos.

## D-023 — Auditoría de cobertura y criterio de materialidad

- **Fecha:** 2026-10-17. **Estado:** auditoría documental autorizada expresamente por el usuario; Fase I exclusivamente.
- **Alcance:** revisar corpus, hipótesis, fuentes y evidencia favorable/adversa después de relaciones/interacciones. Dos revisiones por bloques cubren las fichas de 53 trabajos; otras dos examinan on-chain y derivados/eventos. Auditoría interna con criterio independiente, sin atribuir independencia externa ni relectura íntegra de todos los originales.
- **Criterio:** investigar adicionalmente solo una carencia capaz de cambiar elegibilidad, validez temporal, economía/riesgo o viabilidad de datos. Familias, fuentes de información, estimadores y políticas de riesgo no son categorías equivalentes.
- **Presupuesto comunicado antes del contraste de lagunas:** por bloque, máximo tres consultas bibliográficas de hasta cinco resultados y cuatro recuperaciones públicas de originales/documentación oficial. No es necesario agotarlo; no descargar series ni conseguir resultados positivos para cerrar.
- **Alternativas descartadas:** ampliar automáticamente el catálogo, equiparar una hipótesis general con evidencia específica de toda variable, o declarar que ausencia de acceso/demostración refuta el mecanismo. Se registra cobertura parcial, se integra en familias existentes y se limita la búsqueda.

## D-024 — Dictamen de cierre limitado y condiciones posteriores

- **Fecha:** 2026-10-17. **Estado:** recomendación para revisión del usuario; cierre de I y comienzo de II no aprobados ni ejecutados.
- **Dictamen:** [coverage-audit](docs/research/coverage-audit.md) recomienda cerrar la búsqueda bibliográfica general. Los principales mecanismos están suficientemente representados para una comparación posterior condicionada; no hay evidencia propia para operar. No se exige una ganadora ni otra familia.
- **Lagunas materiales:** semántica/vintages de on-chain, población/unidades de posicionamiento, cobertura/recepción de liquidaciones y calendario/oferta/universo de tokens. No hay prueba específica incremental neta suficiente para todas ellas. Son condiciones de admisión/evaluación de preguntas existentes, no una obligación de estudiar cada indicador antes de cerrar I. Integridad del universo y margen propio serán obligatorios donde proceda, aunque no generen señales.
- **Líneas pospuestas:** ejecución rápida de liquidaciones, alpha on-chain sin histórico temporal verificable y ejecución específica DEX/AMM, MEV, staking/préstamo DeFi en esta entrega. No se afirma inviabilidad universal ni se seleccionan candidatos. El acceso/alcance futuro y una decisión concreta podrán justificar una lectura acotada.
- **Alternativas:** seguir una búsqueda general hasta saturación, o cerrar sin reconocer las lagunas. Se recomienda la alternativa ya prevista de límite explícito de alcance/acceso/recursos; aceptación del usuario necesaria. No se rebajan umbrales de estrategias, que aún no están fijados ni probados.
- **Hipótesis:** H-00–H-24 conservadas; no H-25. Se explicita H-00 como decisión sobre alternativas evaluadas, riesgo/utilidad frente a alpha y H-24 como incremento relativo a un aditivo, sin causalidad estructural automática.
- **Trazabilidad:** se detectaron logs de descarga sin eventos posteriores aunque sus fichas sí declaran lectura. Se añaden conciliaciones actuales basadas en esas fichas, identificadas como tales; sin alterar registros, fechas históricas ni simular nueva lectura PDF. El corpus permanece en 53.
- **Reapertura propuesta:** identificar decisión, fuente/pregunta y presupuesto; proceder por contradicción material o necesidad selectiva de un candidato, no por mera novedad. Fuentes parciales siguen parciales. Datos, capital, ejecución y métodos deberán verificarse antes de cualquier experimento autorizado.
- **Publicación:** actualización documental comprendida en D-013; verificación y envío normal al repositorio. No autoriza fase posterior, contratos de datos, cuentas ni órdenes.

- **Contraste de fuentes realizado:** tres consultas bibliográficas intentadas (una 429), diez resultados antes de deduplicar; seis recuperaciones de páginas oficiales, tres con contenido pertinente leído. Dos respuestas Glassnode «Page Not Found» y una portada Binance genérica no certifican sus productos/feeds. Dos preprints de dilución/unlocks permanecen solo en metadatos/resumen. Ficha `docs/research/evidence-coverage-audit.md` y registro `search-coverage-audit.jsonl`; cero originales académicos nuevos.
- **Correcciones y revisión final:** once conciliaciones DIR-001/002/006/010, RV-E01–03 y ML-06/08/09/10; RP conserva cierre agregado y no necesitaba la misma corrección. Revisión adicional del informe, ficha de fuentes y diffs principales sin errores materiales de integración; corregida una errata. Ese cotejo final no releyó cuerpos originales ni valida economía.
- **Verificación documental de la auditoría:** 35 Markdown, 167 enlaces locales (cuatro con ancla), 21 JSONL con 468 registros válidos y 84 hashes citados coincidentes con el cache; sin incidencias. `git diff --check` correcto. No se validaron todos los enlaces remotos ni datasets; estas comprobaciones no son experimentos ni pruebas de rentabilidad.

## D-025 — Cierre limitado de I aceptado e inicio de II autorizado

- **Registro/consolidación:** 2026-10-18. **Estado:** instrucción explícita del usuario: «acepto el cierre limitado de la Fase I» y «Autorizo comenzar la Fase II».
- **Decisión:** cerrar I bajo sus límites de cobertura, acceso y ausencia de saturación documentados; iniciar comparación, evaluación de viabilidad y selección documental de hipótesis candidatas. No reescribir resultados, convertir fuentes parciales en completas ni afirmar rentabilidad.
- **Aceptación:** I.7 y aceptación de las ampliaciones I.N5/I.X4 satisfechas por el usuario, con reservas explícitas. La auditoría anterior conserva su estado histórico de recomendación pendiente; esta entrada registra el cambio posterior.
- **Límites:** no laboratorio Python, descargas de datasets para backtests, implementación de estrategias, entrenamientos, optimizaciones, experimentos, paper trading u operativa real. Fases III–VI requieren nuevas aprobaciones.
- **Recursos:** aún no se han fijado capital, moneda, jurisdicción, productos/venues, apalancamiento, horizonte, drawdown, infraestructura o presupuesto. Se autorizan escenarios provisionales; no se convierten en preferencias del usuario. Las preguntas imprescindibles se agruparán al final de la entrega.
- **Publicación:** el usuario ratifica registro y envío documental a GitHub según el procedimiento previo. No hay necesidad de credenciales de exchange ni cuentas financiadas.

## D-026 — Método de comparación de Fase II

- **Fecha:** 2026-10-18. **Estado:** marco de comparación documental adoptado; selección definitiva pendiente.
- **Decisión:** cubrir H-00–H-24 y todas las líneas investigadas en matrices enlazadas de evidencia y viabilidad, con fuentes, adversos, escenarios y motivos. Distinguir indicio empírico, plausibilidad, evidencia metodológica y dimensiones no evaluables; ninguna etiqueta es una probabilidad.
- **Filtros:** mecanismo/pregunta falsable, comparador justo, datos temporalmente aptos y accesibles, coste/capital/riesgo compatibles, posibilidad de validación reproducible y esfuerzo proporcionado. Una dimensión favorable no compensa un impedimento crítico. La verificación de datos reales se reserva a la fase que se autorice.
- **Alternativas descartadas:** escoger el mayor Sharpe publicado, imponer una candidata por familia, estudiar todas las combinaciones o exigir rentabilidad marginal positiva a cada variable. Se comparan estrategias, información e interacciones sin confundirlas con diversificación de P&L.
- **Presupuesto de trabajo actual:** reutilizar la revisión y documentación existentes; ninguna nueva búsqueda bibliográfica general. Las lecturas selectivas y verificaciones comerciales posteriores deberán responder a decisiones concretas, una vez aclaradas restricciones. No se fijan tarifas actuales, proveedores aptos ni rendimientos esperados por suposición.

## D-027 — Propuesta provisional de candidatas, no autorización experimental

- **Fecha:** 2026-10-18. **Estado:** propuesta documental revisada; selección definitiva pendiente de restricciones del operador y aceptación.
- **Entregables:** [comparación completa](docs/phase-ii/COMPARISON.md), [viabilidad y universo](docs/phase-ii/FEASIBILITY.md) e [informe de selección](docs/phase-ii/SELECTION.md). Se conservan los 53 trabajos y H-00–H-24, sus nulas, fuentes parciales y adversos; no se añaden estudios ni resultados propios.
- **Recomendación:** C1/H-01 y C3/H-11/H-24 como dos preguntas primarias; C2/H-06 como comparación secundaria de riesgo. C4/H-23 y C5/H-08 quedan en reserva condicionada. Son cinco fichas de admisión, no cinco estrategias independientes ni una cartera aprobada. C3 no exige que C1 o sus inputs individuales sean rentables; su evidencia económica directa es limitada y se reserva si no caben datos, muestra y presupuesto adecuados.
- **Razones y alternativas:** menor dependencia operativa favorece estudiar momentum y la información endógena acotada; no acredita superioridad económica. Carry tiene mecanismo contractual pero exige acceso/margen/capital; relaciones entre activos exigen panel histórico y sincronización. Se posponen ejecución rápida/MM, opciones, pares complejos, DL/grafos y texto premium por coste, datos o incremento no acreditado; se conservan controles simples, comparadores y motivos explícitos para reconsiderar. No se impone cuota por familia ni rentabilidad máxima.
- **Comparaciones:** referencias comunes, individual→aditivo→interacciones y propio→factores→otros activos; ablaciones, información/riesgo/costes/presupuesto equivalentes. La mezcla de P&L no prueba interacción. Compartir datos no permite multiplicar gratuitamente variantes. El protocolo y presupuesto finitos se fijarán antes de experimentar, sin consultar ni reutilizar el holdout.
- **Universo y recursos:** escenarios S/D/E provisionales; elegibilidad histórica sin cantidad arbitraria y separación entre activos informativos y operables. Cinco grupos de preguntas al final de viabilidad: capital/moneda/riesgo, jurisdicción/venues, productos/margen, horizonte/supervisión, presupuesto. Ninguna preferencia, tarifa vigente ni aptitud de dataset se da por confirmada.
- **Revisión:** contraste documental adicional de matrices, fichas y HYPOTHESES sin errores materiales; precisados capital no duplicado si spot es colateral y universo conocido al inicio, sin selección de supervivientes actuales. Revisión interna, no réplica independiente de los estudios. Verificación de integridad documental registrada en ROADMAP.
- **Siguiente decisión:** ajustar admisión a respuestas y dependencias concretas, solicitar aceptación de la selección de II y solo entonces plantear una autorización separada para III. Laboratorio, datasets de backtesting, estrategias, entrenamiento y ensayos siguen sin autorización; contadores experimentales en cero.

## D-028 — Preferencias recibidas y decisiones que permanecen abiertas

- **Fecha:** 2026-10-18. **Estado:** instrucciones explícitas del usuario incorporadas; conformidad con C1–C5 todavía provisional, no aceptación final de II.
- **Confirmado:** USD como moneda principal; España como jurisdicción inicial; recursos informáticos personales y objetivo de automatización ordinaria con alertas/controles. USDT/USDC se valoran con conversiones disponibles entonces y riesgos propios; moneda de cuenta no sustituye moneda de liquidación ni determina obligaciones fiscales.
- **Escenarios:** 1.000/5.000/10.000 USD son referencias, sin mínimo/máximo de capital o rentabilidad. Sensibilidades ilustrativas de drawdown no son límites personales aceptados. Capital real, riesgo, exchange, producto operativo, apalancamiento y presupuesto definitivos siguen abiertos.
- **Apertura condicionada:** derivados, opciones, cortos, fuentes comerciales, cloud y todas las escalas pueden investigarse con justificación. No se autoriza operarlos, contratar ni gastar. España con exchange extranjero no equivale a otra residencia; otras jurisdicciones requieren situación jurídica legítima, sin presumir que VPN/offshore elimina obligaciones.
- **Recursos:** separar adquisición/investigación, desarrollo-validación y operación/mantenimiento. Gratuito apto primero, sin excluir comercial; tabla F/K solo aritmética de cargas hipotéticas, no cotizaciones ni rentabilidades. Facilidad técnica y potencial económico son dimensiones distintas.
- **Consecuencia:** las preferencias bastan para proponer cierre documental de II. No repetir preguntas resueltas ni exigir capital real/frecuencia favorita antes de entregar la selección; cerrar cada dependencia antes del trabajo que la necesite.

## D-029 — Horizontes por mecanismo, alcance progresivo y acceso

- **Fecha:** 2026-10-18. **Estado:** proceso propuesto para revisión; ninguna frecuencia ni experimento seleccionado mediante resultados propios.
- **Horizontes:** [HORIZONS](docs/phase-ii/HORIZONS.md) separa observación/disponibilidad, lookback, target, mantenimiento, decisión/rebalanceo, ejecución y riesgo; reestimación explícita. Escalas según mecanismo y evidencia, después datos/latencia/costes, después familia finita. Días/semanas en momentum no excluyen otros plazos justificados; segundos/minutos en lead-lag no se convierten en horas por comodidad. Spot, velocidad e infraestructura son ejes distintos.
- **Control de búsqueda:** especificación principal y sensibilidades justificadas por pregunta; exploración en desarrollo, validación del procedimiento, presupuesto de comparaciones que incluye horizontes/decisiones abandonados, y test final único. No producto cartesiano de activos/fuentes/modelos/relojes ni filtros de rentabilidad marginal que eliminen interacciones puras.
- **Tres disposiciones:** prioridad de investigación; reserva con impedimento y condición de reconsideración; construcción sin fundamento suficiente para invertir ahora. Reabrir requiere evidencia o dependencia material distinta, comparación identificable y sustitución/presupuesto explícito; nunca rescatar un holdout ni continuar solo para hallar beneficios.
- **Acceso:** [ACCESS](docs/phase-ii/ACCESS.md) documenta seis objetivos oficiales y diez recuperaciones contando rutas alternativas: tres fuentes pertinentes leídas, dos originales EUR-Lex con respuesta 202 vacía y una ruta ESMA genérica. CNMV diferencia entidad y autorización/transitorio; ESMA trata clasificación de derivados; AEAT distingue residencia real/administrativa/fiscal. Registros de lectura y hashes en `access-sources.jsonl`; no certificación de proveedor/producto ni revisión normativa exhaustiva. Son fuentes oficiales adicionales, **no nuevos trabajos académicos**.
- **Puertas:** aceptación II; autorización independiente y alcance/recursos antes de III; aptitud/licencias antes de incorporar datos; protocolo, presupuesto finito y autorizaciones antes de ensayos; capital/riesgo y acceso actualizados antes de cualquier eventual operación. El roadmap conserva estas dependencias sin ejecutarlas.

## D-030 — Propuesta final revisada de Fase II para aceptación

- **Fecha:** 2026-10-18. **Estado:** propuesta final documental entregable; cierre de II pendiente de aceptación explícita. Se mantiene cerrado el alcance general de I.
- **Selección:** C1/H-01 y C3/H-11/H-24 como preguntas prioritarias; C2/H-06 secundaria de riesgo; C4/H-23 y C5/H-08 reservas condicionadas. Las nuevas preferencias no añaden evidencia económica que justifique ascenderlas automáticamente. C5 podría cambiar de prioridad si acceso, datos, capital completo y coste de contrastación ofrecen razones materiales; no queda subordinada permanentemente por recursos desconocidos. No se declara una ganadora ni mayor potencial por facilidad.
- **Precisión de C3:** C3-I compara información combinada con referencias individuales; C3-X identifica interacción frente al aditivo no lineal a igual información. Una combinación aditiva puede ser útil sin rechazar H-11/H-24 ni justificar más complejidad. C3-I caracteriza referencias dentro del alcance previo; no añade H-25, cambia nulas ni permite multiplicar variantes. C3 no depende de éxito previo de C1 ni de utilidad marginal de todos sus inputs.
- **Fuera del alcance inicial:** primas factoriales negociadas, pares, opciones, ejecución rápida/MM, políticas complejas de regímenes, texto/NLP/LLM, fuentes adicionales y DeFi conservan razones/condiciones en SELECTION y COMPARISON. No se abre otra búsqueda general. Premisas de complejidad automática, costes omitidos, convergencia inventada o ventaja solo retrospectiva no justifican recursos.
- **Aceptación propuesta:** matriz y evidencia trazables, preferencias/escenarios diferenciados, candidatas y reservas razonadas, proceso de horizontes y dependencias explícitos. Capital real, riesgo personal, venue, infraestructura y presupuesto concretos pueden seguir abiertos hasta su puerta. Esto precisa la aceptación documental y no modifica retrospectivamente criterios experimentales: no existen resultados propios.
- **Revisión e integridad:** revisión interna adicional de selección detectó y corrigió la ambigüedad adición/interacción de C3; cotejo de fuentes oficiales y de estados vigentes. Comprobaciones finales registradas en ROADMAP. Sin réplica financiera, implementación, compras ni experimentos; publicación documental expresamente ratificada por el usuario.
- **Siguiente decisión:** el usuario revisa y acepta o solicita cambios a esta propuesta. Aceptar II no autoriza III; cada fase posterior y cualquier gasto siguen requiriendo su autorización aplicable.

## D-031 — Phase II accepted; complete Phase III authorized

- **Date:** 2026-10-18. **Status:** explicit user authorization in the attached Phase III request; final Phase II proposal at `f8f4ff8` accepted with limitations.
- **Scope:** III.A technology research and integral architecture, then III.B modular platform, quantitative laboratory, real web UI, persistence, migrations, reproducibility and synthetic technical tests. No additional approval between III.A and III.B once architecture criteria pass.
- **Boundaries:** IV–VI, market datasets for financial evaluation, financial model training/optimization/backtests, prospective market paper trading, funded accounts/live orders, production autonomous agents and expenses remain unauthorized.
- **Delivery:** code in English; new technical documentation EN canonical + synchronized ES; preserve scientific history and adverse results. Demonstrate tests A–F, install/startup and real browser integration; commit/publish authorized changes. Selection acceptance is not evidence of profitability.

## D-032 — Phase III.A architecture admission and implementation baseline

- **Date:** 2026-10-19. **Status:** architecture reviewed; III.B foundation implementation admitted under D-031, without additional user approval. This is technical design acceptance, not software or financial validation.
- **Evidence:** official-source comparisons for engines, stack and research/chart tools; EN/ES architecture and acceptance traceability cover all fifteen requested domains, nineteen III.A deliverables and twenty III.B deliverables. Source-log recovery after the environment interruption preserves original and new retrieval dates. Adopted component licensing and relevant APIs show no material unresolved blocker; exact locked-release compatibility will be verified during installation.
- **Decision:** modular Python 3.12 monolith; typed Pydantic contracts and explicit trusted module/capability registration; FastAPI HTTP adapter; SQLAlchemy/Alembic SQLite on local disk for metadata; immutable Parquet artifacts with an isolated DuckDB reader; React/TypeScript/Vite same-origin frontend; Lightweight Charts adapter with required license/NOTICE attribution. Dedicated durable finite-task worker; no broker or distributed service yet.
- **Alternatives:** PostgreSQL is a later deployment adapter, not claimed tested; Next.js SSR does not solve a current authenticated-dashboard requirement. Celery/RQ add broker operations not needed for bounded local technical jobs. MLflow/Qlib/RD-Agent remain optional future integrations, not the platform authority, autonomous execution or mutable source of reproducibility.
- **Engine:** implement only a deterministic synthetic spot-ledger contract harness. Do not build a production financial engine or add queue/margin/liquidation realism opportunistically. NautilusTrader/LEAN are later adapter alternatives behind an instrument/protocol/compatibility gate. No live-capable execution dependency or adapter is installed for III.
- **Safety and reproducibility:** technical-only runtime, immutable input/version/provenance identity, explicit failure/recovery, role and partition denial, no arbitrary import/code/SQL/URL execution. Final partitions remain inaccessible in III, even to administrators. Local bootstrap authentication requests no external credential; restart may revoke local sessions. Auth/CSRF/paths/bounds and denied modes must be tested.
- **Implementation order:** core contracts/configuration/registry/persistence first, then synthetic data/laboratory and harness, then API/worker, frontend/chart and integration. III closure requires passing essential tests A–F and reproducible startup. Historical hypotheses, adverse results and zero financial-experiment counts remain intact.

## D-033 — Compatible architectural supplement; bounded implementation

- **Date:** 2026-10-20. **Status:** user supplement integrated within III; no phase or financial authorization change. [Critical review EN](docs/en/architecture/supplement.md), [ES](docs/es/architecture/supplement.md) and targeted evidence preserve current design and C1–C5.
- **Decision:** retain the modular monolith, versioned generic repository, separate worker and six functional web sections. Add a reusable `VersionedReference` and optional frozen hypothesis associations to technical runs, resolving exact historical versions/hashes. Association does not evaluate or validate the hypothesis. No new table, framework or dependency is introduced by the supplement.
- **Boundaries:** document independent scientific, implementation, permission, environment, operational and capital states. The current Signal is a narrow synthetic quantity target. General predictions/targets/intentions, instance/session/account/portfolio ownership, virtual versus venue net positions, shared capital and reconciliation must be resolved before their first operational adapter; they are not prerequisites for today's technical lab.
- **Alternatives deferred:** operational lifecycle/decision executor, multibot allocation, risk/drift/Monte Carlo analytics, shadow/paper/testnet/live adapters, autonomous retrieval/RAG and external notifications. Structured evidence retrieval and append-only review/disposition records precede vector/graph/workflow infrastructure if a real need appears. No private-platform rules, universal promotion metrics, fixed capital allocations or extra empty pages adopted.
- **Evidence:** six directed official pages plus prior MLflow source reuse; examined scope and caveats recorded. No general scientific review repeated. LEAN documents limits of rigid Framework decomposition; Nautilus distinguishes virtual/venue positions and unknown outcomes; Freqtrade diagnostics have coverage limits; NIST CUSUM assumptions do not supply universal trading thresholds.
- **Technical corrections:** independent backend review identified stale imported-code attribution and omitted prior transformation delay. Both corrected with regression tests. Document hashes now verified on read; future-input/prefix invariance checked for the finite-window synthetic transform. These tests prove software properties, not economic advantage.
- **Continuity:** preserve published `2cf79b4` and local implementation. Original III acceptance A–F remains mandatory; final browser/install evidence and EN/ES verification are required before closure. New expenses/dependencies require applicable authorization; existing authorized locks remain the installation baseline.
