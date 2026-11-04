# Fase IV — cobertura, decisiones pendientes y acceso a Fase V

**Estado vigente — D-053:** [E1/ejecución con velas](bar-execution.md) aporta evidencia nativa, temporal y causal acotada: seis grupos, 15 contextos, 135 comprobaciones de componentes. El mismo cierre sigue siendo inadmisible para nuestro contrato; la frontera con cotizaciones sintéticas apoya candidatura condicionada. Integración de producción/ciclo de órdenes y admisión financiera pendientes. Sin cambios de criterios ni decisiones económicas E3/E4.

**Estado histórico — D-051:** [corrección acotada](engine-correction.md): comprobaciones E3-L2 correctas; idempotencia E4 del supervisor conserva estado nativo, pero falta el segundo fill original exigido. Sin admisión incondicional del motor. E1/ejecución con velas, E3/E4 económicos y permisos financieros pendientes; criterios originales intactos.

**Solo estado de ejecución — D-049:** la [recuperación E](engine-recovery.md) desbloqueó Nautilus y ejercitó nueve casos funcionales de componentes y cuatro diagnósticos. Sin admisión E completa: quedan cantidad L1, estado de órdenes duplicadas, precio de riesgo L2, cobertura causal nativa y recuperación antes de actuar. M/R y LEAN anteriores conservados. Sin cambio de criterios científicos ni permisos financieros.

Documento: ACCEPT-IV-001 · Versión: 9 · Actualización de evidencia: 2026-11-03 UTC · Traducción del [original inglés](../../en/phase-iv/acceptance.md).

## Dictamen

El paquete metodológico está desarrollado según la [solicitud autorizada](../../phase-iv/REQUEST.es.md); el usuario ha [aprobado E1/E2 de ba6c20b de forma condicionada](../../phase-iv/APPROVAL-E1-E2.es.md), D-038. **No se representa la Fase IV como cerrada incondicionalmente ni ejecutable financieramente.** La aceptación del roadmap exige diseño reproducible aprobado, presupuesto trazable, protección final y costes/rechazo prospectivos. Siguen pendientes E3/E4, vinculaciones completas dependientes de datos, aprobación del protocolo concretado y sellado real del holdout. No se rebaja ningún criterio para declarar la fase terminada. El [informe consolidado de viabilidad](feasibility.md), D-039, conserva la evaluación documental anterior. D-040 autoriza A/B acotados; la [auditoría técnica](admission.md) registra adquisición efectiva, pruebas aisladas, negativos y límites. La admisión financiera de fuentes/motor sigue sin resolver. D-044 registra la [aprobación metodológica de T/D/U/V/F](../../phase-iv/APPROVAL-STAGED.es.md); [IV-AMEND-001](staged-amendment.md) cambia únicamente cuándo deben completarse las vinculaciones dependientes. No concede Fase V ni ejecución financiera.

La aplicación conserva el alcance sintético verificado de III. Se adquirieron los dos archivos reales Q3 autorizados para QA estructural externo y se probó un motor sintético aislado. No se ajustaron modelos financieros, implementaron estrategias de inversión, ejecutaron experimentos financieros ni abrieron holdouts financieros. Las filas reales de QA no entraron en la aplicación sintética. El nuevo método y su ejecutor financiero no están probados. La revisión documental se distingue de las 110/7/2 pruebas históricas de software: no se repitieron ni cuentan como nueva evidencia de IV.

## Correspondencia con las tareas originales — sin otra fase

