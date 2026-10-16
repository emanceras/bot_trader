# Evidencia metodológica: selección, multiplicidad y validación

Consulta de metadatos: 2026-10-13. Lectura reanudada: 2026-10-14. Alcance: Fase I; ningún cálculo, simulación o experimento de los artículos se ha replicado. Los métodos se evalúan como posibles herramientas, no como protocolo experimental aprobado.

Registro de acceso y hashes: [search-methodology.jsonl](search-methodology.jsonl). Los PDF originales y sus extracciones permanecen en `/workspace/literature-cache/methodology`, fuera del repositorio. «Texto completo» indica disponibilidad y lectura de las secciones detalladas, no revisión exhaustiva de cada referencia o apéndice.

## MET-03 — Deflated Sharpe Ratio

- **Identidad:** David H. Bailey y Marcos López de Prado, *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality*. Publicación identificada mediante Crossref: *The Journal of Portfolio Management* (2014), [DOI](https://doi.org/10.3905/jpm.2014.40.5.094).
- **Versión realmente leída:** manuscrito del autor fechado 31 de julio de 2014, 22 páginas; [PDF del autor](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf). La portada dice «forthcoming»; no se presume que sea idéntico a la versión editorial. SHA-256 `ca4a1e834a2954b84eb560776e903329cd9cef318d458aadf6d67bc8166d10b5`. La página SSRN se leyó, pero su enlace de descarga devolvió HTML: no contarlo como otro PDF.
- **Secciones examinadas:** definición y justificación pp.7–9, ejemplo y parada pp.9–11, apéndice A.3 p.14; portada, resumen y conclusiones.
- **Resultado metodológico:** el máximo Sharpe observado aumenta al seleccionar entre más alternativas incluso sin habilidad, bajo el modelo de ensayos de p.7. La ecuación 2, pp.8–9, eleva el umbral mediante la multiplicidad y considera longitud de muestra, asimetría y curtosis. Requiere también la dispersión de los Sharpes ensayados y número de intentos independientes.
- **Límite relevante:** el apéndice A.3 distingue intentos totales de intentos independientes y propone una aproximación basada en correlación media. Esa aproximación no es una reconstrucción exacta de toda selección manual, búsqueda de universo, periodos y modelos. Suponer un número de intentos conveniente después de observar el resultado sería otra elección sesgada.
- **Juicio crítico propio:** una CDF de significación bajo este modelo no es la probabilidad de que el bot gane en el futuro ni una garantía frente a ruptura estructural, costes omitidos o datos contaminados. Antes de aplicarla habrá que justificar momentos estimables, dependencia temporal, frecuencia coherente y registro completo de ensayos. La recomendación de parada basada en el «secretary problem» de pp.10–11 no se adopta como presupuesto universal: sus supuestos no sustituyen una hipótesis económica y preregistro.
- **Transferibilidad:** metodología financiera general, no estudio empírico de estrategias cripto. Se conserva como diagnóstico potencial complementario a OOS cronológico y evaluación prospectiva. No se ha calculado un DSR para este proyecto.

## MET-04 — Probability of Backtest Overfitting

- **Identidad:** David H. Bailey, Jonathan M. Borwein, Marcos López de Prado y Qiji Jim Zhu, *The Probability of Backtest Overfitting*. Identidad editorial contrastada mediante [DOI](https://doi.org/10.21314/JCF.2016.322), *The Journal of Computational Finance*. El registro Crossref recuperado fecha publicación en septiembre de 2016; la referencia semilla citaba volumen de 2017. La fecha de la versión examinada es independiente de esa diferencia bibliográfica.
- **Versión leída:** manuscrito del autor de 27 de febrero de 2015, 34 páginas, [PDF](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf), SHA-256 `d8bfbadaaedb430d9dec929646d92f3580fdf18238f34121ae7738fa1c69a63d`. Página/resumen SSRN consultados; no son una réplica ni otra investigación independiente.
- **Secciones examinadas:** motivación y holdout pp.6–8, definición formal y CSCV §§2.1–2.2 pp.9–12, selección de particiones p.22, limitaciones §5.1 p.23 y conclusión p.28.
- **Objeto exacto:** la definición 2.2 en p.10 mide la probabilidad, bajo las particiones consideradas, de que el modelo seleccionado como mejor dentro de muestra quede por debajo de la mediana de rangos fuera de muestra. No es probabilidad de perder dinero ni de insolvencia. La conclusión p.28 usa «mean»; para describir el procedimiento se sigue la definición formal de rangos/mediana, no esa redacción final.
- **Datos necesarios:** matriz temporal sincronizada del P&L de **todas** las alternativas; la selección entre estrategias es distinta de estimar cada estrategia. §2.2 exige que la métrica pueda estimarse en las submuestras. No disponer de los ensayos fallidos limita el análisis.
- **Límites que el propio trabajo reconoce:** §5.1 advierte que la división simétrica puede ser inadecuada bajo fuerte autocorrelación y que otras particiones pueden ajustarse mejor al modelo. El número de combinaciones no crea por sí solo observaciones de mercado independientes.
- **Juicio crítico propio:** CSCV reordena qué bloques sirven para elegir y evaluar configuraciones; no reproduce por sí mismo una política que se entrena exclusivamente con el pasado. No sustituirá walk-forward ni el holdout final sellado. Un PBO bajo tampoco implica que todas las estrategias candidatas tengan beneficio neto: puede elegirse de forma estable la menos mala. No se adopta el número de particiones sugerido en p.22 sin analizar horizonte y dependencia.
- **Estado:** fundamento y límites verificados; aplicabilidad y parametrización pendientes de Fase IV. No hay PBO calculado ni validación de estrategias propias.

## MET-05 — Multiplicidad en factores

- **Identidad:** Campbell R. Harvey, Yan Liu y Heqing Zhu, *… and the Cross-Section of Expected Returns*. [DOI editorial](https://doi.org/10.1093/rfs/hhv059), *Review of Financial Studies*, publicación online 2015; referencia de volumen 2016. Identidad y autores contrastados con Crossref.
- **Versión leída:** NBER WP20592, octubre de 2014, [PDF](https://www.nber.org/system/files/working_papers/w20592/w20592.pdf), SHA-256 `15387ff6505c7eafdf18a89b63883b130a1497aaa41a9160d260a5ba045dfcef`. La portada declara que NBER working papers no se revisan por pares. No se mezclan sus cifras con una versión editorial posterior.
- **Secciones examinadas:** introducción; §4.1–4.4, PDF pp.7–15; modelo y resultados §5, PDF pp.28–34; conclusiones PDF pp.37–38. Páginas impresas = página PDF menos dos en esas secciones. No se revisó de forma exhaustiva el catálogo de factores/apéndices.
- **Aporte verificado:** diferencia entre controlar la probabilidad de al menos un falso positivo —FWER— y la proporción esperada de falsos descubrimientos —FDR—, §4.3. Las correcciones necesitan definir la familia de pruebas y reconocer ensayos no publicados. La significación de cada hallazgo por separado no controla la selección conjunta.
- **Resultado contextual:** el WP propone umbrales mayores que el t convencional cercano a dos para su catálogo financiero y modelos. §5.1 asume, en una especificación, normalidad conjunta y ausencia de correlación serial; §5.2 y la conclusión muestran dependencia de hipótesis y cantidad de pruebas. **No trasladamos un t fijo de tres como criterio universal a cripto.** El propio final dice que no necesariamente debe ser el mismo para todo factor futuro.
- **Límites:** literatura principalmente de acciones y factores tradicionales; sesgo de publicación y número real de pruebas desconocido. La modelización de estos faltantes no revela todos los ensayos efectivamente realizados. El texto cita degradación posterior a publicación de otros estudios; aquí esa mención es secundaria, no lectura independiente de esos originales.
- **Implicación:** conservar registro integral de pruebas, separar objetivo confirmatorio de exploración y fijar correcciones antes de experimentar. Una p ajustada no cuantifica coste, tamaño económico, ejecutabilidad o persistencia del efecto.

## Fuentes identificadas sin texto completo leído

| ID | Identidad verificada por Crossref | Acceso y límite |
|---|---|---|
| MET-01 | Halbert White (2000), *A Reality Check for Data Snooping*, Econometrica, [DOI](https://doi.org/10.1111/1468-0262.00152) | Metadatos. PDF Wiley respondió HTTP403; no se atribuyen aquí detalles de supuestos o resultados del original. Su uso en un estudio aplicado debe evaluarse por separado. |
| MET-02 | Peter Reinhard Hansen (2005), *A Test for Superior Predictive Ability*, Journal of Business & Economic Statistics, [DOI](https://doi.org/10.1198/073500105000000063) | Metadatos. PDF editorial HTTP403. El campo de enlaces de Crossref apuntaba a otro DOI; no se utilizó como texto de este trabajo. Método original pendiente de lectura. |
| MET-06 | Andrew W. Lo (2002), *The Statistics of Sharpe Ratios*, Financial Analysts Journal, [DOI](https://doi.org/10.2469/faj.v58.n4.2453) | Metadatos. PDF editorial HTTP403. No se presentan fórmulas/resultados como extraídos de su texto. |

## Consecuencias para el proyecto

1. Conservar estrategias fallidas, búsquedas manuales y cambios de datos/costes en el registro; contar solo el último grid subestima selección.
2. Evaluar el procedimiento completo con información causal; no confundir bloques de CSCV con entrenamiento cronológico.
3. Separar significación, tamaño económico neto, estabilidad y riesgos operativos. Ningún ajuste estadístico corrige fills imposibles.
4. Mantener holdout final y prueba prospectiva. Son complementarios al diagnóstico de selección, con tamaño efectivo y dependencia por justificar.
5. Contrastar también los métodos de validación: no elegir retrospectivamente el que dé una conclusión favorable.

Tres textos metodológicos examinados; tres referencias adicionales limitadas a metadatos. El contraste sobre leakage de ML-10 se documenta en [evidence-ml.md](evidence-ml.md). No se ha implementado ni seleccionado todavía un procedimiento experimental de Fase IV.
