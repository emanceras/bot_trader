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
