# Propuesta de decisión — pruebas técnicas M, E y R

Documento: IV-TECH-001 · Versión: 1 · Fecha: 2026-10-28 · Traducción del [original inglés](../../en/phase-iv/technical-packages.md).

## Decisión preparada para autorización

**Recomiendo una autorización acotada para las pruebas aisladas M/R y la comparación E de los dos motores, con condiciones de parada y sin migrar producción.** No se ha concedido ni se ha instalado o ejecutado ningún paquete. La [aprobación metodológica](../../phase-iv/APPROVAL-STAGED.es.md) queda registrada por separado en [IV-AMEND-001](staged-amendment.md); T/D/U/V/F no autoriza acceso financiero, Fase V ni estos nuevos trabajos técnicos. E3/E4 siguen pendientes.

El alcance sirve para decidir; no construye otra plataforma, reabre una revisión tecnológica general ni desarrolla un adaptador financiero completo. Conserva C1/C3 prioritarias, C2 secundaria, C4/C5 reservas, 26 especificaciones, inferencia aprobada, historial sintético v1 y negativos A/B. No necesita más datos de mercado ni streams. Los precios/órdenes sintéticos son fixtures contables inventados, no backtests financieros ni evidencia de ventaja.

| Paquete | Decisión concreta | Ruta técnica exacta | Qué demuestra pasar / qué no |
|---|---|---|---|
| **M — almacenamiento/dependencias** | ¿Podemos actualizar Arrow conservando la aplicación y la semántica de los artefactos existentes? | Python 3.12.14; lock actual Arrow 23.0.1/DuckDB 1.5.6 frente a un candidato desechable que cambia solo Arrow a 26.0.0. Detalles/límites en [anexo M/R](technical-packages/dependencies-temporal.md) | Pasan regresiones sintéticas aplicables, lectura/inmutabilidad anterior y valores/identidad/disponibilidad exactos. No autoriza migración estable ni permite ejecutar Nautilus v2 en Python 3.12 |
| **E — motores de ejecución** | ¿Qué motor, si alguno, cumple ejecución/contabilidad/interfaz con un coste de implementación razonable? | Nautilus **2.0.0rc7**, commit `55c0e82053142bce3a5cba4de4221d3929c2d3bc`, Python **3.13.18**; LEAN commit **`22404ea28b8d3f3c9eb74d6ed9f0444426f8e417`**, SDK .NET **10.0.403**. Mismas entradas/oráculo sintéticos, entornos separados y supervisor mínimo Python 3.12; [anexo E](technical-packages/engines.md) | Demuestra semánticas exigidas para esos casos/versiones, distinguiendo comportamiento nativo y protección del harness. No certifica producción, recuperación live ni cualquier producto |
| **R — tiempo y decisiones** | ¿Una misma transformación/decisión causal produce salidas iguales con igual información disponible en lotes, replay e interfaz de streaming simulada? | Python/lock actual, diario sintético y casos de calendario fijos; contrato de fixtures compartido con E. Inyección local sin conexión de mercado | Cumple prefijos, disponibilidad, agregación y decisiones bajo precisión/orden definidos. No demuestra calidad de un feed real, predicción económica ni fills reales idénticos |

## Por qué estas versiones cambian la propuesta anterior

La comprobación de versiones es dirigida y reutiliza lo investigado. Nautilus **1.231.0** sigue siendo el último v1 estable con mantenimiento de seguridad limitado; su conflicto Arrow y negativos L1/recuperación permanecen como evidencia histórica. El candidato activo v2 **2.0.0rc7** requiere Python `>=3.13,<3.15`, no declara PyArrow obligatorio en los metadatos examinados y es **prerelease**, no una versión estable preparada para producción. El anexo E fija wheel y código. Probarlo puede detectar incompatibilidades arquitectónicas; pasar no elimina el riesgo de madurez. Si se exige una versión estable mantenida antes de cualquier prototipo, se pospone esta rama, sin llamar estable a rc7 ni instalar silenciosamente otra versión.

La última entrada de releases de GitHub de LEAN es antigua y no sirve como indicador de mantenimiento. Se fija un commit reciente de desarrollo y sus requisitos .NET 10: snapshot de rama mantenida, no garantía de soporte de una release. Ambas versiones siguen siendo candidatas. Una release posterior requiere revisión; no se actualiza automáticamente dentro de este permiso.

**M es independiente de E.** Arrow 26 puede resultar viable para almacenamiento sin ser necesario para el motor elegido. Un fallo M no bloquea E mediante workers; pasar M tampoco justifica actualizar producción. E utiliza deliberadamente Python 3.13 y .NET separados de la aplicación estable: es la frontera de la prueba, no una decisión permanente de arquitectura. Queda excluida una actualización de Python para integrar el motor en el mismo proceso.

## Secuencia mínima y trabajo permitido si se aprueba

