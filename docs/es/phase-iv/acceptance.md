# Fase IV — cobertura, decisiones pendientes y acceso a Fase V

Documento: ACCEPT-IV-001 · Versión: 3 · Fecha: 2026-10-25 · Traducción del [original inglés](../../en/phase-iv/acceptance.md).

## Dictamen

El paquete metodológico está desarrollado según la [solicitud autorizada](../../phase-iv/REQUEST.es.md); el usuario ha [aprobado E1/E2 de ba6c20b de forma condicionada](../../phase-iv/APPROVAL-E1-E2.es.md), D-038. **No se representa la Fase IV como cerrada incondicionalmente ni ejecutable financieramente.** La aceptación del roadmap exige diseño reproducible aprobado, presupuesto trazable, protección final y costes/rechazo prospectivos. Siguen pendientes E3/E4, vinculaciones completas dependientes de datos, aprobación del protocolo concretado y sellado real del holdout. No se rebaja ningún criterio para declarar la fase terminada. El [informe consolidado de viabilidad](feasibility.md), D-039, distingue hechos documentales, admisión de fuentes/motor sin ejecutar y dependencia de secuencia estadística pendiente.

La aplicación conserva el alcance sintético verificado de III. No se adquirieron datasets de mercado, ajustaron modelos financieros, implementaron estrategias, ejecutaron experimentos ni abrieron holdouts financieros. El nuevo método y su ejecutor financiero no están probados. La revisión documental se distingue de las 110/7/2 pruebas históricas de software: no se repitieron ni cuentan como nueva evidencia de IV.

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
| Diseño reproducible y aprobado | Diseño EN/ES versionado y selección/comparación determinista; E1/E2 aprobadas condicionalmente en D-038. Faltan E3/E4 e instanciación/revisión exacta |
| Sin decisiones basadas en resultados ocultos | IV no consultó datos/resultados financieros; reglas futuras prohíben retornos reservados. El conocimiento previo de literatura debe declararse |
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

La adquisición posterior de fuentes, admisión técnica y ejecución financiera requieren autorización separada. Los paquetes de viabilidad A (dos archivos trimestrales identificados, QA estructural) y B (motor fijado aislado, pruebas sintéticas) son propuestas concretas, no aprobadas ni ejecutadas. Esta entrega no solicita aprobación anticipada de V. E1/E2 no cierra IV incondicionalmente ni autoriza adquisición, gastos o experimentos. El paquete mínimo siguiente permanece intacto.

**Límite estadístico:** QA estructural/pruebas sintéticas no establecen varianza pareada ni precisión estimadas solo en desarrollo, requeridas antes de validación. Viabilidad §7 identifica la tensión con vincular todo antes de cualquier ejecución financiera. Una aclaración prospectiva de admisión por etapas y cualquier desarrollo financiero necesitan revisión/autorización explícitas separadas; aquí no se adopta excepción ni enmienda.

No necesitas elegir cada proveedor, fecha, parámetro de spline o adaptador: son vinculaciones técnicas guiadas por evidencia que se prepararán en el alcance aplicable y se presentarán en un manifiesto concreto. No hacen falta credenciales, cuenta financiada ni exchange de producción definitivo. Antes de abrir el test deben identificarse custodio/revisor y autoridad; acumular roles en una persona conserva una limitación procedimental explícita.

## Paquete mínimo antes de una ejecución financiera de Fase V

- Diseño IV/versionado aprobado y autorización V separada; permiso de adquisición/uso de fuentes y de cualquier gasto.
- Auditoría apta de fuentes, identidades/universo históricos, conversión/efectivo USD, cobertura/disponibilidad/calidad y conocimiento previo declarado.
- Relojes/folds/validación/test exactos, precisión, márgenes económicos/riesgo, parámetros de modelos/reglas, política ejecutable predicción→posición y registro completo de ejecuciones/recursos.
- Costes de comisiones/funding/préstamo/margen, capacidad/demora/estrés; motor elegido mediante interfaces existentes y técnicamente admitido para el producto. Renombrar el banco sintético no lo convierte en motor financiero.
- Inferencia pareada implementada con casos límite/calibración nula y supuestos documentados; informe honesto de inválidos/inconcluyentes. Sin elegir otra estadística después de un fallo.
- Paquete congelado con hashes/versiones, custodia/restricciones de holdout, lote único autorizado y decisiones anexadas. Controles futuros probados; `execution_ready` no concede permisos.

Las tareas de admisión pueden resolver evidencia faltante sin lanzar selección de estrategias. La ejecución financiera permanece bloqueada hasta revisar todas las vinculaciones necesarias y disponer de autorización para esa acción. VI, paper/shadow/live y capital real conservan puertas separadas aunque V aporte evidencia favorable.

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
