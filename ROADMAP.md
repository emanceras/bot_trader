# Roadmap del proyecto cuantitativo

Fecha de inicio: 2026-10-13 · Actualización: 2026-11-03 · Versión: 1.1 · Alcance autorizado: **Fase IV metodológica; sin Fase V**.

## Objetivo y estado general

Determinar si existe evidencia suficiente de una ventaja neta, robusta y viable para un operador particular. Una conclusión negativa y reproducible constituye un resultado útil. I cerrada con límites; II aceptada en `f8f4ff8`; III.A/III.B implementadas y verificadas dentro de su alcance técnico, D-031–D-034. III aceptada por el usuario; IV metodológica autorizada en D-035. V–VI y operativa siguen sin autorización. Los registros fechados anteriores conservan el estado histórico; el encabezado y el punto de reanudación indican el vigente.

| Fase | Entregable principal | Dependencias | Estado |
|---|---|---|---|
| I. Investigación | Preguntas, protocolo, revisión crítica y mapa de evidencia | Acceso a fuentes primarias | Cierre limitado aceptado por el usuario; 53 trabajos, sin saturación ni validación económica |
| II. Comparación y selección | Matriz con evidencia y candidatos falsables | I aceptada y aprobación explícita | Aceptada por el usuario en D-031, con reservas y dependencias |
| III.A Arquitectura | Investigación tecnológica y arquitectura integral EN/ES | II aceptada; fuentes técnicas oficiales | Completada y revisada; D-032/D-033, fuentes oficiales y límites |
| III.B Plataforma y laboratorio | Núcleo modular, persistencia, APIs, laboratorio sintético, web y pruebas A–F | Criterios de III.A satisfechos; ya autorizada | Implementada y probada; cierre técnico D-034, [verificación](docs/es/verification.md) |
| IV. Protocolo experimental | Registro prospectivo, particiones, costes y pruebas | II; viabilidad técnica de III; sin resultados de selección | E1/E2 aprobadas condicionalmente; A/B documentados con límites; admisión por etapas aprobada D-044; M/R ejecutados; E con correcciones D-051 y ejecución causal acotada D-053; E3/E4, instanciación/sellado pendientes |
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
| I.4 | Revisión de las 13 familias | I.2–I.3 | Por familia: mecanismo, evidencia positiva/negativa, OOS, costes, datos, sesgos y viabilidad | Documentado para las 13 familias; ampliadas las cuatro lagunas prioritarias, límites de cobertura explícitos |
| I.5 | Auditoría de bibliografía | I.4 | Identidad/versiones verificadas; afirmaciones enlazadas a fuente y ubicación; no contar preprint/publicación dos veces | Auditoría documental de cobertura realizada; conciliaciones de logs; alcance de cotejos originales limitado, sin réplica |
| I.6 | Primer informe y mapa de lagunas | I.1–I.4 | Conclusiones limitadas a lo observado; prioridades de lectura justificadas | Informe y auditoría crítica de materialidad documentados, versión 0.6 |
| I.7 | Revisión y aprobación del usuario | I.5–I.6 | Usuario acepta la cobertura o sus límites y autoriza el siguiente paso | Cierre limitado aceptado e inicio de II autorizado; D-025 |

### Ampliación paralela: noticias, sentimiento y eventos

Solicitada por el usuario; **mantiene las trece familias y sus pendientes**. Las tareas se documentan sin seleccionar estrategias. PORT-04 continúa carteras durante esta ampliación.

| ID | Tarea/dependencia | Criterio de aceptación | Estado actual |
|---|---|---|---|
| I.N1 | Preguntas y mecanismo; I.1–I.2 | Separar sorpresa, reacción, anticipación y riesgo; hipótesis incrementales falsables | Documentado en news-events y H-15–H-22 |
| I.N2 | Literatura macro/regulación, sentimiento/NLP/LLM y eventos; I.3 | Fuentes/versiones/páginas, positivos y adversos, OOS/costes/latencia; declarar carencias | Nueve lecturas dirigidas; alcance acotado, Mai/IMF y otros contrastes pendientes |
| I.N3 | Fuentes/datos; I.N1–I.N2 | Histórico, timestamps, revisiones/consenso, licencia y coste; distinguir documentación de feed probado | Ocho fuentes evaluadas documentalmente; Benzinga pendiente; no hay validación de dataset/latencia |
| I.N4 | Integración comparativa; I.4 + I.N2–I.N3 | Noticias solas e híbridos frente a precio/calendario, igual información/riesgo; conservar líneas anteriores | Integrado; PORT-04 añade continuidad de carteras, sin ranking ganador |
| I.N5 | Auditoría y revisión; I.5–I.6 + I.N1–I.N4 | Trazabilidad, límites y pendientes revisables; aceptación del usuario para cerrar alcance | Cotejo acotado realizado; límites aceptados con el cierre de I, D-025 |

### Ampliación acotada: relaciones entre criptomonedas e interacciones

Se integra en las familias existentes; no se abre otra familia ni se cambia la prioridad por iniciativa del usuario. Presupuesto previo D-021: hasta seis textos nuevos; entregados cuatro, con originales inaccesibles separados y sin búsqueda de confirmación.

| ID | Tarea/dependencia | Criterio de aceptación | Estado |
|---|---|---|---|
| I.X1 | Revisar corpus y dos preguntas; I.1–I.4 | Diferenciar predicción crosscoin e interacción, antecedentes sin duplicar | Documentado |
| I.X2 | Contraste bibliográfico; I.3 + I.X1 | Métodos/versiones, favorables/adversos, OOS/factores/ejecución y límites | Cuatro lecturas dirigidas, referencias parciales explícitas; sin saturación |
| I.X3 | Integración y evaluación futura; I.X2 | Comparadores propio/factores/otros activos e individual/aditivo/interacción; universo dinámico, ablaciones y descartes | Documentado en síntesis y H-23/H-24; no implementado |
| I.X4 | Revisión de entrega; I.5–I.6 + I.X1–I.X3 | Trazabilidad, no nuevas familias ni ganadores, límites revisables | Integrado; límites aceptados con el cierre de I, D-025 |

