# Microestructura, ejecución, Machine Learning y Deep Learning

Fecha de elaboración: **2026-10-13**. Alcance: Fase I, marco conceptual y agenda de revisión. Estado: **documentado, revisión bibliográfica pendiente**. No hay implementación, backtests, optimización ni hipótesis validadas.

## 1. Acceso, procedencia y límites

Se intentó consultar fuentes primarias por HTTPS conservando la verificación TLS. El proxy rechazó las conexiones con `Tunnel connection failed: 403 Forbidden`. No se accedió a texto completo, resúmenes ni metadatos bibliográficos externos. **Fuentes efectivamente consultadas: ninguna.**

Los fundamentos siguientes son explicaciones teóricas, no resultados de una revisión empírica completada. Las referencias ML-* son **semillas NO CONSULTADAS**, con datos bibliográficos que requieren cotejo. No se atribuyen cifras de rentabilidad, resultados positivos/negativos ni robustez fuera de muestra a artículos inaccesibles. No se puede establecer la actualidad o exhaustividad de la literatura a partir de este documento.

| Destino intentado | Resultado el 2026-10-13 | Alcance que falta |
|---|---|---|
| `https://arxiv.org/abs/1808.03668` | CONNECT 403 | Resumen y texto de DeepLOB |
| `https://doi.org/10.1093/jjfinec/nbt003` | CONNECT 403 | Resolver DOI, metadatos y texto de Cont et al. |
| `https://financialinnovation.springeropen.com/articles/10.1186/s40854-020-00217-x` | CONNECT 403 | Artículo sobre ML y criptomonedas |
| `https://www.math.nyu.edu/~avellane/HighFrequencyTrading.pdf` | CONNECT 403 | PDF de teoría de market making |
| `https://academic.oup.com/rfs/article/33/5/2223/5758276` | CONNECT 403 | Artículo de ML y valoración de activos |

Los fallos anteriores son incidencias de acceso, no evidencia científica negativa.

## 2. Preguntas científicas comunes

1. ¿Existe información disponible en el instante de decisión que mejore una referencia sencilla y permita una operación ejecutable después de todos los costes?
2. ¿La variable predice rendimientos futuros, explica rendimientos simultáneos o refleja información que habría llegado después de enviar la orden?
3. ¿Cuál es la vida media de la señal y cuánto sobreviven sus beneficios a latencia, spread, comisión, impacto y selección adversa?
4. ¿Una mejora de error predictivo produce una mejora material de utilidad o riesgo neto, o solamente de una métrica estadística?
5. ¿La señal es transferible entre activos, exchanges y regímenes, o depende de una muestra elegida retrospectivamente?
6. ¿El resultado sigue presente al incluir los intentos fallidos de selección de variables, arquitecturas, semillas y parámetros?
7. ¿Qué parte de la ventaja requiere datos, velocidad o capital que un particular no puede obtener razonablemente?
8. ¿Qué evidencia haría abandonar cada línea, y qué resultado observable permitiría distinguir el fundamento económico de una correlación accidental?

## 3. Microestructura y order flow

### Fundamento matemático y económico

El libro contiene ofertas limitadas de compra y venta; su estado resulta de órdenes nuevas, cancelaciones y ejecuciones. El precio medio es `m_t = (bid_t + ask_t)/2`. Una medida simple de desequilibrio de cantidades en el mejor nivel es:

`I_t = (Q_bid,t − Q_ask,t) / (Q_bid,t + Q_ask,t)`.

Debe declararse cómo se tratan un libro vacío, cantidades cero, niveles de profundidad y unidades. Este desequilibrio de **stock** no equivale al flujo de órdenes: un indicador OFI agrega cambios de oferta y demanda a lo largo de un intervalo, incluyendo cancelaciones y cambios de precio. La relación `Δm_(t,t+h) = β·OFI_t + ε_(t,t+h)` solo es predictiva si el OFI se construye exclusivamente con eventos conocidos al decidir; usar eventos del mismo intervalo futuro la convierte en explicación contemporánea.

Fundamentos investigables: presión transitoria de demanda, reposición de liquidez, inventario de proveedores y transmisión de información entre mercados. No implican necesariamente una prima que permanezca disponible después de ejecutar. La orden que consume liquidez paga el spread; la que la provee cambia ese coste por riesgo de no ejecución y selección adversa.

### Evidencia y contrastes pendientes

ML-01 y ML-03 ofrecen entradas bibliográficas para relacionar eventos del libro y predicción. No se han leído y no acreditan rentabilidad en criptomonedas. Hay que extraer el horizonte exacto, si los precios son de punto medio o ejecutables, si la relación es contemporánea y si la validación separa días, mercados y episodios de volatilidad.

