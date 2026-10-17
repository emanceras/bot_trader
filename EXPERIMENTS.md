# Registro de experimentos

**Actualizado:** 2026-10-17 · **Estado:** sin experimentos; ejecución no autorizada en Fase I.

## Estado real

| Actividad | Realizados | Resultado |
|---|---:|---|
| Backtests de estrategias | 0 | No ejecutados |
| Optimizaciones/búsquedas de parámetros | 0 | No ejecutadas |
| Entrenamientos ML/DL | 0 | No ejecutados |
| Pruebas de hipótesis sobre datos de mercado | 0 | No ejecutadas |
| Aperturas de holdout final | 0 | Aún no existe un dataset ni una partición final |
| Paper trading | 0 | No iniciado |
| Órdenes reales | 0 | No autorizadas |

Las comprobaciones de archivos, enlaces locales o acceso HTTPS son verificaciones documentales/operativas, no experimentos financieros. Los errores de acceso a fuentes están en `RESEARCH.md` y sus apéndices. Ninguna validación documental demuestra ventaja estadística.

## Reglas del futuro registro

- Asignar un ID antes de ejecutar cada ensayo; conservar fallos, cancelaciones, resultados nulos y negativos. Las variaciones cuentan aunque no se publiquen en el informe principal.
- Registrar también decisiones de universo, periodo, features, costes y selección que amplían el espacio de búsqueda.
- Preservar configuración y resultados originales; anexar correcciones y relaciones entre ensayos. No borrar ni renombrar fallos para ocultarlos.
- Guardar versiones de código, entorno, datos/transformaciones, hashes, semillas y comandos exactos; distinguir repetición idéntica de nueva hipótesis.
- Informar pruebas realmente ejecutadas, fallidas, omitidas y no aplicables. Cero operaciones o cero muestras válidas no valida una estrategia.
- Bloquear consultas al holdout final hasta la apertura autorizada y registrada. Una vez observado para rediseñar, deja de ser un test independiente.

## Plantilla futura — aún sin instancias

```text
ID / fecha de registro:
Estado: planificado | iniciado | completado | fallido | cancelado
Hipótesis primaria y secundarias / versión del preregistro:
Motivo y relación con experimentos anteriores:
Responsable / aprobación de fase:

Mercado, universo point-in-time, moneda y capital:
Datos: fuente, licencia, versión, hashes, fechas, frecuencia, reglas de calidad:
Intervalos train/validation/test y horizonte informativo:
Purga/embargo (si aplica) y justificación:
Holdout: sellado | abierto; registro de acceso:

Código/commit, entorno, dependencias, semilla y comando:
Señal, cartera, horarios, límites, ejecución y fill:
Comisiones, spread, slippage/impacto, financiación/funding, margen:
Noticias (si aplica): versiones, consenso anterior, recepción, grupos de eventos, demora total:
NLP/LLM (si aplica): snapshot, conocimiento previo, prompts/herramientas y coste de inferencia:
Parámetros probados y presupuesto acumulado de búsqueda:
Comparadores y condiciones comunes:
Métrica primaria, efecto mínimo, método y criterio fijados antes del resultado:
Pruebas múltiples, incertidumbre, sensibilidad y estrés previstos:

Inicio/fin, salida del runner, muestras/trades válidos y excluidos:
Resultados brutos/netos y descomposición de costes:
Rentabilidad anualizada; Sharpe/Sortino; drawdown/Calmar:
Profit Factor/expectancy y definición de trade; turnover/exposición:
Distribución/colas, incertidumbre y desempeño por régimen:
Resultados adversos, fallos, supuestos vulnerados y limitaciones:
Artefactos y hashes; comprobación de reproducibilidad:
Conclusión: apoya | contradice | inconcluso (con razón):
Acción: continuar según plan | detener | propuesta de nueva hipótesis:
Enmiendas: fecha, motivo, datos ya vistos y consecuencias para independencia:
```

No hay resultados numéricos propios, gráficos de rendimiento propios ni estimaciones de rentabilidad del proyecto. Las cifras de RESEARCH y sus fichas pertenecen a publicaciones identificadas; no son experimentos realizados aquí.

## Registro de continuidad documental

- **2026-10-15:** consolidada revisión de literatura con lecturas dirigidas de 28 textos y fuentes parciales. Extracción de tablas/PDF, consultas HTTPS, hashes, JSONL y auditoría de enlaces son tareas documentales. No constituyen entrenamientos, optimización, backtests ni replicaciones financieras. Todos los contadores de la tabla inicial permanecen en cero.

- **2026-10-16, ampliación:** once trabajos adicionales con lectura dirigida, para un total de 39, y cotejos puntuales de cifras frente a PDF. Las restas documentales de costes publicados y comprobaciones aritméticas de tablas no son backtests ni resultados propios. No se ejecutó código de autores ni se alteró ningún contador de experimentos.

- **2026-10-17, noticias y continuidad:** añadidos nueve estudios documentales de noticias/sentimiento/eventos y PORT-04, total 49 textos con lectura dirigida. Evaluación documental de proveedores y sus tarifas, sin feed probado ni dataset de trading adquirido. Las cifras de autores y ejemplos aritméticos de precio de API no son resultados propios. No se entrenó NLP/LLM, ejecutó código de autores, seleccionó estrategia ni abrió holdout. **Todos los contadores permanecen en cero.**

- **2026-10-17, relaciones/interacciones:** cuatro lecturas dirigidas adicionales, corpus 53, con revisiones documentales y fórmulas conceptuales. Ningún dataset de backtesting, entrenamiento, código de autores o experimento propio. El ejemplo lógico XOR y las simulaciones descritas por terceros no son pruebas ejecutadas aquí. H-23/H-24 están propuestas; todos los contadores siguen en cero.

- **2026-10-17, auditoría de cobertura:** revisadas fichas, hipótesis, fuentes y registros; contraste acotado de documentación pública de datos, sin adquirir series de mercado. Conciliaciones de logs basadas en lecturas previamente documentadas, sin nuevas lecturas ficticias ni aumento del corpus académico de 53. Recomendación de cierre limitado pendiente de aceptación; ningún candidato seleccionado ni avance a II. Las comprobaciones documentales no son backtests, entrenamientos ni validaciones financieras. Todos los contadores permanecen en cero.
