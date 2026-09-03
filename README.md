# Plugins de auditoría de Ensys para Gesia

Procedimientos de auditoría que trabajan directamente sobre el expediente de
Gesia y producen papeles de trabajo en Excel y Word.

## Instalación

En Claude, en **Configuración**:

1. En el apartado **Personalizar**, pulsa **Plugins**.
2. Arriba a la derecha, despliega **Agregar** y elige **Agregar marketplace**.
3. En el campo **URL**, escribe esto y pulsa **Sincronizar**:

   ```
   Ensys-Consultores-Informaticos/claude-plugins
   ```

4. En la lista aparece **Gesia — Expediente de auditoría**, de Ensys Consultores
   Informáticos, S.L. Pulsa **Instalar**.
5. **Cierra Claude del todo y vuelve a abrirlo.** El programa que lee el expediente se
   registra al arrancar, y hasta que no reinicias no está disponible.

Los procedimientos funcionan en **Cowork**, no en una conversación normal de chat: desde
el chat Claude no puede leer el expediente ni escribir los papeles de trabajo. Abre una
sesión de Cowork y empieza diciendo con qué expediente trabajas:

```
Conecta con el encargo Ejemplo 24.gs3, que está en C:\Auditorias\Ejemplo 24
```

Para la ruta, sin teclearla: clic derecho sobre el archivo `.gs3` en el Explorador y
«Copiar como ruta de acceso». Claude responderá con el cliente que ha encontrado, el
diario vinculado y si el servidor de Gesia responde: conviene leer eso antes de seguir.

## Actualizar a una versión nueva

**Dónde pulsar depende de dónde uses el plugin**, y es la causa más común de que
parezca que no se puede actualizar:

- **En la aplicación de Claude:** abre la ficha del plugin y pulsa **Actualizar**. Con
  eso basta. Si el botón no aparece, es que la aplicación todavía no se ha enterado de
  que hay versión nueva: revisa sus marketplaces o quita y vuelve a añadir este.
- **En Claude Code:** el marketplace tiene que estar añadido en la propia CLI, con
  `/plugin marketplace add Ensys-Consultores-Informaticos/claude-plugins`. Si no lo
  está, «buscar actualizaciones» falla con un **«No se pudo actualizar el
  marketplace»** que no explica nada — y el motivo es solo ese.

No hay que desinstalar nada.

**¿Hace falta actualizar con el plugin frío?** Ya no. El plugin trae dentro el programa
que lee tu expediente, y ese programa se queda en marcha en cuanto usas un
procedimiento; Windows no deja sustituir un ejecutable que está funcionando, así que
antes la actualización podía fallar con un «No se pudo actualizar el plugin». **Desde la
versión 1.5.6 el ejecutable lleva su versión en el nombre**, de modo que cada
actualización escribe un fichero nuevo en vez de intentar pisar el que está corriendo.
Comprobado el 30/08/2026: dos actualizaciones seguidas con el programa llevando casi
una hora en marcha, sin un solo fallo.

Si aun así te apareciera ese aviso, el remedio de siempre sigue valiendo: cierra Claude
del todo, vuelve a abrirlo y actualiza antes de usar ningún procedimiento. Desactivar el
plugin con su interruptor también suele bastar.

Y si es el **marketplace** el que se niega y el aviso vuelve aunque reinicies, **quítalo y
vuelve a añadirlo** con el nombre de arriba.

**Para saber qué versión tienes**, mira el final de la descripción del plugin: va escrita
ahí, como `(v1.6.4)`. El número que la aplicación muestra en el campo «Versión» **no es
la versión del plugin**: es un contador suyo de actualizaciones, que se reinicia si
quitas y vuelves a añadir el marketplace.

Después de actualizar, **reinicia Claude** una vez más: el programa que lee el
expediente se registra al arrancar, y hasta entonces la versión nueva no está
disponible.

## Antes de usarlo

Dos cosas que fallan a menudo, y las dos son de Gesia, no del plugin:

- **El servidor API de Gesia se arranca a mano en cada sesión**, desde
  *Herramientas → Gesia - Cuadro de mando → Arrancar servidor API*. Si las
  consultas al expediente vuelven vacías o dan error de conexión, es lo primero
  que hay que mirar.
- **El diario contable necesita el driver de Access de 64 bits.** Si el
  expediente se lee bien y el diario no, es eso.

Requiere **Windows** y Gesia instalado. El expediente y el diario se leen en tu
equipo: **ningún dato del cliente auditado sale de ahí**.

