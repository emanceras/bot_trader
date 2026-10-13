# Fase I: valor relativo, cointegración, volatilidad y funding

Fecha de esta revisión inicial: **2026-10-13**. Estado: **documentado; revisión bibliográfica empírica pendiente**. No se han programado estrategias ni ejecutado experimentos.

## Alcance, acceso y qué puede concluirse

Este informe deriva fundamentos matemáticos y plantea preguntas contrastables para cuatro familias. No contiene resultados propios ni considera demostrada una ventaja por la plausibilidad del mecanismo económico.

**Fuentes externas efectivamente leídas en esta sesión: ninguna.** Los accesos a BIS, Oxford Academic, NBER y al resolvedor DOI fallaron con `Tunnel connection failed: 403 Forbidden`. Se registran debajo los destinos relevantes. Esto establece una restricción de acceso en este entorno; no establece que los documentos no existan ni que el editor haya rechazado el acceso. No se ha desactivado TLS ni utilizado rutas para eludir el bloqueo.

Las referencias RV son **semillas bibliográficas NO CONSULTADAS**: sus datos identificativos y enlaces deben verificarse al recuperar el texto o los metadatos. No se atribuyen cifras, resultados positivos o negativos, validaciones fuera de muestra ni conclusiones a documentos inaccesibles. La cobertura no es una revisión actualizada o exhaustiva hasta octubre de 2026.

Convenciones: precios positivos; rendimientos en una moneda de cuenta explícita; `q > 0` denota cantidad comprada de spot; un derivado corto tiene cantidad firmada negativa. Las fórmulas simplificadas no sustituyen las especificaciones contractuales del mercado investigado. «Neutral en delta» no significa ausencia de pérdidas ni ausencia de necesidades de financiación.

## Preguntas científicas comunes

1. ¿Qué flujo de caja o restricción económica podría sostener la oportunidad y quién paga por ella?
2. ¿La señal era observable y ejecutable en el instante de decisión? ¿Se utilizó por error un precio de cierre, un funding realizado o una revisión posterior?
3. ¿La rentabilidad remunera riesgo de mercado, liquidez, crédito, custodia, stablecoin, margen o colas, en vez de un error de valoración?
4. ¿La ventaja permanece después del coste completo de ambas piernas y de todo el capital comprometido?
5. ¿Existe evidencia fuera de muestra con fechas de selección, estimación y ejecución separadas? ¿La selección de pares y mercados también fue realizada fuera de muestra?
6. ¿Cuántas alternativas, ventanas, mercados y reglas se probaron? ¿Qué resultados negativos o abandonados quedaron sin publicar?
7. ¿Qué ocurre cuando deja de existir una pierna, se detienen retiradas, falla una API o divergen precios de ejecución y precios de liquidación?
8. ¿Puede un particular reproducir el acceso a datos, préstamos, derivados, comisiones y tiempos de ejecución del estudio?

Estas preguntas orientan una futura extracción bibliográfica; no son criterios numéricos de aceptación para experimentos ya aprobados.

## 1. Statistical arbitrage

### Fundamento matemático y económico

El término abarca estrategias con expectativa estadística favorable condicionada a un modelo, no necesariamente un arbitraje sin riesgo. Conviene separar dos mecanismos:

- **Mismo activo entre centros de negociación:** diferencias entre precios ejecutables. Comprar al `ask` de A y vender al `bid` de B produciría un margen bruto instantáneo `q(bid_B − ask_A)`. El margen neto debe restar comisiones, financiación, préstamo y recomposición posterior de inventario. La cuenta no incorpora por sí sola el riesgo de ejecución parcial o insolvencia. Preposicionar inventario evita esperar una transferencia para cada operación, pero inmoviliza capital y no elimina el riesgo de custodia.
- **Valor relativo de activos diferentes:** construir residuos de un modelo, por ejemplo `r_i,t = a_i + β_i' f_t + ε_i,t`, y posiciones que reduzcan exposición a factores. Una cartera con `β' w ≈ 0` puede seguir expuesta a factores omitidos, relaciones no lineales y cambios de beta. Una estructura factorial de rendimientos no implica que el residuo acumulado sea una oportunidad de reversión.

