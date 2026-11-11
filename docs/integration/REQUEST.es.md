# BOT_TRADER — DESARROLLO INCREMENTAL DE LA PLATAFORMA INTEGRAL

## Contexto y decisión

Quiero continuar desarrollando `bot_trader` siguiendo su roadmap, metodología científica y visión original: una plataforma modular de investigación, desarrollo, evaluación y futura ejecución de estrategias cuantitativas, con capacidad de incorporar inteligencia artificial, automatización y múltiples fuentes de información.

**Decisión:** cerramos por ahora la evaluación general de NautilusTrader y LEAN. Los resultados E1/velas publicados en `9be75a2` proporcionan evidencia suficiente para avanzar, conservando sus limitaciones. No quiero seguir consumiendo recursos intentando perfeccionar un motor antes de desarrollar el resto del sistema.

Los datos, la investigación, las estrategias, la simulación, el riesgo y la ejecución son componentes de un mismo sistema. Ninguno debe convertirse en un proyecto independiente que bloquee indefinidamente los demás.

**Autorizo implementar una primera integración técnica funcional de extremo a extremo**, con alcance acotado y pruebas reproducibles. No autorizo experimentos financieros, nuevas adquisiciones de datos ni operativa de mercado.

## 1. Preparación

Lee `AGENTS.md`, `ROADMAP.md`, `DECISIONS.md`, los contratos y el código existentes, y los informes de E1 y los paquetes M/R/E.

Comprueba `git status`, identifica lo que ya está implementado y reutiliza sus componentes y pruebas.

Actualiza `AGENTS.md` solamente con las nuevas reglas arquitectónicas permanentes que falten, sin copiar informes extensos ni convertir decisiones temporales en instrucciones universales.

Preserva los resultados originales, los negativos y los criterios científicos.

## 2. Primera integración funcional

Construye la mínima rebanada técnica que conecte:

**Archivo histórico → Normalización → Market Replay → Estado analítico e indicadores → Señal → Ejecución sintética causal → Ledger y oráculo independiente.**

No quiero una plataforma de datos aislada ni un prototipo desechable. Quiero una primera integración del sistema completo, diseñada para crecer de manera modular.

### Datos y contratos temporales

- Archivo bruto inmutable, con identidad, procedencia, hashes, derechos de uso, versiones y adquisición idempotente y reanudable.
- Separación explícita entre datos originales, normalizados y derivados.
- Contrato v2 de eventos para histórico y futura captura directa, con timestamps enteros exactos en nanosegundos, unidad original, fuente, secuencia, esquema y disponibilidad efectiva.
- Conservar diferenciados tiempo de evento, disponibilidad, recepción cuando exista y `ts_init` específico del motor. No equipararlos automáticamente.
- Rechazar explícitamente conversiones con pérdida, precisión no admitida y timestamps incompatibles. Nunca redondear silenciosamente.
- Preparar la migración del `MarketBar` actual basado en `datetime` a representaciones temporales exactas, manteniendo compatibilidad comprobada. No romper producción para forzar la migración.

### Market Replay y señales

- Implementar una capa determinista de ordenación, disponibilidad y reproducción de acontecimientos.
- El Market Replay alimentará al estado analítico, las estrategias y el motor de ejecución; no será otro motor financiero paralelo.
- Reconstruir progresivamente velas e indicadores utilizando únicamente información disponible en cada instante.
- Diferenciar velas abiertas, cerradas y corregidas; una vela completa nunca debe conocerse antes de su cierre y disponibilidad efectiva.
- Implementar una señal trivial y determinista únicamente para verificar la integración, sin introducir hipótesis nuevas de inversión.
- Registrar procedencia, versiones y hashes de entradas y decisiones.
- Reutilizar los canarios temporales pertinentes de R y E1, sin repetir las baterías completas ya superadas.

### Ejecución y contabilidad

Implementar y verificar un ciclo sintético mínimo **long/cash de compra y venta**, con:

