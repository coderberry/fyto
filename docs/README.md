# Fyto Documentation Website

This directory contains the GitHub Pages website for the Fyto project.

## Contents

- `index.html` - Main project website with interactive features
  - **Animated emotions on hover** - Cycles through actual emotion frames
- `wiring-diagram.html` - Detailed wiring guide with connection tables
- `diagrams/` - SVG wiring diagrams and schematics
- `emotions/` - Sample emotion animation frames (60 frames per emotion, ~2MB total)
- `generate_schematic.py` - Script to regenerate schemdraw diagrams
- `_config.yml` - GitHub Pages configuration
- `.nojekyll` - Ensures all files are served by GitHub Pages

### Emotion Animations

The website includes hover animations for each emotion card. When you hover over an emotion, it plays the actual animation frames from the Fyto display. To keep the repository size manageable, we include every 3rd frame (60 frames per emotion instead of the full 180).

## Local Preview

To preview the website locally:

```bash
# From the docs directory
python3 -m http.server 8000

# Then open http://localhost:8000 in your browser
```

## Publishing to GitHub Pages

1. Push this repository to GitHub
2. Go to repository **Settings** → **Pages**
3. Under **Source**, select:
   - Branch: `main` (or your default branch)
   - Folder: `/docs`
4. Click **Save**

Your site will be available at: `https://[username].github.io/[repo-name]/`

## Regenerating Diagrams

The schemdraw-generated diagrams can be regenerated with:

```bash
# From the project root
uv run docs/generate_schematic.py

# Or from the docs directory
uv run generate_schematic.py
```

This will regenerate:
- `diagrams/fyto_schematic.svg` - Circuit schematic
- `diagrams/fyto_pinout.svg` - GPIO pinout reference

The hand-crafted `diagrams/fyto-wiring.svg` is static and should be edited manually if needed.

## Editing the Website

### Main Landing Page (`index.html`)
- Modern single-page design
- Tabbed wiring diagram viewer
- Emotion showcase
- Hardware requirements
- Quick start guide

### Detailed Wiring Page (`wiring-diagram.html`)
- Full-screen wiring diagram
- Color-coded connections
- Interactive hover effects
- Connection reference tables
- Important safety notes

## Dependencies

The website is pure HTML/CSS/JavaScript with no build step required. The only dependency is for regenerating diagrams:

- Python 3.9+
- schemdraw (installed automatically by `uv run`)

## Browser Support

The website works in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (responsive design)
