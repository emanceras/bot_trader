# Uso de la plataforma técnica

Idioma canónico: inglés. Revisión: 2. Actualización: 2026-10-20. Original sincronizado: [usage.md](../en/usage.md).

La plataforma actual comprueba software con datos sintéticos. Las hipótesis científicas originales siguen siendo preguntas de investigación. Una tarea técnica correcta, un gráfico o un invariante contable no demuestran capacidad predictiva ni rentabilidad neta.

## Primera sesión

Sigue la [instalación](installation.md), inicializa el estado y accede con la credencial privada local. El panel consulta registros reales del backend. Los estados vacíos indican ausencia de registros; no se rellenan con resultados inventados.

| Vista | Interpretación |
|---|---|
| Estado de plataforma | Modo técnico, recuentos y operativa real deshabilitada; los recuentos son acotados y no garantizan la salud del worker |
| Hipótesis | Los 25 registros H-00–H-24 preservados, su texto español original y procedencia |
| Datasets | Catálogo sintético, versión, especificación, partición y procedencia; el contenido reservado permanece cerrado |
| Gráfico | Velas `SYNTH-USD`, volumen y media calculados por el backend; relojes y precios simulados |
| Intentos técnicos | Configuración, estado persistente, manifiestos, errores e informes técnicos |
| Módulos | Dependencias, capacidades y estado operativo/preparado/planificado |
| Auditoría | Eventos y errores persistentes de servicios, con identificadores seguros |

La web es cliente de servicios implementados. Lee la descripción de cada módulo junto a su estado: un servicio sintético operativo no implica un feed de mercado, ni un contrato de modelo preparado implica entrenamiento financiero.

## Crear un fixture y enviar una tarea

Crea el fixture con semilla mediante el flujo de datasets o CLI:

```bash
uv run --frozen bot-trader fixture --seed 42 --rows 120
```

El instrumento es `SYNTH-USD`, la moneda es USD y los relojes de disponibilidad son simulados. El intervalo es una configuración técnica, no un horizonte de trading seleccionado. La generación admite como máximo 10.000 filas. La partición final no puede crearse ni abrirse mediante los flujos ordinarios de III; los registros reservados de las pruebas de seguridad se deniegan a todos los roles.

Selecciona una versión registrada del dataset al enviar un intento. El catálogo finito es:

| Tarea | Qué comprueba |
|---|---|
| `quality_check` | Integridad del artefacto/esquema/relojes y consultas agregadas acotadas sobre entradas sintéticas verificadas |
| `transform_check` | Media retrospectiva versionada usando solo observaciones ya disponibles para la transformación |
| `ledger_check` | Contabilidad spot sintética determinista y contratos de costes/riesgo, sin ejecución de mercado |
| `failure_fixture` | Fallo seguro deliberado que demuestra la conservación de intentos fallidos |

Ejecuta el worker como proceso separado. Los estados son `queued`, `running`, `succeeded`, `failed`, `interrupted` o `cancelled`. Cancelar impide persistir un resultado tardío; no mata forzosamente el proceso. La recuperación marca como interrumpidos los intentos pendientes de un worker detenido, sin repetirlos automáticamente.

Las tareas correctas proporcionan informes JSON y Markdown mediante el endpoint autorizado de artefactos. Los fallos conservan códigos de error seguros. El acceso vuelve a comprobar procedencia y partición; adivinar un nombre de archivo o un identificador antiguo no abre datos reservados.

## Repetibilidad y comparación

Cada ejecución congela configuración, versión e identidad del dataset, semilla, hash de código, revisión Git/estado modificado, lockfile y versiones seleccionadas del entorno. El worker comprueba otra vez esa identidad antes y después de ejecutar. Editar Python, cambiar dependencias o crear un commit entre el envío y la ejecución puede invalidar una tarea pendiente. Termina o cancela el trabajo afectado antes de cambiar el desarrollo; conserva los intentos invalidados y crea otros nuevos. Reinicia API y todos los workers después de cambiar código ejecutable/dependencias: un proceso con importaciones antiguas no puede representar los archivos actualizados y se rechaza hasta reiniciarlo.

Los identificadores y fechas difieren entre intentos. El digest determinista del informe debería coincidir con entradas inmutables y código/entorno equivalentes. Compara entre dos y diez intentos distintos mediante el flujo/API de comparación. `comparable` exige configuración y manifiestos congelados iguales; `same_result` exige además resultados correctos con el mismo digest. Ninguno clasifica estrategias ni elige una ganadora.

Registrar una semilla no garantiza por sí solo equivalencia universal entre plataformas o dependencias. La plataforma registra diferencias y comprueba la identidad vigente; no afirma equivalencia numérica arbitraria entre entornos.

## Registros científicos y temporales

`init` importa las hipótesis sin reescribir sus nulas o condiciones de refutación. Las versiones son inmutables: cambiar la fuente crea otra versión y conserva la anterior. La documentación técnica inglesa no sustituye a la fuente científica española.

La API admite una lista opcional `hypotheses` en `TechnicalRunSpec`. Cada asociación utiliza `kind: "hypothesis"`, el `id` persistente, la `version` exacta y el `content_hash` del registro. El envío resuelve y congela estas referencias; la lectura y el worker comprueban las mismas versiones históricas. Una versión posterior de la hipótesis no reescribe una ejecución anterior. Omite la lista para una comprobación de software independiente. Las asociaciones documentan contexto científico: una tarea sintética no valida la hipótesis enlazada. La web actual las muestra en la configuración/procedencia congelada, sin un flujo separado de gestión de estrategias.

Las utilidades temporales preparan planes cronológicos finitos y walk-forward expansivo, con disponibilidad de etiquetas, exclusión de solapamientos y reglas de purga/embargo. No ajustan modelos, leen el conjunto final ni demuestran que los timestamps históricos sean fiables. El protocolo futuro deberá fijar horizontes, costes, presupuesto de búsqueda y criterios antes de evaluar financieramente.

## Propuestas y límites

La API registra propuestas inertes con fundamento, nula, refutación, referencias, procedencia de modelo/prompt y recursos solicitados. Cada actor dispone de un máximo persistente de 20 propuestas y 100 unidades presupuestarias solicitadas. La unidad es una cuota técnica, no dinero ni autorización de gasto. Una propuesta queda pendiente de revisión, sin ejecución ni presupuesto autorizado.

Ningún agente autónomo lee la propuesta y actúa. Textos, URLs y salidas de modelos son datos; no llevan asociado shell, herramientas, descarga de URL ni entrenamiento. Las credenciales de agente permiten metadatos limitados y propuestas, pero no contenido de datasets ni ejecución de trabajos.

Todos los resultados conservan `synthetic: true` y `financial_validation: false`. El contador de experimentos financieros permanece en cero. Avanzar a protocolo científico o experimentos financieros exige la siguiente autorización explícita; la interfaz no puede concederla.