**Aceptación de la fase completa:** cumplir I.1–I.7 e incorporar I.N1–I.N5 e I.X1–I.X4 con sus límites expresamente aceptados. La revisión documental no exige que una fuente comercial ya esté contratada ni que un feed esté implementado; sí exige distinguir qué aptitud sigue sin verificar. Para cada familia con literatura localizable se buscarán al menos un estudio primario y un contraste independiente, además de un trabajo metodológico cuando corresponda. Esto es un mínimo de cobertura, no una garantía de exhaustividad: si no aparecen estudios o resultados negativos, se registrarán las consultas y la laguna, sin inventar evidencia. Las afirmaciones decisivas requieren lectura de métodos, costes y validación del texto completo. Una revisión con solo referencias semilla no satisface este criterio.

**Condición de cierre de la búsqueda:** dos rondas documentadas de búsqueda hacia atrás/hacia delante sin nueva evidencia material, o límite explícito de acceso/recursos comunicado al usuario. La aceptación de una cobertura limitada exige documentar qué conclusiones quedan abiertas.

### Auditoría crítica posterior a las ampliaciones

| ID | Tarea | Criterio de aceptación | Estado |
|---|---|---|---|
| I.A1 | Revisar cobertura por mecanismos, fuentes, hipótesis y adversos | Separar fuente/estimador de mecanismo; examinar las fichas del corpus completo y declarar alcance real de auditoría | Documentado en [coverage-audit](docs/research/coverage-audit.md); 53 trabajos, sin relectura íntegra de todos los originales |
| I.A2 | Examinar materialidad de on-chain, derivados, liquidaciones y eventos de tokens | Relación con familias existentes, carencia decisiva, condiciones de datos y razón para ampliar/posponer | Documentado; ninguna familia nueva ni ronda general adicional recomendada |
| I.A3 | Proponer cierre y conciliar trazabilidad | Dictamen con límites, pendientes acotados y correcciones sin alterar historia | Dictamen y conciliaciones documentados; cierre limitado aceptado en I.7/D-025 |

**Cierre vigente:** aceptado con límites explícitos en D-025; se detiene la búsqueda general. No se cumplieron dos rondas de saturación ni se dispone de réplicas netas independientes para todas las sublíneas; el usuario aceptó la alternativa de acceso/recursos prevista. Las lagunas de datos, capital y ejecución condicionan las hipótesis concretas antes de experimentar. Solo se reabrirá una lectura si puede cambiar una decisión identificada, con fuente/pregunta y presupuesto acotados. On-chain, OI, liquidaciones y eventos de oferta no obtienen prioridad por haber sido propuestos. DEX/AMM, MEV, staking y préstamo DeFi tienen cobertura insuficiente y quedan pospuestos, sin juicio universal de inviabilidad.

## Fase II — Comparación y candidatos

**Objetivo:** seleccionar un conjunto pequeño de hipótesis que merezca el coste de contrastación, sin declarar una ganadora por literatura.

Tareas y criterios de aceptación conservados; la tabla siguiente registra la propuesta de II del 2026-10-18, posteriormente aceptada en D-031:

- II.1: concretar moneda de cuenta, residencia/jurisdicción, capital investigable, mercado spot/derivados, exchanges accesibles, horizonte operativo y recursos. No hacen falta claves de cuenta.
- II.2: construir matriz por familia/estudio: calidad, mecanismo, complejidad matemática/técnica, capital y margen, datos, frecuencia, costes, colas, implementación y sobreajuste.
- II.3: aplicar filtros no compensatorios: datos históricos aptos, legalidad/acceso, costes modelables, riesgo asumible y validación reproducible. Una evidencia favorable no compensa datos inservibles o ejecución imposible.
- II.4: fijar referencias comunes —efectivo definido, buy and hold, momentum simple y reversión simple cuando sean aplicables— y ordenar candidatos por razones explícitas. Documentar alternativas descartadas.
- II.5: estimar esfuerzo, disponibilidad de datos y presupuesto de búsqueda para cada candidato. Cualquier ML necesita un benchmark simple con las mismas variables y costes.
- II.6: incluir noticias solas e híbridos en la matriz común, separados por anticipación/reacción/riesgo; comparar incremento frente a precio/calendario y modelos textuales simples. Examinar capital frente a costes fijos del feed/inferencia y demora alcanzable. No imponer un techo artificial de rentabilidad ni confundir un límite de riesgo con ese techo.

- II.7: evaluar H-23/H-24 dentro de las familias actuales, sin preferencia automática; decidir continuar/posponer/descartar por datos, incrementalidad y viabilidad. No fijar un número de criptomonedas: justificar universo operable y representativo por información histórica, liquidez y capacidad.

- II.8: elegir escalas por mecanismo, disponibilidad y fricciones, separando los relojes de información/operación; proponer proceso finito de exploración, validación y test final. Mantener prioridad, reserva con condición y construcción sin justificación diferenciadas; capital o sencillez no son límites al potencial económico.

- Aplicar a II.2–II.5 el dictamen de cobertura: distinguir variables opcionales on-chain/posicionamiento/eventos de los requisitos obligatorios de universo, cambios de token y margen. Si una hipótesis depende de ellas, verificar definición, disponibilidad histórica y coste antes de admitirla; posponerla si no puede comprobarse. Esta condición está documentada, no ejecutada; no obliga a añadir candidatos ni a investigar todos los indicadores.

**Aceptación:** matriz trazable; requisitos del operador documentados; hipótesis primarias/ secundarias diferenciadas; lista de candidatos y descartes razonada; aprobación del usuario. Ni puntuaciones arbitrarias ni probabilidades de éxito inferidas de etiquetas cualitativas.

