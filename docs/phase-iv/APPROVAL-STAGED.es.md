# Aprobación metodológica por etapas y encargo de paquetes M/E/R

Registrado: 2026-10-27. Mensaje del usuario referido a `9aeae39`. D-044 registra la aprobación metodológica; D-045 registra la propuesta técnica. **No autoriza ejecutar los nuevos paquetes ni la Fase V.** Texto conservado:

---

He revisado la revisión de evolución publicada en el commit 9aeae39.

Apruebo el principio metodológico de admisión estadística por etapas (T, D, U, V y F), con las condiciones y salvaguardas propuestas.

Esta aprobación es exclusivamente metodológica. No autoriza todavía el desarrollo financiero, las evaluaciones con datos reales ni la Fase V.

Puedes preparar y registrar la enmienda metodológica correspondiente, manteniendo los compromisos científicos E1/E2, las 26 especificaciones base, la independencia de validación y holdout final, los requisitos económicos prospectivos y todas las restricciones de acceso.

Quiero que ahora nos centremos en resolver las incertidumbres técnicas que verdaderamente bloquean el proyecto.

Como siguiente paso, concreta los paquetes mínimos de pruebas técnicas M, E y R:

- M — Dependencias: define la prueba aislada para determinar si podemos actualizar PyArrow sin pérdida de compatibilidad ni alterar nuestros datos y artefactos existentes.
- E — Motores: concreta una comparación justa entre NautilusTrader y LEAN, especificando versiones mantenidas, los mismos casos sintéticos, requisitos obligatorios y criterios de aceptación. No presupongas un ganador.
- R — Coherencia temporal: define cómo verificaremos que los datos históricos, la reproducción de eventos y los futuros datos directos producen decisiones equivalentes cuando contienen la misma información disponible.

Para cada paquete, establece dependencias, versiones, recursos estimados, riesgos, condiciones de parada y alcance exacto de ejecución.

Prioriza las comprobaciones que realmente permitan tomar una decisión. Evita nuevas revisiones documentales extensas cuando ya tengamos información suficiente para diseñar una prueba concreta.

No instales ni ejecutes todavía los nuevos paquetes sin presentar el alcance que requiera autorización.

No descargues más datos, no contrates servicios, no actualices producción, no realices backtesting financiero con datos reales ni inicies paper/live trading.

Mantén E3/E4 pendientes.

Al finalizar, presenta una propuesta ejecutiva breve que permita autorizar las pruebas técnicas pertinentes sin necesidad de nuevas rondas de investigación general.

Nuestro objetivo inmediato es seleccionar con evidencia una infraestructura de datos y un motor adecuados, para poder completar la preparación científica y acercarnos a la experimentación real.
