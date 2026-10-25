# Fase IV — revisión ejecutiva de decisiones

Documento: IV-EXEC-001 · Versión: 2 · Fecha: 2026-10-25 · Traducción sincronizada del [original inglés](../../en/phase-iv/executive-decisions.md).

**Estado posterior:** el usuario aprobó E1/E2 de `ba6c20b`, D-038; [registro de aprobación](../../phase-iv/APPROVAL-E1-E2.es.md). La propuesta original siguiente se conserva como fundamento revisado, no como otra solicitud de aprobación. E3/E4 siguen pendientes; el [informe de viabilidad](feasibility.md) define el siguiente paso vigente. No se deriva adquisición ni ejecución financiera automática.

## Recomendación y estado

Hay **dos decisiones de diseño que puedes aprobar ahora** y dos decisiones económicas/de recursos que conviene tomar después con evidencia concreta. Se organizan a continuación en cuatro temas. Tus instrucciones sobre USD, fuentes gratuitas aptas, alternativas comerciales y autorización de gastos no necesitan aprobarse otra vez. No completar el protocolo con umbrales numéricos sin fundamento. Las dos elecciones de diseño siguen siendo propuestas; esta revisión no registra una nueva aprobación. Continuarla no autoriza Fase V, datasets financieros, entrenamiento, gastos, paper prospectivo ni operativa real.

Se reutilizan [protocolo](protocol.md), [candidatas](candidates.md), [requisitos de datos/ejecución](data-execution.md) y [aceptación](acceptance.md), sin bibliografía nueva ni cambios a sus elecciones numéricas. Esta revisión aclara el orden y la responsabilidad de las decisiones; no rebaja la aceptación ni rellena la [plantilla de congelación](../../phase-iv/freeze-template.json). Se conservan los 53 trabajos, H-00–H-24, resultados adversos, C1/C3 prioritarias, C2 secundaria y C4/C5 en reserva.

| Tema / momento de decidir | Recomendación | Qué no se aprobaría todavía |
|---|---|---|
| E1. Alcance inicial — aprobar ahora | Tanda condicionada spot largo/efectivo, financiada íntegramente, con un horizonte justificado y una regla de universo point-in-time | Exchange, vehículo de efectivo accesible, horizonte/parámetros exactos del universo o restricciones permanentes de producto |
| E2. Preguntas y comparaciones finitas — aprobar ahora | Mantener el techo propuesto de 26 especificaciones y tres contrastes primarios, condicionado a viabilidad | Ajustes totales, calendario, presupuesto computacional completo o conclusiones universales sobre ML u otras estrategias |
| E3. Compromiso efectivo de recursos — decidir tras dimensionar | Aplicar tu política de gratuito cuando sea apto; comparar alternativas de pago mediante propuestas desglosadas | Compras, suscripciones, presupuesto monetario inventado o trabajo ilimitado con recursos gratuitos |
| E4. Escenario económico/de riesgo — decidir tras conocer viabilidad | Preparar compromisos de materialidad y riesgo para el capital de investigación; fijarlos antes de evaluaciones dependientes | Capital primario de investigación, umbrales numéricos económicos/riesgo, límites personales reales o permiso de ejecución |

Puedes aprobar E1 y E2 conjuntamente o modificar cada una. E3 y E4 identifican decisiones posteriores, no solicitudes de repetir preferencias existentes. El silencio y una solicitud de continuar no equivalen a aprobación. El gasto efectivo y los compromisos económicos/de riesgo aceptables siguen siendo decisiones tuyas; los detalles técnicos no necesitan convertirse en consultas individuales.

## E1 — primera tanda spot largo/efectivo

| Alternativa | Ventajas | Costes y límites |
|---|---|---|
| **Spot largo/efectivo condicionado primero** | Contrasta C1 y C3 con capital/contabilidad comunes; reduce supuestos de préstamo, funding y liquidación | No evalúa construcciones cortas/derivadas/carry ni horizontes ajenos a esta tanda; mantiene riesgos de mercado, custodia, liquidez y conversión |
| Incluir derivados/cortos o varios horizontes desde el inicio | Aborda directamente otros mecanismos y el acceso a mercados bajistas | Requiere admisión diferenciada de datos, garantías/funding/préstamo, ejecución y contabilidad; amplía comparaciones e ingeniería antes de resolver dependencias |
| Posponer por completo el producto | Evita compromiso antes de conocer viabilidad | Deja costes, efectivo de referencia, relojes y motor demasiado abiertos para cerrar una comparación concreta |

