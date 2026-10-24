# Presentación futura de resultados y ayuda contextual

Documento: UX-PLAN-001 · Versión: 1 · Actualizado: 2026-10-24 · Idioma: es (traducción).

Original canónico: [inglés](../en/ux-evolution.md), sincronizado con UX-PLAN-001 v1. Estado: **trabajo futuro documentado, no implementado por este plan**. La solicitud de Fase IV pide registrar estas mejoras antes del trabajo metodológico y excluye expresamente implementarlas ahora. Ninguna es requisito para terminar IV. Se conservan prioridades científicas, permisos y el [complemento arquitectónico](architecture/supplement.md).

## Base inspeccionada y decisión

Esta es una revisión interna de diseño acotada, no investigación UX externa ni una afirmación de usabilidad probada con usuarios. Se inspeccionaron `web/src/sections.ts`, `views.tsx`, `components.tsx`, la [guía de uso](usage.md) y las recomendaciones de navegación del complemento. Existen seis secciones funcionales. La vista de pruebas técnicas muestra estados, resultados JSON, informes descargables y configuración/procedencia desplegables. `JsonDetails` es reutilizable. Los gráficos separan cálculo backend y representación. La guía explica las tareas actuales y sus límites, pero no existe un glosario integrado, una guía contextual completa ni un servicio de resúmenes financieros.

**Recomendación:** mejorar las vistas de resultados existentes, mantener un único conjunto versionado de contenidos de ayuda y ofrecerlo mediante enlaces contextuales y una entrada compartida de Ayuda cuando exista contenido útil. Conservar la identidad visual y las seis secciones operativas. Glosario y guía pueden compartir navegación de ayuda; no necesitan pestañas principales separadas. La búsqueda empezaría dentro de la ayuda y crecería solo si lo justifican necesidades reales. La propuesta no necesita otra aplicación, framework frontend, dependencia, servicio de base de datos ni página vacía.

| Alternativa | Beneficio | Coste o limitación | Decisión |
|---|---|---|---|
| Solo documentación del repositorio | Disponible, versionable y económica | Obliga a abandonar el flujo; cuesta localizar términos y parámetros concretos | Conservar como contenido canónico y alternativa; mejorar después el acceso contextual |
| Pestañas principales de resultados, glosario y guía | Fáciles de descubrir | Compiten con la navegación funcional y duplican vistas de detalle existentes | No añadir tres pestañas; reconsiderar ante una necesidad demostrada de navegación |
| Solo tooltips | Explicación breve junto al elemento | Inadecuados para textos largos, teclado/táctil y enlaces persistentes | Solo pistas breves opcionales; nunca el único acceso a definiciones o límites esenciales |
| Ayuda compartida con enlaces contextuales y detalle desplegable | Explicación sin abandonar la tarea; una fuente de contenido | Necesita anclas estables, gestión de foco y mantenimiento | Opción incremental preferida |
| Empezar por buscador global, tours o ayuda conversacional | Descubrimiento amplio o incorporación guiada | Permisos del índice, respuestas obsoletas, mantenimiento de tours, coste de inferencia y distracción | Aplazar; comenzar con navegación/búsqueda estática de ayuda, sin requerir un asistente de IA |

## Contrato de presentación de resultados

Mostrar primero qué se comprobó, después una tabla compacta o un gráfico pertinente, el significado de la comparación y sus límites, y finalmente registros completos desplegables e informes descargables. Una comprobación contable técnica debe resumir sus invariantes y unidades sintéticas; no mostrar Sharpe, rentabilidad ni recomendaciones inventadas. Una estadística ausente debe indicar `no aplicable`, `no calculada` o `evidencia insuficiente`, con motivo, nunca un cero ficticio.

Mantener visibles dimensiones distintas en lugar de condensarlas en una sola etiqueta:

