<p align="center">
  <img src="assets/banner.png" alt="Aeropuerto voxel de noche con maletas, un portátil y una mascota voxel naranja" width="100%">
</p>

# Travel Planner Skill (español)

Una skill para agentes de IA que planea viajes de principio a fin: a dónde ir, cuánto cuesta de verdad hoy, cómo encaja con el calendario laboral y los festivos, dónde dormir, cómo llegar, un itinerario a pie y un calendario lleno de enlaces de mapas.

Nació de sesiones reales de planificación, así que recoge lo que de verdad falla: precios caducados, hostales con el dormitorio equivocado, viajes que cuestan un día de vacaciones, requisitos de entrada descubiertos tarde y herramientas que fallan.

> Language: [English](README.md)

## Qué incluye

- **Un flujo de trabajo** desde las preguntas iniciales hasta la lista de compra y la exportación al calendario.
- **Reglas de verificación:** etiquetar cada cifra como `verified`, `from-price` o `estimate`; comprobar en vivo; probar fechas alternativas.
- **Lógica de calendario:** festivos nacionales, autonómicos y locales, días de teletrabajo, puentes y la regla del "viaje gratis".
- **Búsqueda eficiente:** URLs deterministas, búsquedas en paralelo, primero lo barato, extracción compacta.
- **Herramientas y MCPs:** qué usar para normas, precios, calendario y borradores, y cómo manejar los fallos.
- **Diseño de itinerarios** para fotógrafos y videógrafos, con un prompt para otros asistentes.
- **Seguro por defecto:** prepara y abre páginas, nunca paga, envía ni confirma por el viajero.
- **Constructor de URLs probado:** Google Flights, Booking, Hostelworld y Google Maps (con enlace "ir ahora" sin origen).

## Instalación

```bash
git clone https://github.com/ludodelot/travel-planner-skill
cd travel-planner-skill
./install.sh        # copia la skill a ~/.claude/skills/travel-planner
```

Inicia una sesión nueva de Claude Code y pide, por ejemplo: "Tengo un finde largo en noviembre, presupuesto 300, me gusta la fotografía y caminar. Ayúdame a elegir y preparar las compras".

Para el modo navegador y la exportación al calendario, conecta las herramientas descritas en [references/setup-and-mcps.md](references/setup-and-mcps.md).

## Compartir con amigos

El repositorio puede seguir privado: añade a tus amigos como colaboradores en GitHub, ellos hacen `gh auth login`, clonan y ejecutan `./install.sh`. No contiene datos personales, así que podría hacerse público más adelante sin limpiar nada. Cada persona guarda su propio perfil de viajero ([plantilla](templates/traveler-profile.md)) en sus notas.

## Modo navegador

La skill abre pestañas **nuevas** de Chrome, listas para comprar (tren, hostales, autorizaciones de entrada), rellena formularios solo con tu confirmación y se detiene antes de aceptar y enviar. Tú pagas, envías y aceptas.

## Estructura

Consulta el árbol en [README.md](README.md#structure). Todo el contenido de `references/`, `templates/` y `examples/` está en inglés para que cualquier agente lo use.

## Principios

1. Verificar antes de recomendar: fechas y fuentes.
2. Adaptar el viaje al calendario del viajero.
3. Recomendar una opción, mostrar las alternativas y señalar lo no verificado.
4. El viajero paga, envía y confirma; el agente prepara.
5. Cero datos personales en notas, calendarios o este repositorio.

## Licencia

MIT. Ver [LICENSE](LICENSE).