| Tarea original | Especificación entregada | Estado y condición pendiente |
|---|---|---|
| IV.1 Universo/fuentes/periodo/USD | [Datos](data-execution.md) §§1–3: identidades históricas, elegibilidad, bajas, conversión USD y admisión | Método documentado; proveedor, cobertura certificada, calendario y parámetros sin vincular |
| IV.2 Particiones/walk-forward | [Protocolo](protocol.md) §3: desarrollo anidado, bloque único de validación y lote final, calendario por precisión | Método documentado; fechas/folds requieren cobertura apta y evaluación previa de suficiencia |
| IV.3 Purga/embargo | Protocolo §3: intervalos/disponibilidad, fechas comunes entre activos, eventos agrupados y límites | Documentado; los helpers sintéticos existentes no certifican implementación financiera futura |
| IV.4 Holdout sellado | Protocolo §7 y [plantilla](../../phase-iv/freeze-template.json): custodia, hashes, apertura única, fallo/contaminación | La aplicación mantiene denegación; no hay holdout financiero, custodio fijado ni adaptador de apertura. Sellado real pendiente |
| IV.5 Hipótesis/efectos/métricas/presupuesto/rechazo | [Candidatas](candidates.md), protocolo §§2,4–6,8: tres contrastes primarios, 26 especificaciones base, falsadores y resultados | Diseño comparativo desarrollado; márgenes económicos, límites de riesgo de investigación y presupuesto total de ajustes/cómputo pendientes |
| IV.6 Costes/estrés/financiación | Datos §§3,5–6: tarifas alcanzables, rutas de costes, capital completo, funding/préstamo/margen, ejes finitos | Política documentada; sin tarifa histórica, motor ni modelo de costes certificados |
| IV.7 Incertidumbre/selección/regímenes | Protocolo §§5–6 y [métodos](method-evidence.md): bloques pareados, Holm, supuestos, DSR condicionado/PBO aplazado | Método elegido prospectivamente para revisión; no calculado/calibrado ni simulación nula o inferencia financiera ejecutadas |
| IV.8 Congelación/enmiendas | Protocolo §§4,7–8 y JSON: versiones inmutables, intentos, acceso y parada | Plantilla documental; no esquema ejecutable ni manifiesto aprobado |
| IV.9 Noticias/eventos | Datos §7: versiones, consenso, duplicados/solapamiento, conocimiento y ablaciones precio/calendario/texto | Método condicional; sin candidata textual admitida ni presupuesto asignado |
| IV.10 Activos/interacciones | Candidatas §§4–7: individual/aditivo/interacción y ablaciones; propio→factores→otros para C4 | C3 primaria; C4 reserva. Sin grafos/modelos ajustados ni selección retrospectiva de activos |
| IV.11 Horizontes por mecanismo | Datos §4 y candidatas §§2–4: siete relojes, conjunto finito motivado y un horizonte admitido inicial | Proceso definido; H/L1/L2 y relojes pendientes de admisión, sin barrido de frecuencias |

## Conciliación de criterios de aceptación

| Criterio existente | Evidencia / condición |
|---|---|
| Diseño reproducible y aprobado | Diseño EN/ES versionado y selección/comparación determinista; E1/E2 aprobadas condicionalmente en D-038. Secuencia T/D/U/V/F aprobada en D-044; faltan E3/E4 e instanciación/revisión exacta de cada función |
| Sin decisiones basadas en resultados ocultos | Solo se examinó QA estructural autorizado en A, sin rendimientos de estrategias ni resultados reservados. El trimestre inspeccionado queda expuesto; reglas futuras prohíben retornos reservados. El conocimiento previo de literatura debe declararse |
| Presupuesto trazable | 26 especificaciones base contadas; registro total folds×reajustes×semillas×estrés y recursos en null, bloqueando ejecución |
| Holdout inaccesible por defecto | Política III sin cambios, denegación a todos los roles; futura custodia/apertura debe admitirse y probarse. El acceso del propietario del host no queda impedido criptográficamente |
| Costes/rechazo fijados prospectivamente | Rutas contables y decisiones especificadas; cifras de costes,δ/riesgo/estrés se congelarán antes de la evaluación dependiente |
| Sin umbrales ajustados a quién pasa | Ningún resultado financiero observado; campos abiertamente pendientes, sin valores retrospectivos o certificaciones ficticias |

La distinción es deliberada: se entrega cobertura metodológica; no puede obtenerse aptitud empírica desde datos inexistentes. La vinculación numérica completa el prerregistro de IV, no autoriza comenzar V. Debe preceder a cada ejecución financiera dependiente.

## Decisiones del usuario — agrupadas y acotadas

La [revisión ejecutiva](executive-decisions.md), D-037, es la propuesta histórica. D-038 registra la aprobación condicionada del usuario; el orden vigente es:

1. **Aprobada condicionalmente — E1:** construcción inicial spot largo/efectivo, con horizonte justificado por mecanismo y regla de universo point-in-time. No necesita repetirse la aprobación. Los límites de producto/relojes afectan a esta tanda, no a la investigación futura; la viabilidad concreta sigue sin comprobarse.
2. **Aprobada condicionalmente — E2:** estructura comparativa, techo de 26 especificaciones y política de evidencia de tres contrastes, incluidos comparadores/efectivo y Holm. Sigue pendiente el registro completo de ajustes/recursos; 26 no es cantidad óptima ni ajustes totales. Sin expansión automática de modelos ni obligación de agotar especificaciones.
3. **Decidir tras dimensionar — E3:** aplicar la política existente de gratuito cuando sea apto, conservando alternativas comerciales. Presentar costes concretos de adquisición, desarrollo/validación y operación recurrente antes de solicitar compromisos de recursos o gastos. No inventar presupuesto total ni repetir preferencias ya expresadas.
4. **Decidir tras conocer viabilidad — E4:** elegir capital primario de investigación, márgenes incrementales/sobre efectivo, objetivo de riesgo C2/sacrificio de rentabilidad y escenarios de exposición/pérdida como paquete coherente antes de evaluaciones dependientes. No fijan capital real ni límites personales de operativa. Conservar sensibilidades predefinidas de capital sin seleccionar ganador retrospectivamente.

