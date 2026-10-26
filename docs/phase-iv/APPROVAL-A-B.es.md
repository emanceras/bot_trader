# Autorización de paquetes A/B — 2026-10-26

Mensaje del usuario referido al informe publicado en `7e075da`. Registro D-040. Autoriza únicamente la auditoría técnica de los dos archivos identificados y la evaluación aislada/sintética del motor; no constituye permiso general de adquisición o experimentación financiera.

---

He revisado el informe de viabilidad publicado en el commit 7e075da.

Autorizo los paquetes A y B con el alcance y las restricciones que has propuesto.

Paquete A — Auditoría técnica de datos

Autorizo la descarga de los dos archivos gratuitos de Kraken del tercer trimestre de 2026, previa comprobación de sus derechos de uso, identidad y tamaños, para realizar exclusivamente las verificaciones técnicas descritas.

Quiero aclarar un principio fundamental para bot_trader:

Estos tres meses de datos son únicamente una muestra para comprobar la calidad de la información y el funcionamiento de nuestra infraestructura. No representan el histórico que utilizaremos para investigar estrategias.

Cuando llegue el momento de realizar investigación cuantitativa real, quiero que dispongamos de la máxima cantidad de datos históricos relevantes y fiables que sea viable obtener.

No quiero limitarnos a Kraken, Binance, TradingView ni a ningún proveedor concreto. La selección deberá basarse en una investigación comparativa de las fuentes disponibles, considerando profundidad histórica, cobertura de activos —incluidos los deslistados—, granularidad, calidad, licencias, costes y posibilidades de acceso histórico y en tiempo real.

Debemos poder estudiar distintos ciclos y condiciones de mercado, sin imponer arbitrariamente un límite temporal. También quiero que la arquitectura permita incorporar nuevas fuentes e información, como noticias, sentimiento, datos on-chain y derivados, cuando corresponda.

Esto no significa descargar indiscriminadamente toda la información existente, sino disponer de la máxima cobertura científicamente útil y económicamente razonable.

Para la auditoría actual, mantén los límites de adquisición ya establecidos. Cualquier descarga adicional deberá proponerse y autorizarse por separado.

Paquete B — Evaluación técnica de NautilusTrader

Autorizo la instalación y evaluación de NautilusTrader 1.231.0 en un entorno aislado y desechable, utilizando únicamente datos sintéticos.

Comprueba su compatibilidad con nuestra arquitectura, reproducción de órdenes, comisiones, ejecuciones parciales, rechazos, contabilidad, conciliación, recuperación ante fallos y consumo de recursos.

No modifiques las dependencias de producción de bot_trader ni realices todavía una integración financiera completa. Si detectas limitaciones importantes, documenta las alternativas.

Condiciones generales

- Trabaja con autonomía dentro de estos dos paquetes.
- No contrates servicios ni generes gastos sin autorización.
- No incorpores archivos de datos voluminosos al repositorio.
- No ejecutes backtests financieros con datos reales ni entrenes modelos de inversión.
- No actives paper trading ni operativa real.
- No adelantes la Fase V.
- Mantén E3 y E4 pendientes hasta disponer de evidencia suficiente.

Al finalizar, presenta los resultados de ambas pruebas, los problemas encontrados, los recursos consumidos y tu recomendación sobre las siguientes decisiones.

Nuestro objetivo final sigue siendo construir una plataforma de investigación cuantitativa amplia, escalable y capaz de incorporar nuevas estrategias, mercados y fuentes de información sin quedar limitada por las elecciones técnicas de esta primera auditoría.

Continúa con los paquetes A y B bajo estas condiciones.