| Tarea | Progreso comprobable | Pendiente para aceptar II |
|---|---|---|
| II.1 | [FEASIBILITY](docs/phase-ii/FEASIBILITY.md): USD/España, recursos personales y escenarios 1.000/5.000/10.000; capital/riesgo reales abiertos deliberadamente, con puertas | Aceptar que estas decisiones pueden esperar al trabajo que dependa de ellas; no repetir las preguntas resueltas |
| II.2 | [COMPARISON](docs/phase-ii/COMPARISON.md): dos matrices cubren H-00–H-24 y trazan los 53 trabajos; preferencias incorporadas | Aceptación documental; ninguna rentabilidad propia |
| II.3 | Filtros de datos, costes, capital, riesgo y reproducción; [ACCESS](docs/phase-ii/ACCESS.md) distingue entidad/producto y situación jurídica | Aceptar dependencias explícitas; ningún venue/dataset homologado. Su aptitud se verificará antes de comprometer o usar el componente dependiente |
| II.4 | [SELECTION](docs/phase-ii/SELECTION.md): C1/C3 prioritarias propuestas, C2 secundaria, C4/C5 reservas; referencias, adversos y reconsideración razonados | Aceptación de la propuesta final; no admisión experimental automática |
| II.5 | Tres niveles de recursos, costes separados y sensibilidad F/K; capitales sin mínimo/máximo | Presupuesto concreto antes del trabajo/gasto dependiente; protocolo y presupuesto de contrastes en IV |
| II.6 | Noticias solas, híbridos y riesgo por eventos comparados; latencia, versiones y gasto fijo explícitos | Reabrir solo una cuestión de fuente que cambie admisión; líneas primarias textuales pospuestas |
| II.7 | H-23/H-24 diferenciadas; C3-I informativa y C3-X interacción, sin cambiar nulas; universo dinámico y ablaciones | Alcance informativo/operable y datos antes de protocolo, sin número arbitrario ni filtro de rentabilidad marginal |
| II.8 | [HORIZONS](docs/phase-ii/HORIZONS.md): escalas justificadas, relojes separados y proceso prospectivo finito | Aceptar proceso; valores, multiplicidad y particiones se congelarán antes de ensayos autorizados |

**Estado de aceptación vigente:** II aceptada en D-031, junto con autorización separada de III.A/III.B. La tabla conserva los pendientes de aquella propuesta; su aprobación documental ya está resuelta. Capital real, exchange y riesgo definitivo siguen abiertos hasta el trabajo que dependa de ellos. Las cinco fichas no acreditan rentabilidad ni autorizan experimentación financiera.

## Fase III — Plataforma y laboratorio cuantitativo

**Objetivo:** implementar una única plataforma modular verificable, con núcleo, persistencia, laboratorio sintético y web reutilizable, bajo la solicitud de III completa. [Solicitud conservada](docs/phase-iii/REQUEST.es.md), [arquitectura EN](docs/en/architecture/platform.md), [arquitectura ES](docs/es/architecture/platform.md) y [matriz de aceptación](docs/phase-iii/acceptance.md). III.A y III.B autorizadas; no se necesita permiso adicional entre ellas. IV–VI permanecen excluidas.

| Etapa | Entregable/criterio | Estado comprobado 2026-10-21 |
|---|---|---|
| III.A.1 | Diagnóstico y revisión de restricciones/ciencia | Completado; preservadas ciencia, prioridades y autorizaciones |
| III.A.2 | Comparación oficial de motores, stack, investigación IA y gráficos; licencias | Completada con alcance/recepciones/hashes; inventarios de dependencias y atribución |
| III.A.3 | Arquitectura de quince dominios, contratos, seguridad, persistencia, web y plan | Admitida D-032; complemento crítico de 21 capacidades, D-033, sin nuevos frameworks |
| III.B.1 | Contratos, configuración, módulos, permisos, migraciones y repositorios | Implementado y probado; referencias inmutables y aislamiento técnico |
| III.B.2 | Datos sintéticos, hipótesis, transformaciones, jobs, resultados e interfaces | Implementado y probado; 25 hipótesis originales, fallos persistidos, sin evaluación financiera |
| III.B.3 | API/worker, web real y gráficos reutilizables | Implementado y probado en navegador con servicios reales; seis secciones, quince estados de módulo |
| III.B.4 | Pruebas A–F, instalación/arranque, calidad, seguridad, recuperación y reproducibilidad | Superadas en alcance técnico; 110 pruebas Python, 7 frontend, 2 navegador; restauración verificada |
| III.B.5 | Documentación EN/ES, inventario operativo/preparado/futuro y publicación | Entregada con [verificación](docs/es/verification.md), límites y gates posteriores |

La [matriz de cobertura complementaria](docs/es/architecture/supplement.md) clasifica capacidades A/B/C/D y conserva las 14 pruebas propuestas como verificadas en alcance técnico o pospuestas expresamente. No se implementan capital compartido, bots operativos ni transiciones de producción como requisito ficticio del laboratorio. La incorporación futura exige resolver identidad, propiedad contable, permisos, conciliación y semántica de señales antes del primer adaptador dependiente.

Cobertura objetivo para futuras fases: el catálogo, calidad, trazabilidad, transformaciones, trabajos e informes ya funcionan con fixtures; las capacidades financieras siguientes siguen condicionadas a su admisión:

1. Ingesta y catálogo: fuentes, licencias, timestamps de evento/recepción/publicación, símbolos históricos y acciones de tokens; almacenamiento versionado y hashes, sujeto a licencias y obligaciones de borrado. Para noticias: primera versión/recepción, revisiones, consenso anterior y agrupación de eventos; no conservar contenido prohibido por su licencia.
2. Calidad: ausencias, duplicados, husos horarios, datos fuera de orden, revisiones, velas imposibles, unidades, cambios de contrato, exclusiones y activos deslistados.
3. Variables y señales: disponibilidad real, transformaciones ajustadas solo en entrenamiento y contratos explícitos entre módulos.
4. Estrategias y cartera: posiciones objetivo, exposición, capital, rebalanceo y benchmarks comunes.
5. Backtest/ejecución: orden temporal, órdenes/fills, comisiones, spread, slippage, impacto, financiación, margen y liquidaciones cuando apliquen.
6. Riesgos y métricas: resultados comparables, incertidumbre, colas, exposición, capacidad y descomposición del P&L.
7. Experimentos e informes: configuraciones inmutables, versiones de código/datos/entorno, semillas, resultados y fallos; gráficos con datos auditables.

