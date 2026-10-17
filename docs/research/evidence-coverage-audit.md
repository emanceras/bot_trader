# Fuentes del contraste acotado de cobertura

**Recuperación:** 2026-10-17 UTC. **Lectura dirigida y consolidación:** 2026-10-17 UTC. Solo documentación y metadatos; **cero estudios académicos completos nuevos**, cero series de mercado. El corpus de lectura académica permanece en 53. Registro: [search-coverage-audit.jsonl](search-coverage-audit.jsonl). Los cuerpos originales se conservan fuera de Git en `/workspace/literature-cache/coverage-audit-onchain/` y `coverage-audit-derivatives/`.

Objetivo: comprobar si las lagunas señaladas impiden cerrar una revisión limitada o son condiciones selectivas de elegibilidad/datos. No se buscan rendimientos favorables ni se evalúa un proveedor mediante su publicidad. Las tres páginas efectivamente examinadas describen definiciones/reglas, no rentabilidad. Acceder a la documentación no prueba cobertura histórica, licencia, disponibilidad comercial o demora del servicio.

## AUD-D01 — Coin Metrics: Active Addresses

- **Fuente oficial del proveedor:** [Active Addresses](https://docs.coinmetrics.io/network-data/network-data-overview/addresses/active-addresses.md). La URL inicial `/asset-metrics/addresses/adractcnt` redirigió a este recurso. El archivo local termina en `.html`, pero el contenido es texto Markdown, HTTP 200; no se interpreta su tipo por la extensión.
- **Secciones examinadas:** Interpretation; Active Monthly/Weekly/Daily Addresses, Definition/Details/Asset-Specific Details; definiciones de Sent/Received. No lectura exhaustiva de todas las variantes, enlaces de cobertura o API.
- **Declaración verificada:** cuenta direcciones únicas implicadas en cambios del registro, no personas. Las actividades contadas varían entre protocolos; puede incluir pagos a sí mismo, transferencias de valor cero o transacciones fallidas. La página advierte que la actividad puede fabricarse donde crear direcciones y transaccionar resulte barato. La privacidad y los subaccounts cambian cobertura/interpretación.
- **Implicación propia:** interpretar incremento de direcciones como adopción/demanda compradora requiere un argumento adicional. El indicador es candidato a explicaciones alternativas, no una medida automáticamente comparable entre cadenas ni prueba de alpha. La advertencia del proveedor no demuestra que un dataset concreto esté manipulado.
- **Límite:** no se verificaron vintages, tiempos de publicación, tarifas/licencia o archivo de datos. No acredita por sí misma las reglas de revisión de etiquetas de exchanges de otros proveedores.
- **SHA-256:** `aba25b2a8d108115d1973613a04951e7dbc36e593f1c80ca8f6c8b28bb2f5853`.

## AUD-D02 — Ethereum.org: Gasper y finalidad

- **Documentación del protocolo:** [Gasper](https://ethereum.org/developers/docs/consensus-mechanisms/pos/gasper/).
- **Secciones examinadas:** introducción y *What is finality?*; justificación/finalización y checkpoints. No se auditaron todas las cifras de penalizaciones de otras secciones ni se trasladan a parámetros actuales de trading.
- **Contenido verificado:** distingue elección de cadena, bloques justificados y finalizados. La finalización exige acuerdos entre checkpoints; observar un bloque no equivale por sí mismo a disponer de información con ese estado de finalidad.
- **Implicación propia:** una investigación debe fijar qué información podía observar y con qué confirmación al decidir; una marca del bloque no certifica recepción local. No se impone una demora universal ni se supone que todo algoritmo deba esperar finalidad. Dependencia de la cadena y riesgo de reorganización deben ser explícitos.
- **Límite:** no hay prueba de recepción, medición de latencia o estrategia rentable; el documento no sustituye datos históricos de un proveedor.
- **SHA-256:** `6eae5bfe126b347ba174c91ade8accc3cc8a9d16c325059aa417a79f3a4a6b50`.

## AUD-D03 — Binance: Open Interest Statistics

- **Documentación oficial:** [Market Data — Open Interest Statistics](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data#open-interest-statistics), destino de la URL inicial `.../Open-Interest-Statistics`.
- **Alcance leído:** sección de `GET /futures/data/openInterestHist`, parámetros, notas de disponibilidad y respuesta; líneas 2915–3045 de la extracción de texto local. No se leyó ni validó todo el catálogo y **no se consultó el endpoint de datos**.
- **Declaraciones verificadas:** disponibilidad de datos del **último mes** en ese endpoint; límite de respuesta de 500; los periodos sin trades pueden omitirse y no rellenarse. Distingue `sumOpenInterest`, `sumOpenInterestValue` y `timestamp`, descrito como fin del periodo en milisegundos.
- **Implicación propia:** este endpoint documentado no demuestra por sí solo acceso a un histórico multianual. Omisiones no deben interpretarse automáticamente como cero. La hora de fin de intervalo no certifica hora de publicación/recepción. Habría que identificar y auditar otra cobertura o un archivo prospectivo autorizado si se necesita más historia.
- **Límite:** la restricción es de ese endpoint/documentación, no prueba de ausencia de archivos alternativos ni de imposibilidad de obtener datos. No valida la API, contratos históricos, ratios long/short, liquidaciones o P&L. OI no es por sí solo posición direccional neta; esa distinción es contable, no un resultado predictivo de esta página.
- **SHA-256:** `037755001baa339d7a88f7acc4e963f4a1f9669ed3eb64bece0b4b668a7263b2`.

## Accesos sin contenido objetivo: no cuentan como documentación leída

| ID | URL intentada | Contenido inspeccionado y límite | SHA-256 |
|---|---|---|---|
| AUD-X01 | [Glassnode PIT](https://docs.glassnode.com/guides-and-tutorials/metric-guides/point-in-time-pit-metrics) | HTTP 200 con **Page Not Found**. Sugiere una ruta nueva, no recuperada dentro del límite. No acredita reglas de productos PIT | `ead810a3873c6244f4267c41a46ef8db330c4b8e24e030244318141a05731fd7` |
| AUD-X02 | [Glassnode entidades](https://docs.glassnode.com/guides-and-tutorials/metric-guides/entity-adjusted-metrics) | HTTP 200 con **Page Not Found**. No se verificaron reglas de clustering, revisiones o etiquetas históricas | `f7d70e61d558f3da6ce27c874004f1956c077a6915933de7337d01b74b1bc970` |
| AUD-X03 | [Binance Liquidation Order Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams) | HTTP 200 con portada/navegación genérica. No contiene especificación objetivo suficiente; **no se atribuye al feed un intervalo de muestreo ni una garantía de cobertura** | `1a88d0112b684c02f29f0314b6a9a790556d9d763a3db48afe7ec69a4067d339` |

Los riesgos de revisión de etiquetas y cobertura de liquidaciones se mantienen como **condiciones por verificar**, no como características demostradas de esas páginas inaccesibles. No se deduce que todos los proveedores fallen ni se usan los fallos de acceso como evidencia negativa de trading.

## Cribado académico limitado: metadatos y resúmenes, sin originales

Se intentaron tres consultas Crossref de cinco resultados: `cryptocurrency liquidation open interest predictability` (429), `cryptocurrency token unlock vesting returns` y `cryptocurrency exchange listing delisting abnormal returns`. Las dos respuestas recuperadas contienen diez filas antes de deduplicar. El registro conserva título/DOI/tipo y decisión de cribado de cada fila. La búsqueda genérica de listings devolvió material poco específico y no establece que falte literatura sobre el tema.

Dos resultados de oferta son pertinentes, pero **solo se inspeccionaron metadatos y resúmenes devueltos por Crossref**:

- *Token Dilution and the Cross-Section of Cryptocurrency Returns*, [DOI 10.2139/ssrn.6636258](https://doi.org/10.2139/ssrn.6636258), registro `posted-content`, 2026. El resumen afirma una prima y heterogeneidad entre monedas jóvenes y maduras. No se verificaron muestra, calendario, controles, costes, cortos, OOS o independencia de selección. No se atribuye revisión por pares ni se utilizan sus rentabilidades como evidencia comprobada.
- *The 72-Hour Shock? Preliminary Evidence from 52 Token Unlock Events on Binance…*, [DOI 10.2139/ssrn.6632838](https://doi.org/10.2139/ssrn.6632838), `posted-content`, 2026. El resumen declara respuestas negativas y comparación con BTC. No permite verificar representatividad de eventos, disponibilidad previa, autorías/versión del original o P&L después de entrada. Su cita de un informe comercial tampoco es lectura ni confirmación independiente de ese informe.

Estos resúmenes impiden decir «no existe literatura específica», pero **no obligan a promover una estrategia ni a ampliar indefinidamente I**. Si posteriormente se considera una hipótesis de dilución/unlocks, un original pertinente con métodos y datos temporales deberá examinarse de forma selectiva antes de apoyar decisiones en sus resultados. En esta auditoría no se recuperó ningún original nuevo y no se falsaron esos resultados. Los demás candidatos se conservaron en el log sin promoverlos: no aportaban un mecanismo materialmente ausente a esta pregunta de cierre, y algunos trataban ámbitos distintos o posiblemente versiones relacionadas.

Hashes de respuestas Crossref: unlocks `944164639189146717463c71832020474acc1a709c991ee4d565a29f87091ac8`; listings `44a573e0ab1eaf1444f348a6bb1d5f04080eea0b9da2bf485e34216d513921f5`.

## Cierre del contraste

Tres consultas bibliográficas intentadas, dos recuperadas; seis intentos de páginas oficiales, tres con secciones relevantes examinadas y tres sin contenido objetivo. Se detuvo el bloque con esos límites, sin gastar el presupuesto restante en lograr confirmación. Las nuevas comprobaciones apoyan el filtro de semántica/disponibilidad, **no evidencia de beneficio ni saturación**. La recomendación de cierre limitado se argumenta en [coverage-audit.md](coverage-audit.md) y no depende de tratar documentación comercial como investigación académica.
