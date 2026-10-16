# Machine Learning y Deep Learning: revisión crítica

Síntesis actualizada 2026-10-15. Fase I: cinco textos completos examinados —tres estudios cripto y dos contrastes metodológicos— y dos candidatos recientes con acceso limitado. Ningún modelo entrenado ni backtest propio. Identidades, versiones, páginas y límites en [evidence-ml.md](evidence-ml.md); búsquedas en [search-ml.jsonl](search-ml.jsonl). Microestructura y market making se tratan en [execution.md](execution.md).

## 1. ML: estimador y decisión económica

ML estima, por ejemplo, `fθ(x_t)≈E[r_{t+1}|I_t]`, una probabilidad o una distribución de riesgo. El mecanismo económico debe preceder al algoritmo: persistencia, reversión, liquidez o información. Una regla conceptual de cartera maximiza `w_t μ̂_t−C_t(w_t−w_t^−)−λ Riesgo_t(w_t)`, donde `w_t^−` es exposición efectiva antes de operar, incluida la deriva por retornos. La implementación exigiría unidades, órdenes y fills coherentes.

Una mayor precisión de signo puede coexistir con pérdidas si los errores grandes dominan o las señales inducen mucha rotación. Predicción de volatilidad puede mejorar control de riesgo sin anticipar dirección.

### Evidencia favorable y adversa

Sebastião–Godinho (ML-06, Financial Innovation2021) compara modelos lineales, RF y SVM, con 18 conjuntos de variables y ensembles long/flat para BTC/ETH/LTC. Mantiene entrenamiento móvil de648 días, validación de324 y test de325 días, del13-04-2018 al03-03-2019. La selección y el aprendizaje secuencial son más informativos que una división aleatoria.

Tabla7 p.25 ofrece beneficios en algunas combinaciones después de un coste proporcional supuesto del0,5% por roundtrip: ETH Ensemble5 pasa de44,65% anual bruto a9,622%; ETH Ensemble6 da14,35% con ese coste. No hay ganador universal. En p.26, **cinco de nueve** combinaciones tienen rentabilidad anual negativa tras costes. BTC Ensemble5 pasa de+5,868% a−23,66%. Los Sharpes de la tabla son anteriores a esa fila de costes y están expresados porcentualmente; no llamarlos Sharpes netos.

Coste constante no equivale a spread, latencia e impacto simulados por exchange/tamaño. El test contiene principalmente caída de mercado y solo tres grandes activos; superar buy and hold no basta para superar efectivo. Los umbrales de ensembles también se comparan en el test, sin otro holdout exterior reportado. La ambigüedad de alguna transformación temporal se registra como incertidumbre, no como fuga demostrada.

### Datos, infraestructura y viabilidad

Modelos tabulares diarios pueden ser accesibles. Requieren datos point-in-time, timestamps de publicación/recepción, fuentes históricas de variables on-chain, pipelines ajustados solo con pasado y registro de toda búsqueda. Presupuestos equivalentes para referencias lineales y no lineales; latencia y turnover medidos con costes compatibles.

**Condiciones de retirada:** no mejora neta frente a referencia simple comparable; ventaja dependiente de variable no disponible; sensibilidad extrema al periodo o a selección no registrada. La falta de significación con poca potencia no demuestra imposibilidad, pero puede impedir justificar complejidad/capital.

## 2. Deep Learning y series temporales

Una red estima `fθ(x_{t−L+1:t})` minimizando una pérdida más regularización. Ventanas solapadas no crean observaciones independientes. Predecir niveles persistentes exige comparar con último valor y reglas lineales, además de evaluar traducción a P&L. En modelos preentrenados, desconocer corpus y fecha de corte impide acreditar OOS.

### Resultados cripto y sus límites

- **Alessandretti et al.2018 (ML-09):** XGBoost/LSTM sobre panel de1.681 criptomonedas, referencia momentum y selección diaria. Publica resultados favorables y sensibilidad a comisiones; el apéndice A3 muestra deterioro importante de varias alternativas. El numerario principal es BTC, no efectivo sin riesgo en euros. La selección de arquitectura LSTM sobre tres monedas y la delimitación de tuning requieren auditoría; algunas descripciones temporales son ambiguas. Capital/impacto/ejecución y crecimiento compuesto implícitos impiden leer sus grandes retornos como capacidad actual. No se acusa fuga sin inspeccionar código.
- **Jiang–Xu–Liang2017 (ML-11):** preprint con CNN/RNN/LSTM de asignación, tres tests de unas siete semanas y validación de hiperparámetros previa; barras30min, Poloniex, BTC como numerario. Incluye comisión0,25% por compra/venta, pero §2.4 p.8 impone fill instantáneo al último precio, slippage e impacto cero. La conclusión p.21 reconoce la limitación. Hay retornos favorables bajo ese simulador y comparadores con pérdidas; no es neto de toda fricción. Activos seleccionados por volumen **anterior al test**; se rellenan historias previas a su existencia en entrenamiento. No convertir ese problema en una acusación distinta de selección con futuro del test.

### Contrastes metodológicos

Zeng et al. (ML-08, versión arXiv2022) encuentra baselines lineales competitivos frente a varios Transformers en predicción multivariante. No son criptomonedas ni estrategias. Sus tablas contienen excepciones a la universalidad del resumen; ventanas/presupuestos tampoco son idénticos. No demuestra que todo Transformer sea peor ni que un modelo lineal gane dinero.

Kapoor–Narayanan (ML-10, preprint2022) corrige estudios de predicción de guerras civiles y muestra erosión de mejoras de ML al eliminar errores de validación. No es evidencia de prevalencia de leakage en cripto ni una réplica realizada por nosotros. Fundamenta preguntas sobre temporalidad, preprocesamiento, dependencia y comparadores.

### Datos/costes/viabilidad

La carga de datos, cómputo y mantenimiento debe justificarse por valor incremental. Redes pequeñas pueden ser técnicamente accesibles; libros y datos de eventos exigen reconstrucción y sincronización. Modelos más complejos amplían selección de arquitectura, semillas, stopping, pérdidas y ensembles. El benchmark debe tener la misma información, restricciones y costes; las mejoras predictivas no sustituyen utilidad económica.

**Condiciones de retirada:** referencia simple suficiente; corpus/fechas imposibles de auditar; ventaja menor que incertidumbre entre semillas/periodos; costes operativos mayores que efecto plausible; dependencia de fills irreales. No aumentar complejidad para rescatar un resultado negativo tras abrir el holdout.

## 3. Controles que la lectura vuelve necesarios

Transformaciones y selección dentro de cada entrenamiento; purga de etiquetas solapadas cuando aplique; registro de consultas al test y alternativas manuales; timestamps de variables; numerario y tratamiento de efectivo explícitos; costes de cada cambio de exposición efectiva; incertidumbre por bloques y multiplicidad definidas antes de ensayos. DSR/PBO son diagnósticos con supuestos, no autorización para reutilizar el holdout: [evidence-methodology.md](evidence-methodology.md).

## 4. Balance de evidencia

Hay resultados publicados favorables bajo hipótesis de ejecución y resultados adversos por costes, comparadores y validación. No hay base para declarar superioridad general de ML/DL ni seleccionar un algoritmo en este proyecto. Las fuentes recientes ML-12/13 solo tienen metadatos/resumen y no compensan una falta de texto completo reciente.

Prioridad de investigación: hipótesis económica, referencia simple, igualdad de información/riesgo y costes antes de complejidad. La auditoría de código/datos, replicación independiente, cobertura reciente y evaluación prospectiva permanecen pendientes. La Fase II no se ha iniciado.
