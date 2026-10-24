# Protocolo de comparación de candidatas

Documento: IV-CAND-001 · Versión: 1 · Actualizado: 2026-10-24 · Idioma: es (traducción).

Original canónico: [inglés](../../en/phase-iv/candidates.md), sincronizado con IV-CAND-001 v1. Leer junto con el [protocolo central](protocol.md) y la [admisión de datos/ejecución](data-execution.md). **Solo diseño metodológico: este documento no implementa, ajusta, experimenta financieramente ni valida ninguna candidata.** V sigue sin autorización; el ledger sintético actual no es un motor financiero admitido.

## 1. Preguntas y evidencia conservadas

La [selección aceptada de II](../../phase-ii/SELECTION.md), el [proceso de horizontes](../../phase-ii/HORIZONS.md) y [H-00–H-24 originales](../../../HYPOTHESES.md) siguen siendo las referencias. Este documento acota una primera tanda evaluable sin reescribir las hipótesis ni declarar imposibles otras construcciones.

| Candidata | Papel / estimando | Evidencia existente y resultados contrarios | Disposición inicial |
|---|---|---|---|
| C1 / H-01 | Valor económico neto incremental de persistencia temporal frente a exposición pasiva con capital/riesgo comparables | DIR-001 respalda persistencia condicionada; DIR-006 contiene un test temporal BTC adverso; DIR-010 y CTR-01 limitan la generalización. [Síntesis direccional](../../research/directional.md) | Primaria; momentum no tiene que superar todos los mecanismos futuros |
| C2 / H-06 | Cambio de riesgo/utilidad por dimensionamiento causal con volatilidad, manteniendo fija la señal predictiva | RP-01 trata mercados tradicionales, no una réplica cripto; PORT-04 y estudios de riesgo contienen excepciones. [Síntesis de riesgo](../../research/risk-portfolio.md), [continuidad de carteras](../../research/portfolio-followup.md) | Secundaria, no afirmación independiente de alpha |
| C3-I / referencia dentro de C3 | Valor de combinar información frente a bloques individuales | ML-06 incluye casos netos favorables y negativos; IX-01 trata acciones y no prueba cripto. [Síntesis ML](../../research/ml-execution.md), [evidencia de interacciones](../../research/evidence-variable-interactions.md) | Comparación primaria; una mejora aditiva no rechaza por sí sola H-24 |
| C3-X / H-11/H-24 | Incremento de interacciones especificadas frente a un aditivo no lineal con idéntica información | Misma evidencia; mejora predictiva y utilidad de cartera difieren, costes y selección siguen siendo materiales | Primaria; no exige éxito de C1 ni inputs individuales rentables |
| C4 / H-23 | Información adicional de otros activos tras pasado propio y factores comunes | Dependencias descriptivas y enlaces inestables no equivalen a alpha neto ejecutable. [Revisión entre activos](../../research/cross-asset-interactions.md) | Reserva condicionada, cero plazas de búsqueda inicial |
| C5 / H-08 | Carry neto sobre todo el capital comprometido, incluidas garantías y reservas | Flujos contractuales identificables; inversión de funding, persistencia de basis, comisiones y liquidación pueden eliminar el beneficio. [Selección C5](../../phase-ii/SELECTION.md) | Reserva condicionada, cero plazas de búsqueda inicial |

Se reutilizan evaluaciones del proyecto, no artículos recién leídos ni réplicas independientes. Ninguna rentabilidad publicada se atribuye a bot_trader. H-00 sigue siendo una conclusión sobre alternativas efectivamente evaluadas, no un teorema universal de inexistencia de oportunidades.

## 2. Unidad contable común y alcance de la primera tanda

La unidad inferencial es el **retorno emparejado en tiempo calendario de la cuenta completa en USD**, después de todos los costes especificados, incluyendo efectivo no invertido y el mismo capital comprometido. Filas de activos y operaciones no son cuentas independientes. Conservar periodos sin operaciones. Comparar alternativas sobre las mismas fechas admisibles y reglas de disponibilidad; sin subconjuntos favorables de activos ni denominadores restringidos a periodos activos.