**Aceptación comprobada:** [registro de criterios](docs/phase-iii/acceptance.md) y [evidencia EN/ES](docs/es/verification.md) vinculan los 19 entregables arquitectónicos, 20 de implementación y pruebas A–F. Instalación/arranque, persistencia, conservación de caja/inventario/costes sintéticos, causalidad temporal, módulos sustituibles y web real comprobados. Esto verifica el laboratorio técnico; no reconstruye P&L de mercado ni valida una ventaja. La contabilidad financiera completa y el motor se admitirán antes de experimentos autorizados.

## Fase IV — Metodología experimental

**Objetivo:** congelar el diseño antes de ejecutar los ensayos que decidirán candidatos. IV metodológica autorizada en D-035; E1/E2 de `ba6c20b` aprobadas condicionalmente en D-038. [Protocolo EN](docs/en/phase-iv/protocol.md) / [ES](docs/es/phase-iv/protocol.md) y tareas originales conservados. La [matriz de aceptación](docs/es/phase-iv/acceptance.md) distingue aprobación condicionada, E3/E4 y vinculaciones todavía pendientes: no hay holdout financiero sellado ni autorización de V.

Tareas y criterios originales conservados:

- IV.1: fijar universo point-in-time, fuentes, periodo, moneda de cuenta, elegibilidad por liquidez conocida entonces y tratamiento de desapariciones. Separar exploración autorizada de evaluación final.
- IV.2: particiones cronológicas y walk-forward; intervalos exactos decididos por longitud de muestra, horizonte de señales y suficiencia de regímenes, sin mirar el rendimiento del holdout.
- IV.3: purga de observaciones cuyos intervalos de etiquetas se solapen; embargo definido según horizonte informativo y dependencia cuando proceda. No usar cross-validation aleatoria para series financieras.
- IV.4: sellar holdout final: manifiesto con intervalos y hashes, responsable de acceso, comando/registro de apertura y una sola evaluación confirmatoria del procedimiento congelado. Si se usa para rediseñar, pasa a desarrollo y se necesita un nuevo holdout.
- IV.5: hipótesis, tamaños de efecto económicamente relevantes, criterio primario, métricas secundarias, parámetros/candidatos máximos, reglas de descarte y condiciones de parada.
- IV.6: costes por exchange y nivel alcanzable, escenarios de estrés, disponibilidad de préstamos, funding conocido en su momento y límites de participación. Evitar contar spread, slippage e impacto dos veces.
- IV.7: incertidumbre con bootstrap temporal apropiado; dependencia/colas; múltiples pruebas y selección; Deflated Sharpe Ratio como diagnóstico condicionado a sus supuestos; pruebas de sensibilidad y de regímenes definidos sin futuro.
- IV.8: congelar registro, configuración y criterios; fechar y justificar cualquier enmienda antes de usar datos nuevos.
- IV.9: para noticias, joins por disponibilidad, particiones por grupos de eventos/duplicados y etiquetas solapadas; primeras publicaciones y consenso versionado. Congelar NLP/LLM, prompts, herramientas y conocimiento previo; registrar incertidumbre del preentrenamiento. Definir ablaciones precio/calendario/texto y estrés de demora/correcciones antes de resultados.

- IV.10: si se seleccionan estas hipótesis, comparar propio→factores→otros activos e individual→aditivo→interacción con presupuesto común; reestimar universo/grafo/factores solo dentro del desarrollo. Bloquear fechas compartidas entre activos, controlar etiquetas solapadas y dependencia transversal; probar ablaciones y demora sin consultar holdout.

- IV.11: concretar el proceso de horizontes de II: reloj informativo, lookback, target, mantenimiento, rebalanceo, ejecución y riesgo; familia finita motivada y sensibilidades. Registrar todos los horizontes y ajustes descartados en desarrollo; validación del procedimiento completo y test final único. No ralentizar una señal ni elegir intervalos por rendimiento retrospectivo sin contabilizar selección. USD, conversiones y escenarios de capital/riesgo serán comunes en los comparadores pertinentes.

**Aceptación:** diseño reproducible y aprobado; ninguna decisión dependiente de resultados ocultos; presupuesto de pruebas trazable; holdout inaccesible por defecto; costes y rechazo definidos. No se aceptan umbrales elegidos tras ver qué estrategia pasa.

### Entrega metodológica y pendientes — 2026-10-24

IV.1–IV.11 tienen especificación trazable en [protocolo](docs/es/phase-iv/protocol.md), [candidatas](docs/es/phase-iv/candidates.md), [datos/costes](docs/es/phase-iv/data-execution.md) y [métodos/fuentes](docs/es/phase-iv/method-evidence.md). 26 especificaciones base no son 26 ajustes totales: folds, semillas, escenarios y recursos deben enumerarse antes de lanzar. La [plantilla de congelación](docs/phase-iv/freeze-template.json) contiene valores pendientes explícitos y `execution_ready=false`; no es esquema ejecutable ni permiso.

**Aceptación no satisfecha aún de forma incondicional:** E1/E2 ya aprobadas; faltan E3/E4, fuentes/periodos, márgenes económicos/riesgo, parámetros/costes, presupuesto total, motor/inferencia técnicamente admitidos, revisión del prerregistro concretado y custodia/sellado efectivo. No se rebajan criterios ni se pide otra vez E1/E2. El [informe de viabilidad](docs/es/phase-iv/feasibility.md), D-039, precede a la autorización A/B de D-040. La [auditoría técnica](docs/es/phase-iv/admission.md) registra los dos archivos Q3 adquiridos, QA externo y pruebas sintéticas de Nautilus 1.231.0 aislado, con negativos y límites. No equivale a admisión financiera, integración de producción ni cierre de IV. E3/E4 siguen sin cifras inventadas; Q3/Kraken no limita el histórico futuro.

