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
