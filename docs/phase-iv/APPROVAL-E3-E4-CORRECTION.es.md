Recibida: 2026-11-02 (Europe/Madrid). Base: `a3ec18f`. D-050. Texto del usuario; evidencia externa no equivale a ejecución del proyecto.

---

# AUTORIZACIÓN DE EJECUCIÓN — CORRECCIÓN ACOTADA E3-L2 Y E4

He revisado los resultados del commit `a3ec18f` y una reproducción técnica externa adicional de NautilusTrader 2.0.0rc7.

La evidencia externa aporta tres observaciones útiles:

1. Al proporcionar una cotización causal derivada del mismo snapshot L2, Nautilus puede ejecutar órdenes de mercado utilizando la profundidad del libro.
2. Una compra de 6 unidades con solo 4 disponibles puede ejecutar las 4 unidades y mantener las 2 restantes en estado `PARTIALLY_FILLED`, pendientes de ejecución posterior.
3. Reenviar directamente un `client_order_id` previamente utilizado puede generar incoherencias entre la orden almacenada, sus fills y la posición.

Estas observaciones son pistas de diagnóstico obtenidas en otro entorno, con otros instrumentos y fixtures. No constituyen evidencia oficial de bot_trader.

**Autorizo expresamente ejecutar una intervención técnica acotada sobre E3-L2 y E4. Esta autorización sustituye los encargos anteriores relativos a la corrección de estos dos bloqueos. No necesitas presentar otra propuesta ni solicitar nueva autorización dentro del alcance indicado.**

El objetivo es resolver las incertidumbres materiales que impiden decidir qué infraestructura utilizar para nuestra primera investigación financiera offline, evitando repetir trabajo y consumir recursos innecesariamente.

## 1. E3-L2 — Referencia de precio y profundidad

Investiga por qué Nautilus rechaza las órdenes de mercado con `MARKET_PRICE_UNAVAILABLE` cuando el libro L2 contiene bid, ask y profundidad válidos.

Si las interfaces de Nautilus 2.0.0rc7 lo permiten, implementa la alimentación mínima de una cotización de referencia derivada exclusivamente del mismo snapshot L2.

Condiciones:

- Utiliza únicamente los mejores bid y ask presentes en el snapshot.
- Conserva timestamps, orden temporal, disponibilidad y procedencia.
- Registra la transformación aplicada y su hash.
- No introduzcas información futura, precios externos, nuevas cantidades ni liquidez artificial.
- No desactives las comprobaciones de riesgo para conseguir que la orden sea aceptada.
- No alteres los fixtures originales ni sus expectativas congeladas.
- Conserva las observaciones anteriores y diferencia los resultados posteriores a la corrección.

Ejecuta prioritariamente el fixture E3-L2 original con esta alimentación corregida.

Comprueba el consumo nativo de los niveles de precio y cantidad, las comisiones, las órdenes pendientes y el capital reservado.

### Profundidad insuficiente y órdenes parcialmente ejecutadas

Realiza un diagnóstico adicional con los mismos principios causales:

- Compra de 4 unidades frente a una profundidad de 4.
- Compra de 6 unidades frente a una profundidad de 4.
- Identifica qué unidades se ejecutan, sus precios y las comisiones correspondientes.
- Comprueba qué ocurre con las 2 unidades restantes.
- Verifica si el remanente continúa abierto, se cancela o puede ejecutarse posteriormente.
- Comprueba cuánto capital permanece reservado y si se libera correctamente después de una cancelación.

Cuando corresponda, examina si la versión y el tipo de orden soportan políticas IOC/FOK o una cancelación explícita del supervisor.

**No transformes retrospectivamente la orden original en IOC/FOK para declarar superado el fixture congelado.** Las políticas alternativas son diagnósticos separados y deben conservar sus propias identidades y resultados.

Si un remanente abierto es el comportamiento legítimo de la orden, documenta cómo debe representarse y gestionarse; no lo clasifiques automáticamente como defecto del motor.

Si resulta necesario comparar la cotización derivada del snapshot L2 con una variante basada en `TradeTick`, hazlo únicamente cuando aporte información discriminante y queden recursos disponibles.

No presupongas equivalencia entre variantes si no tienen exactamente la misma información y secuencia disponible. Esta comparación tiene prioridad baja.

## 2. E4 — Idempotencia, órdenes, fills y reservas

Investiga la incoherencia observada al reenviar una orden con el mismo `client_order_id`: la posición conserva unidades ejecutadas, pero el estado almacenado de la orden pierde información y permanece capital reservado.

Reutiliza los registros anteriores para identificar la causa. No repitas el fallo nativo únicamente para volver a observarlo.

Distingue explícitamente:

- Comportamiento del motor ante un uso incorrecto de su interfaz.
- Responsabilidad del supervisor al identificar comandos duplicados.
- Estado de la caché y ciclo de vida de las órdenes.
- Conservación de fills, posiciones y comisiones.
- Liberación o mantenimiento justificado de reservas.

### Protección mínima del supervisor