**Dependencia estadística explícita:** la suficiencia basada en retornos netos pareados necesita desarrollo financiero autorizado; auditoría estructural y pruebas sintéticas no la demuestran. El informe identifica la tensión de exigir todas las vinculaciones antes de cualquier ejecución y propone revisar posteriormente una admisión por etapas. No se adopta enmienda ni se ejecuta piloto financiero bajo el nombre de QA.

**Revisión posterior a d70e6bc, 2026-10-27:** [informe EN](docs/en/phase-iv/evolution.md) / [ES](docs/es/phase-iv/evolution.md), D-042/D-043, con seis anexos de fuentes, contratos temporales, información externa, dependencias, motores y admisión por etapas. Propone trazabilidad multirresolución/multiasset futura, comparación de Nautilus y LEAN, pruebas aisladas M/E/R y adquisición H acotada posterior. No selecciona proveedor/motor definitivo, no instala ni actualiza dependencias y no ejecuta las pruebas propuestas. El protocolo y la aceptación vigentes permanecen intactos; la secuencia estadística requiere revisión explícita antes de aplicarse. No se añaden experimentos, mercados ni intervalos a las 26 especificaciones.

**Aprobación posterior y alcance técnico, 2026-10-28:** D-044 registra la [enmienda T/D/U/V/F](docs/es/phase-iv/staged-amendment.md) aprobada metodológicamente por el usuario. Cambia el momento de completar vinculaciones dependientes; conserva economía prospectiva, E1/E2, 26 especificaciones, independencia y acceso. D/U siguen sin permiso financiero. D-045 entrega [paquetes M/E/R](docs/es/phase-iv/technical-packages.md) con versiones, casos sintéticos, recursos y paradas; aún sin permiso ni ejecución. No se instala, modifica producción ni amplía la tanda.

**UX futura registrada antes del desarrollo metodológico:** UX-01 resúmenes/tabla y auditoría desplegable; UX-02 glosario especializado EN/ES; UX-03 guía completa que siga capacidades reales; UX-04 ayuda contextual/accesibilidad e integración. [Plan EN](docs/en/ux-evolution.md) / [ES](docs/es/ux-evolution.md), con dependencias y aceptación. Sin código, secciones ficticias ni nuevas dependencias; no bloquea IV. Verificación Windows permanece separada y no realizada.

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
| Acceso parcial y cobertura limitada | Algunos originales siguen inaccesibles; no todas las familias tienen contraste neto independiente | Aceptación de límites; recuperar una fuente solo si cambia una decisión concreta, sin nueva búsqueda general |
| USD/España confirmados; capital real, riesgo, exchange, horizonte y presupuesto abiertos | Admisión experimental y operabilidad aún condicionadas | Puertas concretas en SELECTION/FEASIBILITY; valores antes del trabajo dependiente, sin bloquear propuesta documental |
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

- **2026-10-16:** el usuario autoriza enviar el avance; se publicó `b468369` en `origin/main` y se comprobó igualdad con el commit local. Posteriormente autoriza continuar la revisión de las lagunas de Fase I: «Adelante, revisa lo que necesites».
- **2026-10-16:** completada ampliación de once trabajos con lectura dirigida: dos de reversión, dos de perpetuos, tres de opciones, tres de carteras y un contraste direccional. Total 39 trabajos con texto y secciones examinadas. DIR-005/008 pasan de acceso parcial a versiones completas identificadas; no cuentan doble. Cinco fichas de ampliación y cinco registros adicionales conservan recuperaciones, exclusiones, lecturas y límites.
- **2026-10-16:** revisión independiente de afirmaciones decisivas de REV-02/03, FUND-01/02 y CTR-01 contra PDF confirmó cifras, versiones y distinción entre costes parciales y completos. Se añadieron eventos finales de lectura donde los logs solo indicaban descarga. Opciones/carteras se consolidaron desde el cache sin repetir búsquedas, con hashes y alcance explícitos. Ningún experimento propio.
- **2026-10-16:** integración final comprobada: 22 Markdown, 79 destinos locales de enlaces, 267 registros JSONL y 55 hashes de artefactos citados; sin errores documentales detectados. Las verificaciones no equivalen a réplica o validación financiera. Preparada la actualización del informe v0.3 y del repositorio autorizado para revisión.

## Punto de reanudación vigente — E1/velas, 2026-11-03 UTC

**D-052/D-053:** [informe EN](docs/en/phase-iv/bar-execution.md) / [ES](docs/es/phase-iv/bar-execution.md), [recibos](docs/phase-iv/technical-results/E-bars/README.md). Ejecutados seis grupos, quince contextos nativos y135 comprobaciones; sin correcciones ni descargas. Se reproduce el cierre100.50 sin latencia y el cierre siguiente112 con1 ms, nunca una apertura garantizada. Canarios de timestamps y cuatro invariancias de la frontera causal correctos. Apertura anterior a decisión omitida; ejecución posterior111.05 o ninguna sin evento elegible. Cotizaciones sintéticas explícitas; no bid/ask observado ni admisión financiera.

El alcance técnico acotado queda entregado. No repetirlo tras interrupciones. Siguiente dependencia: integración temporal de producción y contrato de precios/costes/capacidad y ciclo de órdenes del futuro runner, con alcance específico antes de ampliar implementación. Lado vendedor, parciales/cancelación integrada, recuperación y fuentes reales siguen sin admisión por estas pruebas. Nautilus candidato condicional; criterios de IV, E3/E4 económicos,26 especificaciones y prohibición de V/paper/live conservados. No se añade una nueva tanda científica.

## Punto de reanudación histórico — corrección E3-L2/E4, evidencia 2026-11-02–03 UTC