- Señales y órdenes posteriores a la información que las genera.
- Cotizaciones y precios de ejecución explícitos, causalmente elegibles y con procedencia trazable.
- Casos acotados de ejecución completa, parcial, rechazo, remanentes y cancelación confirmada.
- Conservación correcta de estados e identidades de órdenes y fills.
- Comisiones, spread, slippage, latencia y capacidad como supuestos versionados.
- Conciliación independiente con aritmética Decimal: efectivo, posición, cantidades, comisiones y reservas.
- Ante un estado incierto, no inventar fills ni asumir cancelaciones confirmadas.

NautilusTrader permanece como **candidato condicionado y sustituible**. No utilizar `bar_execution=True` ni una latencia pequeña como sustitutos de la ejecución posterior a una señal de cierre.

Las cotizaciones construidas desde OHLC son supuestos de simulación, no liquidez observada. No atribuir ejecuciones retrospectivas a la apertura siguiente ni a ningún precio que no estuviera causalmente disponible.

No construyas un nuevo motor financiero ni un gestor universal de órdenes. Si algún requisito del ciclo de vida no puede integrarse razonablemente en esta rebanada, demuestra el contrato mediante pruebas sintéticas aisladas, registra el bloqueo de integración nativa y continúa con las partes independientes. No declares superado lo que no hayas probado de extremo a extremo.

## 3. Datos para las pruebas

Utiliza inicialmente fixtures sintéticos pequeños y adversos.

Si aporta valor, reutiliza una muestra del trimestre de Kraken ya descargado, exclusivamente para comprobar lectura, normalización, precisión temporal, integridad y reproducción de eventos.

El histórico de Kraken sigue marcado como expuesto y no admitido para experimentación financiera.

**No ejecutes estrategias financieras sobre esos datos ni calcules, selecciones o publiques PnL, rentabilidades, Sharpe, drawdowns u otras métricas económicas.**

La ejecución y la conciliación de órdenes deben verificarse mediante fixtures sintéticos.

Las muestras pequeñas sirven para validar la infraestructura, no representan una limitación futura del histórico. La arquitectura debe admitir una ampliación sistemática de fuentes, periodos, mercados e instrumentos, incluidos los que hayan dejado de cotizar.

## 4. Criterios de aceptación

La primera integración debe demostrar mediante pruebas ejecutadas que:

1. La misma entrada y configuración producen la misma secuencia de decisiones y resultados canónicos deterministas.
2. No se revela información antes de su disponibilidad efectiva, incluidas correcciones y velas futuras.
3. Los originales permanecen íntegros y pueden relacionarse con las transformaciones y resultados derivados.
4. Los timestamps, unidades e identidades conservan su precisión o se rechazan explícitamente.
5. Las señales, órdenes, fills y movimientos contables son trazables y conciliables mediante un oráculo independiente.
6. Los duplicados no producen efectos dobles y los huecos, desórdenes, corrupciones e interrupciones se detectan sin reparaciones silenciosas.
7. Los componentes se comunican mediante contratos claros, versionados y sustituibles.
8. Las pruebas adversas y las limitaciones quedan preservadas; superar un control negativo no convierte un comportamiento incorrecto en admisible.

Distingue siempre **implementado, probado parcialmente, probado de extremo a extremo y pendiente**.

No exijas ahora garantías propias del trading real o de una simulación universal de microestructura que no sean necesarias para esta primera integración.

## 5. Continuidad y ahorro de recursos

Trabaja en cuatro hitos pequeños y publica un commit verificable al terminar cada uno:

**Hito 1 — Archivo, normalización y contratos temporales.**

**Hito 2 — Market Replay, estado analítico, indicadores y señal sintética.**

**Hito 3 — Ejecución sintética de ida y vuelta y conciliación independiente.**

**Hito 4 — Pruebas de integración, comprobación de criterios y cierre.**

Prioriza resultados funcionales frente a documentación extensa.

Mantén un `STATE.md` breve con:

- Último commit publicado.
- Componentes completados y pendientes.
- Pruebas realmente ejecutadas y resultados.
- Bloqueos concretos.
- Siguiente acción exacta para reanudar.

Actualízalo en cada hito. Si el trabajo se interrumpe por créditos o por cualquier otro motivo, la siguiente sesión debe poder continuar sin repetir tareas completadas.

