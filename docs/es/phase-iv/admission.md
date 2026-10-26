# Fase IV — auditoría técnica de los paquetes A y B

Documento: IV-ADMISSION-001 · Versión: 1 · Fecha: 2026-10-26 · Traducción del [original inglés](../../en/phase-iv/admission.md).

## Alcance y dictamen

La [autorización D-040](../../phase-iv/APPROVAL-A-B.es.md) comprende exactamente dos archivos trimestrales de Kraken para QA estructural privado y una prueba aislada de NautilusTrader 1.231.0 con datos sintéticos inventados. Este informe actualiza el **estado vigente**, no los hallazgos históricos, del [informe de viabilidad](feasibility.md). Código de producción, dependencias, controles de modo sintético y contadores financieros permanecen intactos. No se realizaron ensayos de estrategias financieras, entrenamiento de modelos de inversión, paper/live prospectivo ni contratación de servicios.

**Dictamen:** A y B terminados dentro de su alcance técnico acotado, con aptitud de fuente limitada, conflicto de dependencias en el mismo entorno, supuesto L1 adverso y recuperación sin verificar. Ni fuente ni motor admitidos para ejecución financiera. E1/E2 conservan su aprobación condicionada; E3/E4 siguen pendientes, `execution_ready=false` y `phase_v_authorized=false`. IV no está cerrada incondicionalmente.

## A — derechos, adquisición y cobertura efectiva

Los [registros de fuentes](../../phase-iv/admission/kraken-rights-sources.jsonl) documentan cuatro páginas oficiales nuevas y reutilización de documentación previa. La invitación a descargar archivos permite expresamente usarlos en código y convertir formatos; las condiciones EEE permiten fines aprobados en beneficio propio y conservan restricciones amplias de copia/automatización. Esto respalda el flujo concreto ofrecido de descarga e inspección privada, **no** una licencia abierta, permiso comercial/de redistribución ni certificación jurídica. [Evaluación acotada](../../phase-iv/admission/kraken-rights-assessment.json). No se sortearon controles de acceso, abrieron cuentas, contactaron terceros ni adquirieron datasets adicionales.

| Objeto autorizado | Bytes adquiridos | SHA-256 del cuerpo recibido |
|---|---:|---|
| `Kraken_OHLCVT_2026Q3.zip` | 576.348.633 | `96daae63c7b3acb522892e1f602f9c564d1a3fb659089d9b0699282f30d41226` |
| `Kraken_Trades_2026Q3.zip` | 1.596.570.274 | `67aa726be17a0f3ed14e4737030c777e1aa522e568090e72aa950415d66bce25` |
| Total | **2.172.918.907** | Solo dos cuerpos; originales fuera de Git |

Las comprobaciones HEAD/GET de identidad y tamaño coincidieron con el manifiesto revisado. Los [registros de adquisición](../../phase-iv/admission/kraken-acquisition.jsonl) conservan el HTTP 403 inicial sin descargar contenido y la repetición satisfactoria con User-Agent ordinario, sin cambiar la verificación TLS. No se consultó otro endpoint ni trimestre. El hash local acredita identidad del contenido; ETags multipart y CRC ZIP no certifican independientemente su veracidad.

El [resultado principal](../../phase-iv/admission/kraken-results.json), el [diagnóstico de volumen separado](../../phase-iv/admission/kraken-volume-diagnostic.json) y el [cotejo de etiquetas](../../phase-iv/admission/kraken-pair-review.json) conservan denominadores y negativos.

