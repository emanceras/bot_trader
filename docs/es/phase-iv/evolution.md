# Fase IV — revisión de datos, motores y evolución de la admisión

Documento: IV-EVOL-001 · Versión: 1 · Fecha: 2026-10-27 · Traducción del [original inglés](../../en/phase-iv/evolution.md).

## Recomendación y autorización

**Conservar el núcleo científico y reconsiderar fuentes y motores según capacidades explícitas y pruebas comparables. No se elige proveedor ni motor permanente.** La revisión documental parte de `d70e6bc` y del [encargo](../../phase-iv/evolution/REQUEST.es.md). Añade propuestas y lectura dirigida de fuentes oficiales, sin implementación ni evidencia financiera nueva. IV sigue abierta condicionalmente; E3/E4, V y paper/live prospectivo pendientes. Se mantienen 53 trabajos, H-00–H-24, C1/C3 prioritarias, C2 secundaria, C4/C5 reservas y 26 especificaciones base.

La [auditoría A/B](admission.md) acredita únicamente fuentes/versiones/fixtures comprobados. Descargar un trimestre no selecciona Kraken como histórico. Instalar Nautilus no resuelve soporte, ejecución ni recuperación futuros. Código/locks, contratos sintéticos v1, protocolo estadístico aprobado, campos de congelación y backlog UX permanecen intactos. No se ejecutaron endpoints/streams de mercado, descargas de datasets, instalaciones de motores, migraciones ni experimentos financieros en esta revisión.

| Entregable | Propuesta | Conclusión principal |
|---|---|---|
| Fuentes históricas/directas y adquisición | [Comparación](evolution/sources.md) | Comparar cobertura por instrumento/evento/tiempo/versión y derechos, sin ranking permanente ni elegir solo por años anunciados |
| Normalización y coherencia | [Contratos temporales](evolution/temporal.md) | Separar evento/publicación/recepción/disponibilidad; mismos datos causales/estado pueden dar iguales decisiones, no fills reales idénticos |
| Multirresolución y mercados futuros | Contratos temporales | Conservar eventos originales justificados y agregaciones/calendarios/instrumentos versionados; admitir productos sin ampliar la tanda |
| Noticias/información externa e incremento | [Información externa](evolution/external-information.md) | Versiones iniciales, entidades, disponibilidad, derechos y comparadores preceden a complejidad NLP/LLM |
| PyArrow y procesos | [Dependencias](evolution/dependencies.md) | El límite actual no tiene incompatibilidad demostrada documentada. Contrastar actualización y aislamiento antes de hacerlos permanentes |
| Motores y casos sintéticos | [Evaluación](evolution/engines.md) | Nautilus y LEAN siguen como finalistas; Freqtrade reserva acotada. Velocidad o conectores no compensan incumplimientos obligatorios |
| Secuencia estadística | [Admisión por etapas](evolution/staged-admission.md) | Separar desarrollo financiero acotado, suficiencia solo en desarrollo, validación independiente y apertura final; propuesta sin rebajar puertas vigentes |

## Hallazgos que cambian decisiones concretas

1. **El mismo nombre no significa la misma información.** Kraken define el lado de una operación WS como agresor; Coinbase Exchange match como creador de liquidez. Unidades temporales histórico/directo de Binance pueden diferir y una actualización de vela puede estar abierta. El adaptador debe conservar definiciones, versiones e identidades antes de normalizar. No convertir histórico corregido en primera recepción inventando timestamps.
2. **El techo de PyArrow es revisable.** `>=19,<24` aparece en el commit inicial `2cf79b4`, sin razón de incompatibilidad específica con 24+ en el historial inspeccionado. El lock usa Arrow 23.0.1 y DuckDB 1.5.6. `>=25` de Nautilus 1.231.0 sí entra en conflicto con la restricción actual, pero no demuestra que actualizar sea inseguro o imposible. Documentación de interoperabilidad no certifica una pareja exacta de versiones.
3. **La precisión debe sobrevivir todo el recorrido.** DuckDB 1.5 advierte pérdida de precisión inferior a microsegundos al convertir timestamps con zona y nanosegundos a `TIMESTAMPTZ`. Se proponen ticks enteros de época, unidad/precisión explícita y metadatos de reloj/calendario; rechazar pérdidas silenciosas. Es requisito de contrato futuro, no cambio retrospectivo de v1 sintético.
4. **El mantenimiento de Nautilus importa tanto como resolver dependencias.** El README develop examinado describe backports de seguridad en v1 y otra API v2 candidata de lanzamiento con advertencia de producción. Son afirmaciones documentales de rama, no una nueva prueba de versión instalada. Actualizar Arrow no resuelve ese riesgo. LEAN merece contraste equivalente; sus fills/impacto por defecto y reinicio también requieren pruebas.
5. **La evidencia ausente sigue ausente.** Una respuesta Tardis fue HTTP200 con «Page Not Found». El catálogo Databento establece una opción futura multiactivo relevante, no equivalencia histórico/directo, precios o derechos verificados. Conservar fechas y límites; páginas genéricas o popularidad no equivalen a admisión.