La adquisición posterior de fuentes, admisión técnica y ejecución financiera requieren autorización separada. Los paquetes de viabilidad A (dos archivos trimestrales identificados, QA estructural) y B (motor fijado aislado, pruebas sintéticas) fueron autorizados por separado en D-040 y se documentan con cobertura y límites efectivos en la auditoría técnica. No autorizan otras adquisiciones, un adaptador de producción ni ensayos financieros. Esta entrega no solicita aprobación anticipada de V. E1/E2 no cierra IV incondicionalmente ni autoriza adquisición, gastos o experimentos. El paquete mínimo por función siguiente aplica solo la enmienda metodológica de secuencia; conserva requisitos económicos y probatorios.

**Secuencia aprobada, no ejecución:** QA estructural/pruebas sintéticas no establecen varianza pareada ni precisión exigidas antes de validación. D-044 aprueba T/D/U/V/F e IV-AMEND-001 registra la enmienda prospectiva. D/U siguen siendo trabajo financiero que requiere autorización de Fase V con alcance concreto separado, E3/E4 y sus propios manifiestos completos. No volver a pedir aprobación del principio ni interpretarlo como permiso de ejecutar. D-046 autorizó posteriormente los paquetes técnicos M/E/R; sus [resultados reales y límites](technical-results.md) se registran por separado. Esta actualización de estado no modifica criterios de aceptación ni concede acceso financiero.

No necesitas elegir cada proveedor, fecha, parámetro de spline o adaptador: son vinculaciones técnicas guiadas por evidencia que se prepararán en el alcance aplicable y se presentarán en un manifiesto concreto. No hacen falta credenciales, cuenta financiada ni exchange de producción definitivo. Antes de abrir el test deben identificarse custodio/revisor y autoridad; acumular roles en una persona conserva una limitación procedimental explícita.

## Paquete mínimo por función antes del acceso dependiente

El manifiesto final completo sigue siendo obligatorio antes de F. Las funciones anteriores solo pueden posponer campos que necesitan legítimamente evidencia de desarrollo; todos los campos exigidos por la operación actual deben estar concretados primero. Los null no son excepciones genéricas y una etiqueta de etapa no autoriza acceso.

| Función | Obligatorio antes de ejecutarla | Vinculación que puede completarse después |
|---|---|---|
| T — técnica | Autorización técnica acotada aplicable; versiones exactas, inputs sintéticos/estructurales autorizados, derechos, casos, recursos y conservación de fallos | T no proporciona suficiencia de retornos pareados; ni éxito técnico ni aprobación A/B abren D |
| D — desarrollo financiero | Alcance separado de Fase V; E3/E4; admisión de fuentes/universo/USD/costes/motor; fechas/folds exactos de desarrollo, recetas, relojes y presupuesto completo finito de búsqueda/recursos; objetivos económicos/riesgo y regla de planificación de suficiencia prospectivos; protección verificada del intervalo posterior y regla determinista de partición/parada | Dependencia pareada/suficiencia derivadas del desarrollo; procedimiento final seleccionado; subdivisión exacta V/F solo bajo regla predefinida de metadatos+D/U |
| U — incertidumbre/suficiencia financiera | Alcance autorizado explícito de calibración en desarrollo; retornos externos aptos de procedimiento congelado o calibración intacta dentro de desarrollo; reglas previas de precisión/alternativa y estimación auxiliar/sensibilidad; implementación estadística admitida con pruebas sintéticas de límites/nulas dependientes y presupuesto finito restante | Estimaciones resultantes y suficiencia de soporte independiente V/F; sin revisar márgenes económicos ni buscar inferencia favorable |
| V — validación | Un bloque posterior intacto y subdivisión F exacta congelada; procedimientos/reajustes/comparadores completos y todas las vinculaciones dependientes económicas, temporales, inferenciales, de estrés, recursos y técnicas; custodia/acceso verificados y autoridad explícita de validación | Solo resultado de admisión predefinido, no ajuste de modelos/criterios; la autoridad de apertura final única sigue siendo distinta |
| F — final | Todas las vinculaciones finales originales, paquete completo congelado/hashes, datos finales protegidos independientemente, controles admitidos y autoridad explícita de apertura/lote único dentro del alcance de Fase V | Tras abrir no se permite selección científica ni campo dependiente pendiente |

Antes de D, adquisición/uso de fuentes y cualquier gasto necesitan autorización separada; proteger el final no puede esperar a U. Declarar datos ya expuestos en QA u otras revisiones. Implementar y probar custodia y controles de acceso específicos antes de confiar en ellos; la aplicación actual sigue denegando datos finales y no implementa apertura financiera.