| Dimensión | Representación futura de ejemplo | Interpretación |
|---|---|---|
| Alcance de datos/resultado | Comprobación técnica sintética; evaluación financiera histórica; observación prospectiva | Describe fuente y tarea, no calidad de evidencia |
| Estado de ejecución | En cola, ejecutándose, completado, fallido, interrumpido, cancelado | Terminar un cálculo no confirma una hipótesis |
| Dictamen científico | Sin evaluar, provisional, evidencia contraria, inconcluyente, respalda la afirmación prerregistrada dentro de su alcance | Exige protocolo, comparador, incertidumbre y revisión reales; no se deriva automáticamente del P&L ni de completar un trabajo |
| Alcance de revisión/validación | Verificado técnicamente en comprobaciones identificadas; revisado con datos fuera de muestra identificados | «Validado» debe explicar qué se validó y sus límites; nunca implica rentabilidad garantizada ni permiso de operar |

Son significados de presentación para registros futuros, no un ciclo de vida ejecutable ni una migración en IV. Evidencia financiera negativa, fallo intencionado de software y error de infraestructura significan cosas distintas. Se conservan los tres en sus historiales correspondientes. Un resultado provisional puede también ser adverso o inconcluyente; estas etiquetas no tienen por qué excluirse.

Cada métrica/gráfico futuro debe identificar registro y versión, alcance del dataset, periodo/huso, unidades y moneda de cuenta, versión de cálculo, referencia, tratamiento de costes e incertidumbre cuando proceda. Diferenciar histórico/prospectivo, bruto/neto, USD/stablecoin y observado/modelado. Utilizar estadísticas y criterios de comparabilidad del backend; no recalcular ciencia ni inventar rankings en el frontend. Ejecuciones incomparables o fallidas no deben presentarse como diferencias numéricas demostradas. JSON, hashes, configuraciones y manifiestos siguen accesibles sin abrir contenido reservado o no autorizado.

## Modelo de contenidos del glosario y la guía

Crear términos cuando aparezcan en una función actual, un protocolo admitido o una duda recurrente. El contenido inicial explicaría fixture, dataset/versión, tiempo de disponibilidad, semilla, manifiesto/hash, trabajo/worker, comparación, holdout, leakage, benchmark, costes netos e incertidumbre. Ampliar órdenes/liquidez/riesgo, métricas, carteras y ML solo cuando los use la funcionalidad o el protocolo. No construir un diccionario financiero genérico.

Cada término necesita ID estable independiente del idioma, etiquetas preferidas y sinónimos ES/EN, definición breve, alcance/límite, enlaces a términos relacionados y al flujo correspondiente, revisión y un ejemplo pequeño de bot_trader cuando ayude. Un ejemplo de hash debe explicar integridad, no veracidad; una semilla no debe prometer reproducción en cualquier entorno. Citar la fuente científica o técnica existente cuando el significado dependa de ella. Enlazar material metodológico más amplio sin duplicarlo. Las traducciones comparten ID y significado científico; marcar el contenido sin traducir en vez de sustituirlo silenciosamente.

Ampliar la guía existente hacia ayuda por tareas: propósito y capacidades actuales; primera sesión; tareas por sección; significado y rangos de campos/parámetros; interpretación de estados/gráficos/resultados; errores y recuperación; límites; y relación entre datos, trabajos, worker, resultados y auditoría. Cada tarea debe indicar requisitos, rol/permisos, pasos concretos, resultado visible esperado, errores y dónde consultar evidencia. Ajustar instrucciones a la versión real y al estado de capacidad. Enlazar por separado instalación/desarrollo; explicar lo necesario para comprender el comportamiento sin duplicar documentación de implementación. No describir instrucciones operativas futuras como si ya existiera el botón o servicio.

## Backlog acotado

Todos los elementos están **planificados, sin implementar**, y no aprueban nuevas dependencias. Podrán admitirse como trabajo de software posterior junto a la fase autorizada pertinente; presentar finanzas exige además un servicio de cálculo/evaluación admitido por separado. Su orden no retrasa IV.

