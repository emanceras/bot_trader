# Fase IV — Admisión de datos, universo, horizontes y ejecución

Documento: IV-DATA-001 · Versión: 1 · Actualizado: 2026-10-24 · Idioma: es (traducción).

Original: [inglés](../../en/phase-iv/data-execution.md), sincronizado con IV-DATA-001 v1. Este anexo metodológico desarrolla ROADMAP IV.1, IV.6, IV.9 e IV.11. Reutiliza la [evaluación de viabilidad](../../phase-ii/FEASIBILITY.md), el [proceso de horizontes](../../phase-ii/HORIZONS.md), la [evaluación de acceso](../../phase-ii/ACCESS.md) aceptados y la evidencia científica indicada abajo. Sus estados fechados de fase/aprobación son históricos; la nueva autorización permite exclusivamente metodología de IV.

**Estado actual:** especificación documentada; ningún dataset de mercado, proveedor, contrato, tarifa ni motor financiero ha superado admisión. `ready_to_execute = false`. No se adquirieron históricos de mercado, probaron feeds ni realizaron experimentos financieros para este anexo. Un valor pendiente es un bloqueo explícito, no permiso para elegirlo después de observar rendimientos de estrategias.

## 1. Alcance, unidades y registro de concreción

C1/C3 siguen como primarias, C2 como comparación secundaria de riesgo y C4/C5 como reservas condicionadas. Spot sin préstamo es un escenario inicialmente evaluable, no una restricción permanente de productos ni una acreditación de acceso. Una fuente informativa no tiene que ser un instrumento que el sistema pueda negociar. España es la jurisdicción inicial; un exchange extranjero no cambia residencia ni obligaciones legales. Debe comprobarse acceso por producto/entidad/cliente antes de tratar una oportunidad como disponible para este operador. Otra jurisdicción legítima futura sería un escenario versionado separado, no una suposición de VPN. Disponibilidad legal histórica y acceso actual son preguntas distintas.

Antes de admitir un ensayo financiero debe concretarse un registro versionado con los campos siguientes. Es un contrato documental, no un esquema implementado ni un manifiesto de datos cumplimentado. Todos los campos sin resolver tienen actualmente valor `null`; una cadena vacía o un valor inventado no satisfacen la admisión.

| Grupo | Campos obligatorios | Quién/qué lo resuelve antes del uso |
|---|---|---|
| Alcance | `protocol_id`, `protocol_version`, `candidate_id`, `product_scenario`, `account_currency`, `jurisdiction_scenario`, `research_only_instruments` | Responsable del protocolo; la moneda de cuenta ya es **USD**. Escenario e instrumentos concretos necesitan decisión explícita |
| Fuente | `source_id`, `source_version`, `source_url`, `retrieved_at_utc`, `licence_scope`, `retention_policy`, `acquisition_cost_usd`, `approval_reference`, `raw_manifest_hash`, `coverage_start`, `coverage_end` | Revisión de admisión y permiso aplicable de adquisición; la cobertura declarada en metadatos no equivale a cobertura real verificada |
| Identidad/universo | `instrument_master_version`, `universe_rule_version`, `eligibility_asof_rule`, `venue_entity`, `product_class`, `listing_history_source`, `token_event_policy` | Inventario histórico de instrumentos y especificación de elegibilidad |
| Relojes/calidad | `timestamp_semantics`, `timestamp_precision`, `clock_error_bound`, `availability_policy`, `max_age_by_field`, `gap_policy`, `duplicate_policy`, `correction_policy`, `quality_report_hash` | Auditoría temporal/de calidad anterior a calcular resultados financieros |
| Ejecución | `engine_adapter_version`, `order_policy_version`, `fill_model_version`, `fee_schedule_version`, `latency_model_version`, `capacity_rule`, `borrow_margin_policy`, `funding_rule_version`, `usd_conversion_policy`, `cash_return_policy` | Ingeniería/admisión específica del instrumento; no se presume que el ledger técnico satisfaga este requisito |
| Concreción financiera | `capital_scenarios_usd`, `cost_budget_usd`, `fixed_cost_allocation`, `minimum_economic_effect`, `period_partition_manifest`, `stress_plan_version` | Concreción del protocolo basada en datos y aprobación de recursos; las reglas estadísticas residen en el protocolo principal |