Para candidata `j`, definir `d(j,t) = r(j,t) - r(reference_j,t)`. El estimando incremental primario es `E[d(j,t)]`; debe superar un margen económico congelado prospectivamente `delta_j >= 0`, en el mismo intervalo de retorno. Exigir además rendimiento neto superior a la alternativa accesible de efectivo USD por su margen congelado. El protocolo central especifica inferencia, reglas conjuntas y multiplicidad de C1, C3-I y C3-X. Media aritmética, patrimonio compuesto y riesgo son distintos; anualizar no debe cambiar la unidad inferencial ni ocultar insolvencia.

La **propuesta de especificación de investigación** inicial es una comparación spot long/flat financiada íntegramente, un horizonte admitido `H`, una regla de universo point-in-time y un escenario primario de ejecución/capital. No es una preferencia operativa del usuario ni una restricción permanente de producto/frecuencia. Otro producto u horizonte justificado puede reemplazarla **antes** de la admisión; necesita contabilidad y presupuesto propios. Otros capitales y escenarios de ejecución serán sensibilidades preespecificadas, no oportunidades adicionales para elegir una ganadora.

Usar un calendario fijo de decisiones separadas por `H` y un **límite de salida programada fijo por ciclo**. La entrada sigue la disponibilidad/latencia real y solo se admite antes del límite de entrada congelado; de lo contrario, abstenerse. Una entrada tardía no desplaza la salida a entrada+H. Las etiquetas abarcan el intervalo ejecutable restante, cuya duración puede variar. Observación y controles de riesgo/datos conservan relojes separados. Salidas fallidas/parciales necesitan política congelada de mantenimiento/exposición y conciliación: separar decisiones no garantiza posiciones, etiquetas o capital sin solapamiento. No afirmar ausencia de solapamiento hasta comprobar los intervalos efectivos; aplicar purga y capacidad a esos intervalos. Un mecanismo con posiciones solapadas o salidas condicionadas debe especificar propiedad y capital antes de admitirse, sin reutilizar silenciosamente esta construcción inicial.

En cada decisión elegible, el peso potencial del activo será `1/N_t`, donde `N_t` es el tamaño del universo causalmente elegible, no una cuota fija de monedas. Una decisión larga positiva utiliza ese peso; una decisión inactiva conserva su asignación en el vehículo de efectivo declarado. Nunca renormalizar únicamente activos rentables/activos después de observar resultados. El turnover incluye cambios de universo y deriva por precios; las órdenes solo se ejecutan después de disponer de información y transcurrir toda la latencia. Un universo sin activos elegibles sigue la política congelada de mercado no disponible. Las posiciones persistentes durante fallos o bajas no se valoran ni cierran a precios ejecutables inventados.

Transformaciones, escalado, ajustes, selección y escalado de referencias usan solo la ventana de entrenamiento vigente. Los pesos negociados proceden de la regla congelada, no de volatilidad o exposición media fuera de muestra. Las restricciones de capital/exposición/riesgo son escenarios prospectivos de investigación, no límites personales de pérdidas aceptados.

## 3. Referencias y reglas deterministas

| ID | Regla prospectiva | Finalidad / límite |
|---|---|---|
| R0 | Vehículo accesible de efectivo USD declarado, con devengo, custodia y costes documentados; devengo nominal cero será un escenario separado explícito cuando proceda | Obstáculo económico obligatorio; USDT/USDC no equivalen silenciosamente a efectivo USD |
| R1 | Cesta pasiva plenamente invertida `1/N_t` del universo elegible, con la misma regla de reconstitución y costes | Referencia de exposición pasiva; informar buy and hold de instrumentos fijos descriptivamente cuando corresponda, sin seleccionar supervivientes |
| R2 | Exposición pasiva R1 multiplicada por la exposición bruta media de la regla C1 seleccionada, **estimada en entrenamiento**; resto en R0 | Detecta mejoras debidas solo a menor exposición. No garantiza igual volatilidad/beta futuras; informar sus diferencias |
| R3 | Reversión temporal sencilla: largo si el retorno logarítmico USD pasado en `L1` es negativo; si no, efectivo; señal cero implica efectivo | Control con signo opuesto; no selección o ajuste independiente de H-02 |
| C1-L1 / C1-L2 | Largo si el retorno logarítmico USD pasado en cada lookback admitido es positivo; si no, efectivo; cero implica efectivo | Dos memorias de persistencia distintas y justificadas, sin umbral de señal optimizado ni política de volatilidad añadida |
| C2-V | Aplicar a R1 una regla causal de exposición inversa a volatilidad, con suelo y límite, antes de planificar órdenes | Pregunta secundaria de riesgo sobre base fija, independientemente de que C1 gane |
| C2-F | Exposición pasiva R1 constante igual a la exposición bruta media de C2-V en entrenamiento, resto en R0 | Control de mantener simplemente menos riesgo; sin equiparar con datos de test |