La fragmentación de mercados y las restricciones de capital constituyen mecanismos plausibles que investigar. Una diferencia entre un mercado con retiradas habilitadas y otro con retiradas suspendidas puede expresar riesgo de crédito o de convertibilidad, no un precio realizable del mismo activo económico.

### Evidencia a buscar y límites actuales

RV-01 es una semilla directamente centrada en mercados de criptomonedas. RV-02 aborda statistical arbitrage en acciones; RV-03 aporta teoría sobre restricciones al arbitraje. Ninguna ha sido consultada aquí: **resultados positivos, negativos y evidencia fuera de muestra, pendientes de verificación**. La literatura de acciones solo podrá apoyar el método o un mecanismo; no demostrará transferibilidad a criptomonedas.

La extracción deberá comprobar si los diferenciales se calculan sobre transacciones, cotizaciones ejecutables o precios indicativos; si las retiradas, conversiones fiat y transferencias eran factibles; y si los beneficios presuponen inventario o apalancamiento ilimitado. Se buscarán activamente estudios que reduzcan o eliminen el resultado al incorporar sincronización y restricciones de financiación.

### Datos, costes y viabilidad

Para divergencias entre exchanges: cotizaciones bid/ask y profundidad sincronizadas, timestamp del mercado y de recepción, especificación de tokens y redes, disponibilidad histórica de depósitos/retiradas, límites y costes de transferencias, comisiones por nivel realista de cuenta y saldos inmovilizados. Velas diarias no permiten demostrar una oportunidad intradía entre mercados.

Para residuos factoriales de frecuencia baja: universo históricamente disponible, retornos ajustados a redenominaciones/migraciones, disponibilidad de cortos y fechas efectivas de composición. El coste incluye todas las piernas, rebalanceos, préstamo o funding, spread, slippage e impacto condicionado por tamaño. El retorno se calcula sobre el capital total comprometido, incluidas garantías y saldos prefondados.

La investigación con barras y modelos simples puede ser viable para un particular; demostrar ejecución rentable entre centros de negociación exige datos e infraestructura considerablemente superiores. No se presume que capital reducido elimine fricciones fijas.

**Motivos para descartar una línea:** margen explicable por costes realizables; falta de préstamo; conversiones imposibles; desfases de timestamp; exposición dominante a un exchange insolvente; resultado concentrado en incidentes de retiradas; o dependencia de niveles institucionales de comisiones no accesibles.

## 2. Pairs trading y cointegración

### Fundamento matemático y económico

Sean `x_t = log P_A,t` e `y_t = log P_B,t`. Si ambas series son integradas de orden uno y existe `β` tal que `z_t = x_t − a − βy_t` es estacionario, existe cointegración bajo esa especificación. La correlación entre rendimientos no implica cointegración entre niveles. Las pruebas con residuos estimados requieren valores críticos adecuados; aplicar sin más una prueba de raíz unitaria estándar a los residuos puede producir inferencias inválidas.

Una aproximación de reversión es `dz_t = κ(μ − z_t)dt + σdW_t`, con `κ > 0`. La vida media teórica `log(2)/κ` depende de que ese modelo sea pertinente y estable; estimarla no demuestra que una posición pueda cerrarse con beneficio antes de una ruptura. Un `κ` estimado casi nulo o una distribución incompatible con el modelo puede volver irrelevante la vida media.

Cuando `z_t` es alto, la dirección teórica es corto A y largo B si `β > 0`; cuando es bajo, se invierte. Para rendimientos pequeños, exposiciones monetarias proporcionales a `(+1, −β)` aproximan una posición larga en el diferencial, pero requieren rebalanceo. Una combinación de logaritmos no es por sí sola el P&L de cantidades fijas de tokens. Si se utiliza cointegración en precios, las unidades del coeficiente de cobertura cambian; debe derivarse la cartera ejecutable de esa especificación.

