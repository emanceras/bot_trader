# Autorización E1 y contrato causal con velas — D-052

Solicitud del usuario posterior a `c1d4029`, registrada el 2026-11-03. Este documento es un resumen del alcance, no una transcripción literal. Las observaciones externas son motivos de comprobación, no resultados del proyecto.

Se autoriza ejecutar directamente en el entorno existente CPython3.13.16/NautilusTrader2.0.0rc7:

- Fixture N con cierre100.50 y N+1 con apertura110.00: ejecución nativa sin latencia, ordenación adaptativa, latencia positiva y su combinación.
- Canario prioritario de vela etiquetada por apertura: `ts_init` incorrecto frente a disponibilidad al cierre; etiqueta de cierre sin sumar dos veces el intervalo; unidades y precisión sin pérdidas silenciosas.
- Alternativa `bar_execution=False` con señal retenida y evento posterior elegible. Una cotización derivada de la apertura es una hipótesis sintética con spread versionado, nunca bid/ask observado ni precio garantizado. Si la apertura antecede a la disponibilidad de la decisión, no puede ejecutarse retroactivamente.
- Invariancia separada frente a máximos, mínimos y cierres futuros, y una corrección posterior de N. Reutilización selectiva de R1/R2/R3/R7 sin repetir las160 comprobaciones.
- Registro de tiempos, callbacks, libros, decisiones, envío, llegada observada o modelada, ejecución, cantidades, configuración y procedencia.

El contrato inicial se limita a spot largo/efectivo, velas cerradas y órdenes de mercado; no incluye stops ni límites en reposo dependientes de una trayectoria OHLC desconocida. Debe distinguir OHLC de quotes/trades históricos y documentar elegibilidad, formación del precio, costes, spread, slippage, latencia, capacidad, rechazos, parciales, cancelación, remanentes y conciliación con oráculo independiente.

Límites: máximo ocho invocaciones técnicas iniciales, agrupación explícita de controles permitida,1800 segundos de máquina vigilada,4 vCPU/8 GiB RAM y512 MiB temporales adicionales. Un solo ciclo correctivo por defecto comprobado del harness, dentro de los límites; se aplica conservadoramente un máximo de ocho invocaciones totales incluyendo una eventual corrección. Cero descargas de software/datasets, servicios o gastos.

Prioridad: nativo sin latencia → timestamps → latencia/ordenación → alternativa causal → invariancia → complementarios. No repetir M, R completo, E3-L2, E4 ni LEAN; no construir otro motor ni alterar expectativas para obtener un pase.

Publicación autorizada de resultados reproducibles, incluidos adversos e inconclusos. Sin selección definitiva de motor, modificación de producción, experimentación financiera real, Fase V, paper ni live. E3/E4 económicos pendientes,26 especificaciones y compromisos científicos intactos. No hace falta una nueva propuesta o permiso dentro de este alcance.