`L1`, `L2`, `H`, calendario de reconstitución y constantes de volatilidad necesitan valores concretos y razones en el manifiesto de admisión antes de evaluar con datos. Dos lookbacks son una comparación local finita de memoria, no evidencia de que dos sean óptimos ni exclusión perpetua de otras escalas. La evidencia en días/semanas puede motivar un horizonte inicial; no rellena timestamps ausentes ni identifica el valor mejor.

La referencia primaria de C1 es R2; R0 constituye la condición económica absoluta. R1 y R3 se informan obligatoriamente como contexto, sin convertirse en benchmarks primarios intercambiables elegidos tras ver resultados. Restricciones de riesgo y diagnósticos de factores/exposición impiden llamar habilidad temporal a mayor palanca/beta. Precisar cuándo una mejora neta satisface el contraste económico elegido pero no demuestra alpha estructural o ajustado por factores.

Para C2-V, usar `w_t = min(w_cap, sigma_target / max(sigma_hat_t, sigma_floor))`, con `sigma_hat_t` calculada desde la memoria fija y retornos disponibles; `w_cap <= 1` en este escenario financiado íntegramente. El estimador inicial es volatilidad realizada muestral, no varianza inversa ni una familia GARCH. Congelar unidades, ventana, tratamiento de historia insuficiente, suelo, objetivo, límite y rebalanceo. Un límite no elimina pérdidas por saltos.

El endpoint secundario de C2 es la reducción del funcional de riesgo de pérdidas registrado frente a C2-F, junto con un margen preespecificado de no inferioridad de retorno neto y todas las métricas obligatorias de riesgo/coste. Congelar funcional, convención de cola/objetivo, incertidumbre y oportunidad perdida admisible antes de evaluar. Menor drawdown aislado o menos tiempo invertido no permiten promoción. C2 no crea una afirmación confirmada de alpha ni otro presupuesto confirmatorio; observaciones efectivas de cola insuficientes producen evidencia de riesgo inconcluyente.

## 4. Escalera de comparación C3 y transformaciones

Los inputs iniciales constan de tres bloques **del propio activo**, definidos una sola vez, con observaciones completas disponibles por primera vez:

- **P — precio:** retorno logarítmico USD pasado en `L1`.
- **V — actividad:** logaritmo del cociente entre nocional USD negociado del último ciclo de decisión completo y su referencia pasada compatible con entrenamiento en `L2`. Nocional cero o ausente sigue la política congelada de validez; no ajustar un epsilon arbitrario para rescatar resultados. Volumen negociado no es profundidad, desequilibrio de órdenes ni flujo informado.
- **Q — volatilidad:** volatilidad realizada de retornos en `L2`, calculada con el intervalo de observación admitido; no una medida contemporánea del periodo futuro.

Agregación exacta, conversiones de tokens/cotización, mínimo de observaciones válidas, denominadores y estimador de referencia se fijan en el manifiesto. No optimizar varias definiciones bajo un mismo nombre de variable. Funding, on-chain, noticias y otros activos no entran automáticamente. Un input no tiene que ser rentable o significativo individualmente; tiempos/semántica inválidos sí justifican excluirlo, no un P&L univariante desfavorable.