1. Congelar IDs/salidas esperadas, hashes de paquetes/código, inventario de dependencias y manifiesto de ejecución en directorio desechable. Comprobar recursos y aislamiento de escritura/red. Conservar checkout, locks, artefactos y hashes previos. Sin acceso a archivos de mercado ni credenciales.
2. Implementar el pequeño oráculo/fixtures R y harness M fuera de producción; comprobar expectativas independientemente antes de interpretar los motores. Reutilizar A/B sin reinstalar v1 para acumular positivos.
3. Ejecutar M/R dentro de sus límites. En E, resolver/instalar/compilar solo runtimes y subconjunto de código fijados, después casos obligatorios. Parar por capacidad obligatoria sin resolver, acceso inseguro o límite de recursos; no cambiar versiones ni relajar el oráculo para aprobar.
4. Medir transporte/recursos y recuperación E cuando contabilidad y semánticas básicas permitan interpretarlo. Solo se incluye configurar modelos de fills existentes del motor. Si hace falta desarrollar otro, registrar la laguna y detener la comparación dependiente; no implementarlo en este paquete. El harness no puede inyectar resultados esperados ni declarar recuperación nativa mediante un wrapper no probado.
5. Informar aprobado, adverso, no soportado y no ejecutado por separado, recursos exactos, versiones, observaciones contables/de transporte y fallos conservados. Recomendar motor únicamente para un uso admitido concreto; posponer ambos si incumplen. El alcance solicitado permite publicar harnesses y resultados sintéticos pequeños; binarios/caches voluminosos quedan fuera de Git.

La **nueva autorización solicitada** cubre instalación, implementación del harness y ejecución M/E/R. Configuración y diagnóstico ordinarios dentro de sus límites no requieren consultar cada campo. Cambiar versión, requisito, techo de recursos, fuente, producción o desarrollar un adaptador completo queda fuera. No se oculta desarrollo financiero dentro de estas pruebas.

## Recursos, riesgos y condiciones de parada

Los anexos fijan estimaciones y techos por paquete. Son decisiones de planificación técnica, no mediciones ni presupuesto de investigación financiera. Se utiliza el host actual secuencialmente: máximo **4 vCPU y 8 GiB RAM** para un paquete, **12 GiB agregados de almacenamiento temporal**, incluidos caches y fallos conservados. El host inspeccionado tiene límite cgroup de 4 CPU/32 GiB y aproximadamente 27 GiB libres; se revalida tras interrupciones. Disponer de capacidad no autoriza ampliar servicios de pago. Parar antes de superar límites; agotarlos deja resultado inconcluso sobre corrección del motor.

| Paquete | Trabajo inicial acotado | Tiempo máquina activo estimado / techo | Transferencia de software / disco máximos |
|---|---|---|---|
| M | 20 casos propios, hasta seis lecturas antiguas y dos invocaciones de suite backend | 20–60 min / **2 h** | **512 MiB / 3 GiB** |
| R | Ocho diarios × cinco rutas × cuatro ejecuciones completas/prefijos = 160 | Menos de 10 min / **1 h** | **Ninguna / 0,5 GiB** |
| E | Nueve intentos funcionales y cuatro de recursos por motor = 26 | 1–2 h / **4 h** | **2 GiB / 8 GiB** |

Techo conjunto: **7 horas máquina activas, 2,5 GiB de software transferido y 12 GiB de disco**, manteniendo los límites de cada paquete. Incluye un único ciclo correctivo de defecto diagnosticado del harness dentro de esos mismos recursos, con techos de intentos en anexos. Preparar/revisar los harnesses se estima por separado en 0,5–1,5 jornadas-persona M, 1–2 R y 2–4 E; son estimaciones inciertas de ingeniería, no tiempo de cómputo ni promesa de entrega. No autorizan contratar personal ni suscripciones.

El permiso de descarga, si se concede, cubre solo software/runtimes especificados y dependencias de compilación. La adquisición de LEAN excluye `Data/` y muestras de mercado incluidas en upstream; no se admite archivo completo, descargador de históricos de ejemplo, CLI pagada, plugin de broker, imagen Docker ni ejemplo conectado. Se limita/registra tráfico de instalación y tamaños transitivos desconocidos; los casos no acceden a red/mercado. Fallos de compilación, dependencias ocultas de datos/red o aislamiento imposible detienen esa ruta.

No se propone servicio, suscripción ni gasto nuevo en USD. Se conservan licencias/procedencia y hashes; la licencia del repositorio no certifica derechos de redistribución transitivos. El tiempo humano es estimación, no promesa; defectos inesperados consumen el presupuesto finito de reparaciones y pueden terminar el contraste. Pasar técnicamente no estima rentabilidad, materialidad económica ni drawdown personal aceptable.

## Qué queda abierto después

E3/E4, adquisición histórica/derechos/cobertura, migración estable, adaptador financiero completo, feeds prospectivos, paper/live, certificación Windows y Fase V siguen separados. M/R pueden probar la mecánica local del contrato; no elegir un proveedor cuyo histórico/directo aún no se ha examinado. E puede justificar una recomendación acotada, no un ganador universal permanente. UX/glosario/guía futura se conservan sin implementación.

La decisión actual es autorizar o no el alcance técnico acotado, incluyendo la limitación explícita de madurez rc7. **El principio metodológico por etapas ya está aprobado y no se vuelve a someter a aprobación.** No hace falta otra revisión general antes de esta decisión técnica. El [checkpoint y evidencia](../../phase-iv/technical-packages/PROGRESS.md) separa documentación terminada y pruebas pendientes de permiso.
