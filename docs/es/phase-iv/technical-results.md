# M, R y E — admisión técnica ejecutada

**Actualización de recuperación, 2026-11-02:** D-048/D-049 registra ejecución efectiva de Nautilus con Python 3.13.16 estándar, casos adversos/parciales y diagnóstico finito de consumo. Consultar el [nuevo informe](engine-recovery.md). El texto fechado siguiente conserva la entrega original `00131bc`; M/R y LEAN no se repitieron.

Documento: IV-TECH-RESULT-001 · Versión: 1 · Fecha: 2026-11-01 · Traducción del [original inglés](../../en/phase-iv/technical-results.md).

La autoridad es la [aprobación expresa de ejecución](../../phase-iv/APPROVAL-M-R-E.es.md) del alcance exacto de `fa435a4`, registrada en D-046. Las propuestas conservan su redacción histórica; este informe registra lo ejecutado. No implica migrar producción, experimentos financieros, nuevos datos de mercado, Fase V ni operativa prospectiva. E3/E4 siguen pendientes.

## M — compatibilidad demostrada en el ámbito de almacenamiento probado

Las dos copias desechables usan aplicación/pruebas de `fa435a4`, Python **3.12.14**, uv **0.12.23** y DuckDB **1.5.6**. Una resolución offline de la candidata cambió **únicamente PyArrow 23.0.1 → 26.0.0** entre las 37 entradas del lock. Tamaño y SHA256 del wheel coinciden con los metadatos aprobados. Los entornos aislados reutilizaron copias del cache; producción no fue el directorio de ejecución de las pruebas.

| Comprobación ejecutada | Resultado | Interpretación |
|---|---|---|
| Tres packs × dos escritores × dos lectores | **12/12 pasan** | Valores y metadatos Parquet/IPC y proyecciones DuckDB cumplen sus invariantes |
| Digest corrupto, partición reservada y etiqueta de datos reales en ambos entornos | **6/6 pasan** | Los controles existentes rechazan los objetos prohibidos |
| SIGKILL del escritor antes de publicación atómica, ambos entornos | **2/2 pasan** | No se admite salida parcial y el artefacto original sobrevive a ese punto de interrupción |
| Suite backend existente, control | **110 pasan**, sin omisiones/fallos | Una invocación |
| Suite backend existente, candidata | **110 pasan**, sin omisiones/fallos | Una invocación |
| Coherencia de dependencias | Ambas pasan | Ninguna otra versión cambia |
| Artefactos sintéticos locales anteriores elegibles | **Ausentes; cero lecturas opcionales** | Inventario vacío; no equivale a lectura fallida ni a comprobar archivos históricos |

No fue necesario corregir/repetir casos. Ambas suites conservan la misma advertencia de deprecación Starlette/httpx. La [evidencia M](../../phase-iv/technical-results/M/) conserva locks, comandos, expectativas congeladas, logs y resultados individuales.

Los packs son la receta sintética v1 existente de 120 filas/semilla 42, 32 filas de límites y 32 eventos de precisión. La referencia v1 procede del control: comprueba compatibilidad, no demuestra independientemente la corrección científica del generador. Las expectativas de límites/precisión se especificaron independientemente.

**Observación adversa conservada:** la conversión de timestamps con zona de DuckDB pierde nanosegundos en los cuatro cruces escritor/lector. El caso pasa porque detecta esa pérdida y exige conservar valores por la ruta canónica de ticks enteros; no declara seguras todas las representaciones temporales de DuckDB. Mantener ticks, unidades y disponibilidad explícitos en la futura interfaz.

Los resultados respaldan Arrow 26 como **candidata de migración técnicamente viable** para esta versión. No ejecutan ni autorizan migración, certifican archivos antiguos ausentes, prueban fallos eléctricos/transacciones del catálogo ni recuperación de órdenes/motor. Nautilus v2 no exige Arrow, por lo que el motor no justifica precipitar este cambio independiente.

## R — prototipo causal ejecutado; equivalencia del proveedor sin probar

**160/160 ejecuciones iniciales pasan**, sin repetir casos: ocho diarios fijos, cinco rutas (lotes 1/7/64, reproducción e inyección que simula directo), cada una completa y con tres prefijos. El oráculo independiente por evento, hashes y TZif exacto de New_York se conservan en la [evidencia y revisión R](../../phase-iv/technical-results/R/REVIEW.md).

