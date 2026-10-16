# Estrategias direccionales y factores: revisión crítica

Actualización de síntesis: 2026-10-16. Fase I. La base de cuatro textos se amplía con tres lecturas dirigidas: DIR-005/CTR-01, DIR-008/REV-02 y Farag/REV-03. Quedan cinco fuentes direccionales del catálogo inicial con acceso parcial; no hay réplica ni resultados propios. Véanse [contrastes](gap-contrasts.md) y [reversión](gap-reversal.md), con versiones y alcance precisos. Las [fichas](evidence-directional.md) identifican versiones, páginas, métodos y límites; el [registro de búsqueda](search-directional.jsonl) conserva consultas y errores. La revisión inicial sin acceso se conserva en Git; las conclusiones actuales la sustituyen.

## 1. Trend following y momentum

**Fundamento.** Momentum temporal utiliza, por ejemplo, `m(i,t,L)=Σ_{s=t−L+1}^t log(1+r(i,s))` para decidir exposición posterior. Momentum transversal clasifica activos según retornos previos; no es la misma hipótesis. Flujos persistentes, incorporación gradual de información o remuneración de riesgos pueden generar continuidad, sin que la correlación identifique su causa. Escalar la señal por volatilidad cambia exposición y riesgo, no crea por sí solo capacidad predictiva.

**Evidencia favorable.** Liu–Tsyvinski WP2018 (DIR-001, §4.1/tablas14–17) documenta predictibilidad semanal BTC y una prueba que fija cortes con los primeros dos años. Hudson–Urquhart (DIR-006) encuentra reglas técnicas con resultados favorables bajo controles de multiplicidad; parte de sus activos conserva métricas positivas en su prueba posterior. Ambos justifican estudiar el mecanismo, pero sus objetos no equivalen a beneficios netos de una cuenta.

**Contrastes adversos.** La lectura completa de Grobys–Sapkota 2019 (CTR-01/DIR-005) confirma ausencia de momentum significativo al 5% en sus especificaciones principales, con medias TSMOM positivas pero inciertas, costes omitidos y discrepancias en tabla 2 que se conservan. No prueba ausencia universal de momentum; comparte autor con DIR-010. DIR-001 muestra sensibilidad al horizonte y al estimador de incertidumbre. Hudson selecciona entre 14.919 reglas: las mejores reglas para las dos series BTC presentan retorno, Sharpe y Sortino negativos en enero–junio2018, mientras LTC/XRP/ETH difieren (tabla9, PDF22–23). Grobys et al. (DIR-010, editorial2025, muestra2016–2023) obtiene momentum transversal bruto no significativo en la muestra completa y pérdidas extremas; la escala de volatilidad no elimina uniformemente los peores resultados. Sus carteras largas/cortas teóricas permiten retornos inferiores a −100%: no representan una cuenta spot totalmente financiada que pudiera continuar sin liquidación.

**Fuera de muestra.** Separar cortes históricos, prueba temporal, análisis de subperiodos y seguimiento posterior a publicación. Se ha encontrado evidencia temporal, pero no una réplica independiente confirmatoria de una especificación minorista común con todos los costes. Distintas ventanas, universos y ponderaciones no son experimentos idénticos; no agregar sus Sharpes.

**Costes, datos y viabilidad.** DIR-001 no descuenta fricciones en las tablas de momentum; Hudson estima costes de equilibrio, no fills integrales; DIR-010 no establece neto negociable. Una implementación spot long/flat de frecuencia moderada sería técnicamente sencilla, pendiente de ventaja. Requiere OHLCV de un venue, reloj causal, liquidez, historial de listado/baja, tarifas y costes condicionados al tamaño. Cortos añaden instrumentos, financiación y margen; un backtest largo/corto no se traslada automáticamente a spot.

**Falsadores.** Resultado explicado por exposición comparable; selección de una sola subida o de parámetros estrechos; señal al cierre ejecutada antes de estar disponible; ventaja que desaparece con retrasos/costes realistas. Ganar sobre todo en tendencias no refuta por sí mismo una regla de tendencia.

## 2. Mean reversion

**Fundamento.** Una señal `z_t=(x_t−μ_t)/σ_t` exige una referencia estimada con pasado y un mecanismo de corrección. El modelo `x_{t+1}−μ=φ(x_t−μ)+ε_{t+1}`, `|φ|<1`, describe reversión bajo sus supuestos; no prueba que el precio de un token sea estacionario. Separar reversión de retornos, reversión transversal y reversión de spreads.