Ajustar un modelo agrupado de coeficientes compartidos sobre el panel histórico elegible, con peso total uno por fecha y pesos condicionales iguales entre activos elegibles. No introducir ID del activo, universo obtenido de listados actuales ni retorno de otros activos de la fecha objetivo. Compartir observaciones pasadas de entrenamiento comparte información de estimación; los predictores rezagados de otras monedas de C4 son otra pregunta. Partir y remuestrear fechas completas conjuntamente entre activos.

El target `y(i,t)` es retorno futuro USD en exceso del efectivo declarado durante el resto ejecutable del ciclo programado, desde la primera entrada elegible tras disponibilidad/latencia hasta el límite fijo de salida; `H` separa decisiones, no añade otro periodo de mantenimiento después de entrar tarde. Las salidas no ejecutadas siguen la política congelada de conciliación/validez de etiquetas. La etiqueta no captura un movimiento anterior a recibir la señal. Las predicciones son salidas estadísticas; la simulación económica modela por separado cotizaciones, restricciones, fills, costes y efectivo. No descontar dos veces una fricción redefiniendo la etiqueta y restándola además del ledger.

Antes de cada ajuste, centrar/escalar inputs válidos con estadísticas exclusivas del entrenamiento. Especificar varianza cero y comportamiento fuera del soporte; la regla inicial no incluye winsorización ni imputación elegidas por resultados. Ajustar efectos principales con bases finitas de splines cúbicos naturales, cuartiles del entrenamiento como nudos interiores, límites del rango de entrenamiento y continuación exterior explícita. Reducir determinísticamente bases de rango deficiente y registrarlo. Centrar las bases en entrenamiento; estandarizar columnas penalizadas con estadísticas de entrenamiento, sin penalizar el intercepto. Fijar paquete/solver/convención de base exactos antes de implementar.

| Paso | Modelo / información | Qué identifica |
|---|---|---|
| S-P, S-V, S-Q | Un bloque por vez, modelo univariante aditivo no lineal, cada uno con las mismas dos penalizaciones positivas | Controles individuales de información; sin filtro de rentabilidad marginal |
| J-L | Modelo lineal regularizado conjunto P,V,Q | Referencia combinada simple; no se presupone superioridad no lineal |
| J-A | Aditivo no lineal regularizado `a + fP(P) + fV(V) + fQ(Q)` | Procedimiento combinado primario para C3-I y referencia de C3-X |
| J-X | Misma base aditiva más **dos productos preespecificados**, `P*Q` y `P*V` estandarizados, con la misma convención de regularización | Persistencia condicionada a riesgo/actividad; sin búsqueda genérica de todas las parejas o interacciones profundas |
| A-minus-P / V / Q | Reajustar J-X eliminando el bloque y toda interacción que lo contenga; repetir entrenamiento/selección con lo restante | Contribución por ablación; poner a cero un input de un modelo ya ajustado o usar importancia/SHAP no sustituye reajustar |

Ajustar regresión de error cuadrático penalizado. Congelar dos penalizaciones positivas, normalización de objetivo y tolerancias numéricas antes de evaluar financieramente; compartirlas entre controles correspondientes y J-A/J-X. Igual número de alternativas no iguala capacidad: registrar grados efectivos de libertad y cómputo. Los nudos por cuantiles son una decisión de ingeniería previa para un comparador suave pequeño, no arquitectura cripto óptima observada. No probar otras cantidades de nudos, penalizaciones, escaladores, pérdidas o listas de productos fuera del registro.

Todas las predicciones utilizan el mismo mapa congelado hacia posiciones, incluidos entrada/salida/no negociar, previsión de costes, límite de riesgo/capital y demora. Propuesta inicial: en cada ciclo, largo si el exceso de retorno previsto supera la previsión prospectiva del coste round-trip más el obstáculo de entrada; si no, efectivo. El obstáculo deriva de la política económica/de costes antes de resultados, sin buscar un umbral de probabilidad. C3 usa un mapa idéntico; mantener una posición tiene costes distintos de abrirla y debe tratarse expresamente en ese mapa. Si el mapa de ciclos simple no es económicamente apropiado, modificarlo antes del lanzamiento y contabilizar la comparación en el presupuesto.