Los diarios cubren velas cerradas retrasadas, sesiones/DST, operaciones y eventos tardíos/corregidos, precisión, huecos/duplicados/recuperación, conversión causal, orden de evento/disponibilidad y restauración del estado de transformación. Comparan información admitida y decisiones, impiden contaminación de prefijos por información futura y conservan estados indisponibles/bloqueados. No comparan fills simulados con ejecución real.

El alcance es estrecho: agregación de operaciones de un instrumento e intervalos fijos; la combinación de entradas es una conversión fija, no un motor genérico entre mercados. No hay validación del vínculo de una revisión con su versión anterior. R8 restaura estado de transformación en memoria; **no** prueba interrupción de procesos E5, conciliación persistente del venue ni recuperación nativa del motor. La equivalencia histórico/directo real sigue necesitando una prueba específica de fuente autorizada por separado.

Dos sondeos iniciales de aislamiento fallaron antes de su carga prevista al no estar disponible Landlock. Un sondeo independiente sí comprobó denegación de sockets IPv4/IPv6. La primera invocación R omitió el argumento de fixtures y terminó antes de ejecutar casos; el comando corregido ejecutó después los 160 casos una vez. Se conservan los logs originales. Los fallos de preparación no se borran, cuentan como casos aprobados ni se presentan como ciclo correctivo de casos consumido.

## E — ejecución parcial; ningún motor admitido

**E no está completado: 3 casos de componentes ejecutados, 23 slots sin ejecutar y cero casos plenamente admitidos.** Las instalaciones se intentaron realmente. No es una comparación terminada entre dos motores. Los [recibos y estados de cada caso E](../../phase-iv/technical-results/E/README.md) distinguen no ejecutado, fallo y aprobado.

| Candidato / trabajo realizado | Resultado | Consecuencia |
|---|---|---|
| Nautilus 2.0.0rc7, Python 3.13.18 mediante uv 0.12.23 | Distribución no disponible; el intento real devuelve `No download found`.13 casos sin ejecutar | Bloqueo de instalación, no evidencia de comportamiento incorrecto. Sin sustituir versiones |
| LEAN commit 22404ea28; SDK 10.0.403 | SDK verificado; adquisición parcial sin cuerpos de datos financieros; restauración, restauración offline con lock y compilación offline satisfactorias | Compatibilidad de compilación de ese grafo, no admisión financiera |
| LEAN E1 | Coincide el ejemplo reducido de decisiones; **evidencia parcial del harness/componentes**, sin admisión completa | Disponibilidad controlada por el harness. Faltan canarios R1/R3/R7, prefijos y ejecución del rechazo de precisión no soportada |
| LEAN E2 | Compra nativa de 2 a 100, comisión 0,4 y saldo USD 799,6/SYN 2 concilian. Venta limitada requerida de 1 a 102 sigue abierta | **Falla la comparación obligatoria**: el modelo exige cruce y la fixture solo toca 102 |
| LEAN E3-L1 | Orden de mercado nativa ejecuta 4 a 100 pese a cantidad visible de venta 1; comisión 0,8 | **Falla la comparación de liquidez visible finita**; la ejecución total no queda limitada por el tamaño L1 suministrado |
| Resto LEAN | E3-L2, E4, E5 referencia/tres cortes y cuatro pruebas de recursos **sin ejecutar** | El puente carece de consumo L2/IOC finito, identidades de broker/atribución compartida y conciliación del mismo diario; rendimiento requiere admisión funcional |

**Interpretación de los resultados adversos:** E2 no demuestra contabilidad incorrecta ni un defecto universal de LEAN. Tocar el precio no garantiza una ejecución maker sin información de cola/prioridad; la venta esperada es un supuesto de la fixture congelada y el modelo configurado no lo satisface. No se cambiaron precios, tolerancias ni expectativas después de observarlo. E3 demuestra un límite concreto del modelo predeterminado frente al requisito L1 conservador aprobado; no prueba que todos los modelos o integraciones futuras de LEAN sobre-ejecuten.

El worker invoca realmente `ImmediateFillModel`, `CoinbaseFeeModel` configurado y `SecurityPortfolioManager` nativos; no ejecuta el Launcher ni el ciclo completo del broker. Conserva fills/comisiones/caja nativos. Admisión de órdenes, caja disponible/libre/reservada, programación, identidades de observación y etiquetas maker/taker indican expresamente su origen en el harness. No prueban rechazo nativo, idempotencia, asignación multibot ni recuperación. No se sustituyeron fills por resultados esperados ni se escribió otro modelo de ejecución.