**Evidencia accesible y límites.** El WP institucional de Fičura (REV-02, ampliación de DIR-008) permite examinar métodos: tabla 3 registra reversión semanal bruta en pequeñas/ilíquidas y momentum en grandes/líquidas; los filtros de volumen debilitan la reversión. No hay coste integral ni holdout sellado. El PDF identifica autor único, frente a coautoría en metadatos de otra versión: no mezclarlas. Farag et al. 2025 (REV-03), autoría y proveedor distintos, aporta una cartera contraria a cinco minutos y previsión recursiva de su proxy de liquidez, con selección de supervivientes, cortos supuestos y costes omitidos. Su test interviene en selección de variables; no demuestra P&L neto de una política. DIR-007/013 siguen a nivel de resumen. Las dos lecturas reducen la laguna documental, sin establecer ventaja operable ni una réplica exacta.

**Contraste económico.** Bid–ask bounce, precios obsoletos y tokens pequeños pueden producir autocorrelación negativa sin beneficio capturable. Una noticia permanente, depeg o cambio de régimen impide suponer vuelta a una media. La expectativa de beneficio bruto agregada debe exceder los costes esperados; no se exige ganar en cada operación.

**Datos/costes/viabilidad.** Un horizonte intradía exige trades y bid/ask; para horizontes muy cortos, libro y fills. Una orden límite intercambia spread por riesgo de no ejecución/selección adversa. Puede formularse una referencia simple spot, pero no se justifica todavía su rentabilidad. No promediar pérdidas sin límites para forzar convergencia.

**Falsadores.** Efecto limitado a precios medios no ejecutables; media o vida media inestable; señal eliminada por latencia/spread; pérdidas de tendencia no financiables. La laguna económica es reversión con selección temporal y costes ejecutables; el acceso a métodos ya mejoró, pero no justifica añadir complejidad.

## 3. Factores en criptomonedas

**Fundamento.** `r(i,t)=α_i+β_i'f_t+ε(i,t)` explica covariación; un factor contemporáneo no predice automáticamente retornos. Mercado, tamaño y momentum pueden remunerar riesgos y restricciones. Una característica observable, una prima y su cartera ejecutable son objetos distintos.

**Favorable.** Liu–Tsyvinski–Wu WP2019 (DIR-002) estudia 1.707 monedas, 2014–2018, y un modelo parsimonioso de tres factores. Su universo incluye desaparecidas según los autores; esto es mejor que elegir solo supervivientes, pero no sustituye auditoría del proveedor. Justifica medir exposición a factores antes de atribuir alpha.

**Adverso.** De 25 características, el WP informa 16 no significativas, incluidos horizontes momentum largos. §5.1, PDF29, muestra que momentum de 1,2 y4 semanas pierde significación cuando la pata corta de perdedores se sustituye por BTC. Las restricciones de acceso cambian la evidencia. El WP habla de nueve características exitosas y el resumen editorial2022 de diez: no mezclar versiones.

**Validación/costes.** No se identificó un holdout de toda la selección de los factores ni una simulación integral de comisiones, préstamo, spread e impacto en las secciones examinadas. Significación nominal en carteras de inversión cero no demuestra rendimiento sobre capital real ni independencia de las pruebas.

**Datos/infraestructura/capital.** Universo point-in-time, identificadores, oferta circulante conocida entonces, datos de bajas, liquidez y disponibilidad histórica de cortos. Capitalización no garantiza profundidad. Comisiones fijas, mínimos de orden y rotación afectan la accesibilidad; no se fija capital mínimo sin elegir mercado.

**Falsadores.** Prima que desaparece con desaparecidos o datos no revisados; payoff dependiente de activos no negociables; uso de variables contemporáneas como predictores. Un factor puede seguir siendo útil para explicar riesgo aunque no produzca una estrategia.

## 4. Balance y continuidad

| Línea | Qué sostiene la lectura | Qué sigue sin sostener |
|---|---|---|
| Momentum temporal | Predictibilidad histórica condicionada; prueba temporal con resultados mixtos | Persistencia neta actual y superioridad minorista |
| Momentum transversal | Primas en algunas especificaciones y riesgos de cola/implementabilidad | Generalización entre horizontes, universos y acceso a cortos |
| Reversión | Dos textos con métodos: heterogeneidad por liquidez y predicción de un proxy | Ventaja neta ejecutable; OOS sellado; réplicas exactas |
| Factores | Marco para separar exposición y rendimiento residual | Alpha negociable de cada prima |

Los mecanismos merecen investigación por razones explícitas; esta tabla no selecciona estrategias de Fase II. Regímenes, escala de riesgo y combinaciones se desarrollan en [risk-portfolio.md](risk-portfolio.md). Quedan pendientes textos de reversión, versión final de factores, réplicas independientes y datos/costes recientes. La búsqueda no alcanzó saturación; las limitaciones constan en las fichas.