El fundamento económico importa: utilidad compartida, vínculo contractual o convertibilidad podrían sostener una relación; una categoría comercial común o una correlación histórica alta son fundamentos más débiles. Incluso una relación contractual puede quebrarse por fallo del custodio, protocolo o garantía.

### Evidencia a buscar y límites actuales

RV-04 es la referencia metodológica sobre cointegración y RV-05 una semilla clásica de pairs trading en acciones. RV-06 es una revisión amplia de trading de criptomonedas que puede proporcionar cadenas de citas. **No hay todavía un estudio empírico de cointegración cripto consultado que permita afirmar eficacia positiva o negativa.** La contribución teórica de RV-04 no es evidencia de una estrategia negociable; RV-05 tampoco puede trasladarse sin replicación a este mercado.

La búsqueda debe cubrir «cryptocurrency pairs trading cointegration transaction costs out of sample» y sus variantes con structural breaks, delisting, short selling, negative results y replication. Para cada estudio se separarán descubrimiento del par, estimación de beta, fijación de umbrales y evaluación posterior. Se registrará si publica también pares y periodos fallidos.

### Sesgos, costes y datos

Seleccionar los mejores pares de un universo de `N` activos examina hasta `N(N−1)/2` relaciones antes de contar ventanas y reglas: una sola prueba significativa no corrige esa selección. Se requiere evaluación cronológica de la selección completa y un registro de todas las variantes; ni una prueba de cointegración ni una corrección aislada de p-valores resuelven por sí solas el problema económico.

Los datos deben incluir activos desaparecidos, rupturas contractuales, cambios de ticker, fechas de listado y cortos realmente disponibles. Una pareja solo negociable en spot no permite ejecutar sin restricciones ambas direcciones de una estrategia larga/corta. El coste de dos piernas puede absorber diferenciales pequeños; si cada pierna es un perpetuo hay dos series de funding, además del riesgo de desalineación de ejecuciones.

Para un particular, estudiar pares líquidos a frecuencia horaria o diaria podría ser técnicamente viable si existen datos adecuados y acceso legal a instrumentos cortos. Eso no establece conveniencia ni rentabilidad.

**Motivos para descartar:** relación seleccionada con datos futuros; cointegración inestable en periodos consecutivos; rentabilidad dependiente de una sola ruptura recuperada retrospectivamente; imposibilidad de una pierna; coste de financiación acumulado durante la convergencia superior al beneficio esperado; o beneficio que desaparece con spread y retraso plausibles. Estos motivos serán hipótesis de falsación; aún no se han contrastado.

## 3. Estrategias de volatilidad

### Separar tres preguntas distintas

1. **Predecir volatilidad:** estimar una distribución o una varianza condicional. Una mejora en una pérdida de predicción no prueba rentabilidad.
2. **Controlar riesgo:** dimensionar una cartera, por ejemplo `w_t = min(w_max, σ_objetivo / σ̂_t)`. El pronóstico solo utiliza datos disponibles al decidir. El escalado puede alterar riesgo, exposición, costes y retornos, pero no crea automáticamente una prima económica.
3. **Negociar volatilidad:** comprar o vender instrumentos cuyo resultado depende de volatilidad implícita, realizada, saltos y cobertura. Son necesarias cotizaciones históricas de derivados y modelos de ejecución, no solo una serie spot.

En una aproximación continua y local, el componente de P&L de una opción comprada y cubierta en delta puede escribirse como `½ Γ_t S_t²(σ_real,t² − σ_impl,t²)dt`, bajo las hipótesis del modelo de valoración y sin fricciones. Esto orienta el signo: pagar volatilidad implícita superior a la realizada puede perjudicar al comprador. **No es una identidad general de ganancias**: cobertura discreta, cambios de volatilidad implícita, sonrisa, saltos, tipos y costes alteran el resultado. La venta de opciones invierte exposiciones y puede concentrar pérdidas extremas; una sucesión de pequeñas ganancias no demuestra robustez.

