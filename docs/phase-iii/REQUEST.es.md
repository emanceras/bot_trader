# BOT_TRADER — FASE III COMPLETA
## Arquitectura e implementación de una plataforma cuantitativa modular, extensible y preparada para investigación autónoma

### 1. Contexto y autorización

He revisado y acepto la propuesta final de la Fase II, documentada en el commit `f8f4ff8`, con todas sus limitaciones, incertidumbres y condiciones de reconsideración.

**Autorizo el cierre formal de la Fase II y la ejecución de la Fase III completa, incluyendo diseño arquitectónico e implementación del núcleo de la plataforma y del laboratorio cuantitativo.**

Quiero reorganizar la Fase III en dos etapas internas:

- **III.A — Investigación tecnológica y arquitectura integral.**
- **III.B — Implementación de la plataforma base y el laboratorio cuantitativo.**

Esta instrucción autoriza ambas etapas. Puedes continuar de III.A a III.B sin solicitar otra autorización, siempre que se cumplan los criterios establecidos y no se sobrepasen los límites de esta fase.

No confundas la autorización de desarrollar infraestructura de investigación con autorización para ejecutar experimentos financieros.

Las fases IV, V, VI, la activación de paper trading prospectivo y cualquier operativa real continúan requiriendo las autorizaciones correspondientes.

### 2. Objetivo final del proyecto

Quiero que `bot_trader` evolucione hacia una plataforma integral que reúna:

- Investigación cuantitativa y científica.
- Gestión y generación de hipótesis.
- Obtención y análisis de datos de mercados.
- Análisis estadístico, Machine Learning y Deep Learning.
- Backtesting y experimentación reproducible.
- Paper trading.
- Gestión de estrategias, carteras y riesgos.
- Ejecución de trading real bajo controles independientes.
- Herramientas gráficas avanzadas similares a TradingView.
- Investigación autónoma mediante agentes de inteligencia artificial.
- Una interfaz web centralizada para interactuar con el sistema.

**No quiero desarrollar varias aplicaciones provisionales para sustituirlas después.**

Quiero una única plataforma con arquitectura coherente, diseñada desde el principio para poder ampliar y mejorar sus funcionalidades durante años.

Sin embargo, no significa que debas implementar todas las funcionalidades finales en esta fase.

Diseña la arquitectura objetivo completa e implementa únicamente los componentes correspondientes a la Fase III y las bases reutilizables estrictamente necesarias.

Evita tanto la sobreingeniería como las soluciones provisionales que obliguen a rehacer partes importantes del proyecto.

### 3. Revisión inicial del repositorio

Antes de desarrollar:

1. Inspecciona el estado real del repositorio.
2. Lee `ROADMAP.md`, `AGENTS.md`, `DECISIONS.md`, `RESEARCH.md`, `HYPOTHESES.md` y `EXPERIMENTS.md`.
3. Revisa los documentos y conclusiones de la Fase II.
4. Comprueba qué existe realmente y qué sigue siendo una propuesta.
5. Conserva toda la documentación, las hipótesis, los resultados adversos y las decisiones históricas.
6. Actualiza el roadmap para reflejar la nueva organización de la Fase III y la arquitectura futura de la plataforma.

La implementación debe respetar el trabajo científico existente.

No interpretes la aceptación de candidatos como evidencia de rentabilidad.

### 4. Requisito prioritario: modularidad avanzada

Este es uno de mis requisitos fundamentales.

**Quiero que la plataforma sea modular en tres niveles.**

#### 4.1. Extensibilidad de la plataforma

Debemos poder añadir módulos completamente nuevos sin reconstruir el núcleo.

Ejemplos:

- Paper trading.
- Nuevos proveedores de mercado.
- Noticias económicas.
- Datos on-chain.
- Nuevos motores de modelos.
- Optimización de carteras.
- Nuevas herramientas gráficas.
- Nuevos exchanges.
- Investigadores de IA especializados.

#### 4.2. Extensibilidad interna de cada módulo

Cada módulo debe poder evolucionar sin obligarnos a modificar otros módulos independientes.

Ejemplo:

Un módulo de noticias inicialmente obtiene, normaliza y almacena información.

Posteriormente quiero añadirle análisis de sentimiento, extracción de entidades, detección de eventos, clasificación mediante LLM o generación de variables para modelos predictivos.