**D-050/D-051:** [informe EN](docs/en/phase-iv/engine-correction.md) / [ES](docs/es/phase-iv/engine-correction.md), [evidencia](docs/phase-iv/technical-results/E-correction/README.md).6pruebas de12;4nativas/2supervisor,2preparaciones, sin descargas. E3-L2 correcto en componente; remanente mercado2 no reservado ni completado con el nuevo snapshot, cancelación explícita verificada. E4 evita duplicado y conserva historial/contabilidad con reserva legítima de limitada abierta, pero total6/dosfills original incumplido. Consolidación artificial solo supervisor17/17;32checks originales27correctos/5negativos conservados. Correcciones porbloqueo consumidas; detener rutaE4 dependiente sin rescatar su expectativa. Próximo requisito mínimo: E1 y contrato de ejecución causal para velas, independiente de exigir L2 o recuperación live. Ningún motor ni ledger financiero admitido; producción/E3/E4económicos/V intactos.

## Punto de reanudación histórico — recuperación E, 2026-11-02

**D-048/D-049:** [informe EN](docs/en/phase-iv/engine-recovery.md) / [ES](docs/es/phase-iv/engine-recovery.md), [evidencia y continuación](docs/phase-iv/technical-results/E-recovery/README.md). Nautilus rc7 instalado con CPython3.13.16 estándar; nueve casos funcionales ejercitados parcialmente y cuatro diagnósticos. Contabilidad E2 correcta en alcance; L1 excede cantidad visible, L2 mercado bloqueado por precio de referencia, E4 diverge orden/fills y deja reserva. Tres cortes y reconstrucción determinista comprobados a posteriori, sin conciliación antes de actuar. Un ciclo correctivo usado solo para E2; no repetir ni ampliar por inercia. E6 no ejecutado, ningún motor plenamente admitido; E3/E4 y V pendientes. Producción intacta. M/R y LEAN anteriores no repetidos. Nueva corrección del puente requiere un alcance separado; no una revisión general.

## Punto de reanudación histórico — ejecución M/R/E, 2026-11-01

**Autoridad:** D-046 conserva aprobación expresa de ejecutar los tres paquetes de `fa435a4`, sin otra solicitud de permiso. [Resultados EN/ES](docs/es/phase-iv/technical-results.md) y [checkpoint reproducible](docs/phase-iv/technical-results/PROGRESS.md). No repetir adquisiciones ni pruebas ya ejecutadas tras interrupciones.

**Ejecutado:** M, 20 casos específicos y 110 pruebas backend en cada entorno; R, 160 comprobaciones. Pasan dentro de su alcance sintético, con pérdida zoned-ns detectada en DuckDB y ausencia de objetos históricos locales delimitadas. Producción no se migra. E no puede declararse completado mientras no se ejecuten sus casos: Python3.13.18 no disponible por la ruta uv fijada; LEAN compiló y ejecutó tres casos de componentes: uno parcial y dos con comparación obligatoria fallida. Veintitrés slots E sin ejecutar, cero casos plenamente admitidos. No hay motor seleccionado. Auditoría final sin cambios de producción; recursos dentro de límites. Consultar recibos y bloqueos en el checkpoint, D-047.

**Continuidad:** E3/E4, adquisiciones financieras, migración de producción y Fase V requieren decisiones independientes. E1/E2, 26 especificaciones, T/D/U/V/F, corpus53, H-00–H-24, negativos A/B y UX futura se conservan. Siete contadores financieros en cero. Las pruebas no seleccionan una estrategia rentable ni cierran IV incondicionalmente.

## Punto de reanudación histórico — 2026-10-28

**Estado:** aprobada y registrada la admisión metodológica T/D/U/V/F, D-044; protocolo v3, aceptación v5 y plantilla documental revisión 4. [Propuesta técnica M/E/R](docs/es/phase-iv/technical-packages.md) y [checkpoint](docs/phase-iv/technical-packages/PROGRESS.md), D-045. No ejecutada. Nautilus rc7 requiere Python 3.13 sin Arrow obligatorio; M es independiente del motor. Se comparará rc7 con LEAN fijado por commit solo si se autoriza el alcance, sin ganador anticipado.

**Siguiente decisión material:** autorización de las pruebas técnicas acotadas propuestas; no volver a pedir el principio T/D/U/V/F. Un alcance conjunto M/R/E permite implementar harnesses aislados y probarlos con los límites publicados, sin otra revisión general. No descargar software de los paquetes ni ejecutar casos antes del permiso. Cambios de versiones/techos/alcance, adquisición financiera, producción o fases posteriores requieren decisión aparte.

**Continuidad:** E3/E4, datos/ejecución financieros y V pendientes; siete contadores cero. Reutilizar archivos/metadatos conservados tras interrupciones. Comprobaciones documentales no son pruebas M/E/R. Mantener 53 trabajos, H-00–H-24, prioridades, 26 especificaciones, negativos A/B, UX y producción. La plantilla conserva flags falsos y manifiestos sin instanciar.

## Punto de reanudación histórico — revisión de evolución del 2026-10-27

**Estado:** revisión documental solicitada desde `d70e6bc` entregada en [evolution.md](docs/es/phase-iv/evolution.md), seis anexos EN/ES y [checkpoint](docs/phase-iv/evolution/PROGRESS.md). Se conservan resultados A/B, 53 trabajos, H-00–H-24 y siete contadores financieros en cero. Producción, protocolo, plantilla, aceptación y UX intactos. IV sigue condicionada; E3/E4 y V pendientes.

**Siguiente trabajo/decisión:** revisar el principio propuesto de admisión por etapas, sin confundirlo con autorización financiera. Preparar manifiestos exactos de versiones/recursos para las comprobaciones técnicas mínimas M/E/R que resuelvan incertidumbres decisivas y obtener su alcance antes de instalarlas/ejecutarlas; no se ha elegido una frontera de proceso ni un motor. Una adquisición H necesita fuentes, campos, cobertura, derechos, tamaños y presupuesto concretos antes de autorización. E3/E4 dependen de esa evidencia; no inventar cifras ni repetir E1/E2/A/B. No son tareas pendientes dentro del alcance documental ya completado.