`approval_reference` distingue aprobación metodológica, adquisición de datos, ejecución financiera y gastos. Completar un registro no concede ninguno de esos permisos. Conservar versiones, recibos de fuentes, enmiendas y alternativas rechazadas. Fechas exactas, umbrales numéricos, tarifas y latencias permanecen pendientes hasta disponer de evidencia; deben congelarse antes de la selección o evaluación dependiente.

## 2. Universo point-in-time y admisión de fuentes (IV.1)

La unidad es **identidad del activo / contrato / venue / par / intervalo de existencia**, no una cadena ticker. Conservar monedas de cotización, liquidación y garantía, multiplicador, precisión, lote/notional mínimo y fechas de vigencia. Distinguir cambio de nombre de activo nuevo, redenominación de retorno y representación envuelta de su subyacente. Cadena, dirección de contrato o IDs del proveedor son referencias asociadas, no identidades universales.

Definir en cada instante de decisión `t`:

- `U_I(t)`: instrumentos cuyas observaciones y metadatos de identidad necesarios se conocen en `t`, incluidos posibles predictores no negociables. No exigir supervivencia al final del estudio.
- `U_O(t; K)`: subconjunto admisible para el escenario jurídico/producto elegido, conversiones, tamaño/precisión, financiación/préstamo cuando corresponda y liquidez accesible al capital `K`.
- La inclusión usa solo información retrasada disponible en `t`: calentamiento suficiente, cobertura utilizable, semántica de precios/volumen, spread/profundidad o proxy de capacidad validado y regla congelada. Declarar cadencia de actualización y corte informativo. No fijar un número de monedas ni ordenarlas por rendimientos posteriores.

Un primer alcance representativo puede ser todos los instrumentos históricamente elegibles de un dataset admitido de un venue/producto, con sus límites. Un alcance multivenue más amplio se admite solo si permite conciliar identidad, duplicados, relojes, saldos accesibles y ejecución. Un alcance más pequeño de alta liquidez puede justificarse con una regla congelada, pero no representa automáticamente todo el mercado cripto. Estratos grandes/medianos/pequeños pueden usar liquidez retrasada y, solo si existe histórico apto, oferta/capitalización; describen segmentos, no buscan retrospectivamente el rentable. No exigir historia completa de todos los activos durante toda la muestra: eliminaría nuevas entradas y desapariciones.

La admisión es específica de **campo × instrumento × intervalo × uso previsto**. Primero obtener los permisos y decisiones de licencia/coste aplicables a una auditoría posterior de calidad; IV no realiza esa adquisición. La auditoría futura deberá examinar identidad cruda/derivada, altas y cierres, significado de timestamps, unidades, correcciones, ausencias, reconstrucción muestral e integridad. Registrar aceptación, uso condicionado o rechazo con la afirmación afectada. Un endpoint público documentado, cita académica, listado actual de símbolos o checksum no acredita aptitud histórica. Las reglas históricas de tarifas/tiers no se reconstruyen por suposición desde la página actual.

### Ausencias, cierres y correcciones

| Condición | Tratamiento preespecificado |
|---|---|
| Mensaje/barra duplicados | Usar identidad de evento por proveedor y versión/secuencia cuando existan; duplicados exactos idempotentes. Los conflictivos permanecen marcados y bloquean cálculos afectados hasta resolverse; nunca escoger el más rentable |
| Registro tardío/corregido | Conservar original y tiempos de recepción/revisión. La reconstrucción usa la versión conocible entonces; una vista investigadora corregida es distinta de lo que un operador podía saber |
| Hueco u observación obsoleta | Marcar calidad/disponibilidad. No fabricar barra negociable, retorno cero ni interpolar silenciosamente. El último precio puede permitir valoración provisional explícita con antigüedad máxima congelada, pero nunca acredita liquidez ejecutable |
| Predictor ausente | Aplicar política congelada ajustada solo dentro del desarrollo o abstenerse; no elegir imputación/exclusión con resultados de validación/finales. Informar exclusiones por causa y candidata |
| Deslistado, suspensión, quiebra | Conservar instrumento y evento. Bloquear nuevas entradas cuando la restricción era conocible; simular cierre solo con evidencia de ejecución/liquidación. Recuperación desconocida no equivale a salida al último cierre ni a recuperación cero automática |
| Valor terminal desconocido | Informar posición sin resolver y cotas económicamente defendibles por separado; si puede cambiar la conclusión, clasificar evaluación inconcluyente/no admisible en lugar de eliminar el activo |
| Fork, migración, redenominación | Aplicar regla versionada de derechos/unidades con tiempos conocidos de anuncio/vigencia/recepción y acceso efectivo. Evitar tratar reclamaciones duplicadas o cambios de unidades como beneficio |