## Qué incluye

| Skill | Qué hace | Entregable |
|---|---|---|
| **Cuadro de mando del diario** | Verifica el diario, lo concilia con los saldos del expediente y analiza punteo y apuntes atípicos | Panel HTML |
| **Revisión del contenido de la memoria** | Contesta el cuestionario de cuentas anuales a partir de las cuentas en PDF, justificando cada respuesta | Excel para importar en Gesia + papel en Word |
| **Cancelación de saldos** | Empareja las facturas de una cuenta con sus pagos o cobros y deja a la vista lo que queda pendiente de verdad. Respeta el punteo que ya trae el diario y completa el resto | Papel de trabajo en Excel |
| **Continuidad de saldos de apertura** | Compara cuenta por cuenta la apertura del diario con el cierre auditado del ejercicio anterior (NIA-ES 510) | Papel de trabajo en Excel |
| **Identificación de riesgos** | Elige los riesgos del encargo del catálogo de tu máster, a partir del balance, la cuenta de resultados y los ratios de los cinco ejercicios (NIA-ES 315) | Informe en Word |
| **Investigación de la entidad** | Investiga al cliente en fuentes públicas de internet —BORME, contratación pública, subvenciones, jurisprudencia y prensa— con tres agentes en paralelo, citando cada hecho a su fuente y declarando lo que no consta | Papel de trabajo en Word + evidencia JSON |
| **Registro de ejecución** | Escribe en el chat, de forma anónima, cómo ha ido un procedimiento: con qué tropezó y qué convendría mejorar. Sirve para reportarnos incidencias sin tener que explicarlas | Texto en el chat |

Los entregables se escriben en `InformesGesia\<carpeta del procedimiento>`
dentro de la carpeta del propio expediente, para que estén donde los esperas.

Para la identificación de riesgos hace falta además **la ruta de tu máster de
Gesia**, el `.gs3` que lleva `CON RIESGOS` en el nombre: los riesgos se eligen de
tu propio catálogo, no de uno que venga con el plugin. **No hay que abrirlo en
Gesia**, basta con indicar dónde está.

## Cómo pedirlo

No hace falta recordar nombres. Basta decir lo que quieres:

- «lanza el cuadro de mando del diario»
- «revisa la memoria de este cliente» (adjuntando las cuentas anuales en PDF)
- «comprueba los saldos de apertura»
- «identifica los riesgos de este encargo»
- «investiga a este cliente en fuentes públicas»

## Lo que estos papeles son, y lo que no

Son **propuestas de papel de trabajo**. Las cifras salen del expediente y de tu
diario, y cada comprobación dice de dónde sale; pero la valoración, el alcance y
la conclusión son del auditor, que es quien firma. Ningún papel se entrega sin
que se hayan contado los avisos que hayan salido durante su preparación.

## Versión publicada

**1.8.0** — las pruebas de ForSampling **leen las facturas con un agente lector**, por lotes y
en paralelo. Las páginas escaneadas se miran igual, pero fuera del contexto principal: en una
MUM de 42 elementos la lectura pasó de unos diez minutos a menos de dos. El lector recibe el
nombre de la entidad auditada para no confundir el lado del documento en una prueba de
ventas, no toca la muestra y no opina. Además: el papel no repite el tipo de prueba en el
nombre, al terminar se imprime un bloque con los avisos y hallazgos para trasladarlos tal cual,
el inventario de la carpeta lista los ficheros que no son PDF en vez de omitirlos, y los
ejemplos de los skills usan valores sintéticos.

**1.7.0** — el plugin **lee ForSampling**, el módulo de muestreo de la suite de Gesia, y
trae los dos primeros skills sobre sus pruebas. Desde el expediente (`.gs3`) deduce solo el
cliente de muestreo (`.cli`) vinculado, y con él las pruebas, la muestra seleccionada, sus
parámetros y la evaluación del auditor.

- **Prueba de cumplimiento** (`fsp-cumplimiento`): localiza el documento de cada elemento
  seleccionado entre las facturas escaneadas, comprueba lo que se puede comprobar desde el
  documento —que existe, que base + IVA = total, que importe y fecha coinciden con libros— y
  propone la observación para ForSampling con la fórmula «Asistente IA: A1: Ok · A2: … · A3:
  auditor». Las casillas de atributo se dejan en blanco: rellenarlas es concluir.
