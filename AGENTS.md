# Instrucciones persistentes del proyecto

## Objetivo y alcance autorizado

Investigar un sistema cuantitativo de criptomonedas con evidencia reproducible de ventaja neta y robusta fuera de muestra. La complejidad no es un objetivo. La conclusión «evidencia insuficiente para operar» es válida.

El usuario **aceptó el cierre limitado de Fase I y autorizó exclusivamente la Fase II**: comparación, viabilidad y propuesta/selección de hipótesis para experimentación futura. Registro de la transición: D-025. No están autorizados el laboratorio de III, descargas de datasets para backtesting, implementación de estrategias, entrenamiento, optimización, experimentos, paper trading ni bot. Se necesita aprobación explícita para fases posteriores. No conectar cuentas financiadas ni enviar órdenes reales sin autorización independiente. El paper trading tampoco autoriza operativa real.

## Método y honestidad científica

- Separar fundamentos teóricos, evidencia empírica publicada, replicaciones independientes y resultados propios.
- Comprobar contenido e identidad de cada descarga: HTTP 200 o extensión `.pdf` pueden contener HTML. No inferir versión por nombre del archivo ni asociar el DOI de un artículo a una referencia citada. Al terminar una lectura, añadir evento al log sin borrar el estado histórico de descarga.
- Distinguir PDF completo disponible de lectura exhaustiva: registrar las secciones efectivamente examinadas. No contar documentos metodológicos o de acciones como evidencia empírica cripto, ni versiones como réplicas.
- Consultar fuentes primarias y registrar URL/DOI, versión, fecha de consulta y nivel de acceso: texto completo, resumen, metadatos o referencia pendiente. Nunca presentar como leído un artículo inaccesible.
- No inventar referencias, cifras, datos ni resultados; indicar límites de acceso a Internet y de cobertura temporal.
- Buscar evidencia contraria y condiciones de fracaso de cada hipótesis. No presuponer superioridad del ML, del deep learning ni de una estrategia compleja.
- Distinguir predicción estadística de rentabilidad negociable, costes omitidos de costes simulados y validación retrospectiva de evaluación prospectiva.
- Predefinir hipótesis, universo, horizonte, métricas, costes, reglas de descarte y presupuesto de búsqueda antes de los experimentos. Registrar todo ensayo, incluso fallos y resultados negativos.
- Tratar selección de artículos, activos, periodos, parámetros, variables, modelos y regímenes como posibles fuentes de sesgo.
- Reservar un holdout final con acceso controlado. Tras abrirlo, no reutilizarlo para seleccionar o corregir modelos; cualquier revisión necesitará nuevos datos independientes.
- No cambiar retrospectivamente criterios para favorecer una estrategia. Las enmiendas serán fechadas, justificadas y prospectivas.
- No convertir puntuaciones cualitativas de literatura en probabilidades de éxito. La decisión de operar requiere evidencia propia y evaluación prospectiva.

## Continuidad y control de cambios

- Leer `ROADMAP.md`, `DECISIONS.md` y las instrucciones aplicables antes de trabajar. Revisar `git status` y preservar cambios existentes.
- Utilizar el checkout existente: cada tarea cloud ya está aislada. No crear worktrees salvo petición explícita.
- Tras una interrupción, revisar el punto de reanudación, fichas `docs/research/evidence-*.md`, ampliaciones `gap-*.md` y registros `search-*.jsonl` antes de buscar. Reutilizar `/workspace/literature-cache/` si existe; no repetir consultas o lecturas completadas. Si cambia el entorno y falta el cache, recuperar solo lo necesario y verificar identidad/versión/hash. Los procesos o agentes interrumpidos no equivalen a pérdida de archivos.
- Mantener `ROADMAP.md`, `RESEARCH.md`, `HYPOTHESES.md`, `EXPERIMENTS.md`, `DECISIONS.md` y este archivo.
- Distinguir estados: **planificado**, **documentado**, **implementado**, **probado** y **validado**. Un documento redactado no valida una hipótesis; una prueba que pasa no demuestra ventaja económica.
- No marcar una fase como terminada sin comprobar sus criterios de aceptación. La Fase I inicial puede entregarse con cobertura bibliográfica pendiente claramente delimitada.
- Documentar decisiones importantes con alternativas, consecuencias y qué aprobación falta. No hacer cambios ajenos al alcance.
- No borrar resultados negativos ni sustituir silenciosamente criterios o registros de experimentos. Utilizar Git para conservar las revisiones; no hacer push ni publicar sin autorización.
- Se permite delegar revisiones bibliográficas independientes. Cada colaborador debe declarar sus fuentes y limitaciones; la integración debe comprobar referencias y evitar contar versiones del mismo estudio como evidencia independiente.