Las comparaciones emplean los mismos instantes objetivo elegibles y convenciones de ejecución cuando necesitan información común. Informar universo completo y cada exclusión, además de comparación emparejada con soporte común; cambiar soporte puede cambiar el objeto estimado. El soporte común no debe convertirse en un filtro encubierto de supervivientes al final. Si una candidata necesita una historia más corta, informar la limitación y comparar todas las referencias pertinentes en ese mismo intervalo.

## 3. Contabilidad USD y capital

Patrimonio, rentabilidad y costes comparables se expresan en USD. USDT, USDC, BTC y otros numerarios siguen siendo instrumentos distintos. Para cada activo/pasivo o flujo fijar fuente de valoración, moneda, ruta a USD, disponibilidad, antigüedad máxima y regla alternativa/abstención. No convertir toda la historia al cambio final ni suponer paridad permanente de una stablecoin con USD.

Separar valorar un saldo de convertirlo realmente. La conversión ejecutada incurre en su bid/ask/comisión/latencia solo cuando sucede. Un depeg ya incorporado en valoración USD no se vuelve a restar como pérdida separada. El patrimonio de derivados incluye valor/P&L contractual y obligaciones; su nocional no es un activo adicional. Colateral aceptado para varias funciones se cuenta una sola vez. Capital restringido/reservado, saldos en distintos venues, garantías y reservas operativas forman parte del comprometido; retorno sobre margen mínimo no es retorno sobre el capital de la plataforma.

Usar `K = 1.000 / 5.000 / 10.000 USD` como escenarios de sensibilidad solicitados, no como límites ni fondos decididos. Para cada `K`, recalcular tamaños mínimos, asignaciones factibles, tarifas/tier, capacidad y margen, sin escalar linealmente P&L. Si hace falta otro capital, justificarlo por instrumento/recursos, no por rentabilidad deseada. Apalancamiento real y drawdown personal siguen sin aprobarse. Ninguna sensibilidad numérica de riesgo es un umbral personal aceptado.

Mostrar referencias de efectivo y buy-and-hold con convenciones equivalentes de cuenta, conversión y costes. El efectivo ocioso puede usar USD sin remuneración cuando sea accesible en el escenario; de lo contrario definir un instrumento accesible. No asignar automáticamente rendimiento de Treasury o stablecoin. La elección se congela con el escenario. Aportaciones/retiradas externas se separan del beneficio de inversión; el convenio inicial más sencillo es un ledger financiado equivalente sin flujos externos.

## 4. Relojes causales y elección finita de horizontes (IV.11)

Fijar por separado resolución de observación, disponibilidad, lookback, intervalo de predicción, mantenimiento/salida, decisión/rebalanceo, reajuste del modelo, demora de ejecución y controles operativos de riesgo. Una señal de cierre de barra está disponible después de esa barra, no en su apertura o un cierre anterior. La etiqueta predictiva no puede comenzar antes de la entrada ejecutable especificada; un target diagnóstico al mid debe distinguirse expresamente de su aplicación negociable posterior.

Para cada valor `x`, escoger la última **versión elegible** cuya cota fiable de disponibilidad/recepción no supere el corte de decisión. La disponibilidad de una transformación será al menos la máxima de sus entradas más demora de cálculo/recepción. Normalizar a UTC conservando zona original, DST, precisión, reloj e incertidumbre. Un tiempo desconocido sigue desconocido. Una cota conservadora documentada puede servir para una pregunta más lenta solo si está respaldada y precede a la decisión; inventar un retraso no repara procedencia ausente.

Para variables entre activos/exchanges, usar joins as-of, tolerancias explícitas de frescura y fronteras UTC comunes. No unir por timestamp más próximo si selecciona un valor posterior. Coincidir en timestamp no elimina demoras distintas, relojes desincronizados o precios obsoletos. El ajuste futuro de factores/normalización/universo/grafo usa únicamente entrenamiento permitido. Incorporar el futuro contemporáneo de otra moneda atravesando una frontera cronológica es leakage.