| Comprobación | Resultado observado | Dictamen / límite |
|---|---|---|
| Inventario completo y CRC | 10.054 miembros OHLCVT + 1.438 de operaciones; **11.492/11.492** leídos correctamente, 8.380.534.210 bytes descomprimidos en streaming; sin extracción | Pasa integridad interna; sin checksum independiente del proveedor ni garantía de completitud |
| Manifiestos de archivos/filas | 10.052 CSV de velas con 36.966.491 filas; 1.436 CSV de operaciones con 116.477.432 filas; conjuntos idénticos de 1.436 etiquetas de pares | Recuentos conciliados; no certifican identidades históricas, deslistados ni universo operable |
| Comprobación numérica acotada | Primeras/últimas 64 filas por CSV sin solapamiento: **1.190.284 filas de velas / 182.180 de operaciones**; sin errores comprobados de esquema/números/OHLC/tiempos/ID | Solo muestra de extremos; no aleatoria, orden global ni estimación de tasa de error. Huecos o zonas sin muestrear no se declaran operaciones perdidas |
| Esquemas/avisos | OHLCVT esquema 1 sin cabecera; operaciones esquema 2 con siete campos nombrados y timestamp primero. README documenta cambios previos y metadatos ausentes en algunos pares deslistados | Parser según versión. No hubo ausencia de metadatos en la muestra de extremos: no se seleccionó el tercer par diagnóstico opcional. No demuestra cobertura de deslistados |
| Posibles duplicados | 1.241 triples adyacentes de timestamp/precio/cantidad idénticos; sin IDs duplicados en la muestra | **No** deduplicar por igualdad de valores; no se comprobó unicidad global de IDs |
| Conciliación operaciones/velas | Etiquetas XBTUSD/ETHUSD, tres días UTC completos fijos (2 julio, 15 agosto, 29 septiembre), siete intervalos incluidos; 9.661.747 filas examinadas para orden temporal, 331.121 operaciones en ventanas, **11.105 velas** comparadas | OHLC y recuentos coinciden exactamente; sin intervalos poblados sin correspondencia. Agregados solapados no son observaciones independientes ni horizontes de investigación seleccionados |
| Volumen exacto | Se conservan **7.011/11.105 discrepancias** frente a suma Decimal | Diagnóstico separado reproduce los 11.105 volúmenes mediante suma binaria ordenada. Explica diferencias de representación en la muestra; sin tolerancia ajustada ni «pasa exacto» retrospectivo. Diferencias absolutas máximas: 5,22e-10 y 2,62e-9 unidades base respectivas |
| Importe negociado exacto | `cierre × volumen` difiere de `Σ(precio × cantidad)` en **10.774/11.105** agregados | C3 debe reconstruir importe por operaciones o usar un campo verificado. Se refiere a valores publicados; identidad/conversión USD independiente y exactitud de fuente siguen sin verificar |

Ambos README mencionan `SHA256SUMS.txt`, ausente en ambos ZIP. No se adquirió otro archivo de checksums. Los avisos internos no añadieron restricciones de uso incompatibles. El diagnóstico de volumen explica esta muestra; no demuestra cómo implementa el proveedor sus cálculos, ausencia de operaciones perdidas ni calidad global.

**Recomendación A: aptitud estructural con reservas, no admisión del dataset financiero.** Conservar este formato como fuente posible. Faltan elegibilidad histórica independiente, recepción original, bid/ask/profundidad ejecutables, checksum del proveedor y auditoría de histórico completo/deslistados para certificar costes, disponibilidad de C3 o cobertura científica. El trimestre autorizado cumplió su función técnica; no ampliar descargas automáticamente.


## B — evidencia del motor aislado y compatibilidad

La versión estable fijada se instaló en `/workspace/admission/nautilus-1.231.0/venv`, separada de bot_trader. La prueba conserva versiones resueltas y resultados sintéticos efectivos. No se presupone que ejemplos de v2 sean compatibles con esta API estable. Comisiones, precios y cantidades sintéticos son datos de prueba, no costes de mercado, capital ni criterios económicos recomendados.

Se conservan [resultados efectivos](../../phase-iv/admission/nautilus-results.json), [procedencia de instalación/intentos y aclaraciones](../../phase-iv/admission/nautilus-provenance.json) y [versiones aisladas resueltas](../../phase-iv/admission/nautilus-requirements-resolved.txt). La batería final tiene **15 casos en procesos hijos: 14 satisfacen sus comprobaciones y uno conserva un resultado adverso**. Son casos técnicos, no experimentos financieros independientes.