**Continuidad:** reutilizar lecturas y registros; no reiniciar el estudio ni ampliar proveedores indiscriminadamente. La arquitectura puede evolucionar a otros mercados y fuentes, pero el ejemplo de apertura de Nueva York no añade una hipótesis, duración ni experimento. Las pruebas sintéticas propuestas aún no están ejecutadas. Datos voluminosos y entornos aislados permanecen fuera de Git; no descargar, instalar o activar operaciones por una petición genérica de continuar.

## Punto de reanudación histórico — auditoría del 2026-10-26

**Estado:** III aceptada; E1/E2 de IV aprobadas condicionalmente, D-038. A/B autorizados en D-040 y resultados efectivos en el [informe técnico EN](docs/en/phase-iv/admission.md) / [ES](docs/es/phase-iv/admission.md) y [checkpoint](docs/phase-iv/admission/PROGRESS.md). Se conservan adquisición, fallos y mediciones. Sin cambios de producción, ensayos financieros ni apertura de holdout. IV continúa condicionada; E3/E4 pendientes.

**Siguiente trabajo/decisión:** resolver las lagunas concretas de fuentes y ejecución mediante una propuesta finita de cobertura histórica comparativa y adaptador versionado; cualquier adquisición adicional o integración fuera de A/B requiere su alcance autorizado. Preparar E3/E4 con costes/cobertura reales y revisar expresamente la posible admisión separada de desarrollo frente a validación/final. QA estructural y simulación sintética no dan precisión de retornos pareados. No pedir otra vez E1/E2/A/B, inventar capital/márgenes ni anticipar autorización de V.

**Continuidad:** conservar 53 trabajos, H-00–H-24 y negativos; siete contadores financieros en cero. UX/glosario/guía futura intactos; aplicación III sintética intacta. Datos voluminosos y entornos desechables fuera de Git. El histórico futuro buscará máxima cobertura útil, fiable y económicamente razonable entre ciclos/proveedores y activos desaparecidos, sin fijar trimestre/venue por esta auditoría. No repetir lecturas, instalar alternativas, adquirir más datos, realizar compras o certificar Windows por implicación.

## Punto de reanudación histórico — consolidación del 2026-10-17

**Entregado:** preguntas y protocolo; criterios de evidencia; revisión de 13 familias y línea transversal de noticias; 53 textos con lectura dirigida, fuentes parciales diferenciadas y resultados adversos; roadmap completo. La síntesis vigente es [RESEARCH.md](RESEARCH.md), §§2, 6–7 y 10. Las notas `gap-*.md` amplían las fichas originales sin borrar sus versiones ni fallos.

**Auditoría de aceptación vigente:** I.1/I.2 documentadas; I.3 comprobada con acceso parcial; I.4 cubre los mecanismos con evidencia desigual; I.5 auditada documentalmente con conciliaciones, sin réplica; I.6 incluye dictamen crítico de cobertura y materialidad. Se recomienda cierre limitado sin más búsqueda general. I.7 y aceptación de límites pendientes. No se cumplieron dos rondas de saturación. **La Fase I no se declara finalizada ni se inicia II.** La insuficiencia de evidencia neta es una conclusión válida; no se exige encontrar un ganador para cerrar una revisión.

**Entrega vigente:** noticias y relaciones/interacciones ya integradas; auditoría posterior en [coverage-audit](docs/research/coverage-audit.md). Se entregan síntesis, fichas, documentación de fuentes de datos e hipótesis para revisión, sin datasets de backtesting. No se presupone aceptación ni inicio de II. Las referencias pendientes —entre ellas DIR-007/013, Cederburg y métodos originales— siguen identificadas; no se les atribuyen resultados no leídos ni se convierten en una lista obligatoria de nuevas búsquedas. La condición de cierre no cambia.

**Próxima fase, aún sin autorización:** II concretaría capital, moneda, jurisdicción, exchanges/productos accesibles, frecuencia, tolerancia al drawdown y presupuesto de datos; después compararía hipótesis por criterios explícitos. III/IV deberán preparar laboratorio y protocolo antes de cualquier ensayo. No hace falta cuenta financiada ni claves para decidir II.

**Continuidad:** reutilizar `evidence-*.md`, `gap-*.md` y `search-*.jsonl`. Cache auxiliar `/workspace/literature-cache/`; comprobar versión/hash si falta un archivo y hay que recuperarlo. No reiniciar búsquedas ya resueltas, ni contar como texto examinado un PDF solo descargado o un HTML con extensión `.pdf`. Documentación en Git y actualización normal del remoto autorizado; ninguna orden de mercado programada.

## Progreso de la ampliación de noticias

- **2026-10-16–17:** integrados nueve estudios con lectura dirigida y un contraste adicional de carteras (PORT-04); corpus de 49. Evaluadas secciones relevantes de 22 páginas oficiales de datos, fuera del recuento académico. Actualizados preguntas, matriz transversal, H-15–H-22 y tareas de II/III/IV; sin implementarlas.
- **2026-10-17:** auditoría acotada de identidad/hash de diez originales y afirmaciones decisivas de cuatro estudios de noticias; sin contradicciones materiales nuevas en los cotejos. Se conservan discrepancias de fuentes, resultados adversos y accesos parciales. No equivale a réplica ni cierre de toda la fase.
- **Siguiente trabajo dentro de I:** revisar las entregas acotadas y sus lagunas, incluidas consenso/recepción, control exacto de factores e interacciones netas OOS. Priorizar una nueva lectura solo si puede cambiar una decisión y cabe en un límite explícito; no prolongar la revisión para conseguir confirmación. No reiniciar búsquedas completadas ni buscar hasta obtener una ganadora. Fase II sigue pendiente de aprobación explícita.