Aplicar el proceso de horizontes aceptado en este orden:

1. Especificar pregunta económica y duración informativa, reutilizando evidencia y adversos. C1 tiene motivación documentada de días/semanas; el target C3 se justifica independientemente; la memoria de riesgo C2 se distingue de su rebalanceo. Son argumentos iniciales, no restricciones universales de frecuencia.
2. Comprobar si tiempos/resolución de fuente y demora alcanzable permiten resolver la pregunta. La evidencia rápida lead–lag de C4 no se transforma en señal horaria por facilidad de datos. El calendario de funding C5 es contractual y no tiene por qué ser el mantenimiento.
3. Concretar una especificación principal de relojes por comparación admitida y alternativas/sensibilidades finitas justificadas en el registro central de búsqueda. Sin producto cartesiano automático monedas × ventanas × modelos × frecuencias. Si dos relojes no pueden distinguirse antes de investigar, ambos consumen el mismo presupuesto declarado.
4. Elegir solo dentro de desarrollo y validar el procedimiento completo. Los vecinos de sensibilidad no sustituyen una especificación final fallida. Reabrir un horizonte pospuesto solo por cambios en datos, latencia alcanzable, evidencia de mecanismo o recursos, con enmienda prospectiva y presupuesto explícito.

Para variantes rápidas exigir distribución/colas de demora completa, precios ejecutables posteriores a recepción y profundidad/secuencias suficientes; un benchmark de inferencia no basta. Si la demora medida o sustentada conservadoramente consume la oportunidad propuesta, posponer la variante; no rechazar universalmente su mecanismo. Este anexo no inventa duraciones, frecuencias ni cifras de latencia.

## 5. Política de ejecución y costes (IV.6)

Un motor financiero futuro deberá superar la admisión pertinente de contrato/adaptador de la [arquitectura de III](../architecture/engines.md) y su [complemento](../architecture/supplement.md). El ledger sintético actual no es ese motor. Simular órdenes solo tras disponer de información y transcurrir cálculo, envío y aceptación. Respetar precisión, notional mínimo, capacidad, rechazos/fills parciales, cancelaciones y mercados no disponibles. Lo no soportado debe impedir la admisión, no convertirse en fill perfecto.

Elegir una representación de fills/costes explícitamente conciliada por ensayo:

- **Ruta de cotizaciones ejecutables:** usar bid/ask y profundidad accesible al tiempo simulado de aceptación/fill, más impacto residual sustentado aparte de lo que esa profundidad ya refleja. Spread y consumo de profundidad están dentro del precio ejecutado. Añadir una vez comisiones explícitas y flujos efectivos de financiación.
- **Ruta de precio de referencia:** si faltan quotes suficientes, partir de una referencia contemporánea definida y añadir modelo de spread/liquidez/impacto respaldado empíricamente, con incertidumbre. Etiquetar resultados condicionados al modelo. Una barra OHLC no identifica prioridad intrabar, secuencia de stops/límites ni posibilidad de ejecutar sus extremos. Si esos hechos deciden la afirmación, rechazar la especificación de ejecución en lugar de asignar fricción cero.

Cantidades firmadas y precios efectivos actualizan caja/inventario; comisiones y pagos de liquidación actualizan caja. El P&L neto de negociación es cambio de patrimonio valorado coherentemente menos flujos externos, con dichos cargos ya contabilizados. La atribución a spread, timing, impacto, selección adversa y comisiones debe conciliar con ese ledger; atribuir no añade otro cargo. La liquidación terminal o mantenimiento continuado tiene política congelada; valorar al mid no demuestra salida ejecutable.

