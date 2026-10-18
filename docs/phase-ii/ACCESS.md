# Fase II — Acceso a productos y jurisdicción

Fecha de consulta: **2026-10-18**. Estado: **contraste documental acotado**, sin elección de exchange, cuenta, contrato o autorización operativa. España es la referencia inicial indicada por el usuario. Este documento complementa [viabilidad](FEASIBILITY.md) y [selección](SELECTION.md); sus fuentes regulatorias **no amplían los 53 trabajos científicos**. El registro de recuperaciones, fallos y lecturas está en [access-sources.jsonl](access-sources.jsonl).

## Qué cambia y qué no queda resuelto

Spot sigue siendo un escenario investigable con menos dependencias contractuales que una cobertura con derivados; no se presume accesible cualquier token, servicio o entidad. Futuros, perpetuos, cortos, opciones y otros instrumentos permanecen investigables cuando exista una pregunta fundada. Que una alternativa requiera otro producto o una jurisdicción distinta puede justificar **reserva condicionada**, no su refutación económica ni su autorización para operar.

La distinción decisiva es entre **hipótesis investigable**, **producto jurídicamente clasificable**, **acceso efectivo del operador** y **ejecución económicamente viable**. Una página comercial visible, una API disponible o la marca de un grupo no resuelven las cuatro cuestiones. No se selecciona un intermediario ni se presume categoría de cliente profesional, permiso para apalancamiento o admisión individual.

## Fuentes oficiales efectivamente consultadas

Se limitaron las recuperaciones a seis documentos/páginas objetivo; tres proporcionaron contenido pertinente. Las consultas alternativas al mismo texto EUR-Lex no son fuentes independientes. Se leyó el alcance señalado, no toda la normativa aplicable.