**Recomendación:** aceptar spot largo/efectivo como construcción de investigación provisional, comprobando viabilidad antes de resultados. La simplicidad operativa reduce supuestos; no implica mayor oportunidad económica. Un horizonte admitido controla la búsqueda de esta tanda, no la frecuencia futura de las estrategias. Se seleccionará por mecanismo, disponibilidad de información y costes ejecutables, no por comodidad o mejor rentabilidad histórica. No se fija un número arbitrario de activos: elegibilidad histórica, bajas y liquidez gobiernan el universo.

«Efectivo» debe ser una alternativa accesible valorada explícitamente en USD. Contabilizar en USD no convierte USDT/USDC en dólares ni hace instantánea o gratuita una conversión repetida a USD bancarios. Si no se puede reproducir el efectivo propuesto o el horario de salida, habrá que modificar o posponer la construcción antes de evaluarla. La financiación íntegra evita préstamos en esta propuesta; no hace seguro el spot ni limita pérdidas a un drawdown supuesto.

**Si se pospone:** pueden compararse requisitos de fuentes/motores como escenarios, pero no congelar un diseño único de ejecución/efectivo. C4, C5 y otros instrumentos siguen en reserva; un mecanismo mejor justificado puede sustituir prospectivamente la construcción inicial con su contabilidad y presupuesto.

## E2 — qué aportan las 26 especificaciones

El techo propuesto tiene una derivación auditable, no una optimalidad estadística:

| Especificaciones base | Cantidad | Propósito |
|---|---:|---|
| Reglas y referencias | 8 | Efectivo, exposición pasiva, control de exposición calibrado en entrenamiento, reversión, dos memorias C1, política de volatilidad C2 y su control de exposición fija |
| Bloques individuales C3 | 6 | Precio, actividad y volatilidad, cada uno con dos penalizaciones |
| Modelos conjuntos C3 | 6 | Lineal, aditivo no lineal e interacciones explícitas, cada uno con dos penalizaciones |
| Ablaciones C3 reestimadas | 6 | Omitir cada bloque y sus interacciones, cada uno con dos penalizaciones |
| **Total** | **26** | Especificaciones, no ajustes totales, observaciones independientes ni 26 contrastes primarios |

| Alternativa | Ventajas | Costes y límites |
|---|---|---|
| **Conservar este techo condicionado** | Distingue persistencia, información combinada e incremento por interacciones con controles comparables | Folds anidados, reestimaciones, sensibilidades e inferencia multiplican el trabajo; su viabilidad aún no está determinada |
| Reducir preguntas antes de evaluar | Menos coste de datos/ingeniería/cómputo y mayor concentración | Reduce las conclusiones. Quitar un comparador o ablación esencial no permite mantener intacta la afirmación asociada |
| Añadir ahora boosting, redes, inputs u horizontes | Más clases de funciones y mecanismos | Más selección, datos y mantenimiento; la evidencia actual no hace necesaria esa ampliación para la primera comparación |

**Recomendación:** conservar provisionalmente la estructura y exigir el registro completo de intentos/recursos antes del lanzamiento. Es un techo, no una cuota que haya que agotar. Si no es asumible, reducir prospectivamente una pregunta y sus conclusiones; no mantener un modelo complejo eliminando la referencia sencilla necesaria para interpretarlo. C3 no depende del éxito de C1, y los inputs individuales no necesitan ser rentables. No hay derecho automático a gastar especificaciones sobrantes en otro modelo.