| Componente | Evidencia y tratamiento necesarios |
|---|---|
| Comisiones/rebates | Vigencias versionadas, venue/producto y tier alcanzable, maker/taker, moneda y requisitos de token. No conceder rebate institucional ni conocer al principio el volumen futuro de todo el mes |
| Spread/profundidad/impacto | Ruta anterior correcta, capacidad según tamaño, rechazo de quotes obsoletas y participación acotada; volumen declarado no garantiza volumen económico accesible |
| Latencia/órdenes sin ejecutar | Política recepción→decisión→aceptación→fill, interrupciones y fills ausentes/parciales. Tocar precio maker no garantiza fill; snapshots L2 no establecen prioridad |
| Financiación/préstamo | Tipo accesible, devengo, inventario disponible, recalls, renovación y garantías. No admitir instrumento que requiera préstamo indisponible |
| Funding | Signo pagador/receptor, base de marca/nocional, elegibilidad y pago según contrato. Tasas estimadas, anunciadas y liquidadas son distintas: el funding futuro realizado no entra en una señal anterior |
| Margen/liquidación | Reglas iniciales/mantenimiento, haircuts, valoración, deducciones de funding, liquidación/seguro/impago y capital conjunto. Delta neutral no garantiza solvencia; marcas de fin de barra pueden ocultar liquidación intrabar |
| Varias patas/venues | No presumir cobertura atómica ni transferencia instantánea. Modelar exposición entre patas, prefinanciación, transferencias/costes, interrupciones y estado desconocido. Denominador de capital comprometido completo |
| Costes fijos/investigación | Separar compra de históricos y desarrollo de feeds/inferencia/hosting/soporte recurrentes. Mostrar desembolso y asignación económica. No amortizar y cargar íntegramente la misma compra en el mismo P&L |

Los escenarios de costes históricos y costes actuales accesibles tienen significados distintos. Si faltan versiones históricas de tarifas, un contrafactual de tarifa actual puede ser útil si se predeclara, pero no acredita retorno neto histórico exacto. Si la conclusión depende de un coste no identificable, conservar incertidumbre o posponer, sin imputar silenciosamente el caso más barato. No se certifica aquí ningún venue/tarifa actual; las revisiones regulatorias/de fuentes no son homologaciones renovadas de proveedores.

Con coste fijo recurrente anual `F` y capital comprometido `K`, `F/K` es la carga fija de equilibrio antes de fricciones variables. La tabla previa de II usa costes hipotéticos, no cotizaciones. El valor incremental es `ΔΠ_neta = ΔΠ_antes_de_costes_incrementales − ΔC_variable − ΔF`; no restar costes ya incluidos en el primer término. Un predictor útil puede fallar económicamente; un modelo más sencillo puede necesitar menos mejora para cubrir costes, sin acreditar mayor potencial bruto. Evaluar incertidumbre, colas y capacidad junto con el efecto. No imponer rentabilidad máxima posible.

## 6. Estrés y comprobaciones de imposibilidad preespecificados

Congelar supuestos base, alternativas documentadas e incertidumbre antes de observar resultados de candidatas. Usar las mismas definiciones de escenarios para comparadores emparejados, permitiendo diferencias reales de turnover/tamaño/ejecución. Los siguientes ejes definen comprobaciones pertinentes exigidas, no una búsqueda cartesiana ilimitada:

| Eje | Qué debe concretar el plan de estrés |
|---|---|
| Tarifa/acceso | Tier base alcanzable y otro peor documentado aplicable; pérdida de rebates/descuentos cuando proceda |
| Liquidez/capacidad | Mayor spread, menor profundidad accesible e incertidumbre de impacto respaldados por propiedades de mercado del desarrollo o escenarios estructurales explícitos; límites de participación/rechazo |
| Demora/continuidad | Más demora de recepción/ejecución, input obsoleto/ausente, venue inaccesible, fills parciales/ausentes; política definida de parada/abstención |
| Moneda/custodia | Depeg/iliquidez de conversión, bloqueo de transferencias y pérdida por emisor/venue si es material; distinguir reproducción histórica observada de pérdida hipotética |
| Derivados, si se admiten | Funding negativo, ampliación de basis, recall, haircut, presión de margen y pérdida de una pata; no presumir cierre inmediato siempre posible |

Registrar IDs, datos de construcción, parámetros/rangos, incertidumbre de fuente, duración, coherencia entre variables, capital y regla comparativa. Calibrar solo con desarrollo permitido o evidencia independiente contractual/de ingeniería, nunca con rendimiento final reservado. No adoptar «doblar slippage» universal ni drawdown garantizado. Informar todos los escenarios predefinidos, incluidos no estimables; el fallo puede justificar rechazo económico, uso condicionado o posposición según protocolo, no otra búsqueda de estrés favorable.

## 7. Admisión de noticias/eventos (IV.9; condicionada, inactiva)