La búsqueda contraria debe incluir replicaciones con latencia, cambios de régimen, transferencias entre exchanges y comparación con desequilibrios sencillos. También deben registrarse estudios donde la predicción persiste pero el PnL desaparece al valorar ejecuciones realizables.

### Datos, costes e infraestructura

- Eventos históricos del libro con secuencias, timestamps del exchange y de recepción cuando existan, snapshots para reconstrucción, operaciones y especificación de ticks/lotes. Las velas OHLCV no permiten validar esta línea.
- Datos L2 agregados pueden permitir señales y simulaciones conservadoras; modelar posición exacta en cola exige información adicional o límites explícitos de identificación. Un histórico L3 tampoco elimina la latencia desconocida de nuestra hipotética orden.
- Comisiones maker/taker según la categoría realmente accesible, spread observado, latencia, impacto dependiente de volumen y profundidad, cancelaciones y degradación durante desconexiones. Los rebates deben incorporarse solo si corresponden al contrato real.
- Archivo de eventos, reconstrucción determinista y control de huecos, mensajes duplicados y reordenados. No descargar ni implementar todavía.

### Viabilidad y condiciones de descarte

Para un particular, priorizar eventualmente horizontes cuya duración sea compatible con adquisición de datos y conexión ordinaria; esto sigue pendiente de evidencia. Descartar una hipótesis si requiere anticiparse a participantes con una latencia inalcanzable, si depende de mensajes ausentes o si su ventaja desaparece al imponer costes y retrasos plausibles. Una asociación de OFI y precio no es por sí misma una justificación para operar.

## 4. Market making

### Fundamento matemático y económico

Un creador de mercado cotiza compra y venta e intenta cobrar compensación por suministrar liquidez. Con caja `X_t`, inventario `q_t` y precio medio `S_t`, el patrimonio marcado es `W_t = X_t + q_t S_t`. Las ejecuciones alteran caja e inventario; una posición que gana spread puede perder mucho más por movimiento del activo.

Una formulación teórica posible elige distancias de cotización para maximizar:

`E[−exp(−γ·(X_T + q_T S_T))]`, con `γ > 0`.

En un modelo estilizado de precio aritmético con volatilidad constante, utilidad exponencial y horizonte finito, un precio de reserva toma la forma `r_t = S_t − q_t γ σ²(T−t)`. Expresa que un inventario largo incentiva cotizar a menor precio. La fórmula ilustra el papel del riesgo; no debe trasladarse automáticamente a saltos cripto, colas reales, tasas de llegada cambiantes ni inventarios ilimitados.

El beneficio neto exige contabilizar spread efectivamente capturado, comisiones o rebates, cobertura, cambios de inventario, selección adversa y liquidación final. La selección adversa puede medirse mediante el desplazamiento posterior del precio condicionado a ejecuciones; al construir un PnL con precios reales, no debe restarse otra vez como coste independiente si ya queda reflejada.

### Evidencia y contrastes pendientes

ML-02 es una semilla de teoría, no una prueba de rentabilidad cripto ni de resultados alcanzables por un operador particular. Revisar supuestos de llegada de órdenes, independencia entre ejecuciones y precio, inventario, liquidez terminal y competencia. Buscar evaluaciones con posiciones en cola, ejecuciones parciales y simulación de eventos; compararlas con cualquier simulación que asuma ejecución por tocar un precio.

La evidencia contraria relevante son pérdidas concentradas en saltos, cancelaciones lentas, ejecuciones tóxicas y beneficios que solo sobreviven con rebates o prioridad no accesibles. **No se ha consultado todavía ningún estudio que documente estos resultados en una configuración comparable.**

### Datos, costes e infraestructura

Se necesitan libro de eventos, colas o un modelo conservador de fills, órdenes parciales, límites del exchange, latencias de envío/cancelación y reglas de post-only. La liquidez en dos mercados exige capital inmovilizado y riesgo de contraparte en ambos. Coberturas con perpetuos añaden funding, márgenes, liquidación y base; cubrir a posteriori no elimina el riesgo entre ejecuciones.

La futura infraestructura requeriría reconciliación de órdenes e inventario y supervisión continua. Esta Fase I solo documenta requisitos; no diseña ni implementa un bot.

### Viabilidad y condiciones de descarte

La prioridad provisional para una primera investigación individual es baja por dificultad de identificar fills y riesgos de ejecución. Reconsiderar si se obtiene acceso fiable a datos y una razón concreta para una oportunidad alcanzable. Descartar simulaciones que equiparen tocar el límite con ejecución segura, ignoren inventario terminal, presupongan cancelación instantánea o atribuyan un rebate no disponible al usuario.