## Seguridad operativa y datos

- No solicitar ni registrar claves secretas en chat, archivos versionados, informes o logs. Para la comparación documental de Fase II no se necesitan credenciales de exchanges.
- No descargar datos privados ni contratar servicios sin autorización. Respetar licencias y condiciones de acceso.
- No habilitar trading real por defecto. Las futuras decisiones de arquitectura deberán incluir límites de riesgo, reconciliación, validación de órdenes y parada de emergencia.
- No desactivar verificaciones TLS, firmas ni checksums para sortear problemas de acceso.

## Noticias, sentimiento y eventos — ampliación de Fase I

- Mantener esta línea en paralelo a las trece familias; consultar `docs/research/news-events.md`, fichas `evidence-news-*.md`, `news-data-sources.md` y logs antes de continuar. `portfolio-followup.md` registra el avance paralelo de PORT-04.
- Distinguir anticipar, reaccionar después de recibir información y gestionar riesgo. CAR, Granger, accuracy/F1 y reducción de exposición no equivalen a P&L neto incremental.
- Exigir versiones de primera publicación, revisiones, consenso anterior, zona/DST y precisión, primera observación del proveedor y recepción local cuando existan. No inventar timestamps ni usar texto final, engagement final o veracidad conocida después como si fueran iniciales.
- Separar eventos independientes de noticias duplicadas, traducciones, actualizaciones y hilos. El agrupamiento usado para decidir debe ser causal; la evaluación debe controlar contaminación entre particiones.
- Congelar modelo/snapshot, prompts, herramientas y fecha de conocimiento conocida o desconocida. Un split cronológico no elimina contaminación del preentrenamiento; anonimización tampoco lo prueba. Declarar limitaciones y exigir posterior evaluación prospectiva.
- Comparar precio, calendario, texto y combinaciones con información/riesgo/costes/búsqueda comunes; incluir NLP sencillo antes de atribuir valor a complejidad. Incorporar demora completa, spread/impacto, costes del feed e inferencia.
- Evaluar contratos, licencias y borrados; un endpoint histórico o una promesa comercial de tiempo real no certifica versiones point-in-time o SLA de recepción. No contratar ni solicitar secretos para esta revisión.
- No imponer un límite máximo artificial a la rentabilidad. Aplicar idéntico rigor a toda magnitud, sin confundir límites de riesgo/capital con techo de beneficios. No seleccionar ganadores ni iniciar implementación/backtests en esta ampliación.
- Publicación documental autorizada en esta sesión según D-013; comprobar cambios y envío normal al repositorio. Esa autorización no permite nuevas fases, operaciones de mercado ni modificación de criterios para favorecer resultados.

## Relaciones entre criptomonedas e interacciones — Fase I

- Consultar `docs/research/cross-asset-interactions.md`, sus tres fichas y registros antes de reanudar. D-021/D-022 limitan la tanda a un máximo de seis textos; entregados cuatro con lagunas explícitas. No reiniciar búsquedas ni ampliarlas para obtener confirmación.
- Integrar en familias existentes; separar predicción entre monedas de interacciones entre variables. No priorizar propuestas por venir del usuario ni cambiar conclusiones previas para acomodarlas.
- Distinguir mismo activo entre venues de monedas distintas; sincronización/recepción, numerario, factores comunes y pasado propio preceden a atribuir incremento. Precio en BTC no equivale a neutralidad al factor BTC.
- Un modelo multivariable, importancia/SHAP, autoencoder o grafo no prueba interacción predictiva ni beneficio. Exigir comparación aditiva con mismos inputs/presupuesto y ablaciones; separar mezcla de P&L de combinación de variables.
- Universo futuro dinámico, elegibilidad conocida antes, liquidez/capacidad y bajas; ningún número de monedas arbitrario ni selección de supervivientes. La complejidad y un p-value no justifican operar. Mantener nulas, resultados adversos, criterios de posponer/descartar y todas las restricciones de Fase I.

## Auditoría de cobertura y cierre limitado