Las reservas textuales/noticias siguen pospuestas. Si se admiten después, fijar `event_id`, `event_group_id`, `instrument_mapping_version`, `publication_time_original`, `publication_timezone`, `publication_precision`, `provider_first_seen_at`, `received_at`, `revision_id`, `revision_available_at`, `content_hash`, `licence_scope` y regla causal congelada de agrupación. Contenido original, traducciones, duplicados, ediciones y desmentidos posteriores son versiones distintas. Conservar tiempos ausentes/inciertos y límites de retención; no prometer almacenamiento perpetuo cuando la licencia exige borrado.

La sorpresa macro usa primera publicación menos consenso de unidades compatibles disponible antes de ella; fijar corte, definición de participantes, versión y fuente. El pronóstico propio de un proveedor no es intercambiable con consenso. Vintages ALFRED por fecha no prueban recepción intradía; `LastUpdate` no es necesariamente primera observación. Calendarios actuales no sustituyen horarios conocidos históricamente. Publicación, recepción local, decisión y fill siguen siendo relojes separados.

Particionar copias/grupos y ventanas de resultados solapadas coherentemente entre activos. La agrupación causal usada por la señal no emplea texto posterior; una auditoría offline conservadora puede descubrir vínculos e invalidar un split, pero no introducir esos vínculos futuros en el predictor histórico. Congelar snapshot NLP/LLM, tokenizer, extracción, prompts, herramientas, corte de entrenamiento/conocimiento conocido o desconocido, latencia y costes de inferencia. Split cronológico y anonimización no prueban ausencia de contaminación del preentrenamiento. Si no puede descartarse, limitar la afirmación retrospectiva y exigir posterior evaluación prospectiva autorizada aparte.

Predeclarar comparaciones precio, calendario, texto e híbrido con información elegible/target/riesgo/costes/búsqueda equivalentes; incluir referencia textual léxica/estadística sencilla. Examinar demora, noticias obsoletas/corregidas y retirada de cada bloque informativo con ablaciones ajustadas en desarrollo. Separar anticipación, reacción a información ya publicada y reducción de riesgo por eventos: cambian target y coste de oportunidad. No se autoriza adquirir corpus, ejecutar inferencia ni activar la reserva.

## 8. Evidencia reutilizada y admisión pendiente

Esta síntesis metodológica no es un estudio empírico nuevo ni una auditoría renovada de proveedores. Identidad/acceso y limitaciones se conservan en las fichas existentes:

| Evidencia previa | Decisión apoyada y límite |
|---|---|
| [Evidencia direccional](../../research/evidence-directional.md), DIR-001/DIR-006; [horizontes](../../phase-ii/HORIZONS.md) | Motivación temporal C1 y resultados adversos de test; no intervalo rentable prescrito |
| [Síntesis de ejecución](../../research/execution.md), EX-01/02/05 | Importan tarifas accesibles, profundidad, cola y latencia; accuracy y rebates favorables no certifican valor neto particular |
| [Revisión de funding](../../research/gap-funding.md), FUND-01/02 | Distinguir funding/convergencia, tasas conocidas/liquidadas y capital completo; los favorables conservan omisiones de costes/margen |
| [Síntesis cross-asset](../../research/cross-asset-interactions.md) | Sincronización, factores y particiones comunes preceden al incremento; correlación no es lead–lag negociable |
| [Fuentes de noticias](../../research/news-data-sources.md), [auditoría de cobertura](../../research/coverage-audit.md) | Versiones, recepción/consenso, licencia y campos opcionales on-chain/derivados requieren admisión; producto documentado no es feed probado |
| [Acceso](../../phase-ii/ACCESS.md), [viabilidad](../../phase-ii/FEASIBILITY.md) | Entidad/producto/residencia y USD/capital completo requieren concreción; revisiones fechadas no certifican cuenta/producto actual |

Faltan dataset/venue/producto de referencia y sus derechos/coste, cobertura histórica real y eventos de instrumentos, evidencia de costes/latencia/capacidad ejecutables, supuestos de capital/recursos y efecto económico mínimo numérico, y concreción de relojes/particiones. Capital real, drawdown personal y venue operativo definitivo pueden seguir abiertos si no afectan al escenario acotado propuesto. No se inferirán silenciosamente del escenario que después rinda mejor. Aprobación de calidad de datos, admisión del motor y autorización explícita de V siguen siendo puertas separadas.