Implementa, si resulta suficiente, una frontera de idempotencia que impida enviar dos veces una orden con la misma identidad lógica.

La protección debe:

- Detectar comandos procesados y pendientes.
- Conservar el resultado y estado de la solicitud original.
- Evitar la sustitución o sobrescritura de una orden previamente ejecutada.
- Mantener la correspondencia entre comando, orden, fills y posición.
- Evitar duplicaciones de reservas, efectivo utilizado y comisiones.
- Conservar la información necesaria para reproducir correctamente el estado después de una reconstrucción offline.

No basta con rechazar un duplicado si desaparece o queda incoherente la información de la primera ejecución.

### Deduplicación de fills

Está expresamente permitido generar o reinyectar eventos sintéticos duplicados **en la capa de consolidación del supervisor** para verificar idempotencia.

No se permite inyectar fills artificiales dentro del motor y presentarlos como ejecuciones nativas.

Comprueba separadamente:

1. Reentrega de un fill con el mismo identificador: no debe producir dos efectos contables.
2. Dos fills legítimos con identificadores distintos, aunque tengan el mismo precio y cantidad: ambos deben conservarse.
3. Consistencia de comisiones, efectivo, inventario y posiciones.
4. Coherencia entre órdenes terminales, órdenes pendientes y reservas asociadas.

Clasifica qué garantías aporta Nautilus de forma nativa y cuáles proporciona nuestro puente de integración.

No atribuyas al motor una protección que solo hemos implementado en el supervisor.

## 3. Política de corrección del harness

Quiero conservar el rigor metodológico sin que los defectos técnicos del banco de pruebas bloqueen indefinidamente el trabajo.

Permanecen inmutables:

- Los fixtures originales y sus identidades.
- Las expectativas y criterios de aceptación congelados.
- Los resultados adversos ya observados.
- Los requisitos científicos y económicos previamente aprobados.

Se permiten correcciones verificables de defectos demostrados del harness dentro de este alcance.

Cada corrección debe conservar:

- Diagnóstico concreto.
- Código anterior.
- Diff exacto.
- Justificación técnica.
- Código corregido.
- Resultados originales y posteriores.
- Pruebas de regresión relevantes.

Una corrección del harness que permite ejecutar correctamente una prueba no equivale a modificar su expectativa para obtener un resultado favorable.

Tampoco debe considerarse un pase automático del motor.

**Autorizo una corrección acotada por cada uno de los dos bloqueos identificados: alimentación L2 e idempotencia E4.** Si no bastan, documenta la limitación y detén esa ruta.

No interpretes esta autorización como permiso para realizar correcciones ilimitadas, modificar hipótesis o desarrollar modelos generales nuevos de ejecución.

## 4. Prioridad de ejecución y conservación de recursos

Dispones de un máximo de **12 nuevas ejecuciones**, no de una obligación de realizarlas todas.

Sigue este orden de prioridad:

1. **Fixture E3-L2 original**, corrigiendo únicamente la referencia de precio y comprobando las ejecuciones frente a la profundidad disponible.
2. **Orden de 6 unidades contra 4 disponibles**, analizando remanente, estado abierto, cancelación y reservas.
3. **Protección contra órdenes duplicadas**, comprobando que conserva el estado y resultado de la primera orden y la contabilidad correspondiente.
4. **Deduplicación de fills en el supervisor**, verificando identidades, comisiones, efectivo, inventario y reservas.

En segundo plano quedan las comprobaciones adicionales sobre IOC/FOK, variantes de cancelación y otras diferencias de configuración.

La comparación con `TradeTick` tiene la prioridad más baja y puede omitirse si no aporta evidencia decisiva.

Agrupa comprobaciones relacionadas cuando sea metodológicamente correcto, sin ocultar ejecuciones ni sobrescribir resultados.

### Límites autorizados

- Máximo **12 nuevas ejecuciones** de diagnóstico/prueba.
- Máximo **30 minutos adicionales de máquina activa**.
- Máximo **1 GiB adicional de almacenamiento temporal**.
- Máximo **4 vCPU y 8 GiB de RAM**.
- Ninguna descarga nueva de software o datos financieros.
- Ningún gasto o servicio contratado.

Reutiliza Python 3.13.16, NautilusTrader 2.0.0rc7, sus instalaciones, fixtures, cachés, manifiestos, logs y resultados existentes.

No repitas M, R, las pruebas concluyentes de LEAN ni las observaciones anteriores de Nautilus que ya aportaron evidencia suficiente.

No ejecutes E6 mientras sigan incumplidas condiciones funcionales obligatorias.

Si una ruta no puede completarse dentro de estos límites, conserva el resultado como pendiente o inconcluso. Continúa solamente con las comprobaciones independientes que permanezcan dentro del permiso.

## 5. E1 — Coherencia temporal todavía pendiente

Antes de recomendar Nautilus para investigación offline, revisa expresamente los requisitos de E1 que continúan sin demostrar.

En particular:

- Paridad temporal causal entre la entrada normalizada y las decisiones del motor.
- Precisión de timestamps y rechazo explícito de representaciones no soportadas.
- Disponibilidad efectiva de información.
- Orden reproducible de eventos.
- Ausencia de información futura en las decisiones.
- Correspondencia con los contratos temporales previamente comprobados en R.

No es necesario repetir las 160 comprobaciones R.

Determina qué propiedades pueden garantizarse mediante la frontera de datos/decisiones de bot_trader y cuáles requieren verificación adicional del motor.

Explica si las carencias pendientes bloquean realmente el uso propuesto para la primera investigación con velas o si pueden resolverse mediante un control técnico más acotado.

No declares una propiedad demostrada cuando únicamente esté documentada o inferida.

## 6. Separación entre investigación y operativa futura

Quiero distinguir claramente tres modalidades.

### A. Primera investigación financiera offline basada en velas

Determina qué necesitamos realmente para evaluar estrategias de momentum y señales relacionadas de baja frecuencia.

Analiza si un motor externo, nuestro ledger sintético acotado o una combinación de componentes podría cubrir los requisitos específicos.

No presupongas que el ledger propio está certificado como simulador financiero general.

La integridad contable, los costes, las transformaciones causales, la reproducibilidad y los supuestos de ejecución deben estar justificados.

### B. Investigación sensible a profundidad y microestructura

Determina si Nautilus con L2, después de las correcciones, resulta una opción técnicamente viable.

Distingue capacidad de consumir niveles de un libro sintético de realismo financiero con datos históricos.

Identifica qué datos y modelos adicionales serían necesarios cuando la estrategia dependa de profundidad, spread, liquidez, cola o ejecución rápida.

No impongas L2 universalmente para todas las estrategias.

### C. Futuro paper/live trading

Conserva para evaluación posterior los requisitos de:

- Conciliación con exchanges reales.
- Recuperación de órdenes desconocidas después de caídas.
- Idempotencia de envíos y ejecuciones.
- Persistencia operativa.
- Gestión de riesgos y bloqueo de operaciones inseguras.
- Atribución y reconciliación de capital compartido.

No implementes ahora toda la infraestructura de ejecución prospectiva para justificar una investigación offline.

La recuperación determinista del estado de investigación y la recuperación segura de órdenes reales son capacidades diferentes.

## 7. Decisión final y entrega

Ejecuta directamente las comprobaciones autorizadas, sin elaborar otra propuesta ejecutiva ni solicitar autorización adicional dentro del alcance definido.

Publica en GitHub los resultados nuevos y reproducibles, conservando el historial, los casos fallidos y los archivos originales.

Presenta un resumen ejecutivo que responda:

1. ¿Se ha resuelto E3-L2 y se ha demostrado el consumo de profundidad con una referencia de precio causal?
2. ¿Qué sucede con las órdenes parcialmente ejecutadas y sus reservas al agotarse la liquidez?
3. ¿Se ha resuelto E4 mediante una frontera de idempotencia sin perder fills ni alterar la contabilidad?
4. ¿Qué capacidades están demostradas de forma nativa y cuáles dependen del supervisor?
5. ¿Qué requisitos E1 siguen pendientes y cuáles bloquean la primera modalidad de investigación offline?
6. ¿Es Nautilus un candidato viable para la investigación offline con velas, con L2 o para ambas, bajo qué condiciones concretas?
7. Si Nautilus no es admisible para el primer laboratorio, ¿qué comprobaciones mínimas necesitaría una alternativa, incluido nuestro ledger acotado, sin asumirla automáticamente válida?
8. ¿Qué requisitos quedan reservados para una futura operación prospectiva?

**La recomendación debe estar fundamentada por modalidad de uso, no por popularidad o preferencias arquitectónicas.**

Si E3-L2 y E4 se resuelven, puedes recomendar Nautilus como candidato para un uso offline delimitado, siempre que el resto de requisitos obligatorios de ese uso estén satisfechos.

Si no se resuelven, no selecciones Nautilus por inercia ni declares automáticamente apto el ledger propio. Conserva el bloqueo correspondiente e identifica el mínimo siguiente paso.

No interpretes superar pruebas técnicas como autorización financiera.

## 8. Restricciones que permanecen vigentes

Mantén:

- Producción y sus dependencias intactas.
- E3/E4 económicos pendientes.
- E1/E2 científicos aprobados, sin modificaciones.
- Las 26 especificaciones experimentales originales.
- Las prioridades C1/C3, C2 y las reservas C4/C5.
- La admisión estadística T/D/U/V/F aprobada.
- La Fase IV abierta en sus condiciones pendientes.
- La Fase V sin autorización.
- Paper trading y trading real sin autorización.

No descargues nuevos datasets, no amplíes mercados, no añadas estrategias ni contrates servicios.

**El objetivo de esta intervención es cerrar E3-L2 y E4 con el mínimo trabajo necesario, identificar una ruta defendible hacia la primera investigación financiera y evitar que la selección del motor se convierta en un proyecto interminable. Puedes comenzar directamente.**