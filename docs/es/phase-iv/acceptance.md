# Fase IV — cobertura, decisiones pendientes y acceso a Fase V

Documento: ACCEPT-IV-001 · Versión: 1 · Fecha: 2026-10-24 · Traducción del [original inglés](../../en/phase-iv/acceptance.md).

## Dictamen

El paquete metodológico está desarrollado y se presenta para revisión según la [solicitud autorizada](../../phase-iv/REQUEST.es.md). **No se representa la Fase IV como cerrada incondicionalmente ni ejecutable financieramente.** La aceptación del roadmap exige diseño reproducible aprobado, presupuesto trazable, protección final y costes/rechazo prospectivos. Existen diseño y reglas; faltan aprobación, vinculaciones dependientes de datos y sellado real de un holdout financiero. No se rebaja ningún criterio para declarar la fase terminada.

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
| Diseño reproducible y aprobado | Diseño EN/ES versionado, comparación/selección determinista y vinculaciones explícitas. Aprobación e instanciación exacta pendientes |
| Sin decisiones basadas en resultados ocultos | IV no consultó datos/resultados financieros; reglas futuras prohíben retornos reservados. El conocimiento previo de literatura debe declararse |
| Presupuesto trazable | 26 especificaciones base contadas; registro total folds×reajustes×semillas×estrés y recursos en null, bloqueando ejecución |
| Holdout inaccesible por defecto | Política III sin cambios, denegación a todos los roles; futura custodia/apertura debe admitirse y probarse. El acceso del propietario del host no queda impedido criptográficamente |
| Costes/rechazo fijados prospectivamente | Rutas contables y decisiones especificadas; cifras de costes,δ/riesgo/estrés se congelarán antes de la evaluación dependiente |
| Sin umbrales ajustados a quién pasa | Ningún resultado financiero observado; campos abiertamente pendientes, sin valores retrospectivos o certificaciones ficticias |

La distinción es deliberada: se entrega cobertura metodológica; no puede obtenerse aptitud empírica desde datos inexistentes. La vinculación numérica completa el prerregistro de IV, no autoriza comenzar V. Debe preceder a cada ejecución financiera dependiente.

## Decisiones del usuario — agrupadas y acotadas

1. **Revisar el diseño científico:** aceptar o modificar la propuesta inicial spot largo/efectivo, prioridades C1/C3, enfoque secundario C2, 26 especificaciones base y presupuesto de error de tres contrastes. Spot y un horizonte acotan esta tanda, no las oportunidades futuras. No existe expansión automática a modelos complejos.
2. **Fijar recursos de investigación:** gasto aceptable en adquisición, cómputo/desarrollo o primera admisión estrictamente gratuita. No se implica compra ni CI/cloud de pago. Los límites de tiempo/almacenamiento pueden recomendarse tras dimensionar fuentes/motor, pero deben aprobarse antes de incurrir en gasto.
3. **Elegir economía/riesgo de investigación:** capital de referencia; efecto incremental y sobre efectivo mínimamente relevante; objetivo de riesgo de C2/pérdida de retorno tolerada; escenarios de exposición/pérdida. Son decisiones experimentales, no capital real ni apalancamiento autorizado. Si hay incertidumbre, cabe una sensibilidad pequeña predefinida, con escenario primario y sin elegir ganador retrospectivo.
4. **Precisar el próximo alcance autorizado:** aprobar admisión/calidad de fuentes y preparación de compatibilidad del motor financiero, indicando si los ensayos requieren otra revisión tras el manifiesto completo. La solicitud actual no autoriza esas acciones posteriores. Puede solicitarse revisión de fuentes/motor antes de autorizar experimentos.

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