## 5. Machine Learning

### Fundamento matemático y económico

ML es una familia de estimadores, no una fuente económica autónoma de rentabilidad. El objeto típico es `f_θ(x_t) ≈ E[y_(t,t+h) | información disponible en t]`, o una distribución condicional. El objetivo `y` puede ser rendimiento, volatilidad, probabilidad de una cola o coste de ejecución. Cada objetivo requiere una conexión separada con una decisión de inversión.

Una regla de decisión abstracta sería elegir exposición `w_t` maximizando:

`w_t·μ̂_t − C_t(w_t−w_t^−) − λ·Riesgo_t(w_t)`.

Aquí `w_t^−` es la exposición efectiva inmediatamente antes de negociar, que incorpora la deriva de pesos por retornos y los flujos previos; no equivale necesariamente al peso objetivo del periodo anterior. La implementación futura calcularía costes a partir de órdenes ejecutables y patrimonio, con unidades coherentes.

La utilidad económica depende de la calibración, incertidumbre y tamaño de los errores, de la frecuencia con que se cambia exposición y de los costes, no solo de la precisión de clasificación. Acertar muchos movimientos pequeños y equivocarse en pocos movimientos grandes puede perder dinero. Mejorar la predicción de volatilidad puede ser útil para gestionar riesgo sin predecir el signo del rendimiento.

Las hipótesis económicas deben preceder al estimador: persistencia, reversión, premio por riesgo, flujo o información específica. Comparar inicialmente una regla sencilla y una regresión regularizada con una alternativa no lineal cuando la investigación la justifique. Complejidad adicional requiere una mejora neta e incierta debidamente cuantificada.

### Evidencia y contrastes pendientes

ML-05 ofrece una semilla metodológica en valoración de activos; no debe trasladarse como prueba directa de ventaja cripto. ML-06 corresponde por su título a predicción y trading de criptomonedas bajo condiciones cambiantes y es una prioridad de lectura. ML-07 permite rastrear una línea de predicción de Bitcoin; ser artículo de conferencia no equivale automáticamente a validación económica o replicación independiente.

Extraer por estudio: universo conocido en cada fecha, disponibilidad de variables, construcción de etiquetas, separación temporal, búsqueda de modelos/hiperparámetros, referencias simples, estrategia que transforma predicción en orden, costes, resultados netos y datos/código. Buscar expresamente comparaciones donde el modelo simple iguala o mejora al complejo, resultados negativos y reproducciones que desaparecen al corregir fuga de información. **Resultados publicados positivos, negativos y OOS: pendientes de consulta; no se atribuyen conclusiones.**

### Riesgos particulares de fuga y selección

- Ajustar escalado, imputación, selección de variables y reducción de dimensión dentro del entrenamiento de cada partición. Un preprocesamiento no supervisado puede filtrar información futura.
- Respetar la hora de publicación y recepción: revisiones de métricas on-chain, funding liquidado o clasificaciones de activos conocidas después no son variables disponibles antes.
- Purgar etiquetas solapadas cuando el horizonte futuro cruza fronteras de particiones; definir un embargo pertinente a la información utilizada. Un embargo arbitrario no corrige todos los sesgos.
- Un split aleatorio en series temporales o un panel que mezcla el mismo episodio de mercado entre entrenamiento y prueba puede producir validación engañosa.
- Tratar selección de features, semillas, ensembles y decisiones manuales como parte del presupuesto de búsqueda. Los intentos no publicados dentro del proyecto también cuentan.
- No reutilizar el holdout final para calibrar umbrales, elegir activos, retocar costes ni escoger entre modelos.

### Datos, costes y viabilidad

Modelos tabulares sobre datos diarios o horarios pueden ser técnicamente accesibles si existe historial trazable. Datos alternativos requieren su versión histórica disponible en tiempo real, licencias y coste económico. La rotación inducida por predicciones ruidosas puede consumir el margen; no se puede asignar una comisión universal sin elegir instrumento, venue y contrato accesible.

Descartar una línea si no mejora una referencia comparable en términos netos con incertidumbre razonable, si la mejora depende de una variable no disponible a tiempo o si solo aparece tras una búsqueda extensa no registrada. Una mejora de clasificación por sí sola no justifica implementación ni trading.

## 6. Deep Learning y modelos de series temporales

### Fundamento matemático y económico

