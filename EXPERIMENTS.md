# Registro de experimentos

**Actualizado:** 2026-10-15 · **Estado:** sin experimentos; ejecución no autorizada en Fase I.

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