Estas ampliaciones deben poder incorporarse sin modificar innecesariamente el motor de trading, el paper trading o el laboratorio.

#### 4.3. Sustitución de componentes internos

Debe ser posible cambiar una implementación conservando los contratos que utilizan los demás componentes.

Ejemplos:

- Sustituir un modelo de sentimiento.
- Cambiar un proveedor de noticias.
- Añadir otro algoritmo de Machine Learning.
- Sustituir una biblioteca gráfica.
- Modificar un sistema de almacenamiento.
- Introducir una nueva implementación de un simulador de ejecución.

Estudia interfaces, contratos tipados, inversión de dependencias, separación de responsabilidades, esquemas versionados, gestión de eventos y mecanismos de extensión.

No utilices microservicios ni sistemas complejos de plugins sin justificación.

**La modularidad no debe consistir únicamente en crear carpetas diferentes.**

Debe ser posible demostrar que un módulo puede ampliarse, sustituirse o incorporarse sin romper componentes independientes.

### 5. Arquitectura objetivo

Estudia y define las responsabilidades de los siguientes dominios funcionales.

No presupongas que todos deban convertirse en paquetes o servicios independientes.

#### Core Platform

Configuración, contratos, registro de módulos, seguridad, permisos, gestión de estados, eventos y servicios comunes.

#### Market Data

Conectores, ingesta histórica, datos en tiempo real, normalización, sincronización, calidad y procedencia.

#### Research Lab

Hipótesis, investigación estadística, análisis cuantitativo y comparación de modelos.

#### ML & Models

Interfaces de entrenamiento e inferencia, gestión de modelos, versiones y métricas.

#### Experiment Management

Registro de experimentos, configuraciones, datasets, resultados y reproducibilidad.

#### Backtesting

Simulación histórica con separación entre estrategia, cartera, órdenes y ejecución.

#### Paper Trading

Operaciones simuladas con datos nuevos y capital virtual.

#### Trading Engine

Ejecución futura de estrategias reales mediante adaptadores autorizados.

#### Risk Management

Exposición, capital, garantías, pérdidas, riesgo operativo y controles independientes.

#### Portfolio Analytics

Posiciones, rendimiento, atribución, riesgos y comparaciones.

#### Charting & Technical Analysis

Gráficos, indicadores, screeners, visualizaciones y herramientas de análisis.

#### News Intelligence

Noticias, eventos, entidades, sentimiento y fuentes externas.

#### AI Researcher

Investigación autónoma, generación de hipótesis y propuestas experimentales.

#### Alerts & Notifications

Alertas de mercado, incidencias técnicas y eventos del sistema.

#### Web Dashboard

Interfaz centralizada que permita consultar y administrar las capacidades disponibles.

Elabora un mapa de dependencias entre dominios y define qué interfaces y datos podrán compartir.

### 6. Investigación tecnológica antes de implementar

Compara tecnologías existentes mediante documentación oficial y fuentes técnicas verificables.

Investiga especialmente, cuando sean pertinentes:

- NautilusTrader.
- QuantConnect LEAN.
- Freqtrade.
- vectorbt.
- Backtrader.
- Microsoft Qlib.
- Microsoft RD-Agent.
- MLflow.
- FastAPI.
- React y Next.js.
- PostgreSQL.
- DuckDB y Parquet.
- TradingView Lightweight Charts.
- Sistemas de workers y tareas programadas.

Puedes proponer alternativas mejores.

No presupongas que debamos adoptar ninguna herramienta concreta.

Evalúa:

- Capacidades reales.
- Madurez y mantenimiento.
- Licencias.
- Compatibilidad con nuestro uso privado.
- Extensibilidad.
- Integración con Python.
- Rendimiento.
- Seguridad.
- Complejidad operativa.
- Costes.
- Dependencia de terceros.
- Posibilidad de reutilizar componentes en fases posteriores.

Dedica especial atención a la decisión entre adoptar un motor existente de backtesting/ejecución e implementar uno propio.

Distingue entre adoptar un framework completo, integrar una biblioteca y utilizar únicamente patrones arquitectónicos.

**No reinventes funcionalidades maduras sin justificación, pero tampoco conviertas el proyecto en una simple adaptación de otro bot.**

Registra las decisiones técnicas y sus alternativas.