Redes recurrentes, convoluciones temporales, atención y modelos de estado representan funciones de un historial `x_(t−L+1:t)`. Su capacidad para modelar no linealidades no crea información predictiva inexistente. Hay dependencia temporal, mercados cambiantes y una cantidad efectiva de observaciones menor que el número de filas cuando las ventanas y etiquetas se solapan.

Una pérdida `Σ_t ℓ(y_(t,t+h), f_θ(x_(t−L+1:t))) + λΩ(θ)` define un problema de estimación. Minimizarla no demuestra una ventaja ejecutable. Predecir niveles de precio puede beneficiarse mecánicamente de persistencia; comparar siempre con el último valor conocido y examinar rendimientos y utilidad de la decisión. Modelar muchos activos no garantiza independencia si comparten el mismo factor de mercado.

Un modelo preentrenado introduce preguntas adicionales: fecha de corte, composición del corpus, contaminación del periodo de evaluación, normalización y revisiones de datasets. Sin información suficiente, no se puede calificar como fuera de muestra una prueba sobre fechas posiblemente incluidas en el entrenamiento.

### Evidencia y contrastes pendientes

ML-03 sirve de semilla sobre libros y redes profundas; ML-04 sobre LSTM y mercados financieros. Ninguna debe presentarse como evidencia cripto automáticamente. ML-08 propone una entrada bibliográfica para comparar arquitecturas complejas con referencias temporales sencillas; falta consultar texto y ámbito, y no se presupone cuál gana.

La ficha de extracción debe registrar longitud de ventana, resolución, horizonte, universo, pérdidas, arquitectura, semillas, stopping, búsqueda de hiperparámetros, splits, preprocessing y elección de referencias. Identificar si se reportan errores predictivos, PnL bruto o PnL neto con ejecuciones factibles. Revisar estabilidad entre semillas y periodos y si ablations permiten identificar qué aporta la arquitectura.

**Evidencia favorable, contraria y fuera de muestra en configuraciones cripto comparables: pendiente.** El objetivo de esta revisión es encontrarla y valorar su calidad, no presentar una arquitectura como ganadora.

### Datos, costes y viabilidad

Redes pequeñas con datos de baja frecuencia pueden entrenarse en infraestructura modesta, pero tamaño, necesidad de GPU y coste total no se fijarán antes de justificar los datos y el problema. Series de eventos y libros profundos multiplican almacenamiento, reconstrucción y coste de investigación. También importa el retraso de inferencia si el horizonte es breve.

Descartar o posponer si una referencia simple es suficiente, no se puede auditar el corpus de preentrenamiento, la incertidumbre entre semillas supera la mejora, o la ventaja depende de una elección retrospectiva entre muchas arquitecturas. El coste de cómputo y mantenimiento debe compararse con la mejora económica plausible para el capital real del usuario, todavía no especificado.

## 7. Comparación conceptual provisional

Esta tabla ordena **diligencias de investigación**, no estrategias ganadoras ni probabilidades de éxito. La selección de candidatas corresponde a una Fase II aún no autorizada.

| Línea | Fundamento que merece investigar | Principal obstáculo | Prioridad de lectura inicial |
|---|---|---|---|
| ML tabular de baja frecuencia | Relación no lineal o combinación de señales con explicación previa | Fuga, selección, rotación y débil señal | Alta como comparación metodológica con reglas simples |
| Predicción de riesgo con modelos sencillos y ML | Tamaño de posición adaptado a volatilidad/colas | Error de riesgo en cambios bruscos; confundir gestión de riesgo con alpha | Alta como apoyo conceptual, sin seleccionar modelo |
| Order flow | Demanda/oferta y transmisión de información | Datos de eventos, horizonte/latencia y costes | Media, para determinar si existe un horizonte accesible |
| Deep Learning | Representaciones temporales de datos complejos | Comparación justa y presupuesto de búsqueda; datos efectivos | Condicionada a evidencia de que referencias simples resultan insuficientes |
| Market making | Compensación por provisión de liquidez e inventario | Fills, selección adversa, latencia y colas extremas | Baja para la primera futura implementación individual; sí revisar teoría y fracasos |

## 8. Referencias semilla y preguntas de extracción

**Todas las referencias siguientes están NO CONSULTADAS.** Autoría, título, edición, DOI, estado editorial y ámbito se anotan como pista bibliográfica y deben cotejarse antes de citarlas como fuentes verificadas. La fecha indicada en la sección 1 es la fecha del intento de acceso, no una fecha de lectura del artículo. Un DOI o URL plausible no constituye verificación.

