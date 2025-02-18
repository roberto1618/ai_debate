# 🤝 **DebateAI: La Batalla de las IAs**

## ✨ **¿Qué es DebateAI?**

DebateAI es una aplicación que enfrenta a dos inteligencias artificiales en un debate estructurado. Cada IA defiende una postura opuesta sobre un tema determinado, generando un intercambio de argumentos enriquecedor y bien estructurado. Además, un supervisor AI resume la discusión y ofrece una conclusión imparcial.

**¡Genera un debate de absolutamente lo que quieras!**

## 💡 **Características Principales**

- 🧠 **Debates Automatizados**: Dos IAs intercambian argumentos sobre temas opuestos.
- ✨ **Moderador Inteligente**: Una IA supervisora resume y evalúa el debate.
- 📝 **Generación de Informe**: El debate se guarda en un archivo PDF.
- 🎧 **Salida de Voz**: Las intervenciones pueden ser escuchadas con generación de voz.
- ⚡ **Altamente Personalizable**: Define el número de intervenciones y los temas a debatir.

## 🗒 **Instalación y Uso**

### ⚡ **Requisitos Previos**

- Python 3.8+
- Librerías requeridas (instalar con `pip install -r requirements.txt`)
- Configuración de OpenAI/Azure para LLMs

### ⚙ **Configuración**

Asegúrate de configurar correctamente las variables de entorno con las credenciales correspondientes para utilizar el modelo LLM.

### ▶ **Ejecución del Debate**

Ejecuta el siguiente comando en la terminal para iniciar un debate entre dos ideas:

```bash
python main.py -i "Se deben pagar los máximos impuestos posibles en un país" -j "Hay que bajar los impuestos lo máximo posible" -n 16
```

Donde:

- `-i` es la idea que defenderá la primera IA.
- `-j` es la idea que defenderá la segunda IA.
- `-n` es el número de intervenciones en el debate.

## 🔎 **Funcionamiento Interno**

1. **Interlocutores AI**: Dos modelos LLM defienden posturas opuestas y alternan intervenciones.
2. **Resúmenes Dinámicos**: Se generan resúmenes cada 8 intervenciones para mantener la coherencia.
3. **Finalización y Supervisión**: Cuando se alcanza el límite de intervenciones, el supervisor AI concluye el debate y decide cuál de las dos ideas tiene mayor veracidad.
4. **Exportación a PDF**: Todas las intervenciones se guardan en un archivo PDF con un resumen final.
5. **Salida de Voz**: Se genera audio para cada intervención usando `pyttsx3`.

## 📈 **Ejemplo de Debate Generado**

```text
Interlocutor1: Con impuestos altos, el gobierno puede invertir en infraestructura, educación y salud de calidad. Esto crea empleos mejor pagados y reduce la desigualdad. Además, un país con buenos servicios públicos atrae inversiones extranjeras, lo que también dinamiza la economía.
Interlocutor2: Eso suena bien en teoría, pero en la práctica, muchos gobiernos no gestionan eficientemente esos fondos. Si los impuestos son más bajos, la gente puede elegir en qué invertir su dinero, apoyando empresas y servicios que realmente les benefician. Esto fomenta la competencia y mejora la calidad de los productos y servicios disponibles.
...
Supervisor: Después de revisar los argumentos presentados, me inclino más a favor de la idea de bajar los impuestos lo máximo posible. Los argumentos más originales e ingeniosos que apoyan esta postura incluyen:...
```

## 🔧 **Contribución y Mejoras**

Si quieres mejorar DebateAI, puedes:

- Agregar nuevos estilos de argumentación.
- Mejorar el modelo de generación de voz.
- Integrar otros LLMs para ampliar capacidades.

## 🗣️ **Cómo incluir más voces**

Se pueden incluir más voces en castellano en Windows de la siguiente forma:

1. Pulsa `Win + R`, escribe `regedit`, y navega a `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens`.
2. Observa las voces disponibles que tienes, y compáralas con las que aparecen en la ruta *SAPI5* `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens` (normalmente aparecen menos).
3. Escoge una voz en castellano de la primera ruta, y expórtala con, por ejemplo, el nombre `voz.reg`. Guárdala en una ruta donde encuentres el archivo fácilmente.
4. Abre el archivo con un *Bloc de Notas* y, en todos los lugares donde aparezca la ruta `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens`, cámbiala por `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens`. Guarda el archivo.
5. Ejecútalo con el *Editor de Registro*. Se añadirá la nueva voz a la ruta *SAPI5* y ya la podrás utilizar en tu aplicación de debates.😊
---

✨ **¡Pon a prueba tu DebateAI y descubre qué IA es más persuasiva!**