- **Prueba MUM** (`fsp-mum`): mide el importe que sostiene cada documento y propone las tres
  columnas de ForSampling —saldo según auditoría, error y tasa—. El término de comparación
  (base, total o neto) lo deduce de la propia muestra. **No proyecta el error, no lo compara
  con el error tolerable y no netea**: eso lo hace ForSampling.

Las facturas escaneadas las lee el propio modelo, página a página; los scripts inventarían la
carpeta, renderizan solo la primera página de cada documento y cruzan con la muestra. Se
comprueba la aritmética con retención de IRPF y con exenciones, y cuando un elemento se queda
sin documento y sobra uno del mismo tercero, el papel lo señala como posible diferencia real.

El programa que lee el expediente pasa a **1.9.3**: además de ForSampling, `configurar` deja
de afirmar cosas del expediente cuando no ha podido abrir el fichero.

**1.6.4** — la **cancelación de saldos deja fuera las cuentas que ya cierran a cero**.
Antes el papel llevaba una hoja por cuenta del grupo pedido, y muchas eran hojas que se
abren para no encontrar nada. Medido sobre un grupo 43 completo: de todas sus cuentas
quedaban **17** con saldo vivo. El umbral es medio céntimo, por debajo de eso el saldo es
residuo de redondeo.

Y un aviso que faltaba: **si el expediente está en OneDrive**, el entorno puede rechazar
la escritura del papel antes de ejecutar nada y pedir autorización expresa. No es un
fallo; hay que concederla y repetir la orden.

Las dos cosas se habían probado en agosto pero solo habían llegado al canal de ChatGPT.

**1.6.3** — retoques de redacción en los comentarios del código. **Sin cambios de
comportamiento**: los papeles salen exactamente igual que con la 1.6.2.

**1.6.2** — afina la **revisión del contenido de la memoria** a partir de una segunda
calibración sobre un expediente real: 137 preguntas contestadas leyendo solo las cuentas
anuales en PDF. El **86 %** coincidió con las respuestas del auditor en lo que importa —si
la pregunta arroja hallazgo o no—, y **ninguna** discrepancia fue de las peligrosas, esas
en las que el plugin da por bueno un desglose que falta.

Lo que cambia: **la frontera entre «Sí» y «No aplica» deja de perseguirse.** Los dos
códigos significan lo mismo para el trabajo —esta pregunta no arroja hallazgo— y cuál se
pone es convención de quien contesta; se comprobó que no se puede deducir de la memoria.
Antes el plugin gastaba media página de instrucciones en esa frontera y seguía fallándola.
A cambio, las instrucciones son más cortas y el esfuerzo va a donde está el valor.

Lo que no cambia, porque ahí sí hay criterio: si contestar exige saber algo que no está en
las cuentas anuales, la respuesta es **«Pendiente»**, nunca «No aplica». Y en esa misma
calibración el plugin señaló **19 desgloses que el auditor no había marcado**, cuatro de
ellos cuadres que no salen. Son propuestas: las valora quien firma.

**1.6.1** — corrige la **escala de valoración de riesgos**, que estaba invertida. Los
códigos van `1 = Máximo · 2 = Alto · 3 = Moderado · 4 = Poco`, y el plugin los leía al
contrario: un riesgo valorado como máximo se imprimía como «poco». Afecta a los tres
valores de cada ficha —inherente, de control y de incorrección material— en el informe de
identificación de riesgos.

**Si has generado ese informe antes de hoy, sus valoraciones están invertidas y conviene
regenerarlo.** El resto del papel —riesgos elegidos, cifras, procedimientos— no se ve
afectado.

Queda escrita la trampa que lo causó: en el mismo expediente hay dos escalas de cuatro
niveles con la misma forma y sentidos opuestos, así que ninguna se deduce de la otra.

Sigue todo lo de la 1.6.0: el plugin lee también los ficheros de **AudiQ**, el sistema de
gestión y control de calidad de la firma (`.qat` y `.qal`), y adapta de qué habla según el
fichero; y devuelve los **ficheros vinculados con su ruta ya resuelta** —modelos,
plantillas, cartas, papeles—, tanto en un manual como en un expediente.

El programa que lee el expediente pasó a **1.8.0** en esa versión, y desde la 1.5.6 lleva su versión en
el nombre para que actualizar con el plugin en marcha ya no falle.

## Soporte

Ensys Consultores Informáticos, S.L. · [Incidencias](https://github.com/Ensys-Consultores-Informaticos/claude-plugins/issues)