- **Verificación documental del 2026-10-17:** 29 Markdown, 116 enlaces locales (incluidas dos anclas), 17 JSONL con 393 registros válidos y 68 hashes citados en Markdown encontrados en el cache. Además se cotejaron los hashes de las 22 páginas oficiales al registrar su lectura. Sin errores detectados en estas comprobaciones; no validan resultados financieros ni disponibilidad futura de las fuentes.

- **2026-10-17, relaciones e interacciones:** cuatro nuevas lecturas (CX-01/02, CF-01, IX-01), total 53; tres textos cripto descriptivos y un contraste en acciones. Dos hipótesis y comparadores/ablaciones futuros, sin nuevas familias ni estrategias. Pospuestos diseño operativo rápido y complejidad de grafos; originales parciales y falta de prueba incremental neta preservados. Cierre de esta tanda, no aceptación de toda Fase I.

- **Auditoría del 2026-10-17, relaciones/interacciones:** revisión adicional de coherencia de síntesis, hipótesis, roadmap y decisiones contra las tres fichas, y cotejo dirigido de identidad/hash, tablas, Bonferroni y objetivo de reconstrucción de CX-02. Sin errores materiales en ese alcance; precisado que los pesos de la mezcla estática suman uno. CX-01 también cotejado localmente en ecuación 2 y tablas 1–4. No fue auditoría exhaustiva ni réplica financiera.

- **Comprobación documental de esta entrega:** 33 Markdown, 144 enlaces locales (tres con ancla), 20 JSONL con 435 registros válidos y 76 hashes citados encontrados en el cache; sin incidencias. Comprobación de integridad documental, no validación económica ni verificación futura de los enlaces externos.

## Auditoría de cobertura — entrega posterior del 2026-10-17

- Revisados los 53 trabajos a través de sus fichas, las hipótesis y los resultados favorables/adversos. Auditoría interna con revisiones paralelas, no certificación externa ni réplica. Contraste acotado de semántica/disponibilidad de datos sin ampliar familias.
- Dictamen: cobertura de mecanismos suficiente para recomendar cierre limitado; lagunas de información incremental, universo, ejecución/capital y datos point-in-time deben condicionar admisión y diseño posterior. No hace falta otra ronda general ni hallar una ganadora.
- Conciliación de estados de lectura entre fichas y logs mediante eventos nuevos que preservan fechas/descargas históricas. Ninguna conciliación cuenta como nueva lectura ni aumenta los 53 trabajos.
- **Siguiente decisión:** revisión del informe y aceptación explícita del cierre limitado por el usuario. La comparación de candidatos sigue planificada y requiere autorización de II. No se seleccionaron estrategias, adquirieron datos para backtesting, entrenaron modelos ni ejecutaron ensayos.
- **Comprobación final de esta auditoría:** 35 Markdown, 167 enlaces locales (cuatro anclas), 21 JSONL con 468 registros válidos y 84 hashes citados coincidentes con el cache. Once conciliaciones preservan el historial de lecturas; tres páginas oficiales examinadas no aumentan el corpus académico. Sin incidencias documentales; no validación financiera.

## Progreso de Fase II — 2026-10-18

- Registradas aceptación del cierre limitado de I y autorización de II; actualizados estados vigentes sin borrar las entregas anteriores.
- Documentadas comparación completa, escenarios/universo y selección provisional. Dos preguntas primarias, una comparación secundaria de riesgo y dos reservas condicionadas; restricciones y aceptación de II pendientes. Corpus conservado en 53 trabajos; cero experimentos propios.
- Revisión adicional de coherencia de los tres entregables, HYPOTHESES, ROADMAP y D-025–D-027; sin bloqueos materiales en ese alcance. Precisados capital sin doble cómputo de colateral y universo histórico sin elección de supervivientes actuales. No se releyeron todos los originales ni se validó rentabilidad.
- **Verificación documental:** 38 Markdown, 236 enlaces locales (cuatro anclas), 21 JSONL con 468 registros válidos; H-00–H-24 presentes una vez en cada matriz, cinco fichas con los siete campos requeridos e inventario bibliográfico que suma 53. Sin incidencias. No se comprobaron de nuevo todos los enlaces externos, hashes históricos ni datasets; estas comprobaciones no son ensayos financieros.

## Revisión final propuesta de Fase II — 2026-10-18

- Recibidas preferencias: USD, España, infraestructura personal, apertura de productos/horizontes y escenarios de 1.000/5.000/10.000 USD. Capital real, riesgo personal, venue y presupuestos siguen abiertos por decisión del usuario, con puertas para resolverlos antes del trabajo dependiente. D-028–D-030 conservan razones y alcance.
- Mantenidas C1/C3 prioritarias, C2 secundaria y C4/C5 reservas condicionadas. Precisados valor de información frente a facilidad, combinación aditiva frente a interacción, proceso finito de horizontes y condiciones para reconsiderar o no invertir en una construcción. No se repite la revisión general ni se añade una hipótesis para llenar una cuota.
- Contraste oficial acotado: seis objetivos, diez recuperaciones por rutas alternativas, tres fuentes con contenido pertinente leído (CNMV, ESMA y AEAT); fallos y alcance de originales inaccesibles registrados. Corpus académico sigue en 53; no homologación de exchange/producto ni asesoramiento fiscal individual.
- **Verificación de esta revisión:** 40 Markdown, 275 enlaces locales (cuatro anclas), 22 JSONL con 481 registros válidos. Dos matrices completas H-00–H-24, cinco fichas con siete campos, inventario de 53 y diez hashes de recuperaciones oficiales cotejados. Filas originales de hipótesis/nulas y contadores experimentales conservados frente al commit anterior. `git diff --check` correcto. Sin incidencias documentales; no validación financiera ni revisión de todos los enlaces remotos.
- **Estado:** propuesta final preparada para aceptación del usuario; no declarar II cerrada todavía. Laboratorio, datos para backtesting, estrategias, entrenamiento, experimentos, compras y operación no iniciados ni autorizados.
