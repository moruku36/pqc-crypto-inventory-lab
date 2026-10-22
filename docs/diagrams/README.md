# Rebuild the architecture SVG

Source: [`architecture-overview.mmd`](architecture-overview.mmd). Renderer: [Obsidian Pele 1.8.0](https://github.com/obsidianmd/pele/tree/1.8.0), published bundle at `https://cdn.jsdelivr.net/npm/pele@1.8.0/dist/pele.js`. SHA-256 of that exact bundle: `30d94f823025c873abb2ec3676e34124e543583731e228ca957f51ddda415a05` (695,333 bytes). The script verifies bytes before executing them. It adds light/dark CSS during generation and checks a byte-for-byte match with the committed SVG.

From the repository root, with Node 20+:

```sh
node docs/diagrams/render.mjs
node docs/diagrams/render.mjs --check
```

For offline reproduction, download the exact bundle and pass `--bundle PATH` to either command. Keep the checksum gate. Do not edit the SVG alone; edit the Mermaid source or generator and regenerate it. The SVG uses a 227 px wide vertical layout and scales to its container. Its XML, text, light/dark variables and responsive size were inspected statically. Foreground versus surface contrast is 15.00:1 in light mode and 11.79:1 in dark mode by relative-luminance calculation. An interactive browser rendering check is still needed.
