# Recuperación acotada del paquete E — autorización y precisiones

Recibida: 2026-11-01 (Europe/Madrid). Base de resultados: `00131bc`. D-048. Texto aportado por el usuario; las observaciones externas no constituyen evidencia ejecutada del proyecto.

---

Quiero continuar la recuperación acotada del paquete E, aprovechando los resultados publicados en el commit 00131bc y una comprobación técnica externa realizada con NautilusTrader.
La revisión externa aporta tres precisiones útiles que quiero incorporar, sin considerar sus resultados como evidencia oficial de nuestros ensayos.
Esta instrucción complementa la autorización de recuperación ya concedida. No quiero otra propuesta documental ni repetir pruebas M/R o resultados anteriores de LEAN.
La comprobación externa consiguió instalar NautilusTrader 2.0.0rc7 con Python 3.13.13 y la wheel previamente fijada, conservando su tamaño y SHA256.
No es necesario fijar específicamente Python 3.13.13.
Comprueba con nuestro uv 0.12.23 qué distribuciones estándar de CPython 3.13.x están disponibles, priorizando una versión parche reciente compatible y verificable.
Utiliza exclusivamente CPython 3.13 estándar, no la variante free-threaded (cp313t, +freethreaded) ni Python 3.14. La wheel aprobada utiliza la ABI estándar cp313.
Fija y registra la versión seleccionada, procedencia, integridad y dependencias antes de instalarla.
Mantén intactas la wheel de Nautilus 2.0.0rc7 y sus verificaciones de identidad.
Reutiliza las cachés existentes y respeta los límites de recursos y adquisición de software ya autorizados. No modifiques Python ni las dependencias de producción.
Si el runtime resulta compatible, ejecuta las pruebas pendientes de Nautilus dentro del alcance de recuperación.
La prueba externa observó que Nautilus puede ejecutar una venta limitada post_only a 102 cuando el bid alcanza exactamente 102, mientras que el modelo probado de LEAN exige un cruce estricto.
Nuestro fixture congelado espera la ejecución, por lo que Nautilus podría cumplir esa expectativa.
Sin embargo, cumplirla no demuestra que la ejecución sea realista.
Clasifica separadamente:
- Cumplimiento de la expectativa congelada.
- Supuesto del modelo de ejecución.
- Realismo de mercado todavía no demostrado.
Conserva el orden temporal exacto de nuestro fixture: comandos, cotizaciones anteriores, nuevos eventos y disponibilidad. No adelantes ni retrases un evento para conseguir un resultado favorable.
Si el comportamiento cambia al alterar el orden, documenta la diferencia sin modificar el caso original.
La prueba externa obtuvo:
- L1: ejecución total de cuatro unidades pese a observar una sola unidad disponible.
- L2: consumo de los niveles 100@1, 101@2 y 102@1 para completar cuatro unidades.
- IOC: ejecución parcial de una unidad y cancelación del remanente.
Estos resultados son orientativos y deben reproducirse con nuestros fixtures, configuración y oráculo.
No presupongas que L2 garantiza automáticamente ejecuciones realistas ni que una limitación L1 invalida todas las investigaciones basadas en velas.
Distingue la precisión necesaria según el mecanismo de la estrategia. La profundidad L2 resulta especialmente relevante para afirmaciones que dependan de la liquidez, pero no es un requisito universal para investigar momentum de menor frecuencia con supuestos conservadores de ejecución.
La comprobación externa no consiguió discriminar el efecto de liquidity_consumption=True/False porque utilizaba órdenes individuales.
Autorizo, dentro de los recursos restantes y sin modificar los criterios originales de admisión, un diagnóstico sintético adicional y acotado para estudiar esta propiedad.
Diseña dos órdenes consecutivas que compitan por el mismo nivel visible de liquidez, sin una actualización intermedia del libro.
Comprueba por separado L1 y L2, con liquidity_consumption activado y desactivado cuando esas configuraciones sean aplicables.
Registra:
- Liquidez inicial disponible.
- Secuencia exacta de órdenes y eventos.
- Cantidades ejecutadas por orden.
- Liquidez consumida y restante según el modelo.
- Diferencias observadas entre configuraciones.
- Comportamiento nativo frente a comportamiento aportado por el harness.
No presupongas que activar la opción resuelve automáticamente las limitaciones de L1.
Este diagnóstico es evidencia complementaria, no un sustituto de los casos E congelados ni una nueva especificación financiera. No adaptes sus expectativas después de observar los resultados.
Si no puede realizarse sin exceder los límites o implementar un nuevo modelo de ejecución, documenta la limitación y no lo ejecutes.
Separa explícitamente los requisitos de integridad científica de los requisitos prospectivos.
Para investigación financiera:
- Contabilidad y comisiones correctas.
- Rechazo de duplicados y conservación de identidades.
- Capital y posiciones sin doble contabilización.
- Reproducción determinista y recuperación de estados de investigación cuando sea necesaria.
Para futura operativa:
- Conciliación de órdenes pendientes con el exchange después de una caída.
- Recuperación ante ejecuciones desconocidas.
- Reanudación segura y bloqueo de riesgo nuevo.
- Integración y atribución de broker cuando corresponda.
No elimines E4/E5 del registro original. Clasifica qué partes son imprescindibles para cada modalidad y cuáles permanecen sin demostrar.
No desarrolles ahora infraestructura completa de trading real para intentar superar casos fuera del alcance.
Prioriza desbloquear Nautilus y obtener evidencia comparable con los casos ya realizados en LEAN.
No repitas M, R ni pruebas anteriormente concluyentes.
Conserva todos los resultados originales, incluidos fallos, casos parciales y casos sin ejecutar.
No elijas un motor ganador anticipadamente. Separa cumplimiento de fixtures, comportamiento del motor, limitaciones del harness y aptitud para investigación o producción.
No amplíes los presupuestos globales, no adquieras datos financieros adicionales, no modifiques producción, no actives paper/live y no inicies la Fase V.
Puedes continuar directamente con la ejecución autorizada.
Al terminar, publica los resultados nuevos y presenta una conclusión concreta sobre Nautilus, LEAN y los obstáculos restantes para seleccionar un motor adecuado a bot_trader.
