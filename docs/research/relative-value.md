# Valor relativo, pares y funding/basis: revisión crítica

Síntesis actualizada 2026-10-16. Fase I. Tres textos en la base, más dos estudios de perpetuos con lectura dirigida en [gap-funding.md](gap-funding.md); fuentes y ubicaciones detalladas en [evidence-relative-value.md](evidence-relative-value.md) y accesos en [search-relative-value.jsonl](search-relative-value.jsonl). No hay réplicas propias, backtests ni estrategias seleccionadas. Volatilidad se desarrolla en [risk-portfolio.md](risk-portfolio.md).

## 1. Statistical arbitrage

El término describe oportunidades condicionadas a un modelo, no beneficio garantizado. Entre mercados, comprar al ask de A y vender al bid de B da margen bruto `q(bid_B−ask_A)` antes de fees, financiación, recomposición de inventario y ejecuciones parciales. Preposicionar fondos evita esperar cada transferencia pero inmoviliza capital y añade contraparte. Una prima en un exchange con retiradas bloqueadas puede expresar riesgo de crédito/convertibilidad.

Para activos distintos, un modelo `r_i=a_i+β_i'f+ε_i` permite estudiar residuos y carteras `β'w≈0`. Neutralidad estimada no garantiza estacionariedad del residuo, cobertura de factores omitidos ni ausencia de riesgo de cola. Los pares de la sección siguiente son una subfamilia, no confirmación independiente de todo statistical arbitrage.

**Evidencia/cobertura.** La identidad/resumen de Makarov–Schoar se localizó; el texto completo no se obtuvo en esta tanda. No le atribuimos cifras ni prueba de ganancias realizables. La evidencia completa de este bloque procede de pares y carry, con mecanismos diferentes. La fragmentación y ejecución entre venues tienen contraste en [execution.md](execution.md), sin que un modelo de impacto valide transferencias o inventarios ilimitados.

**Datos/viabilidad.** Bid/ask y profundidad sincronizados, timestamps de recepción, token/red, estado de depósitos/retiradas, financiación, cortos, límites y saldos prefondados. Velas diarias no validan arbitraje subsegundo. Descartar margen explicado por desfases, transferencia imposible, crédito no comparable o comisiones institucionales inaccesibles. El retorno debe usar capital total, no solo el nominal de la operación ganadora.

## 2. Pairs trading y cointegración

**Matemática.** Para `x_t=log P_A,t`, `y_t=log P_B,t` integrados de orden uno, cointegración exige `z_t=x_t−a−βy_t` estacionario. Correlación de retornos no basta. Valores críticos de residuos estimados difieren de una prueba de raíz unitaria aplicada sin ese ajuste. Un OU `dz=κ(μ−z)dt+σdW`, `κ>0`, tiene vida media `log(2)/κ` bajo el modelo, no garantiza convergencia antes de costes o ruptura. Con β positivo, spread alto sugiere corto A/largo B; el P&L de cantidades de tokens debe derivarse, no igualarse al cambio del log-spread.

**Fil–Kristoufek2020 (RV-E02).** Evalúa distancia y cointegración con formación/negociación cronológicas, retraso de una observación y costes simulados. Hay resultados positivos —y distancia diaria negativa—; cointegración no supera pares aleatorios en los dos intervalos intradía de la tabla2. El número de pares posibles `N(N−1)/2`, frecuencias, entradas y stops amplía selección.

Su universo conserva monedas negociadas durante todo enero2018–septiembre2019, excluyendo listados/deslistados y filtrando volumen: sesgo de disponibilidad futura. El coste de cortos se omite explícitamente y parte de esas posiciones no existía. La aproximación de impacto proviene de acciones antiguas, no del libro cripto. Un alto Sharpe simulado no acredita ejecución minorista. Las ventanas diarias de resultados se solapan; la comparación requiere dependencia y anualización coherentes.

**Tadi–Witzany2025 (RV-E03).** Trabaja con20 contratos con margen USDT, datos2021–2023 y ciclos de tres semanas de formación/una de negociación; estima cointegración y cópulas. Algunas variantes mantienen beneficios después de comisiones taker supuestas. A la vez, la rotación transforma beneficios brutos de varias referencias en pérdidas netas (tabla7). No todos los comparadores fracasan.

El denominado neto no incluye una reconstrucción verificada de funding, slippage, margen o liquidación. Se prueban variantes de test/frecuencia/entradas y se mencionan salidas exploradas no mostradas: no hay holdout intacto del procedimiento completo. Pérdidas/drawdowns superiores al100% en sus tablas exigen reconciliar deuda, capital y parada por insolvencia; no representan automáticamente una cuenta que pudiera seguir operando. Las dos investigaciones son de autorías/periodos distintos, pero no réplicas exactas del mismo método.