Los contrastes primarios son C1, C3-I y C3-X, cada uno con mejora frente al comparador y requisito separado de mejora neta frente al efectivo. La propuesta existente controla el error familiar de falsos rechazos mediante Holm al 5%, condicionado a contrastes componentes válidos; es una política convencional de evidencia, no una probabilidad del 95% de rentabilidad futura. C2 sigue siendo análisis secundario de riesgo. Los contrastes no ejecutados conservan p=1 dentro de la familia; no se recicla su presupuesto de error. La aprobación cubre esta política como conjunto, no exige que elijas semillas bootstrap o tolerancias del solver. Las 9.999 réplicas existentes atienden a granularidad de simulación, no a suficiencia de muestra de mercado; aquí no se introduce ninguna regla numérica nueva.

C3-X estudia únicamente los productos precio–volatilidad y precio–actividad especificados. Un resultado negativo no rechazaría todas las interacciones, boosting, deep learning o información condicional débil. El mismo límite se aplica a las dos memorias C1 y al horizonte admitido. Estudios más amplios necesitan una pregunta material, nuevo presupuesto prospectivo y evaluación independiente adecuada, no búsquedas sobre el test final motivadas por su fracaso.

**Si se pospone:** no pueden cerrarse registro y requisitos de potencia/precisión porque las afirmaciones siguen sin decidirse. Si solo falta dimensionar recursos, puede aprobarse ahora la estructura condicionada y dejar abiertos ajustes totales y calendario.

## E3 — recursos de investigación y operación

| Alternativa | Ventajas | Costes y límites |
|---|---|---|
| Fuentes/recursos gratuitos exclusivamente y para siempre | Evita cargos directos de servicios | Puede excluir integrantes históricos, bajas, timestamps o evidencia de ejecución necesarios; «gratuito» puede exigir mucha ingeniería |
| **Gratuito cuando sea apto; pago revisado con propuestas concretas** | Conserva calidad y oportunidades futuras sin comprometer fondos ahora | Exige una elección posterior desglosada; datos gratuitos inadecuados pueden obligar a posponer |
| Aprobar ahora una asignación amplia | Fija una frontera de asequibilidad | Sin presupuestos comerciales, cobertura y dimensionado del motor no establece entregables ni justifica el gasto |

**Recomendación:** aplicar la segunda política, que ya has indicado y no necesita permiso nuevo. Separar (a) adquisición histórica/investigación y licencias, (b) desarrollo, validación y cómputo y (c) feeds, alojamiento, mantenimiento e inferencia recurrentes. La infraestructura personal es el punto de partida, no prueba de coste nulo ni de capacidad para cualquier carga. Estimar almacenamiento, ajustes, tiempo de ejecución y esfuerzo de ingeniería tras dimensionar fuentes/motor. La estimación debe declarar supuestos e incertidumbre; el capital de referencia no determina el presupuesto de gasto.

La propuesta posterior debe mostrar una ruta gratuita apta cuando exista, una de pago solo si resuelve una limitación material y otra de posponer/acotar. Incluir precios contrastados/licencias, incertidumbre de entrega/calidad, costes únicos y recurrentes en USD, capacidades que habilita cada alternativa y límite de trabajo. En esta revisión no se aprueba proveedor, inventa tarifa ni adquiere dataset financiero. Un techo de asequibilidad que ya conozcas puede orientar la comparación, pero no es necesario para revisar ahora el diseño ni da permiso para gastarlo.

El presupuesto monetario y el de búsqueda estadística son distintos. Cómputo barato no justifica combinaciones ilimitadas. Ajustes, sensibilidades, duración del trabajo y almacenamiento requieren un techo finito incluso con infraestructura gratuita. El gasto de investigación ya realizado no justifica prolongar una hipótesis sin respaldo.

**Si se pospone:** puede concluir la revisión documental, pero no se admite recurso de pago ni la carga experimental futura completa. Si no existe una ruta gratuita adecuada, se informa; no se sustituye con supuestos inventados sobre los datos.

## E4 — capital, materialidad y riesgo

### Capital de referencia: elegir el importe primario después de conocer viabilidad

Tus escenarios de 1.000/5.000/10.000 USD siguen siendo sensibilidades, no límites del proyecto ni tres oportunidades de elegir el resultado más rentable. Las alternativas son designar uno ahora, elegirlo tras evidencia de viabilidad o mostrar únicamente rentabilidades normalizadas. Elegir ahora simplifica, pero puede ser inviable; normalizar ayuda a comparar, pero no demuestra viabilidad de órdenes mínimas, costes fijos o capacidad.