## 5. Selección, afirmaciones y resultados

Dentro de cada ventana de entrenamiento permitida, el walk-forward interno anidado selecciona solo alternativas registradas, maximizando la media del **retorno neto USD emparejado diferencial**, tras exigir las mismas reglas de datos, ejecución y riesgo. Congelar calendario interno, precisión del ranking y desempate. Empates: menor complejidad y después ID estable; sin preferencia informal por una técnica propuesta por el usuario. Una configuración que incumpla riesgo no puede ganar por rentabilidad. La validación exterior evalúa el procedimiento completo congelado de selección/reajuste y no permite retocarlo. Para seleccionar cada penalización/bloque C3, la referencia interna es la misma política de efectivo R0 sobre el mismo calendario de evaluación interna; las afirmaciones conjunto-versus-individual e interacción-versus-aditivo se evalúan en los bloques externos/reservados. En C1, cada lookback se compara con su propio R2 del fold, calibrado exclusivamente en el entrenamiento interno. Ni exposición del bloque de evaluación interno ni exposición externa/final calibran comparadores; C2-F sigue la misma regla de entrenamiento.

- **C1:** seleccionar L1 o L2 en entrenamiento; construir R2 desde la exposición de entrenamiento de la regla seleccionada. Contrastar incremento frente a R2 y la condición separada de efectivo.
- **C3-I:** seleccionar penalización de J-A en entrenamiento; seleccionar el mejor procedimiento individual elegible S-P/S-V/S-Q en entrenamiento. Comparar políticas congeladas sobre las mismas fechas, efectivo/ejecución y límites de riesgo. Seleccionar la referencia individual forma parte del procedimiento y presupuesto; nunca escoger el comparador más fácil en el conjunto final.
- **C3-X:** comparar J-X y J-A seleccionados en entrenamiento con idénticos inputs, fechas, relojes, mapa de posiciones y oportunidad de búsqueda entre dos penalizaciones. Puede contrastarse C3-X aunque C3-I sea inconcluyente: un efecto condicional puro no necesita señales marginales rentables. Cada afirmación económica conserva la condición frente a efectivo.

Para cada afirmación primaria, la nula es **incremento no superior al margen económico registrado O incapacidad para superar el margen registrado frente a efectivo**. Deben superarse ambos componentes; el protocolo central usa el máximo p-value de la unión-intersección y después Holm entre las tres afirmaciones. Informar intervalos e incertidumbre, no solo aprobado/rechazado. Las diferencias de pérdida predictiva son estimandos diagnósticos secundarios; un MSE menor no prueba mejora económica.

C3-I favorable / C3-X desfavorable respalda un procedimiento combinado más sencillo, no superioridad de interacciones. C3-X favorable ofrece evidencia condicional sobre la clase funcional y política ejecutora probadas, no causalidad ni generalización de todas las interacciones. Si las políticas combinadas siguen siendo económicamente negativas, una mejora predictiva o relativa no justifica desplegarlas. Conservar resultados negativos/inconcluyentes aunque otra rama funcione.

Distinguir combinación de **inputs** de diversificación del **P&L de estrategias**. Con pesos fijos no negativos que suman uno y costes aditivos, estrategias cuyas medias netas verdaderas sean todas negativas conservan media ponderada negativa. Predictores condicionales, políticas variables, neteo y capital compartido cambian la pregunta y requieren hipótesis y contabilidad propias. Nada de eso se infiere de esta comparación C3.

## 6. Presupuesto finito y parada

La primera tanda tiene **26 plazas de configuraciones base únicas**, para un horizonte/universo/escenario primario de ejecución-capital admitidos:

