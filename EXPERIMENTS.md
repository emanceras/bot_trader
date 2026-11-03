# Registro de experimentos

**Registro técnico D-051:** [corrección E3-L2/E4](docs/es/phase-iv/engine-correction.md), [recibos](docs/phase-iv/technical-results/E-correction/README.md).6ejecuciones nuevas bajo D-050: originalE3-L2corregido, D6cancel, E4idempotente,32comprobaciones supervisor(27pasan/5fallan), D6replenish y17comprobaciones de consolidación supervisor(pasan).4procesos nativos/2supervisor; no fills artificiales en el motor ni resultados económicos. E4 original sigue sin segundo fill; no reescribir criterio. E1 pendiente, cero contadores financieros.

**Registro técnico D-049 (2026-11-02):** [recuperación E](docs/es/phase-iv/engine-recovery.md), [casos/recibos](docs/phase-iv/technical-results/E-recovery/README.md). Nueve casos funcionales Nautilus ejercitados parcialmente, cuatro diagnósticos y una repetición correctiva E2; 17 procesos nativos incluyendo los tres reinicios E5. Contabilidad E2 favorable; negativos L1/E4 y bloqueo L2 conservados. E5 solo reconstrucción y conciliación posterior, sin pase completo. M/R/LEAN anteriores intactos; cero experimentos financieros y sin avance de fase.

**Actualizado:** 2026-11-03 · **Versión:** 1.1 · **Estado:** cero experimentos financieros. IV metodológica autorizada, E1/E2 aprobadas condicionalmente; [diseño](docs/es/phase-iv/protocol.md) y [plantilla sin ejecutar](docs/phase-iv/freeze-template.json) conservados. La [enmienda por etapas](docs/es/phase-iv/staged-amendment.md) registra aprobación metodológica; las [pruebas M/E/R](docs/es/phase-iv/technical-results.md) fueron autorizadas por D-046 y sus ejecuciones técnicas, limitaciones y bloqueos se registran por separado. E3/E4 y V–VI pendientes; operativa no autorizada. Las pruebas técnicas de III y A/B permanecen separadas de los experimentos financieros.

## Estado real

| Actividad | Realizados | Resultado |
|---|---:|---|
| Backtests de estrategias | 0 | No ejecutados |
| Optimizaciones/búsquedas de parámetros | 0 | No ejecutadas |
| Entrenamientos ML/DL | 0 | No ejecutados |
| Pruebas de hipótesis sobre datos de mercado | 0 | No ejecutadas |
| Aperturas de holdout final | 0 | No hay holdout financiero constituido; los dos archivos Q3 de QA están expuestos y fuera de la aplicación. Las fixtures reservadas son pruebas de denegación |
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

- **2026-10-18, transición y comparación documental:** el usuario acepta el cierre limitado de I y autoriza II; D-025 registra el alcance. La [matriz](docs/phase-ii/COMPARISON.md), la [viabilidad provisional](docs/phase-ii/FEASIBILITY.md) y el [informe de selección](docs/phase-ii/SELECTION.md) reutilizan los 53 trabajos y H-00–H-24, sin nueva búsqueda general, adquisición de datasets, código de estrategias ni ensayos. C1/C3 son preguntas primarias propuestas, C2 una comparación secundaria de riesgo y C4/C5 alternativas condicionadas; no son resultados, preregistros definitivos ni permiso de ejecución. Recursos y aceptación de la selección pendientes. **Todos los contadores permanecen en cero.**

- **2026-10-18, preferencias y propuesta final de II:** USD y España confirmados; capitales y drawdowns solo sensibilidades documentales. La tabla F/K es aritmética ilustrativa de costes, no un ensayo ni una rentabilidad observada. Proceso de horizontes y contrastes C3-I/C3-X definidos conceptualmente, sin cambiar nulas. Fuentes oficiales de acceso consultadas sin datos de mercado ni cuentas; corpus académico sigue en 53. No laboratorio, backtests, modelos entrenados, compras o gasto. Propuesta final pendiente de aceptación; **todos los contadores experimentales permanecen en cero**.

- **2026-10-26, auditoría técnica A/B (D-040/D-041):** adquisición autorizada de dos archivos KrakenQ3 para QA estructural externo; pruebas de Nautilus1.231.0 aislado con datos sintéticos. [Resultados y negativos](docs/es/phase-iv/admission.md). Ninguna señal, rendimiento de estrategia, ajuste de inversión, selección de activos por resultados ni apertura de holdout. Reconciliar importes de operaciones para QA no es un experimento financiero. **Los siete contadores permanecen en cero.** Q3 queda expuesto, no es histórico de investigación completo ni final intacto. E3/E4 y V siguen pendientes.


- **2026-10-27, revisión metodológica de fuentes y motores (D-042/D-043):** comparación documental y lectura dirigida de fuentes oficiales; contratos temporales/multirresolución, información externa, dependencias, motores y admisión por etapas propuestos en [informe EN/ES](docs/es/phase-iv/evolution.md). Verificaciones de documentos, hashes, enlaces y conservación del historial; sin adquisición adicional, instalaciones, migraciones, nuevas pruebas de motores ni experimentos financieros. M/E/R/H son propuestas no ejecutadas. Se corrige la descripción del contador de holdout para reconocer los dos archivos de QA ya adquiridos; su valor sigue en cero y ningún conjunto final está constituido. Protocolo/aceptación/plantilla intactos; E3/E4 y V pendientes. **Los siete contadores financieros permanecen en cero.**


- **2026-10-27, aprobación metodológica por etapas y paquetes técnicos (D-044/D-045):** enmienda prospectiva T/D/U/V/F aprobada en principio; cambian únicamente momento de completar vinculaciones y registros de acceso, sin habilitar desarrollo financiero. Consulta acotada de metadatos oficiales para fijar versiones/runtimes y diseño de casos sintéticos M/E/R. No se instalaron motores ni paquetes, no se ejecutaron harnesses ni se adquirieron datasets adicionales. Recurso estimado/techo de prueba no es medición ni presupuesto E3. E1/E2, 26 especificaciones, nulas, inferencia, negativos y **siete contadores financieros en cero** preservados. E3/E4 y V pendientes.


- **2026-10-29–30, ejecución técnica M/R/E (D-046):** M ejecutó 20 casos específicos y dos suites de 110 pruebas cada una; R ejecutó 160 casos de coherencia con diarios inventados. Pasan sin corregir casos. Se conserva el control adverso de precisión DuckDB, inventario vacío de objetos sintéticos antiguos y fallos de preparación. E requiere consultar el estado real de instalación/casos en el [informe](docs/es/phase-iv/technical-results.md); una instalación o bloqueo no se cuenta como prueba del motor. Sin nuevos datos financieros ni retornos de estrategias, entrenamiento, selección o apertura de holdout. **Los siete contadores financieros permanecen en cero.**

- **2026-11-01, consolidación D-047:** E conserva tres casos LEAN realmente ejecutados (uno parcial y dos comparaciones obligatorias fallidas), 23 slots sin ejecutar y ninguna admisión completa. Runtime Nautilus bloqueado; no ganador. Auditoría final de conservación satisfactoria, recursos instrumentados dentro de límites, resultados negativos publicados junto con M/R. Ningún experimento financiero añadido.