**Recomendación:** seleccionar capital primario de investigación después de documentar tamaños mínimos, comisiones alcanzables, costes de efectivo/conversión y capacidad, y antes de seleccionar por rendimiento. Tú elegirías el escenario económico relevante a partir de ese informe; ni el importe intermedio ni el mejor capital del modelo son valores por defecto. Para coste fijo anual recurrente F y capital K, F/K describe una carga de equilibrio; mínimos e impacto impiden asumir escalado lineal de rentabilidad. Un capital materialmente distinto podría justificar una reserva con presupuesto propio. El capital real a aportar puede seguir pendiente.

**Si se pospone:** valor monetario de la mejora y viabilidad operativa siguen condicionados; no pueden fijarse completamente márgenes económicos y objetivos de precisión de muestra.

### Materialidad económica: evidencia de mejora frente a mejora que merece el esfuerzo

| Alternativa | Implicación |
|---|---|
| Solo efecto neto positivo, con margen de materialidad cero | Pregunta válida sobre mejora tras costes modelados; incluso evidencia convincente puede aportar demasiado poco para justificar complejidad, incertidumbre o recursos |
| **Efecto neto mínimo justificado prospectivamente** | Contrasta una mejora que merezca seguir investigándose; requiere un juicio tuyo sobre valor, informado por costes, capital y esfuerzo; detectarla puede necesitar más datos |
| Varios umbrales sin jerarquía o mejor capital elegido después | No produce una decisión de aceptación estable y favorece selección retrospectiva; no adoptarlo |

Recomiendo la segunda política sin inventar su valor. Conservar tanto margen incremental sobre el comparador adecuado como margen absoluto sobre efectivo accesible. Expresar cada uno en USD y rentabilidad por intervalo coherente para el capital primario; los resúmenes anualizados deben explicar su conversión. Fijarlos antes de evaluaciones dependientes, junto con las reglas de selección en desarrollo/validación. Una métrica predictiva o significación estadística no basta, y un modelo menos negativo no es un éxito económico.

Los costes recurrentes de ejecución y operación se deducen una vez. El margen de materialidad es el beneficio adicional exigido después de esos costes; la incertidumbre del modelo de costes se muestra por separado y no se cobra dos veces. Adquisición/desarrollo únicos deben figurar en un análisis transparente de recuperación de la inversión del proyecto. La suficiencia estadística limita lo que puede aprenderse: si los datos no distinguen el efecto económicamente relevante, acotar la conclusión, obtener evidencia autorizada por separado o concluir inconcluso. No reducir el requisito económico solo para hacerlo detectable. No se propone techo de rentabilidad.

**Si se pospone:** pueden documentarse mecanismos comparativos, pero no certificar «económicamente interesante» ni la precisión necesaria. No rellenar silenciosamente el margen con cero.

### Riesgo: escenarios de investigación y compromiso de C2, no límites personales reales

Los posibles objetivos de riesgo bajista tienen límites distintos: desviación bajista describe déficits repetidos, pero no limita pérdidas extremas; expected shortfall aborda colas, pero exige información suficiente en ellas; máximo drawdown representa pérdida dependiente de la trayectoria, muy sensible a muestra/régimen. Informar medidas complementarias pertinentes; no optimizar la que cuente la mejor historia ni adoptar un umbral universal de Sharpe, drawdown o número de operaciones.

**Recomendación:** conservar el papel secundario de C2 ya aceptado, comparando riesgo frente a su control de exposición fija calibrado en entrenamiento, con sacrificio de rentabilidad permitido explícito. Seleccionar el criterio primario según el objetivo económico y si la muestra permite estimarlo; después aprobar el compromiso riesgo/rentabilidad y escenarios de exposición/pérdida antes de evaluar. Estimaciones y estrés describen incertidumbre, no garantizan una pérdida máxima. Reducir exposición u observar menor drawdown histórico no demuestra por sí solo mejor gestión de riesgo.