### Evidencia a buscar y límites actuales

RV-07 es una semilla sobre carteras gestionadas por volatilidad, y RV-08 y RV-09 sobre valoración de opciones y prima de riesgo de volatilidad en mercados tradicionales. No se han consultado. No existe en esta revisión inicial evidencia verificada de una prima de volatilidad cripto accesible a un particular. Un marco de valoración tampoco demuestra que el precio de mercado permita una ventaja.

Se necesitan trabajos directamente sobre opciones cripto y futuros que distingan predicción, valoración y retorno de una estrategia ejecutable. Se buscará evidencia contraria sobre estabilidad de primas, selección de vencimientos, contratos ilíquidos, interpolación de cotizaciones, costes de cobertura y sensibilidad a saltos. La existencia o signo de una prima no se presumirá a partir de acciones.

### Datos, costes y viabilidad

Control de riesgo: series de retorno completas, estimación causal de volatilidad y costes por cambiar exposición. Negociación de opciones: bid/ask, volumen y profundidad por vencimiento y strike; superficie observable en cada instante; convenciones de liquidación, multiplicador, margen, moneda de garantía, tipos y comisiones; precios del subyacente para simular coberturas. La moneda de margen puede introducir otra exposición incluso en una posición cubierta en delta.

Se evaluarán pérdidas por saltos sin posibilidad de rebalanceo, cambios de margen, liquidación, errores de interpolación y precios medios que no podían ejecutarse. Comparar una estrategia cubierta frecuentemente con otra que usa únicamente velas diarias requiere resolver primero la diferencia de información y ejecución.

El control de volatilidad a baja frecuencia es una línea de investigación accesible y útil como capa de riesgo. Opciones y venta de convexidad requieren otra calidad de datos, más capital de reserva y gestión especializada; no son un punto de partida justificable por la sola promesa de rendimientos suavizados.

**Motivos para descartar:** retorno favorable solo usando precios medios ilíquidos; pérdida de ventaja al incorporar cobertura; rentabilidad dependiente de exposición de cola no aceptada; capital o acceso a instrumentos insuficiente; o predicción superior sin traducción a resultados netos.

## 4. Funding rates, basis y cash-and-carry

### Futuros con vencimiento y perpetuos son problemas distintos

Para spot `S` y un futuro lineal con vencimiento `T`, comprar `q` unidades spot y vender `q` unidades del futuro a `F_0` proporciona, si la liquidación converge al mismo subyacente y todo se cumple, un P&L bruto terminal `q(F_0 − S_0)`. Faltan financiación, negociación, garantías, impuestos aplicables y cualquier coste de mantener o liquidar las posiciones. Antes del vencimiento el basis puede ampliarse, generando llamadas de margen aunque el razonamiento terminal sea correcto. No existe garantía de poder mantener la operación hasta el vencimiento.

Un perpetuo no tiene esa fecha obligatoria de convergencia. Definamos una posición firmada `n` en un contrato lineal cuyo valor por unidad sea `P_k`. Con la convención contractual «funding positivo lo paga el largo al corto», el flujo aproximado en un pago es `−n P_k f_k`. Un corto (`n < 0`) recibe funding positivo; un largo (`n > 0`) lo paga. Deben verificarse signo, periodicidad, multiplicador, referencia del nocional y moneda de liquidación de cada contrato: esta fórmula no se aplica sin adaptación a inversos ni a contratos quanto.

Comprar spot y vender el perpetuo da antes de costes y pagos de funding:

`q[(S_T − S_0) + (P_0 − P_T)] = q[(P_0 − S_0) − (P_T − S_T)]`.