- Consultar `docs/research/coverage-audit.md` antes de proponer otra ampliación. Su recomendación histórica de cierre limitado ya fue aceptada por el usuario en D-025; las fichas conservan su fecha/alcance y no se convierten en evidencia exhaustiva. La búsqueda general de I está cerrada; II está autorizada.
- Reabrir una lectura solo si puede cambiar una decisión concreta de elegibilidad, datos, ejecución/riesgo o interpretación; indicar fuente, pregunta y presupuesto finito. Una nueva métrica o falta de ganador no justifican expansión automática.
- On-chain, posicionamiento, liquidaciones y eventos de token son fuentes/estados integrables en hipótesis actuales; no presumir alpha ni crear familias por cantidad. Exigir disponibilidad temporal, semántica y comparación incremental. Bajas/migraciones/cambios de unidades son requisitos de integridad con independencia de su uso predictivo.
- Conciliar estados de logs mediante eventos actuales que remitan a fichas previas; no alterar fechas originales ni presentar una conciliación como nueva lectura del PDF. La auditoría documental interna no equivale a revisión externa o réplica financiera.

## Fase II — comparación autorizada

- Reutilizar los 53 trabajos y H-00–H-24. Mantener trazabilidad de evidencia favorable/adversa y distinguir mecanismo, fuente informativa, estimador y política de riesgo. Las restricciones históricas de selección en las ampliaciones de I describen aquella fase; D-025 autoriza ahora la selección documental de candidatas.
- Usar criterios cualitativos explícitos y filtros no compensatorios; no puntuaciones arbitrarias, probabilidades inventadas ni techos de rentabilidad. Una candidata recomendada no está probada ni validada.
- Preferencias confirmadas en D-028: USD como moneda principal, España como jurisdicción inicial, infraestructura personal y automatización supervisable. Escenarios de 1.000/5.000/10.000 USD no son capital real ni límites. USDT/USDC no equivalen automáticamente a USD. Capital real, drawdown personal, exchange, palanca y presupuesto siguen abiertos; no repetir preguntas ya contestadas ni exigir cerrarlas para presentar la propuesta documental.
- Comparar estrategias individuales y combinación de información por separado. No excluir un input solo porque su estrategia individual pierde. Distinguir C3-I (incremento por información combinada frente a referencias individuales) de C3-X (interacciones frente al aditivo no lineal con los mismos inputs y presupuesto); una combinación aditiva útil no valida H-11/H-24 ni debe rechazarse si la complejidad falla. H-23/H-24 no reciben prioridad automática.
- Universo dinámico y conocido en cada fecha, sin fijar cantidad arbitraria ni elegir por resultados; distinguir investigación y operabilidad. Compras de datos, datasets, código de trading y fases posteriores continúan sin autorización.
- Actualizaciones documentales y publicación normal en GitHub expresamente autorizadas; conservar historial y comprobar el envío. La matriz y el informe de II no convierten fuentes anunciadas en datasets verificados.
- Consultar `docs/phase-ii/HORIZONS.md`: mecanismo, disponibilidad y fricciones preceden al horizonte; separar observación, formación, predicción, mantenimiento, decisión, ejecución y riesgo. No imponer spot lento, número de monedas, modelos o capital por comodidad ni explorar su producto cartesiano. Selección dentro del desarrollo, presupuesto finito y holdout único.
- Tres disposiciones: prioridad de investigación, reserva con impedimento y condición de reconsideración, o construcción sin justificación suficiente para invertir ahora. Facilidad no implica potencial económico. Reabrir requiere cambio material, pregunta concreta y sustitución/presupuesto explícitos, nunca búsqueda para rescatar el test.
- Productos investigables no son productos autorizados para operar. Acceso desde España se comprueba por entidad/producto/cliente; otra jurisdicción requiere situación jurídica legítima, no VPN/portal extranjero. `ACCESS.md` documenta alcance y fuentes, sin homologar venues. Gastos y apalancamiento requieren aprobación explícita.
- Separar adquisición/investigación, desarrollo-validación y coste recurrente; fuentes gratuitas aptas primero, comerciales evaluables sin contratación automática. Automatización ordinaria no requiere vigilancia humana constante, pero sí continuidad técnica, alertas y respuesta a incidentes según riesgo.
- La propuesta final revisada de II espera aceptación; D-029/D-030 definen dependencias futuras. Aceptar II no autoriza III ni ensayos; no declarar ventaja validada por aprobar documentación.