### 7. Arquitectura de software

Evalúa preferentemente un monolito modular con procesos especializados cuando estén justificados.

Considera un repositorio único que integre backend, frontend, infraestructura, pruebas y documentación.

Define:

- Contratos entre módulos.
- Interfaces públicas.
- Modelos de datos.
- Dependencias permitidas y prohibidas.
- Comunicación síncrona y asíncrona.
- Registro y descubrimiento de módulos.
- Gestión de errores.
- Versionado.
- Migraciones.
- Configuración.
- Gestión de secretos.
- Autenticación y autorización.
- Procesos de ejecución prolongada.
- Observabilidad y alertas.
- Recuperación ante fallos.
- Pruebas automáticas.
- Despliegue reproducible.

Evita dependencias circulares y acoplamientos innecesarios.

Elige tecnologías en función de los requisitos, no de su popularidad.

### 8. Plataforma web definitiva

Quiero que durante la Fase III se implemente una interfaz web real y funcional que forme parte de la plataforma definitiva.

No quiero una aplicación temporal que después tengamos que desechar.

El frontend deberá diseñarse para admitir nuevas secciones y funcionalidades sin reconstrucciones generales.

En esta fase debe permitir, como mínimo, interactuar con los componentes realmente implementados:

- Consultar el estado de la plataforma.
- Explorar las hipótesis registradas.
- Consultar el catálogo de datasets y su procedencia.
- Examinar experimentos y sus estados.
- Visualizar resultados y artefactos de pruebas técnicas.
- Consultar gráficos sobre datos de prueba disponibles.
- Acceder al inventario y estado de módulos.
- Consultar información básica de funcionamiento y errores.

No presentes como operativas funcionalidades que todavía sean únicamente futuras.

Las secciones pendientes pueden aparecer documentadas como tales, pero no mediante botones ficticios o simulaciones engañosas.

Diseña una interfaz clara, profesional, ordenada y extensible.

### 9. Funcionalidades similares a TradingView

Investiga cómo incorporar herramientas visuales avanzadas:

- Gráficos de velas.
- Volumen.
- Indicadores técnicos.
- Indicadores personalizados.
- Herramientas de dibujo.
- Comparación de activos.
- Gráficos múltiples.
- Watchlists.
- Screeners.
- Alertas.
- Calendarios económicos.
- Visualización de señales y operaciones.
- Resultados de estrategias.
- Superposición de predicciones de ML.

No quiero copiar TradingView indiscriminadamente.

Evalúa TradingView Lightweight Charts y alternativas adecuadas, comprobando licencias y limitaciones.

Durante la Fase III implementa únicamente un núcleo gráfico reutilizable e integrado en la plataforma, capaz de visualizar series temporales y ampliarse posteriormente con indicadores y herramientas adicionales.

No implementes por obligación todas las herramientas de TradingView.

El cálculo científico de indicadores debe estar separado de su representación gráfica.

### 10. Laboratorio cuantitativo funcional

Este es uno de los entregables principales de la Fase III.B.

Implementa la infraestructura necesaria para investigar y evaluar estrategias en fases posteriores.

Debe incluir:

- Registro y recuperación de hipótesis.
- Catálogo de datasets.
- Contratos de datos de mercado.
- Validación de esquemas.
- Transformaciones reproducibles.
- Definición de experimentos.
- Configuraciones versionadas.
- Registro de código y entorno.
- Gestión de semillas.
- Persistencia de resultados y fallos.
- Interfaces para modelos estadísticos y ML.
- Métodos de comparación de experimentos.
- Generación de informes y artefactos.
- Control de acceso a particiones reservadas.
- Preparación para evaluaciones temporales y walk-forward.

La infraestructura debe admitir resultados negativos e inconcluyentes.

No implementes supuestos rendimientos financieros predefinidos ni selecciones estrategias ganadoras.

**Quiero un laboratorio técnicamente funcional, pero todavía sin investigaciones financieras propias no autorizadas.**

### 11. Preparación de backtesting, paper trading y trading real

Diseña contratos comunes que permitan reutilizar la lógica estratégica entre tres entornos:

1. Backtesting histórico.
2. Paper trading prospectivo.
3. Ejecución real.

La lógica de señales y estrategias debe estar desacoplada de los mecanismos concretos de ejecución.