Por tanto, cobra por una reducción del basis y puede perder si se amplía. A ello se suman los pagos firmados de funding: una secuencia futura negativa perjudica al corto. Mantener el perpetuo indefinidamente no fija una tasa de carry conocida. Anualizar el funding de una observación no equivale a una rentabilidad anual realizada o asegurada.

### Fundamento económico y riesgos

La demanda asimétrica de exposición apalancada y las restricciones de financiación son mecanismos plausibles a investigar. Las primas pueden compensar costes de balance y riesgos de crédito o liquidez. Una operación con exposición direccional pequeña sigue afrontando:

- Divergencia de mark price, índice, último precio y precio ejecutable.
- Liquidación de una pierna y pérdida de cobertura, límites de posición, cambios de margen y desapalancamiento automático cuando sea aplicable.
- Insolvencia o bloqueo de retiradas; mantener las piernas en distintas entidades añade transferencias y exposición a ambas.
- Riesgo de stablecoin o de la moneda de garantía, y préstamo spot si se invierte la dirección.
- Cambios de signo o metodología del funding, condiciones contractuales, intervalos, topes y disponibilidad de instrumentos.

El denominador del retorno debe incluir spot, garantía, reservas y cualquier saldo prefondado. Dividir únicamente por margen inicial puede inflar la rentabilidad y ocultar la necesidad de liquidez. Ni el volumen del mercado ni una posición inicialmente cubierta eliminan estos riesgos.

### Evidencia a buscar y límites actuales

RV-01 y RV-03 proporcionan puntos de entrada sobre restricciones al arbitraje, pendientes de consulta. Se intentó acceder a `https://www.bis.org/publ/work1087.htm` y a su PDF como posible documento candidato; ambos accesos fueron bloqueados. **No se le asigna título, autores ni resultados sin verificar su identidad.** La página general de publicaciones BIS también resultó inaccesible. Se buscará allí investigación sobre crypto carry y restricciones de balance cuando el acceso esté disponible.

Se distinguirán estudios de basis a vencimiento, funding de perpetuos y divergencias entre exchanges. Para cada uno habrá que verificar si usa funding conocido al decidir o el realizado después; si respeta el mecanismo real de pago; si descuenta préstamos; y si reconstruye margin calls, activos y garantías disponibles históricamente. Buscar también resultados bajo crisis de liquidez y fallos de intermediarios, sin seleccionar únicamente mercados supervivientes.

### Datos, costes y viabilidad

Datos requeridos: spot y derivado sincronizados; cotizaciones ejecutables; historial de funding realizado y, si se usa como señal, previsiones publicadas con su timestamp; metodología histórica; índice y mark price; especificaciones, margen, liquidación y límites; préstamo y garantías; suspensiones y vencimientos. El funding realizado puede servir para contabilizar un flujo pasado, pero no como predictor conocido de antemano.

La frecuencia de rebalanceo puede ser baja respecto de arbitraje de libro; la supervisión de margen y conectividad debe ser continua. Para un particular podría ser investigable en mercados líquidos con acceso permitido y costes reales verificables. La rentabilidad por capital total y el riesgo de plataforma pueden hacerla poco atractiva aunque la tasa bruta parezca elevada.

**Motivos para descartar:** ventaja neta inferior a costes y financiación; uso de funding futuro en la señal; dependencia de apalancamiento incompatible con el estrés de margen; concentración extrema en contraparte; falta de préstamo o historial de especificaciones; o beneficio concentrado en periodos cuya infraestructura real no podía reproducirse.

## Comparación preliminar para organizar la lectura

Esta tabla establece necesidades y preguntas de la **Fase I**; no selecciona candidatos de Fase II ni asigna probabilidades de éxito.

