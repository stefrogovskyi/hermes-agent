---
name: sketchforge-3d
description: "Control local SketchForge 3D CAD editor via MCP server."
version: 1.0.0
author: Formsmith746 & Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [3d, cad, modeling, stl, mcp, sketchforge, threejs]
    category: creative
    homepage: https://github.com/Formsmith746/SketchForge-3D
    related_skills: [architecture-diagram, sketch]
---

# SketchForge-3D CAD & MCP Automation

Inspect and control the live browser-based 3D CAD editor SketchForge via its local MCP bridge (`scripts/sketchforge-mcp-server.mjs`).

## When to Use

Use this skill whenever:
- You need to generate, inspect, or modify 3D models (primitives, cuts, holes, booleans, fillets, chamfers).
- Exporting 3D geometry to STL, OBJ, or STEP formats for 3D printing.
- Inspecting active 3D scenes in the SketchForge editor tab.

## Running Service & MCP Bridge

- **Web Studio Endpoint:** `http://100.99.146.42:3030/` or `http://38.49.219.217:3030/`
- **Systemd Daemon:** `sketchforge.service` (Active on port 3030)
- **Local MCP Script:** `/opt/sketchforge-3d/scripts/sketchforge-mcp-server.mjs`

### Available MCP Actions
- `sketchforge_list_editors`: List active open editor sessions
- `sketchforge_read_scene`: Read scene graph and object hierarchy
- `sketchforge_create_shape`: Create primitives (box, cylinder, sphere, wedge, text)
- `sketchforge_update_object`: Update transform, rotation, scale, color, or hole-mode
- `sketchforge_apply_edge_treatment`: Apply fillet or chamfer to CAD edges
- `sketchforge_capture_image`: Capture viewport screenshot for visual validation