Sin embargo, no presupongas que los tres entornos tienen fills, latencias o garantías equivalentes.

Define interfaces para:

- Datos de mercado.
- Señales.
- Estrategias.
- Órdenes.
- Ejecuciones.
- Posiciones.
- Carteras.
- Costes.
- Financiación y márgenes.
- Reglas de riesgo.
- Eventos y estados operativos.

Durante la Fase III puedes implementar simuladores técnicos mínimos y pruebas deterministas con datos sintéticos para verificar contratos, contabilidad básica y comportamiento del software.

No ejecutes backtests empíricos de hipótesis sobre históricos reales, optimizaciones financieras ni paper trading conectado a mercados durante esta fase.

El paper trading debe quedar previsto como módulo de primera clase para su implementación posterior.

La ejecución real debe permanecer aislada, inactiva y sin acceso a cuentas financiadas.

### 12. Investigador autónomo de IA

Quiero que el diseño contemple un investigador capaz de proponer y estudiar nuevas hipótesis.

Debe poder evolucionar hacia un sistema que:

1. Consulte publicaciones científicas.
2. Analice investigaciones anteriores.
3. Detecte cambios y posibles anomalías.
4. Genere hipótesis por iniciativa propia.
5. Reciba ideas del usuario.
6. Identifique propuestas redundantes.
7. Diseñe experimentos falsables.
8. Solicite recursos o ejecución experimental.
9. Registre resultados.
10. Aprenda del historial de investigación.
11. Detecte deterioros de estrategias.
12. Proponga nuevas líneas de trabajo.

El investigador debe conservar referencias, contexto, versiones y razonamientos verificables.

No debe acceder indiscriminadamente a datos reservados para evaluación final.

Debe existir control de permisos, presupuestos de experimentación, consumo de modelos y número de investigaciones.

El sistema debe protegerse frente a instrucciones maliciosas presentes en páginas web, noticias, artículos y otros datos externos.

**Un agente investigador no podrá modificar estrategias reales, ampliar límites de riesgo o enviar órdenes por iniciativa propia.**

En la Fase III implementa únicamente los contratos, registros y mecanismos básicos de integración necesarios para que este componente pueda incorporarse posteriormente.

No desarrolles ahora un investigador autónomo completo ni ejecutes búsquedas experimentales continuas.

### 13. Datos, trazabilidad y reproducibilidad

Este requisito es especialmente importante porque el proyecto se fundamenta en investigación científica.

Distingue temporalmente:

- Momento del evento.
- Primera publicación.
- Disponibilidad del proveedor.
- Recepción local.
- Transformación.
- Generación de una señal.
- Momento de decisión.
- Ejecución.

Conserva versiones de:

- Datasets.
- Transformaciones.
- Modelos.
- Estrategias.
- Parámetros.
- Código.
- Entorno.
- Experimentos.
- Resultados.

Una mejora posterior de un modelo no debe sobrescribir silenciosamente versiones anteriores.

Debe ser posible reprocesar datos históricos sin presentar información conocida posteriormente como información disponible en el pasado.

Los identificadores y contratos deben permitir reconstruir qué información utilizó realmente cada experimento.

### 14. Investigación abierta y extensibilidad futura

Conserva las decisiones de las Fases I y II:

- USD como moneda de cuenta principal.
- España como jurisdicción inicial.
- Otros escenarios jurisdiccionales solo cuando sean legítimos.
- Apertura razonada a diferentes mercados, instrumentos y horizontes.
- Candidatas C1/C3 como preguntas primarias.
- C2 como comparación de riesgo.
- C4/C5 como reservas condicionadas.
- Posibilidad de reconsiderar otras familias ante información material.
- Presupuestos finitos de investigación.
- Evaluación objetiva y reproducible.

No conviertas la arquitectura en una plataforma exclusiva para momentum ni para un conjunto reducido de criptomonedas.

El sistema debe permitir estudiar nuevas hipótesis sin alterar innecesariamente su infraestructura.

Evita definir interfaces que dependan de un horizonte concreto, un modelo específico o un exchange determinado.

### 15. Documentación bilingüe

Todo el código, nombres de clases, funciones, variables, comentarios técnicos y docstrings estará en inglés.

La documentación deberá estar disponible en inglés y español.

Propón y aplica una estructura sostenible:

