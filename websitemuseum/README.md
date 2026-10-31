# ATELIER Virtual Museum

Open index.html in your browser. No installation, API keys, or build step required.

Alternatively, serve the folder:
    python -m http.server 8000
Then open http://localhost:8000

Controls
- Click Step inside.
- WASD: walk. Up/down arrows: walk. Left/right arrows: turn.
- Drag: look around. E: inspect a nearby artwork.
- On mobile: arrow buttons to walk; swipe to turn.
- The collection: open any artwork directly.

All HTML, CSS, and JavaScript are in index.html.
The 3D perspective is rendered with the Canvas 2D API.
Paintings are generated locally by JavaScript. No external assets or libraries.
This is a frontend project; it has no database or backend.

Customize names and desc arrays for exhibit text, pals for artwork colors,
and build() for room geometry. CSS is in the style element.