Convertir un escenario de investigación en tolerancia personal permanente sería prematuro. Dejar el riesgo de investigación sin restricciones hasta ver rentabilidades perjudicaría la comparación. La tolerancia personal real puede seguir abierta porque no se despliega capital; las restricciones de investigación deben congelarse antes de sus evaluaciones dependientes. Ninguna preferencia de riesgo de esta propuesta autoriza apalancamiento u operativa real.

**Si se pospone:** C2 no permite una decisión de aceptación y la admisión de candidatas permanece incompleta. Describir escenarios como pendientes en vez de inventar un límite personal.

## Decisiones dependientes de evidencia y responsabilidades

Tras aprobar principios, preparar **un único informe concreto de viabilidad**, sin ejecutar estrategias con mercado. Parte de la evidencia puede proceder de documentación contractual pública; cobertura real, calidad de muestra, compatibilidad del motor y calibración necesitan acceso a fuentes o trabajo técnico autorizados por separado. Esta revisión no concede esa autorización.

| Evidencia pendiente | Responsabilidad técnica | Decisión tuya cuando sea concreta |
|---|---|---|
| Proveedor/licencia, integrantes/eventos históricos, disponibilidad y calidad | Comparar cobertura apta e incertidumbres; distinguir campos anunciados de datos auditados | Aprobar adquisición/gasto o reducción material; no hace falta exchange de producción definitivo |
| Motor, mínimos, comisiones, efectivo, demora, capacidad | Demostrar compatibilidad de producto/contabilidad y justificar costes; el banco sintético actual no basta | Revisar restricciones resultantes de producto/horizonte y capital de referencia viable |
| Calendario, dependencia, soporte independiente, relojes y carga total | Proponer particiones, precisión, parámetros, intentos y techos de recursos; conservar inaccesibilidad del test | Aprobar cambio material de alcance o compromiso de recursos; sin consultar cada valor técnico |
| Escenarios de beneficio/riesgo con costes | Presentar implicaciones netas en USD, incertidumbre, criterio primario de riesgo y sacrificio de rentabilidad, sin escoger por resultados de candidatas | Elegir capital primario, márgenes económicos y compromiso de riesgo como escenario coherente |
| Paquete congelado, evidencia de implementación y custodia | Resolver todas las vinculaciones y comprobaciones; documentar límites de custodia en equipo personal | Aceptar prerregistro final y, solo si deseas, autorizar por separado el alcance concreto posterior de adquisición/trabajo técnico/ejecución |

Umbral monetario, capital de referencia y sacrificio de riesgo aceptable no se delegan a un optimizador. Proveedor/adaptador exactos, relojes, tolerancias, semillas y otros detalles pueden resolverse y registrarse por el equipo en un alcance posterior autorizado. Consultar solo cambios científicos materiales, gasto, elección de pérdidas/exposición, incertidumbre irreducible que cambie la decisión o permisos. No hacen falta credenciales.

## Tanda acotada, programa de investigación abierto

Mantener elegibles para consideración posterior derivados, cortos, otros mercados, C4/C5, noticias/on-chain, ML/DL más amplio y horizontes diferentes. Reabrir exige mecanismo o incremento informativo concreto, cambios de acceso/datos/recursos u otra evidencia material, comparación explícita y presupuesto finito. Un resultado inicial negativo no justifica expansión indefinida, y un contraste limitado inconcluyente no refuta la familia completa. Conservar resultados rechazados/negativos y motivo de reconsideración.

Toda revisión es prospectiva y versionada. La exposición a desarrollo, validación o test determina qué sigue siendo evidencia independiente; un documento nuevo no convierte datos finales reutilizados en desconocidos. Aprobar esta tanda no promociona reservas automáticamente, permite barridos de horizontes ni excluye alternativas para siempre.

**Alcance de aprobación sugerido ahora:** E1 y E2 como elecciones condicionadas del diseño metodológico. Aplicar las preferencias de recursos existentes y reservar el compromiso concreto E3 y los valores de capital/materialidad/riesgo E4 para el informe consolidado. No cerraría IV incondicionalmente, autorizaría adquisición o gasto, activaría V ni cambiaría la aplicación sintética. Estos límites permanecen hasta que apruebes expresamente el siguiente alcance concreto pertinente.