| ID | Referencia semilla, pendiente de cotejo | Enlace | Tipo bibliográfico propuesto; qué verificar |
|---|---|---|---|
| ML-01 | Cont, R.; Kukanov, A.; Stoikov, S. (2014). *The Price Impact of Order Book Events*. Journal of Financial Econometrics. | [DOI](https://doi.org/10.1093/jjfinec/nbt003) | Artículo académico; relación contemporánea frente a predicción, profundidad, mercados y validez económica |
| ML-02 | Avellaneda, M.; Stoikov, S. (2008). *High-frequency trading in a limit order book*. Quantitative Finance. | [DOI](https://doi.org/10.1080/14697680701381228) · [PDF autor](https://www.math.nyu.edu/~avellane/HighFrequencyTrading.pdf) | Modelo teórico; supuestos, qué parte es simulación y qué parte observación real |
| ML-03 | Zhang, Z.; Zohren, S.; Roberts, S. (2019). *DeepLOB: Deep Convolutional Neural Networks for Limit Order Books*. IEEE Transactions on Signal Processing. | [arXiv](https://arxiv.org/abs/1808.03668) · [DOI](https://doi.org/10.1109/TSP.2019.2907260) | Artículo y versión preprint del mismo trabajo; datos, splits, baselines, transferibilidad y PnL negociable |
| ML-04 | Fischer, T.; Krauss, C. (2018). *Deep learning with long short-term memory networks for financial market predictions*. European Journal of Operational Research. | [DOI](https://doi.org/10.1016/j.ejor.2017.11.054) | Artículo académico; universo histórico, entrenamiento temporal, costes, supervivencia y extrapolación a cripto |
| ML-05 | Gu, S.; Kelly, B.; Xiu, D. (2020). *Empirical Asset Pricing via Machine Learning*. Review of Financial Studies. | [DOI](https://doi.org/10.1093/rfs/hhaa009) | Artículo académico; aplicación económica, selección, referencias y diferencias entre clases de activos |
| ML-06 | Sebastião, H.; Godinho, P. (2021). *Forecasting and trading cryptocurrencies with machine learning under changing market conditions*. Financial Innovation. | [DOI](https://doi.org/10.1186/s40854-020-00217-x) | Artículo sobre criptomonedas; instrumentos, periodos, OOS, costes y evidencia contraria dentro del estudio |
| ML-07 | McNally, S.; Roche, J.; Caton, S. (2018). *Predicting the Price of Bitcoin Using Machine Learning*. Proceedings of the Euromicro International Conference on Parallel, Distributed and Network-based Processing. | [DOI](https://doi.org/10.1109/PDP2018.2018.00060) | Actas de conferencia; separar predicción, calidad del split y estrategia económicamente ejecutable |
| ML-08 | Zeng, A.; Chen, M.; Zhang, L.; Xu, Q. (2023). *Are Transformers Effective for Time Series Forecasting?* Proceedings of the AAAI Conference on Artificial Intelligence. | [arXiv](https://arxiv.org/abs/2205.13504) | Trabajo metodológico; referencias simples, configuración experimental y límites de extrapolación a finanzas |

No se cuentan preprint, artículo y copia del autor como tres evidencias independientes. Las afirmaciones comerciales no aportan evidencia en esta entrega y, si se añaden posteriormente, tendrán una categoría separada y necesidad de verificación externa.

## 9. Próximas diligencias dentro de Fase I

1. Recuperar acceso autorizado a editoriales, DOI y repositorios académicos; consultar los textos y resolver duplicados/versiones antes de extraer conclusiones.
2. Ejecutar búsquedas trazables por familia, registrando consulta, fecha, fuente, inclusiones y exclusiones. Ejemplos: `cryptocurrency order flow prediction transaction costs out of sample`, `crypto market making adverse selection queue latency`, `cryptocurrency machine learning replication leakage`, `deep learning financial forecasting simple baselines transaction costs negative results`.
3. Buscar citas posteriores, replicaciones y resultados contrarios de cada semilla; no limitarse a los artículos que motivaron la hipótesis.
4. Registrar por afirmación si está sustentada por texto completo, resumen o metadatos. No convertir disponibilidad del código en garantía de reproducibilidad ni revisión por pares en garantía de identificación correcta.
5. Comparar los resultados que realmente midan objetos equivalentes. No combinar Sharpe de periodos, frecuencias, apalancamientos y costes distintos como si fueran ensayos homogéneos.
6. Identificar lagunas antes de decidir qué investigar en una fase posterior: no hay por ahora base verificable para declarar alpha, ordenar rentabilidades esperadas ni aprobar operativa.

La autorización actual termina en investigación y documentación. El cambio a selección formal de candidatas, adquisición experimental de datos, implementación o backtesting requiere la revisión y aprobación del usuario.