- Inglés como idioma técnico canónico para documentación nueva.
- Versión española sincronizada.
- Conservación de los documentos científicos originales.
- Trazabilidad de traducciones y actualizaciones.
- Identificadores de hipótesis invariables.
- Enlaces y referencias comprobables.

No reescribas ni traduzcas masivamente documentos históricos si eso pone en riesgo la integridad de sus evidencias o consume recursos desproporcionados.

Prioriza primero la documentación arquitectónica, de instalación, desarrollo y uso. Registra un plan verificable para la documentación histórica pendiente.

### 16. Seguridad y aislamiento

Diseña e implementa los controles correspondientes al alcance de la Fase III.

Presta atención a:

- Gestión segura de secretos.
- Autenticación y permisos.
- Separación de investigación y ejecución.
- Validación de entradas.
- Restricciones de herramientas de agentes.
- Dependencias y licencias.
- Registro de acciones.
- Recuperación ante fallos.
- Estados de error explícitos.
- Prevención de cambios accidentales.
- Aislamiento entre datos de prueba y datos operativos.

No debe ser posible que una prueba técnica active operaciones reales.

No almacenes claves de exchange ni credenciales en Git.

No solicites credenciales para completar esta fase.

### 17. Desarrollo ordenado y reutilización de recursos

Quiero que trabajes de manera eficiente.

Primero investiga y diseña la arquitectura, después implementa sus componentes siguiendo dependencias técnicas.

No desarrolles simultáneamente funcionalidades que dependen de infraestructura todavía inexistente.

Evita crear aplicaciones temporales, duplicar bibliotecas, introducir dependencias superfluas o diseñar sistemas excesivamente abstractos.

Pero tampoco sacrifiques extensibilidad simplemente para terminar antes.

Utiliza componentes existentes cuando sean adecuados.

Mantén pruebas y documentación a medida que implementes.

Realiza commits coherentes y verificables, preservando el historial.

Si el entorno o los recursos disponibles interrumpen el desarrollo, deja documentados:

- Estado exacto de implementación.
- Componentes terminados y pendientes.
- Pruebas ejecutadas y resultados.
- Errores conocidos.
- Decisiones tomadas.
- Siguiente paso concreto.

No declares completada la Fase III por haber generado únicamente documentación, estructuras vacías o interfaces ficticias.

### 18. Pruebas técnicas y criterios de aceptación

La Fase III.B deberá entregar software ejecutable y verificable.

Define y ejecuta pruebas de:

- Instalación y arranque.
- Calidad y tipado.
- Contratos entre módulos.
- Persistencia.
- Migraciones.
- APIs.
- Frontend.
- Integración.
- Seguridad básica.
- Gestión de errores.
- Reproducibilidad.
- Modularidad.

Demuestra la extensibilidad mediante pruebas técnicas concretas.

Como mínimo:

**Prueba A — Incorporación de un módulo**

Demuestra que puede registrarse e integrarse una extensión de ejemplo sin modificar indiscriminadamente el núcleo.

**Prueba B — Ampliación interna**

Demuestra que puede añadirse una capacidad opcional a un módulo existente sin cambiar módulos independientes.

**Prueba C — Sustitución de implementación**

Demuestra que una implementación puede reemplazarse por otra conservando sus contratos.

**Prueba D — Aislamiento de entornos**

Demuestra que las simulaciones técnicas no pueden enviar órdenes reales.

**Prueba E — Reproducibilidad**

Demuestra que una ejecución técnica determinista puede repetirse conservando configuración, datos, versión y resultado.

**Prueba F — Integración web**

Demuestra que el frontend puede consultar componentes reales de la plataforma y representar resultados y estados sin información simulada presentada como real.

Para estas pruebas utiliza fixtures y datos sintéticos cuando corresponda.

No utilices históricos reales para evaluar rentabilidad sin autorización de las fases posteriores.

### 19. Entregables de la Fase III.A

Produce documentación sobre:

1. Diagnóstico del repositorio.
2. Requisitos funcionales y no funcionales.
3. Arquitectura objetivo.
4. Alternativas comparadas.
5. Stack recomendado.
6. Diagramas de componentes.
7. Contratos de módulos.
8. Estrategia de extensibilidad.
9. Modelo de datos.
10. Arquitectura frontend y backend.
11. Investigación de motores de simulación y ejecución.
12. Diseño del laboratorio.
13. Diseño de paper trading.
14. Diseño del investigador autónomo.
15. Diseño del análisis gráfico.
16. Seguridad y aislamiento.
17. Costes y recursos.
18. Decisiones técnicas.
19. Plan de implementación.