| Línea | Mecanismo a contrastar | Datos mínimos diferenciadores | Obstáculo principal | Uso razonable de la próxima revisión |
|---|---|---|---|---|
| Statistical arbitrage entre mercados | Fragmentación y restricciones de capital | Bid/ask sincronizado, transferibilidad e inventarios | Ejecución y capital inmovilizado; riesgo de custodia | Examinar si los diferenciales son realizables |
| Residuos factoriales | Desajustes relativos tras exposiciones comunes | Universo histórico y cortos disponibles | Modelo omitido e inestabilidad de factores | Buscar replicaciones y costes completos |
| Pairs/cointegración | Relación económica y reversión estable | Historia sin sesgo de supervivencia y dos piernas | Selección entre muchos pares y rupturas | Evaluar estudios que repiten fuera de muestra también la selección |
| Control de volatilidad | Adecuar riesgo a condiciones cambiantes | Retornos y costes de rebalanceo | Confundir menor riesgo con alfa | Separar evidencia de gestión de riesgo y evidencia de rentabilidad |
| Negociación de opciones/volatilidad | Precio del riesgo de varianza y saltos | Superficies históricas bid/ask y cobertura | Colas, iliquidez y margen | Determinar si existen datos y evidencia reproducible accesibles |
| Funding/basis | Demanda apalancada y límites de financiación | Spot/derivado, funding causal, contratos y margen | Riesgo de contraparte y pérdidas intermedias | Auditar signos, capital completo y estrés de financiación |

Funding/basis y cointegración merecen lectura por ofrecer hipótesis económicas y contables concretas que se pueden intentar refutar. Control de volatilidad merece lectura como herramienta de riesgo. Arbitraje entre centros y opciones presentan una carga de datos e infraestructura mayor. **Esta valoración se basa en estructura del problema, no en evidencia empírica que haya sido verificada aquí.**

## Protocolo de extracción bibliográfica pendiente

Por cada estudio se registrarán título, autores, DOI/URL, versión, fecha y nivel de acceso, relación con otras versiones, estado de revisión por pares, mercado, exchange, universo y periodo; disponibilidad de datos y código; mecanismo económico; qué información estaba disponible al decidir; selección y número de variantes; procedimiento fuera de muestra; gastos incluidos y omitidos; capital del denominador; resultados positivos y negativos; incertidumbre y colas; limitaciones declaradas y detectadas; y replicaciones independientes.

Se buscarán resultados adversos con las mismas consultas y filtros que los favorables. Las citas de una revisión se usarán para localizar originales, sin contarlas como confirmaciones independientes. Las versiones de un mismo trabajo no se contarán varias veces. Un resultado no ajustado por costes puede informar sobre una regularidad estadística, pero no validar operabilidad. La extrapolación de acciones a cripto se marcará explícitamente como indirecta.

Secuencia propuesta de lectura: estudios directos de mercados cripto y costes; métodos fundacionales para revisar identificabilidad; evidencia contradictoria y replicaciones; documentación oficial de contratos y fuentes de datos; actualización de conclusiones con fechas y acceso comprobados. Los mínimos de datos y costes de este informe guían el trabajo; los umbrales cuantitativos de futuros experimentos se definirán antes de ejecutarlos y tras la aprobación correspondiente.

## Registro de referencias semilla

**Estado común:** NO CONSULTADA. Los títulos/autores/identificadores de esta lista son referencias candidatas conocidas, pendientes de verificación documental en este entorno. No se han extraído resultados ni se asegura la disponibilidad del texto. «Intentado» indica un intento fallido el 2026-10-13; no implica lectura de metadatos.