| Capacidad | Evidencia | Conclusión |
|---|---|---|
| Runtime/dependencias | Python 3.12.14 Linux ejecuta 1.231.0. Metadatos instalados exigen `pyarrow>=25.0.0`; producción exige `>=19,<24` | **Integración en el entorno único actual incompatible.** PyArrow 26 queda aislado; no cambiar locks. Preferir worker versionado separado si posteriormente se admite |
| Órdenes/tiempos | Secuencia mecánica compra/venta y denegación nativa de venta antes de recibir inventario; latencia positiva encolada se resuelve en un tick posterior | Pasa fixture causal; ticks dispersos no resuelven ejecución sub-tick exacta. Sin calibración realista de latencia |
| Contabilidad/comisiones | Reconstrucción Decimal independiente de efectivo, inventario, posiciones y comisión maker/taker por fill; libre + bloqueado = total; cancelación libera efectivo | Pasa fixture spot/USD inventado y redondeo fijado; sin estado externo de venue ni certificación de conversión stablecoin |
| Fills parciales/ausentes y rechazos | IOC nativa ejecuta 1 de 4 y cancela 3; límite no negociable permanece sin fill y se cancela; post-only negociable rechazado; denegaciones por saldo/mínimo/precisión | Pasan casos nativos. Cambiar una política futura a IOC exige justificación científica/económica propia |
| Liquidez visible finita | Fixture market L1 muestra una unidad; ejecuta 1 a 104 y otras 3 a 104,01 | **Falla requisito conservador de liquidez visible finita.** Extrapolar fuera de L1 no es profundidad observada. No implica rechazar todo Nautilus ni admitir sus supuestos por defecto; L2/colas/impacto sin verificar |
| Duplicados | Envío duplicado no añade orden/fill; reinyectar el mismo evento nativo conserva cuentas/órdenes/posiciones | Pasa idempotencia acotada del motor de ejecución; reinyección no es otra prueba de matching/liquidez ni cubre todo duplicado externo |
| Fallo/repetición | Salida deliberada 23 conserva traza tras compra completada con posición abierta; fixture roundtrip distinto se repite en otro proceso | **No demuestra recuperación:** sin caída con orden pendiente, restauración de checkpoint, continuación/reconstrucción del caso interrumpido ni conciliación externa. La nota de procedencia precisa una formulación excesiva del resultado original |
| Carga técnica | 10.000 ticks inventados procesados sin órdenes | Solo prueba de escala técnica; sin entrenamiento, carga de estrategias ni garantía de capacidad |

Conversión stablecoin, admisión de datos obsoletos, bajas/fallos de salida, profundidad, conciliación externa y despacho de autorizaciones de producción **no se probaron** aquí. Un futuro adaptador debe verificarlos antes del uso financiero dependiente. No se activó nueva conexión/autenticación, cliente live, scheduler ni proceso paper. Los metadatos declaran LGPL-3.0-or-later; obligaciones de integración/distribución se revisarán para el uso concreto.

**Recomendación B: conservar Nautilus como candidato condicionado a motor aislado; rechazar instalación inmediata en el mismo entorno y admisión de fills market L1 por defecto.** Prueba acotada terminada con límites, no certificación de admisión. No hay motivo para reconstruir la plataforma ni instalar otro motor solo por aumentar cobertura.


**Consecuencia arquitectónica:** el contrato actual `Execution.execute(...) -> Fill` y su ledger v1 exigen intencionadamente un único fill sintético completo. Fills parciales y estados asíncronos requieren un límite de eventos/estados versionado por separado, efectivo/inventario conciliables e idempotencia. No se deben importar datos reales como sintéticos, eliminar controles ni afirmar que los eventos del motor ya pasan por producción. La gobernanza experimental, transformaciones, inferencia y custodia del holdout seguirán en bot_trader. Un worker aislado con entradas/salidas versionadas sigue siendo una alternativa coherente de plataforma única; no se implementó un adaptador financiero completo.

LEAN directo sigue como alternativa documentada si una limitación concreta de Nautilus impide el mecanismo requerido; no se instaló ni midió. Freqtrade se conserva como referencia metodológica/alternativa. Cambiar de motor o ampliar el ledger sintético no resuelve carencias históricas de fuentes, cotizaciones o elegibilidad. Una instalación alternativa necesitaría alcance autorizado propio.

## Recursos y reproducibilidad