| Grupo | Cantidad | Enumeración |
|---|---:|---|
| Referencias deterministas y reglas C1/C2 | 8 | R0, R1, R2, R3, C1-L1, C1-L2, C2-V, C2-F |
| Bloques individuales C3 | 6 | S-P/S-V/S-Q × dos penalizaciones |
| Modelos conjuntos lineal/aditivo/interacción | 6 | J-L/J-A/J-X × dos penalizaciones |
| Ablaciones reajustadas por bloques | 6 | Tres omisiones × dos penalizaciones |
| **Total** | **26** | Diseño inicial finito, no 26 pruebas independientes ni probabilidad de éxito |

Este límite deriva de comparadores y ablaciones necesarios, no de resultados optimizados. **No** limita el total de ajustes hasta enumerar folds externos/internos, ajuste final, semillas, escenarios y sensibilidades. El manifiesto debe calcular el total de ajustes/evaluaciones previstos y presupuesto de CPU/tiempo/almacenamiento antes de comenzar. Las semillas son controles deterministas de ingeniería; no se elige una favorable. El bootstrap inferencial tiene presupuesto separado en el protocolo central.

Contar cada alternativa manual, preprocesamiento, horizonte/universo descartado, ajuste fallido y enmienda. Reintentos idénticos por fallos de infraestructura conservan intentos; cambios informados por datos son variantes nuevas. Estrés diagnóstico y ventanas vecinas deben nombrarse y acotarse antes de resultados, sin reemplazar el escenario primario. Informar sus fallos; no elegir el estrés bajo el cual sobrevive una candidata.

Detener una rama por datos point-in-time inutilizables, ejecución/margen inaccesibles, inferencia inválida, recursos agotados o incumplimiento de condiciones económicas/riesgo congeladas. Un fallo de datos implica no evaluable; evidencia adversa válida indica soporte insuficiente para la construcción probada. Ninguno demuestra imposible toda la familia. No añadir boosting, una red, otro horizonte o universo para rescatar el resultado final. Una enmienda material necesita nueva versión prospectiva, presupuesto y tratamiento independiente de evaluación.

## 7. Comparaciones reservadas y dependencias de lanzamiento

La escalera futura de C4 es pasado propio → pasado propio más factores comunes → misma información más bloques retardados preespecificados de otros activos. Estimar cargas, universo, retardos y grafos dentro del entrenamiento; excluir contaminación del objetivo y precios obsoletos, sincronizar fechas y contrastar demora ejecutable. No enumerar todas las parejas dirigidas. Su nula separa incremento predictivo y económico neto. Promoverla exige sustitución o protocolo adicional acotado; no hereda automáticamente plazas C3 no utilizadas.

C5 necesita precios de contratos spot/derivados, funding conocido entonces, liquidaciones contractuales, todas las garantías/reservas/préstamos, rendimiento accesible del efectivo, restricciones de transferencias y margen/liquidación. Comparar retorno de cuenta USD sobre **todo el capital comprometido**, no sobre una pata o margen aportado solamente. Una previsión de funding no es la tasa finalmente liquidada, y la basis de futuros no tiene por qué converger al salir. Ambas patas, inversiones de funding, estrés de saltos/margen y concentración de contraparte deben modelarse antes de admitirla. Este protocolo y el acceso para investigar no autorizan apalancamiento ni operar derivados.

Antes de solicitar un alcance ejecutable de V, resolver y congelar: producto/fuente/universo y cobertura; `H/L1/L2` y relojes; particiones y periodo final exactos; definiciones precio/volumen/volatilidad; dos penalizaciones y convención de splines/solver; mapa de predicción a posición; endpoint/constantes de C2 y margen de no inferioridad; límites de exposición de investigación; efectivo USD/conversiones; tarifas/fills/demora/capacidad completos; márgenes económicos; presupuesto íntegro de ajustes/sensibilidades; validación técnica del motor/contabilidad; IDs/hashes del manifiesto y responsables de aprobación. Campos sin resolver bloquean ejecución. Capital real, venue definitivo de producción y drawdown personal pueden seguir separados hasta el trabajo que dependa de ellos.

Aquí no se inventan fechas, tarifas, umbrales rentables ni un proveedor aprobado. Es un diseño comparativo desarrollado con dependencias de concreción explícitas, no un preregistro financiero sellado ni permiso para ejecutarlo.