Conserva esta documentación como referencia para la Fase III.B.

Si identificas un impedimento técnico importante que invalide la arquitectura elegida, documenta la alternativa y adáptala antes de implementar.

### 20. Entregables de la Fase III.B

Implementa, verifica y documenta:

1. Estructura definitiva del repositorio de software.
2. Núcleo modular de la aplicación.
3. Sistema de configuración.
4. Contratos y esquemas compartidos.
5. Backend funcional.
6. Persistencia y migraciones.
7. Infraestructura de datos y validación.
8. Registro de hipótesis y experimentos.
9. Laboratorio cuantitativo base.
10. Contratos para modelos y estrategias.
11. Infraestructura de simulación técnica.
12. Interfaz web funcional.
13. Componente gráfico inicial reutilizable.
14. Registro y estado de módulos.
15. Sistema básico de observabilidad y errores.
16. Pruebas automatizadas.
17. Comprobaciones de modularidad.
18. Configuración reproducible del entorno.
19. Documentación de instalación, desarrollo y arquitectura en inglés y español.
20. Plan actualizado de las fases siguientes.

No declares un componente implementado cuando solo exista su interfaz o documentación.

Distingue claramente funcionalidades operativas, infraestructura preparada y funcionalidades futuras.

### 21. Límites de autorización

Esta autorización cubre el diseño y la implementación de la **Fase III completa**.

Permite escribir código, instalar dependencias de desarrollo apropiadas, crear pruebas técnicas y utilizar datos sintéticos para verificar el software.

No autoriza:

- Contratar servicios ni generar gastos.
- Descargar datasets de mercado para backtests financieros.
- Ejecutar experimentos de rentabilidad sobre datos reales.
- Entrenar u optimizar modelos financieros con históricos reales.
- Seleccionar estrategias por resultados propios todavía no autorizados.
- Iniciar paper trading prospectivo conectado a mercados.
- Conectar cuentas financiadas.
- Enviar órdenes reales.
- Activar sistemas autónomos con permisos de producción.
- Comenzar las fases IV, V o VI.

No presupongas que una autorización de arquitectura implica autorización de riesgo financiero.

### 22. Finalización de la Fase III

Al terminar:

1. Comprueba el estado de Git.
2. Ejecuta las pruebas técnicas pertinentes.
3. Documenta resultados y limitaciones.
4. Verifica que la plataforma arranca mediante un procedimiento reproducible.
5. Comprueba que la interfaz web funciona con los componentes reales implementados.
6. Revisa los contratos y dependencias entre módulos.
7. Registra las decisiones técnicas.
8. Actualiza el roadmap.
9. Publica los commits autorizados en GitHub.
10. Presenta un informe de cierre.

El informe deberá indicar:

- Qué funciona realmente.
- Qué componentes están preparados pero no implementados.
- Qué requisitos arquitectónicos se han satisfecho.
- Qué pruebas se han ejecutado.
- Qué problemas permanecen abiertos.
- Qué recursos necesitará la siguiente fase.
- Qué decisiones debo aprobar.

No declares la Fase III completada si existen criterios esenciales incumplidos. En ese caso, indica exactamente el estado alcanzado.

**No avances a la Fase IV sin mi aprobación explícita.**

---

## PRINCIPIO FINAL DEL PROYECTO

Quiero construir una plataforma cuantitativa profesional, científicamente rigurosa y diseñada para evolucionar durante años.

La prioridad no es programar muchas funcionalidades rápidamente, sino disponer de una base sólida en la que podamos añadir módulos, mejorar funcionalidades internas y sustituir componentes sin reconstrucciones innecesarias.

El sistema debe estar preparado para investigar continuamente, incorporar nuevas ideas y evolucionar hacia investigación autónoma mediante IA, manteniendo separación estricta entre investigación, validación, simulación y capital real.

**Diseña la plataforma integral y desarrolla toda la infraestructura de Fase III necesaria para hacer realidad esa visión, sin adelantar las fases experimentales y operativas.**