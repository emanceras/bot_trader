# Seguridad y operación local

Idioma canónico: inglés. Revisión: 2. Actualización: 2026-10-20. Original sincronizado: [security.md](../en/security.md).

Este despliegue técnico es local, en un host, con código fuente y cuenta del sistema operativo de confianza. Los controles separan roles y fronteras de investigación; no protegen archivos frente al administrador del equipo, una dependencia maliciosa ni código arbitrario bajo la misma cuenta. Producción o varios usuarios no confiables requieren otra revisión de amenazas.

## Credenciales, sesiones y permisos

`init` crea `.state/admin.token` con permisos privados e imprime solo la ruta. Las credenciales adicionales se crean explícitamente:

```bash
uv run --frozen bot-trader credential researcher
uv run --frozen bot-trader credential viewer
uv run --frozen bot-trader credential agent
```

Los comandos reutilizan archivos válidos en lugar de sobrescribir credenciales. Reinicia el servidor después de añadirlas o cambiarlas porque se cargan al arrancar. Mantén los archivos privados y fuera de Git; se rechazan enlaces simbólicos y permisos de lectura para grupo/otros. Las rutas de estado personalizadas necesitan la misma protección que `.state`.

| Rol | Alcance permitido en la aplicación |
|---|---|
| `viewer` | Lee datasets/resultados técnicos autorizados, hipótesis, módulos, estado y auditoría |
| `researcher` | Lo anterior, creación de datasets sintéticos, envío/cancelación de tareas finitas y propuestas |
| `admin` | Lo anterior y política de worker/recuperación/gestión de sesiones; tampoco accede a contenido reservado ni modo financiero |
| `agent` | Metadatos limitados, hipótesis/módulos y propuestas inertes; sin contenido de datasets, tareas ni operativa |

Las sesiones son aleatorias, limitadas, revocables y permanecen en memoria del proceso API. Las cookies usan HttpOnly, SameSite Strict y caducidad configurada. Cerrar sesión la revoca; reiniciar API revoca todas. Utiliza un solo proceso API: no hay sesiones compartidas entre réplicas.

Las mutaciones autenticadas exigen el token CSRF de sesión. Todas las mutaciones, incluido login, requieren origen explícitamente permitido; el control de host es independiente. No hay acceso API permisivo entre orígenes. Se limitan intentos de login y sesiones activas. Los errores omiten valores de credenciales rechazadas, trazas y texto externo arbitrario; utiliza identificadores de correlación al investigarlos.

La CLI escucha en loopback. Las cookies HTTP de desarrollo no llevan Secure porque el endpoint local utiliza HTTP. Producción exige orígenes HTTPS y cookies seguras, pero esas opciones no instalan TLS, proxy, identidad endurecida ni monitorización. No expongas públicamente la configuración de desarrollo.

## Fronteras de investigación y ejecución

Solo es válido el modo `technical`. No hay adaptador de exchange, transporte de órdenes, paper trading prospectivo, tarea de código arbitrario, carga de datos de mercado ni bucle autónomo de modelos. Un administrador no puede activarlos mediante un campo de petición.

El contenido de la partición final se deniega a todos los roles. Sus metadatos restringidos ocultan semillas, descriptores de artefactos, resúmenes de calidad y hashes del contenido. Datasets, gráficos/transformaciones y accesos derivados a trabajos/artefactos vuelven a comprobar la procedencia persistida. Estos controles actúan dentro de la aplicación; el acceso directo al host/base de datos puede evitarlos y es privilegiado.

Los artefactos usan sufijos registrados acotados y hashes, publicación atómica y verificación de integridad al leer. No se admiten rutas, SQL ni URLs arbitrarias del cliente. DuckDB bloquea acceso externo y extensiones. Peticiones HTTP, filas sintéticas, cola y artefactos tienen límites finitos. Esto acota recursos, pero no constituye aislamiento integral entre usuarios hostiles.

Propuestas y fuentes son datos no confiables, nunca instrucciones. Las cuotas se persisten y comprueban en una transacción: máximo 20 propuestas y 100 unidades solicitadas por actor. No autorizan gastos ni herramientas. No existe reinicio de cuota ni conversión autónoma de propuesta a trabajo.

Los hashes detectan discrepancias en el contenido registrado; no prueban que la fuente fuese correcta, que se hayan observado todos los eventos ni que balances y posiciones externos estén conciliados. Una recomendación aprobada seguiría necesitando ejecución autorizada por separado y confirmación efectiva. La [revisión complementaria](architecture/supplement.md) define estas fronteras futuras de decisión y conciliación sin activarlas.

## Parada, recuperación e investigación

Detén API y worker con la interrupción normal del proceso. Una caída del worker puede dejar un intento como `running`; trabajos y auditoría sobreviven a reinicios de API. No hay toma de control automática por latido ni repetición automática.

Confirma primero que el worker con esa identidad se ha detenido. Después, con el mismo estado:

```bash
uv run --frozen bot-trader recover local-worker
```

La recuperación marca los intentos afectados como `interrupted` sin volver a ejecutarlos. Un worker antiguo no puede finalizar después un intento interrumpido o cancelado. Recuperar no mata el proceso: hacerlo mientras sigue activo puede interrumpir trabajo legítimo. Revisa intento y error seguro antes de enviar otro; conserva el registro anterior.

Panel y CLI sirven para supervisión local. Alertas externas, escalado a responsables, latidos del worker, paradas de emergencia de producción y recuperación automática son capacidades operativas futuras. Su ausencia es una razón por la que esta plataforma no está admitida para ejecutar en mercados.

## Copias y restauración

Para una copia local coherente, detén **todos los escritores**: API, workers y comandos CLI que modifiquen estado. Espera a su salida y copia el directorio completo a un destino privado, conservando permisos. Incluye SQLite y sus archivos auxiliares, artefactos inmutables y credenciales. Registra revisión de código, lockfiles y esquema junto a la copia. No publiques el directorio: contiene credenciales y estado de investigación.

Copiar archivos mientras quedan escritores activos no es un procedimiento soportado. Esta versión no proporciona servicio de copia en línea ni herramienta probada de migración entre hosts. Utiliza un destino privado/cifrado apropiado y conserva el original hasta verificar la restauración.

Restaura con todos los escritores detenidos en otro directorio privado, usando la revisión fuente y dependencias congeladas correspondientes. Comprueba compatibilidad del esquema antes de actualizar. Arranca contra la copia y verifica hipótesis/datasets/trabajos y hashes representativos mediante la aplicación. Hay que iniciar sesión de nuevo. Si la copia contiene intentos en ejecución, confirma que los workers originales están detenidos y márcalos interrumpidos explícitamente. Nunca ejecutes escritores originales y restaurados contra el mismo directorio simultáneamente.

Las pruebas reales de recuperación/restauración y sus límites se registran en la [verificación de III](verification.md). Estas instrucciones no prometen recuperación de pérdida de disco sin copia válida, corrupción fuera de las comprobaciones ni host malicioso. La inmutabilidad en aplicación/base de datos conserva historia dentro de su frontera; no es almacenamiento de auditoría externo inviolable.