| Tarea medida | Tiempo transcurrido / CPU | RAM máxima o almacenamiento conservado |
|---|---|---|
| A adquisición satisfactoria | 32,65 s / 4,94 s CPU; HEAD fallido conservado aparte | 19,25 MiB RSS; 2.172.918.907 bytes de archivos conservados |
| A inventario completo + QA extremos + conciliación | 69,04 s / 68,92 s CPU | 25,52 MiB RSS; ~5,34 MB de inventario privado, sin extracción completa |
| A diagnóstico de volumen separado | 26,27 s / 26,26 s CPU | 23,75 MiB RSS; mismos archivos/ventanas, sin descarga adicional |
| B instalación | 7,38 s; usuario + sistema del instalador 4,21 s CPU | 51,38 MiB RSS de instalación, no RAM del motor |
| B batería final de 15 procesos | 9,52 s / 13,84 s CPU sumada de hijos | 411,60 MiB RSS máximo de un hijo |
| B cuatro baterías conservadas | 37,60 s / 49,49 s CPU sumada de hijos | Máximo 412,54 MiB RSS de un hijo; 935.501.824 bytes asignados en disco para entorno/cache/logs al consolidar |

CPU puede superar tiempo transcurrido por hilos de procesos/bibliotecas; RSS es máximo individual, no memoria total simultánea. Tiempo exploratorio y documental no se midió completamente. El fallo inicial de medición B (`/usr/bin/time` ausente) ocurrió antes de instalar y se conserva. Solo se afirma la instalación aislada efectiva.


Estas mediciones corresponden a archivos y fixtures técnicos en este host Linux cloud; no estiman las 26 especificaciones financieras, el rendimiento del PC Windows ni disponibilidad operativa continua. El instalador muestra tamaños de paquetes redondeados; no se inventa tráfico total exacto ni factura. No se contrató ningún servicio nuevo. Host existente/electricidad y trabajo de ingeniería no se midieron en USD. El registro completo de ajustes/reajustes/semillas/estrés/incertidumbre de E3 continúa pendiente.

Originales, inventario detallado y entornos desechables quedan fuera de Git en `/workspace/admission`. Se versionan métodos, registros, agregados y resultados sintéticos, sin series de precios reconstruibles. Los comandos de reproducción figuran al final. Repetir QA sobre archivos existentes no requiere descargarlos otra vez; el adquirente rechaza sobrescribir artefactos. Si otro entorno carece de ellos, hay que revisar permisos e identidades registradas antes de volver a adquirirlos, sin descargar material adicional silenciosamente.

## Cobertura histórica futura y ampliación de fuentes

El trimestre y Kraken son **elecciones de muestreo técnico únicamente**. El dataset futuro debe maximizar el histórico científicamente útil, fiable y económicamente razonable entre ciclos, según la hipótesis y la calidad observada. No se fija fecha inicial, número de monedas ni proveedor exclusivo. Más histórico aporta valor con unidades, identidades y tiempos comparables y considerando cambios de mercado; no proporciona automáticamente evidencia independiente.

| Dimensión de comparación futura | Evidencia necesaria antes de la investigación dependiente |
|---|---|
| Profundidad y universo cambiante | Cobertura por instrumento/tiempo; altas, bajas, migraciones y denominaciones históricas; activos desaparecidos cuando sean obtenibles; lagunas de supervivencia explícitas |
| Granularidad y ejecución | Operaciones/velas/cotizaciones/profundidad efectivas, precisión y disponibilidad temporal; costes, liquidez, latencia y reglas apropiados al mecanismo |
| Calidad y revisiones | Versiones, cambios de esquema, contrastes independientes, huecos/duplicados/correcciones; histórico corregido actual no equivale a primera publicación |
| Derechos y economía | Retención/investigación/modelos/resultados derivados permitidos, acceso en tiempo real, adquisición y coste recurrente; gratuito primero solo si es apto |
| Información adicional | Versiones/recepción de noticias y sentimiento, finalidad/reorganizaciones on-chain, definiciones de funding/margen/posicionamiento; adaptadores tipados y QA específicos |

Reutilizar la comparación existente antes de nuevas consultas dirigidas. Proponer manifiesto finito con finalidad, cobertura marginal, derechos, tamaños, almacenamiento/procesamiento e intervalos expuestos/reservados. **Toda adquisición adicional requiere autorización separada.** Este informe no autoriza descargar todo el histórico, otro proveedor, licencias premium ni admisión financiera. Q3 inspeccionado es material expuesto de QA, nunca un holdout final intacto.