| ID y fuente | Contenido examinado y extracto breve | Conclusión utilizable y límite |
|---|---|---|
| **ACC-03 — [CNMV: MiCA, nueva regulación de criptoactivos](https://www.cnmv.es/portal/mica/regulacion-criptoactivos)** | Apartados de exclusiones, autorización, recomendaciones, proveedores y régimen transitorio. «las protecciones de MiCA solo se aplican a la entidad jurídica autorizada en la UE»; «El periodo transitorio en España finalizará el 1 de julio de 2026» | Comprobar entidad y servicios concretos; el registro histórico del Banco de España no acredita autorización actual MiCA. La página incluye texto histórico en futuro y también el aviso actual «Desde el 1 de julio de 2026». No se consultaron expedientes individuales ni se certificó ningún proveedor |
| **ACC-06 — [ESMA, informe final de clasificación, 17-12-2024](https://www.esma.europa.eu/sites/default/files/2024-12/ESMA75453128700-1323_Final_Report_Guidelines_on_the_conditions_and_criteria_for_the_qualification_of_CAs_as_FIs.pdf)** | Marco, pp. 4–6; respuesta sobre derivados, pp. 15–16; anexo III, pp. 33–34, y Guía 5, pp. 42–43; cotejo adicional de §§54–55, pp. 44–45, sobre opciones y liquidación. «perpetual futures should be treated as derivative contracts» (§47); análisis referido al anexo I.C(4)–(10) de MiFID II | MiCA no habilita automáticamente derivados. Separar cripto como subyacente de un derivado y token que es instrumento financiero. El informe exige análisis caso por caso; no determina la clasificación, disponibilidad minorista o condiciones vigentes de un contrato concreto |
| **ACC-05 — [AEAT: persona física residente en España](https://sede.agenciatributaria.gob.es/Sede/no-residentes/residencia-personas-fisicas-juridicas/persona-fisica-residente-espana.html)** | Normativa interna, doble residencia y acreditación; actualización visible 21-07-2026. «Una persona puede tener permiso de residencia o residencia administrativa en un Estado y no ser considerada residente fiscal en el mismo» | La residencia depende de circunstancias y reglas efectivas, no de dónde esté el exchange. La página expone permanencia, intereses económicos y convenios; no se determina la residencia fiscal personal ni se calculan impuestos |

**Límites de acceso:** ACC-01, Reglamento MiCA 2023/1114, y ACC-02, Directiva MiFID II 2014/65, devolvieron HTTP 202 sin cuerpo tanto por ELI como por rutas alternativas HTML/PDF. No se presentan sus originales como leídos; las afirmaciones anteriores descansan en CNMV/ESMA. ACC-04, un intento de localizar una noticia ESMA sobre perpetuos, devolvió HTTP 200 con navegación genérica sin la noticia; no sustenta ninguna conclusión. No se hicieron búsquedas generales adicionales ni se comprobaron exhaustivamente modificaciones posteriores al informe ESMA.

## España, MiCA y derivados

Para servicios comprendidos en MiCA, la CNMV distingue proveedores autorizados y determinadas entidades financieras habilitadas por el procedimiento aplicable. También explica la prestación desde otros Estados miembros mediante autorización y comunicación correspondiente. Por tanto, **no se exige que el exchange sea español**, pero sí comprobar la entidad que contrataría con el residente y el alcance territorial y material de su habilitación. No basta que otra empresa del mismo grupo figure en un registro.

El antiguo registro español ligado a prevención de blanqueo y el régimen transitorio no son una autorización indefinida. A la fecha de esta lectura ya ha pasado el 1 de julio de 2026 indicado por CNMV. Los antecedentes históricos podrán servir para reconstruir condiciones pasadas; no se usarán para acreditar acceso actual.

La CNMV excluye del ámbito de MiCA los instrumentos financieros regulados por MiFID II. ESMA distingue expresamente contratos derivados con cripto como subyacente y criptoactivos que constituyen derivados; la tokenización o la liquidación en stablecoins no eliminan por sí mismas su naturaleza. **Tener autorización MiCA para servicios spot no acredita ofrecer futuros, perpetuos u opciones**. Tampoco se infiere que todos estos productos estén prohibidos en España: clasificación, servicio, cliente, comercialización y restricciones aplicables necesitan comprobación concreta. Si un producto resulta ser CFD, se comprobarán además las medidas de intervención correspondientes; no se presume su clasificación por el nombre «perpetuo».

## Comprobaciones que deberá resolver una fase futura

Antes de asumir que un producto es operable o financiar ingeniería específica, registrar para una alternativa concreta:

1. **Entidad y jurisdicción:** razón social contractual, autorización/notificación, servicios cubiertos, prestación a residentes en España y fecha. Revisar registros oficiales y contrato; marca o nacionalidad del portal no bastan.
2. **Producto y cliente:** instrumento exacto, clasificación, acceso para la categoría real del operador, restricciones de comercialización, cortos, margen y apalancamiento. Investigación documental no implica aceptación personal de esos riesgos.
3. **Operación y datos:** permisos contractuales de API/automatización, uso histórico de datos, restricciones geográficas, custodia y conversión USD/stablecoin. Autorización regulatoria no garantiza licencias de datos, fills, solvencia ni reembolso.
4. **Condiciones económicas:** garantías, liquidación, financiación, tarifas, límites y capital completo; distinguir admisibilidad del coste de ejecutar. No asignar condiciones institucionales a una cuenta particular.
5. **Vigencia:** repetir la comprobación al elegir proveedor/producto y antes de una eventual etapa operativa, además de cuando cambien residencia, entidad, contrato o reglas. Conservar fecha y versión; no extrapolar la fotografía actual al pasado.

Una investigación futura podría estudiar un mecanismo no operable actualmente, siempre identificándolo como tal y respetando acceso/licencia de datos. No se contará su rendimiento hipotético como oportunidad disponible para el operador. Si el impedimento es decisivo para la candidata, se pospone la ingeniería específica hasta conocer una vía admisible.

## Otras jurisdicciones y disposición de candidatas

Operar desde España mediante entidad extranjera y operar tras un cambio real de residencia/situación jurídica son escenarios distintos. Un exchange extranjero, una VPN o una estructura offshore no acreditan por sí solos el segundo escenario ni eliminan obligaciones legales o fiscales. La ficha AEAT demuestra que residencia administrativa y fiscal pueden diferir; no se propone una mudanza o estructura para eludir requisitos. Un cambio legítimo exigiría revisar acceso y consecuencias con los hechos entonces vigentes.

**C1/C3 y C2** mantienen su papel propuesto, condicionado al producto que finalmente genere sus posiciones; usar información de derivados no obliga a negociarlos. **C4** puede utilizar activos informativos no operables si sus datos son accesibles y temporales, sin convertirlos en posiciones admisibles. **C5** permanece en reserva por acceso, capital, margen y contabilidad de ambas patas; no se elimina por España ni se promueve por una futura residencia hipotética. **Opciones y market making** conservan sus condiciones de reconsideración de datos, ejecución, riesgo y recursos; la comprobación jurídica será específica. Ningún resultado de esta revisión autoriza laboratorio, experimentos, gastos o negociación.