## Arquitectura objetivo recomendada, sin reconstrucción

Mantener una plataforma con ingestión y mapeo específicos de fuente, eventos canónicos versionados, transformaciones causales y decisiones compartidas, y adaptadores sustituibles de ejecución/contabilidad. Conservar versiones originales cuando su valor científico y derechos justifiquen retención. Identificar velas/variables derivadas por versiones padre, configuración de agregación/calendario y transformación; lotes/replay/directo deben compartir esas definiciones. Distinguir vistas recibidas/conocidas y últimas corregidas.

El contrato debe representar conocimiento y desconocimiento, sin forzar todo a spot base/cotizada o precios positivos. Acciones corporativas, vencimiento/multiplicador/liquidación de futuros, volumen FX, índices no negociables y calendarios son capacidades tipadas admitidas antes del uso dependiente. No obliga a implementarlas ahora. No introducir otra UI, un esquema universal gigantesco, broker de eventos obligatorio, microservicios distribuidos ni motor financiero general propio.

Preferir **contratos lógicos independientes del motor ahora y decidir el despliegue con evidencia**. Un worker de investigación puede intercambiar lotes inmutables con secuencia/corte/procedencia y evitar un salto de red por evento. Compartir proceso reduce serialización/coordinación y puede simplificar si la actualización desechable pasa. Ni aislamiento ni memoria compartida prueban seguridad, estado correcto o efectos exactamente una vez. Medir arranque, copias/serialización, contrapresión, sincronización, propiedad, persistencia del diario y recuperación con igual carga. El futuro live puede necesitar otra separación por razones operativas justificadas; no imponer iguales supuestos de ejecución.

La apertura de Nueva York es ejemplo de infraestructura: sesión por venue, zona/DST, festivos/cierres anticipados, subasta frente a continuo, primer intervalo completo y disponibilidad tras recepción. No se elige duración, regla, hipótesis intermercado ni experimento. Un estudio futuro prerregistrará comparación finita de horizontes por mecanismo y evaluación independiente antes de ver resultados.

## Paquetes prácticos propuestos y permisos

Son diseños revisables, **no trabajos ejecutados ni instalaciones ya aprobadas**. Reutilizar A/B sin repetir para acumular resultados positivos.

| Paquete | Alcance y evidencia buscada | Aceptación / parada | Permiso antes de ejecutar |
|---|---|---|---|
| M — comparación de migración | Control desechable con lock actual frente a candidato Arrow 26.0.0 (solo presente en el antiguo entorno aislado), DuckDB 1.5.6 y dependencias compatibles; fijar lock candidato primero. Round-trips sintéticos de persistencia/IPC/Parquet/Decimal/null/tiempos/esquemas, tests de aplicación y restauración/lectura anterior | Conservar valores, unidades, disponibilidad, IDs y lectura de artefactos; cambios de formato crean versiones, nunca sobrescriben hashes. Rechazar pérdida silenciosa o fallo de resolución/runtime; sin buscar versiones ilimitadas | Alcance separado de instalación/prueba aislada; sin producción. Una actualización estable posterior requiere otra revisión con resultados concretos |
| E — comparación de motores | Release/commit mantenido y licencia/docs exactas para cada finalista; fixtures inventados T1–T8, oráculo independiente, modelos explícitos y separación nativo/wrapper. Continuar realmente el estado interrumpido, no otro replay | Cumplir semánticas obligatorias del uso previsto, declarar no soportados y medir recursos comparables. Conservar negativo L1; no cambiar orden/política para que pase. Casos multicuenta/producción según uso futuro dependiente | Instalar LEAN/otra versión y ampliar adaptadores requiere alcance explícito. Fijar versiones, tamaños/recursos primero; sin CLI pagada, adaptador completo, mercado ni live |
| R — equivalencia temporal/causal | Fixtures sintéticos originales/corregidos/tardíos/gaps/sesiones, variación de lotes/orden, digests de transformación/decisión batch/replay y pruebas de prefijos | Misma información admitida y estado producen iguales salidas bajo política fija; diferencias por disponibilidad/correcciones se explican | Futuro alcance técnico de pruebas/contratos; no abrir stream prospectivo ahora |
| H — adquisición histórica | Preparar manifiesto finito fuente/instrumento/evento/periodo que resuelva una laguna material y añada historia útil más allá de Q3 | Identidad/versión/tamaños, derechos, almacenamiento, muestreo y tratamiento expuesto/reservado revisados antes de descargar; parar por derechos incompatibles o cobertura inadecuada | Cada dataset/descarga o servicio adicional requiere permiso; no se autoriza histórico completo ni compra premium |