## Decisiones materiales siguientes

1. **No elegir cifras E3/E4 a partir de estas pruebas.** Aportan evidencia de fuentes e ingeniería, no presupuesto completo, ventaja neta alcanzable, capital primario, margen de materialidad ni límite de riesgo. Conservar 1.000/5.000/10.000 USD solo como sensibilidades. Tarifas/mínimos/cotizaciones/capacidad históricas y cobertura siguen condicionando el paquete económico.
2. **Siguiente adquisición, si se continúa:** revisar una propuesta concreta y acotada de cobertura histórica comparativa que resuelva las lagunas observadas, en vez de autorizar todo el histórico o elegir proveedor permanente. No se recomienda ahora ninguna compra. Acceso/uso, gastos y alcance técnico adicional deben autorizarse antes de actuar.
3. **Antes del desarrollo empírico:** revisar una aclaración prospectiva de admisión por etapas y el alcance financiero concreto. QA estructural y órdenes/contabilidad sintéticas no estiman varianza/dependencia de rendimientos netos emparejados candidata–referencia. Si se elige esa vía, hay que separar expresamente admisión del desarrollo y admisión de validación/final. Mantener búsqueda finita, criterios económicos prospectivos, una admisión de validación y final protegido; ningún piloto encubierto en QA. La alternativa es mantener preparación metodológica condicionada y posponer el trabajo empírico.

Esquemas, parsers y adaptadores compatibles son decisiones técnicas del proyecto dentro del siguiente alcance autorizado; el usuario no debe aprobar cada campo o llamada. E1/E2 y A/B no necesitan aprobación repetida. UX, glosario y guía siguen como trabajo futuro registrado. La [aceptación](acceptance.md) conserva los requisitos de cierre y transición a V.

## Límites y conservación

Corpus científico, H-00–H-24, prioridades C1/C3, comparación C2, reservas C4/C5 y siete contadores financieros en cero permanecen intactos. Se distinguen documentación, hechos estructurales observados, comportamiento nativo del motor, controles del programa de prueba y capacidades sin verificar. Los negativos se conservan; estas pruebas no aceptan ni rechazan económicamente ninguna estrategia.

## Reproducción y registro de verificación

Usar archivos locales y entorno aislado ya autorizados; estos comandos no descargan datos. Elegir rutas nuevas: las herramientas preservan artefactos anteriores. La batería del motor termina con código **1** por la comprobación L1 adversa conservada; no eliminarla para obtener resultado verde.

```bash
python -m unittest discover -s tools/admission -p 'test_kraken*.py' -v
python tools/admission/kraken_qa.py --archives /workspace/admission/kraken/archives --output /workspace/admission/kraken/qa-repeat --result /workspace/admission/kraken/qa-repeat-result.json
/workspace/admission/nautilus-1.231.0/venv/bin/python tools/admission/nautilus_probe.py --output /workspace/admission/nautilus-1.231.0/probe-repeat
```

Son instrucciones de reproducción, no repeticiones adicionales realizadas en esta entrega. La versión inicial ejecutada de Kraken está en `f548ed0`; la actual añade vinculación explícita al hash adquirido y el diagnóstico de volumen registrado por separado. Se conservan ambos hashes y el digest original del resultado. El código final Nautilus coincide con su hash ejecutado; no se conservaron snapshots anteriores del programa, aunque sí resultados/digests en procedencia. Versiones resueltas y digests de RECORD instalado no son hashes de wheels ni un lock completo de cadena de suministro.

[Registro de verificación](../../phase-iv/admission/verification.json): pasan nueve pruebas offline de controles/QA; hashes ejecutados coinciden; pasan rutas locales y parseo JSON/JSONL. Cuerpos científicos de hipótesis/investigación, protocolo/anexos, UX futura, código/tests/web/locks de producción y vinculaciones financieras siguen intactos. La revisión interna independiente detectó y corrigió el exceso de afirmación sobre recuperación, la interpretación del conflicto de dependencias y la falta de cotejo de conjuntos de pares. No es validación financiera independiente. La batería histórica de producción no se repitió ni se volvió a contar.