**Costes/datos/viabilidad.** Dos patas, borrow o dos funding, ejecución no simultánea, señal observable antes del fill, universo histórico y rupturas contractuales. A frecuencia moderada puede estudiarse con infraestructura accesible si existen instrumentos cortos legales y financiables; esa disponibilidad no se presume. Descartar relaciones seleccionadas con futuro, inestables OOS o cuyo coste acumulado de financiación excede la corrección esperada. No rescatar un par roto añadiendo umbrales después de ver el test.

## 3. Funding rates, basis y cash-and-carry

**Contratos distintos.** Comprar spot q y vender q de un futuro lineal a vencimiento tiene P&L terminal bruto `q(F_0−S_0)` solo si convergen al mismo subyacente, se cumplen obligaciones y se puede mantener la posición. Antes de vencimiento el basis puede ampliarse y generar llamadas de margen.

Un perpetuo no tiene fecha obligatoria de convergencia. Si funding positivo lo paga el largo, una posición firmada n tiene flujo `−n P_k f_k`: un corto recibe cuando f es positivo y paga cuando cambia de signo. Convenciones, multiplicador y colateral deben comprobarse por contrato. No aplicar esta fórmula sin adaptar a contratos inversos/quanto.

Spot largo más perpetuo corto produce, antes de costes/funding, `q[(P_0−S_0)−(P_T−S_T)]`. No bloquea una rentabilidad anual: depende del cambio de basis y de pagos futuros desconocidos. Anualizar una tasa puntual no es rendimiento anual realizado.

**Evidencia completa: Crypto carry (RV-E01).** BIS WP2023 estudia futuros con vencimiento y restricciones de capital. En su tabla5, una combinación con30 observaciones mensuales obtiene Sharpe anualizado0,59 bajo financiación LIBOR, **antes de costes de transacción y diferenciales adicionales de financiación**. No es una tasa neta accesible ni valida perpetuos. La publicación posterior2026 se identificó, pero sus tablas no se leyeron ni se mezclan con el WP.

**Ampliación sobre perpetuos.** He et al., arXiv v1 de 2022 (FUND-01), incluyen funding y fees supuestos, con reestimación mensual de umbrales usando seis meses pasados. Sus tarifas maker requieren volúmenes elevados y no modelan colas; la tabla 7 presenta tarifas distintas de tablas 3/5. Christin et al., WP de agosto de 2023 (FUND-02), estudian 18 activos/36 contratos y muestran deterioro del carry en 2022–2023, pero excluyen comisiones y margen del retorno base. Parte del beneficio es cambio del basis, no ingreso puro de funding. Los dos estudios comparten exchange/periodos; no son réplicas exactas ni validación neta minorista.

**Adverso.** El propio estudio RV-E01 explica margen, liquidaciones y costes de financiación. El beneficio terminal no elimina liquidez intermedia ni riesgo de custodia. Su muestra principal acaba antes de la quiebra FTX; no permite medir ese episodio. El denominador de una cuenta debe incluir spot, garantías, reservas y fondos en cada plataforma; dividir solo por margen inicial infla la interpretación.

**Datos/infraestructura/viabilidad.** Quotes spot/derivado, índice/marca, funding histórico realizado y estimado con timestamps distintos, cambios de reglas, vencimientos, préstamos y liquidaciones. Frecuencia de rebalanceo relativamente baja no elimina supervisión continua de margen. Para un particular puede ser investigable, condicionado a acceso, capital, financiación y concentración en contraparte. FUND-01 y FUND-02 ya aportan lectura de dos estudios de perpetuos con autores distintos y Binance en común; sus resultados no resuelven todos los costes, capital ni OOS.

**Falsadores.** Uso de funding futuro en la señal; beneficio que desaparece con préstamo/comisiones; cobertura liquidada antes de converger; supuesto capital sin reservas; retornos concentrados en plataformas inaccesibles o fallidas.

## 4. Conclusión de lectura

Hay mecanismos económicos claros y resultados favorables bajo supuestos concretos, acompañados de evidencia adversa sobre cortos, rotación, selección y margen. No se ha establecido ventaja neta operable para este proyecto. La prioridad es auditar contabilidad e instrumentos antes de elegir modelos más complejos. Persisten textos completos pendientes de arbitraje entre mercados, réplicas exactas y validación integral de funding perpetuo; no se declara cobertura exhaustiva ni se inicia Fase II.