M responde a compatibilidad concreta, no obliga a mantener Nautilus sea cual sea E. E puede demostrar que otro motor elimina la necesidad de cambiar Arrow. Orden recomendado: completar requisitos de fuentes/relojes y metadatos inmutables de candidatos; realizar la comparación técnica autorizada mínima que discrimine, reutilizando M cuando proceda; después proponer adaptador financiero y tramo de adquisición. Contrastar captura/replay con **grabaciones reales en directo** requeriría autorización separada de recogida finita y derechos, aunque no se envíen órdenes.

## Costes, exclusiones y decisiones

| Categoría | Evidencia disponible | Pendiente |
|---|---|---|
| Históricos/licencias | Archivos directos gratuitos y observaciones comerciales fechadas en [viabilidad](feasibility.md); A midió solo dos objetos | Cobertura/campos/periodos, derechos, cuotas/excesos, copias retenidas, derechos de exchange, impuestos y cotización USD. Sin total ni precio nuevo inventado |
| Ingeniería/validación | Plataforma sintética existente, mediciones A/B acotadas y conflicto de dependencias | Migración, normalización, gaps, acciones corporativas/recuperación; PC/Windows; presupuesto total de ajustes/cómputo. Segundos de smoke test no valoran ese trabajo |
| Operación recurrente | Categorías futuras de feed, almacenamiento/backup, cloud, monitorización, inferencia y mantenimiento | Ninguna suscripción/collector/servidor autorizado. Software gratuito/alojamiento propio tienen costes; tarifa de datos no es comisión de trading |
| Científico/económico | Comparaciones aceptadas y búsqueda limitada | E3 y E4 sin fijar. Ningún benchmark de fuente/motor aporta expectativa de beneficio, potencia garantizada ni tolerancia real al riesgo |

Posponer adquisición amplia, motor permanente, actualización estable de Arrow, captura directa, implementación noticias/LLM/on-chain y estrategias multiactivo. No añadir Kafka/RAG/grafos ni controles live universales solo para aparentar completitud. No ampliar el ledger sintético hasta convertirlo en motor financiero general. Reconsiderar por requisito definido, contraste finito y recursos/derechos viables. Comodidad Freqtrade o catálogo LEAN no implican ventaja económica; Nautilus instalado no obliga por coste ya incurrido.

Decisiones materiales agrupadas:

- **Principio metodológico listo para revisión:** [admisión por etapas](evolution/staged-admission.md). Aceptarla cambiaría el momento de completar vinculaciones, sin aprobar ejecución financiera ni diluir E1/E2. Hasta aceptación e instanciación rigen protocolo y condiciones originales.
- **Siguiente autorización técnica, tras concretar manifiestos:** M/E/R, solo pruebas que resuelvan incertidumbre decisiva. No aprobar cada campo del parser; versiones/recursos de paquetes nuevos se concretan antes de instalar. Proceso compartido/worker y motor final se elegirán con resultados, no preferencias arquitectónicas.
- **Compromisos posteriores dependientes de evidencia:** H y cualquier gasto, después E3/E4 y desarrollo financiero autorizado por separado. Apertura final y paper/live son permisos posteriores distintos. No se solicitan cifras arbitrarias de capital, margen o riesgo ahora.

## Verificación y continuidad

El [checkpoint de evidencia/verificación](../../phase-iv/evolution/PROGRESS.md) registra lecturas, trabajo efectivo/propuesto y reanudación. Anexos EN/ES comparten identificadores y alcance. Fuentes y lecturas son específicas; HTTP satisfactorio no demuestra contenido. Sin reapertura general de I, aumento del corpus académico ni cambios de contadores financieros. La revisión interna apoya una decisión futura; no certifica contratos de proveedores, corrección del motor ni rentabilidad.