| ID | Entregable e incremento mínimo útil | Dependencias | Criterios de aceptación | Reconsideración / momento futuro |
|---|---|---|---|---|
| UX-01 | Resumen legible dentro del detalle de ejecución; comenzar por tareas técnicas actuales y conservar auditoría desplegable | Informes inmutables y semántica tipada existentes; resúmenes financieros necesitan protocolo y servicio de métricas aprobados | Se identifica tarea, alcance/resultado y límites; valores conciliados con el mismo informe/versión; fallos, métricas ausentes e incomparabilidad explícitos; evidencia accesible y sin eludir permisos | Mantenimiento UI posterior autorizado para resúmenes técnicos; visuales financieros cuando exista su servicio, sin fabricar muestras |
| UX-02 | Glosario bilingüe pequeño con anclas estables y enlaces contextuales | Inventario de términos usados; definiciones revisadas y correspondencia de traducciones | Un término se resuelve desde guía y UI; acceso por teclado/táctil; alcance y ejemplos útiles; sin definiciones duplicadas contradictorias ni afirmaciones sin respaldo | Comenzar por un flujo actual; ampliar por demanda de función/protocolo |
| UX-03 | Extender la guía con tareas completas, parámetros, estados esperados, resolución de errores y límites | Registro real de capacidades, guías de uso/instalación/seguridad; términos UX-02 revisados donde se citen | Cada sección/tarea disponible cubierta; permisos y worker coherentes con el software; capturas/ejemplos versionados y etiquetados; módulos futuros siguen futuros; sin secretos en ejemplos | Incrementos por flujo implementado; mantener en la misma entrega que cambie su comportamiento |
| UX-04 | Entrada compartida de ayuda y navegación contextual; después búsqueda acotada si resulta útil | Contenido útil UX-02/03 primero, anclas estables y componentes reutilizables | Enlaces a definición/tarea exacta; retroceso y restauración del foco; sin destinos vacíos; idioma y móvil claros; búsqueda solo sobre ayuda permitida | Admitir cuando exista contenido; buscador amplio o tours solo ante un problema concreto de descubrimiento |

Ningún elemento requiere modificar el protocolo científico, prioridades C1–C5 ni autorización de fases. El esfuerzo futuro debe acotarse por elemento; este backlog no autoriza implementarlos todos a la vez. No implica promesas de calendario, contratación ni servicios de pago.

## Accesibilidad, verificación y mantenimiento

Conservar la identidad visual utilizando títulos/tablas semánticos, foco de teclado visible, etiquetas descriptivas y alternativas textuales de gráficos. Comunicar estados con palabras además de colores. Las explicaciones esenciales deben funcionar por tacto y teclado; un tooltip solo al pasar el ratón no basta. Las definiciones largas necesitan panel/página enlazable, cierre/retroceso explícito y foco restaurado. Respetar movimiento reducido, contraste legible y pantallas estrechas; una animación no sustituye la explicación del resultado.

Al implementar, verificar un éxito técnico, fallo intencionado, interrupción, valores ausentes/no aplicables y comparación no válida contra registros reales del servicio. Los ejemplos financieros negativos/inconcluyentes podrán usar fixtures UI claramente etiquetadas, sin presentarlas como evidencia del proyecto. Comprobar que desplegar auditoría no solicita contenido reservado, que enlaces y traducciones son coherentes y que teclado permite entrar/salir de ayuda de forma predecible. Los gráficos necesitan resumen/tabla legible equivalente; los requisitos exactos de accesibilidad se comprobarán frente a los estándares adoptados entonces, sin atribuir una certificación a esta revisión.

La responsabilidad de contenido sigue al módulo y su documentación canónica: lenguaje científico revisado con el protocolo, instrucciones técnicas con servicios y traducciones en la misma revisión. Priorizar Markdown versionado reutilizado u otra estructura pequeña revisada; elegir renderer/índice cuando lo justifique la implementación. Evitar HTML externo sin tratar o ejecutar instrucciones procedentes de ayuda/investigación. Ningún tutorial modificará estado o lanzará tareas sin acción explícita y permisos normales del servicio.

El plan está terminado como registro de trabajo futuro. No modifica frontend/backend, dependencias, controles, secciones, experimentos ni políticas de autorización; las comprobaciones de usabilidad y accesibilidad anteriores siguen siendo aceptación futura, no pruebas ya superadas.