La cobertura incompleta de E1 es una **carencia del harness**, no un fallo causal nativo observado. Los canarios R originales incluyen tiempos inferiores a 100 ns; la interfaz DateTime de LEAN no puede representarlos silenciosamente. Su rechazo explícito sigue sin ejecutarse. E5 es también una necesidad de integración/conciliación sin demostrar, no evidencia de que el motor nunca pueda recuperarse. Se conservan esas exigencias pendientes sin eliminarlas para declarar éxito.

La primera restauración .NET falló antes de transferir paquetes: su mutex intentaba usar un directorio de usuario de solo lectura. `XDG_RUNTIME_DIR`/`XDG_DATA_HOME` aislados resolvieron la configuración sin cambiar HOME, SDK, fuente upstream ni producción. Se conservan fallo original y una corrección de configuración. La compilación upstream registró4.046 advertencias y cero errores; se conservan junto con la desactivación de la auditoría NuGet en línea, sin declarar ausencia de vulnerabilidades. No se repitieron casos del motor ni se relajaron supuestos del modelo.

## Recomendación y siguientes decisiones materiales

1. **Mantener las dependencias actuales en producción.** M respalda técnicamente una migración exacta a Arrow 26, pero es opcional y necesita autorización separada; no resuelve el Python de Nautilus. Conservar timestamps enteros.
2. **Conservar R como especificación de conformidad futura.** Falta comprobar histórico/directo del proveedor concreto antes de confiar en él; este resultado no autoriza adquirir otros datos o feeds.
3. **No elegir motor financiero con esta comparación parcial.** Para retomar Nautilus, concretar una distribución Python administrada obtenible y su instalador en un cambio de versión acotado; no sustituir silenciosamente la ruta fijada. Para LEAN, decidir primero si interesa estudiar un modelo/puente adicional de liquidez finita, fuera del alcance de modelos existentes, o mantenerlo pospuesto. Deben resolverse las limitaciones observadas y la cobertura E1/E4/E5 antes de admitirlo. No hace falta otra revisión general de frameworks.

E3/E4 —presupuesto/capital/materialidad/riesgo— siguen sin evidencia financiera/de datos suficiente. No se proponen cifras arbitrarias. Estas pruebas no aportan rentabilidades de estrategias ni cierran IV incondicionalmente.

## Recursos, conservación y decisión pendiente

La [auditoría final de conservación](../../phase-iv/technical-results/preservation.json) no detecta cambios en 73 archivos registrados de software/configuración ni 4.630 archivos regulares del entorno estable, ni cambios científicos/de código protegidos. El baseline excluye destinos de enlaces simbólicos y estado privado de ejecución.

| Paquete | Tiempo activo instrumentado | Pico RSS muestreado | Espacio temporal actual | Transferencia contabilizada |
|---|---:|---:|---:|---:|
| M |43,50s|250,50MiB|1,16GiB|51,43MiB|
| R |0,65s|12,63MiB|0,21MiB|0|
| E |154,31s|1,56GiB|1,16GiB|264,84MiB|
| Conjunto, secuencial |**198,46s**|**1,56GiB** máximo|**2,32GiB**|**316,27MiB**|

Los [recibos exactos](../../phase-iv/technical-results/resources.json) incluyen intentos de preparación fallidos y casos. El muestreo puede omitir picos breves; el máximo propio del proceso R es 14,50MiB. Disco es observación actual/postcomando, no certificación continua de máximo. Git/NuGet contabiliza bytes TLS bidireccionales de manera conservadora; las descargas internas cuentan su tiempo una sola vez. No hubo parada por recursos. Estas cifras excluyen preparación/revisión sin medir y días interrumpidos por créditos; no representan coste o duración total de la investigación. No se contrataron servicios.

**Leer resultados, no solo códigos de salida:** workers/supervisores E2/E3 devolvieron 0 al recoger observaciones; `status`, `problems` y `full_case_admitted=false` registran los contrastes fallidos.

Los recibos de recursos y el estado conjunto se reúnen en el [checkpoint de ejecución](../../phase-iv/technical-results/PROGRESS.md). Un bloqueo serializa los paquetes. Afinidad CPU y vigilantes muestreados de RAM/disco acotan el trabajo; sus mediciones no equivalen a picos garantizados por kernel ni certifican aislamiento ante código hostil. El host no permitió el aislamiento anidado del sistema de archivos. Copias desechables y auditoría final de hashes acreditan conservación, no imposibilidad de escribir producción impuesta por el SO.

Se conservan hipótesis, E1/E2, 26 especificaciones, T/D/U/V/F, aceptación original, negativos A/B y UX futura. Siete contadores financieros en cero. Las pruebas técnicas no determinan el presupuesto financiero E3 ni las decisiones de capital/materialidad/riesgo E4.
