# Dark Web Finder

Herramienta diseñada por **CodeRonin** para la recolección autorizada de enlaces `.onion` usando motores como Ahmia u OnionLand. Está pensada para apoyar ejercicios de contrainteligencia y monitoreo de amenazas dentro de un marco legal y ético.

## Advertencia legal

- No somos responsables del uso inadecuado de esta herramienta.
- Rutea todo el tráfico mediante TOR o infraestructura controlada antes de visitar cualquier enlace.
- Respeta regulaciones locales y políticas internas; este código es solo para fines de capacitación.
- Marca: CodeRonin — síguenos en IG `@code_ronin` y TikTok `@code.ronin`.

## Requisitos

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso (CLI)

```
python3 darkwebfinder.py -h
```

Ejemplos:

- Buscar enlaces relacionados con cualquier tema, por ejemplo tarjetas de crédito, y guardarlos en TXT:

  ```
  python3 darkwebfinder.py -f "credit cards" --format txt
  ```

- Buscar fugas de ransomware, limitar a 30 resultados y exportar a XML:

  ```
  python3 darkwebfinder.py -f ransomware --limit 30 --format xml
  ```

- Cambiar de motor de búsqueda (OnionLand) y mostrar los hallazgos en pantalla:

  ```
  python3 darkwebfinder.py -f "database dump" --engine onionland --print
  ```

- Automatizar un reporte (omitiendo la confirmación interactiva) y mostrar los enlaces en consola:

  ```
  python3 darkwebfinder.py -f "database dump" --skip-confirm --print
  ```

## Próximos pasos sugeridos

- Agregar registro (logging) y almacenamiento cifrado según las políticas de tu organización.
- Integrar verificación de conectividad TOR antes de realizar búsquedas.