Conserva la evidencia de defectos y correcciones: versión fallida, resultado original, diff y regresión. No concedas intentos ilimitados para obtener resultados favorables.

No generes informes extensos duplicados en español e inglés durante el desarrollo. Al terminar, publica un único informe técnico breve y reproducible.

**Presupuesto de referencia:** máximo cuatro horas de trabajo técnico y treinta minutos de ejecución de máquina para esta primera rebanada, sin nuevas descargas ni servicios de pago. Si el alcance no cabe, prioriza un recorrido vertical verificable y registra lo restante; no amplíes automáticamente el presupuesto.

## 6. Arquitectura y continuación futura

La plataforma deberá poder incorporar progresivamente:

- Históricos granulares de múltiples exchanges, activos y periodos.
- Trades, bid/ask, profundidad, funding y otros acontecimientos de mercado.
- Captura continua de información y almacenamiento persistente.
- Noticias, macroeconomía, información regulatoria, sentimiento y datos on-chain.
- Indicadores, modelos predictivos y relaciones entre activos.
- Investigación automatizada con IA y generación controlada de hipótesis.
- Cantera de estrategias, comparación de modelos, Monte Carlo, robustez y evaluación de deterioro de señales.
- Supervisión, riesgo, asignación de capital y futura operativa paper/live.

Estas capacidades pertenecen a la visión integral del proyecto, pero **no están todas autorizadas para implementarse en esta entrega**.

Deja expresamente en cola dos siguientes comprobaciones arquitectónicas:

**A. Segunda fuente:** añadir otro proveedor mediante un adaptador sin modificar el núcleo. Si requiere un cambio de contrato, justificarlo como enmienda versionada con migración y regresiones.

**B. Captura directa mínima:** recibir trades y mejor bid/ask de uno o dos pares legalmente accesibles desde España, conservando recepción, secuencias, huecos y reconexiones, sin enviar órdenes.

La captura directa tiene prioridad temporal porque la información que no guardemos hoy podría no recuperarse después. Podrá prepararse sin esperar a completar toda la cobertura histórica, pero su activación requiere autorización separada de fuentes, derechos, recursos y costes.

La recopilación histórica y la integración de noticias podrán ampliarse progresivamente sin bloquear el desarrollo de las demás capacidades.

## 7. Restricciones científicas y operativas

Mantén:

- Las 26 especificaciones científicas actuales y las prioridades C1/C3.
- Las comparaciones C2 y las reservas C4/C5.
- La metodología T/D/U/V/F y sus criterios de aceptación.
- USD como unidad científica actual, salvo enmienda explícita.
- E3/E4 económicos pendientes.
- Custodia y acceso restringido al holdout.
- La Fase V sin autorización.

No repitas la evaluación general de NautilusTrader ni LEAN, los paquetes M/R/E o las pruebas E1 ya publicadas.

No contrates servicios, descargues masivamente datos, actives capturas externas persistentes, uses credenciales de exchanges, ejecutes backtests financieros, entrenes modelos con mercado real ni habilites paper/live.

No modifiques los criterios científicos para favorecer resultados ni alteres componentes ajenos al alcance.

Esta autorización permite implementar y probar la integración técnica aislada, actualizar su documentación mínima y publicar los commits correspondientes. No concede permisos financieros adicionales.

## 8. Entrega final

Quiero **código funcional, pruebas realmente ejecutadas y evidencia reproducible**, no otra propuesta teórica extensa.

Entrega:

- Commits publicados de los cuatro hitos completados.
- Estado de cada criterio de aceptación.
- Resultado de la prueba integral.
- Limitaciones y bloqueos que todavía existan.
- Recursos utilizados.
- Próxima integración recomendada siguiendo el roadmap.

Si un requisito resulta imposible dentro del alcance, registra el motivo y continúa con lo independiente. No sacrifiques la integridad científica para marcarlo como superado.

**Principio rector: desarrollar un sistema cuantitativo completo, robusto y ampliable mediante soluciones técnicas rigurosas, evitando tanto la improvisación como la sobreingeniería.**

La metodología debe guiarnos para resolver problemas y avanzar, no inmovilizar el desarrollo.

**Puedes comenzar directamente con esta integración técnica autorizada.**