| ID | Referencia candidata y tipo | URL | Registro 2026-10-13 | Utilidad y límite |
|---|---|---|---|---|
| RV-01 | Igor Makarov y Antoinette Schoar, *Trading and arbitrage in cryptocurrency markets* (2020), Journal of Financial Economics | https://doi.org/10.1016/j.jfineco.2019.07.001 | NO CONSULTADA; intento DOI bloqueado 403 | Fuente empírica directamente relacionada; resultados y diseño pendientes |
| RV-02 | Marco Avellaneda y Jeong-Hyun Lee, *Statistical Arbitrage in the U.S. Equities Market* (2010), Quantitative Finance | https://doi.org/10.1080/14697680903124632 | NO CONSULTADA; intento DOI bloqueado 403 | Método y evidencia de acciones; transferencia a cripto pendiente |
| RV-03 | Andrei Shleifer y Robert W. Vishny, *The Limits of Arbitrage* (1997), The Journal of Finance | https://doi.org/10.1111/j.1540-6261.1997.tb03807.x | NO CONSULTADA; acceso no intentado individualmente | Marco teórico; no prueba rentabilidad cripto |
| RV-04 | Robert F. Engle y Clive W. J. Granger, *Co-Integration and Error Correction: Representation, Estimation, and Testing* (1987), Econometrica | https://doi.org/10.2307/1913236 | NO CONSULTADA; acceso no intentado individualmente | Fundamento econométrico; no evidencia de beneficio negociable |
| RV-05 | Evan Gatev, William N. Goetzmann y K. Geert Rouwenhorst, *Pairs Trading: Performance of a Relative-Value Arbitrage Rule* (2006), The Review of Financial Studies | https://doi.org/10.1093/rfs/hhj020 | NO CONSULTADA; intento DOI y página editorial bloqueados 403 | Antecedente en acciones; controles y resultados pendientes |
| RV-06 | Fan Fang, Carmine Ventre, Michail Basios, Leslie Kanthan, David Martinez-Rego, Fan Wu y Lingbo Li, *Cryptocurrency trading: a comprehensive survey* (2022), Financial Innovation | https://doi.org/10.1186/s40854-021-00321-6 | NO CONSULTADA; intento DOI bloqueado 403 | Fuente secundaria para descubrimiento; no confirmación independiente |
| RV-07 | Alan Moreira y Tyler Muir, *Volatility-Managed Portfolios* (2017), The Journal of Finance | https://doi.org/10.1111/jofi.12513 | NO CONSULTADA; intento DOI bloqueado 403 | Gestión de riesgo/carteras en otros mercados; extrapolación pendiente |
| RV-08 | Fischer Black y Myron Scholes, *The Pricing of Options and Corporate Liabilities* (1973), Journal of Political Economy | https://doi.org/10.1086/260062 | NO CONSULTADA; acceso no intentado individualmente | Valoración teórica bajo supuestos; no prueba de prima de volatilidad cripto |
| RV-09 | Gurdip Bakshi y Nikunj Kapadia, *Delta-Hedged Gains and the Negative Market Volatility Risk Premium* (2003), The Review of Financial Studies | https://doi.org/10.1093/rfs/16.2.527 | NO CONSULTADA; acceso no intentado individualmente | Semilla sobre prima y cobertura; título no equivale a resultado verificado aquí |

Otros accesos intentados, todos el 2026-10-13: https://www.bis.org/publ/work1087.htm, https://www.bis.org/publ/work1087.pdf y https://www.bis.org/publ/ devolvieron bloqueo de túnel 403. La página editorial intentada para RV-05 fue https://academic.oup.com/rfs/article-abstract/19/3/797/1646694, con el mismo resultado. El resolvedor DOI bloqueado impidió obtener incluso los metadatos de las referencias intentadas. Se requiere restablecer acceso permitido y verificar fuentes antes de transformar esta agenda en conclusiones bibliográficas.

## Conclusión de esta entrega

Hay fundamentos suficientemente concretos para investigar algunas de estas líneas, pero **no hay evidencia consultada suficiente para priorizar su rentabilidad, validar una ventaja o recomendar operativa**. Siguen pendientes fuentes cripto directas sobre pares, opciones y carry, resultados contradictorios, replicaciones y auditorías de costes. Esta entrega documenta preguntas, matemática, fricciones y bibliografía de partida; no satisface por sí sola la revisión exhaustiva de la Fase I.