Cada función conserva versiones/hashes, intentos/errores/negativos y presupuesto restante. Un ensayo reservado parcial o fallido consume exposición registrada; reiniciarlo no restaura independencia. La puerta final original completa se mantiene. La ejecución financiera permanece bloqueada hasta que la autorización cubra la acción concreta y su manifiesto se revise. VI, paper/shadow/live prospectivos y capital real conservan puertas separadas aunque después haya evidencia favorable. Esta enmienda no ejecuta ensayos financieros, paquetes sintéticos ni sellado de holdout.

## UX futura y continuidad

[La evolución UX](../ux-evolution.md) registra UX-01 resultados, UX-02 glosario bilingüe contextual, UX-03 guía y UX-04 integración/accesibilidad. Están planificadas, no implementadas ni son requisitos de IV. Se conserva identidad visual/secciones; sin pestañas, controles ni dependencias vacíos.

Se cierra el presupuesto de tres páginas metodológicas. Se reutiliza el corpus; solo reabrir un hecho concreto que cambie admisión. Al reanudar, leer este documento y la plantilla pendiente/completa, no las notas históricas que indicaban IV no autorizada. Conservar negativos y límites de acceso. Pruebas Windows, actualizaciones runtime e implementación UX son tareas separadas, no realizadas incidentalmente aquí.

## Verificación documental — 2026-10-24

Comprobados 82 Markdown y 604 destinos locales (rutas, no nueva auditoría de enlaces remotos/anclas), sin ausencias. Siete eventos metodológicos parseados y seis referencias de hash cotejadas contra las tres recuperaciones. JSON válido, flags de ejecución/Fase V falsos y 26 especificaciones/tres contrastes conciliados. Las dos traducciones de aceptación cubren los once IDs originales. Los cuerpos científicos de HYPOTHESES y RESEARCH después del encabezado vigente son idénticos byte a byte al commit anterior; se conservan 25 definiciones y siete contadores financieros en cero. Sin cambios runtime, dependencias, datasets de mercado ni cálculo financiero.

Un primer conteo amplio de IDs incluyó indebidamente la frase histórica que indica que no se creó H-25; el patrón siguiente omitió el formato con punto y coma de H-23/H-24. El patrón de definiciones corregido sigue la convención del importador existente y pasa; no se modificó texto científico para satisfacerlo. La revisión metodológica interna detectó ambigüedades en referencia de selección interna y entradas tardías/solapamiento; ambas se aclararon en EN/ES. Es verificación documental/de diseño interna, no rendimiento estadístico calibrado ni certificación científica externa. `git diff --check` pasó antes de publicar.

### Verificación de la revisión ejecutiva — 2026-10-25

La versión 2 solo aclara el momento de aprobación. Comprobados 83 Markdown del repositorio y 626 destinos locales (existencia de rutas, no enlaces externos ni anclas), sin ausencias. Trece documentos científicos/metodológicos/de fuentes/plantilla conservados son idénticos byte a byte al commit anterior; los once IDs de IV siguen presentes en ambas traducciones y la plantilla conserva aprobaciones nulas y flags de ejecución/Fase V falsos. Las decisiones históricas permanecen como prefijo intacto, con D-037 añadido. Los diez archivos nuevos/modificados son documentales; no se necesitaron ni atribuyeron pruebas runtime a esta revisión. Una revisión interna independiente corrigió solicitudes redundantes de aprobación y una frase que podía confundir spot con horizonte lento. `git diff --check` pasó.

### Verificación de viabilidad y aprobación — 2026-10-25

La versión 3 registra D-038/D-039 sin cambiar el protocolo científico. Comprobados 86 Markdown del repositorio y 661 destinos locales, sin ausencias. Doce documentos científicos/metodológicos/UX son idénticos byte a byte a `ba6c20b`; los cuerpos científicos de ambos protocolos y las revisiones ejecutivas originales permanecen intactos. Se conserva el historial de decisiones. Cuarenta y seis eventos de fuentes parseados; 45 referencias de hash coinciden con 24 artefactos del cache. Las dos consultas HEAD registran cero bytes de cuerpo de archivo y tamaños anunciados que suman 2.172.918.907. Estructura EN/ES, enlaces de fuentes, IDs y valores decisivos coinciden. La plantilla cambia solo estado/registro de aprobación limitada: inferencia, presupuesto de búsqueda y vinculaciones no relativas a aprobación permanecen intactos; todos los permisos adicionales a E1/E2 condicionadas siguen nulos y flags de ejecución falsos. Diecisiete archivos nuevos/modificados son documentales; no se necesitó ni repitió la batería runtime. Una revisión interna independiente comprobó alcance, límites de fuentes y secuencia estadística; no es validación financiera. `git diff --check` pasó.
