# Autorización definitiva de ejecución M/R/E

Recibida: 2026-10-28. Registro de continuidad: 2026-10-29. Alcance aprobado: commit `fa435a4f3ff2c15360b5fa0b5da4e2cf2259d14f`, D-046. Mensaje del usuario conservado:

---

AUTORIZACIÓN DEFINITIVA DE EJECUCIÓN — PAQUETES M, R Y E

Los alcances, versiones, límites de recursos y condiciones de parada ya han sido presentados y revisados en el commit "fa435a4".

Autorizo expresamente, desde este momento, la instalación, preparación y EJECUCIÓN efectiva de los tres paquetes M, R y E, exactamente conforme a los documentos aprobados.

Esta autorización incluye:

- M: ejecutar la comparación aislada de PyArrow 23.0.1 y 26.0.0, con sus pruebas de compatibilidad, integridad y regresión.
- R: implementar y ejecutar los ocho diarios sintéticos y las 160 comprobaciones iniciales de coherencia temporal y causal.
- E: instalar en entornos aislados las versiones especificadas de NautilusTrader 2.0.0rc7 y LEAN, preparar los harnesses necesarios y ejecutar los casos sintéticos comparativos autorizados.

No necesitas volver a presentar los límites ni solicitar otra autorización para realizar estos trabajos. Ya están aprobados.

Respeta los techos conjuntos documentados: 4 vCPU, 8 GiB de RAM, 12 GiB de disco temporal, 2,5 GiB de descargas de software y 7 horas de ejecución activa, además de los límites individuales y las condiciones de parada de cada paquete.

Para evitar consumir recursos innecesariamente:

1. Reutiliza toda la documentación, código de pruebas y evidencia ya disponible.
2. No repitas investigaciones documentales ni prepares otra propuesta ejecutiva antes de comenzar.
3. Ejecuta los paquetes siguiendo las dependencias y el orden técnico establecidos, aprovechando resultados comunes.
4. Conserva los resultados adversos y detén únicamente las pruebas afectadas por un bloqueo real, incompatibilidad decisiva o límite de recursos.
5. No modifiques versiones, criterios de aceptación ni alcance para conseguir resultados favorables.
6. No conviertas una limitación del motor en una razón para reescribir repetidamente el harness. Aplica únicamente el ciclo correctivo acotado ya autorizado.
7. Si una prueba resulta imposible, documenta el motivo y continúa con las demás pruebas independientes que permanezcan autorizadas.

Mantén intactos el entorno de producción y sus dependencias. No descargues datos financieros adicionales, no contrates servicios, no desarrolles adaptadores completos ni ejecutes operaciones o experimentos financieros de Fase V.

Quiero que tu siguiente trabajo sea la ejecución técnica real, no otra revisión de lo que planeas ejecutar.

Cuando termines, publica los resultados reproducibles en GitHub y presenta un único resumen con los resultados de M, R y E, las limitaciones observadas, los recursos consumidos y tu recomendación técnica fundamentada.

No declares los paquetes completados hasta haber ejecutado efectivamente las pruebas correspondientes. Si existe un bloqueo material que exceda la autorización, informa de él sin ampliar el alcance por tu cuenta.

Puedes comenzar a ejecutar M, R y E ahora mismo. No requiero una nueva propuesta ni una nueva solicitud de aprobación dentro del alcance establecido.
