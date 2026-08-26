# Case: SketchForge-3D Local CAD Editor with MCP Bridge Integration

- **Date:** 2026-08-25
- **Category:** agent_club / creative
- **Status:** SUCCESS
- **Domain Link:** `ops_infrastructure.md`

## Problem & Context
The user needed a fast, browser-based 3D CAD modeling environment that supports local geometry creation and programmatic control by AI agents without heavy software (Blender/Fusion360) or closed cloud lock-in (Tinkercad).

## Solution & Architecture
1. **Engine & Stack:** Deployed `Formsmith746/SketchForge-3D` under `/opt/sketchforge-3d` (Next.js 15, React 19, Three.js, OCCT-WASM, Manifold CSG engine for boolean operations).
2. **Daemon Service:** Created systemd service `sketchforge.service` running on port `3030` (`active (running)`, auto-start on boot).
   - Tailscale access: `http://100.99.146.42:3030/`
   - Direct IP access: `http://38.49.219.217:3030/`
3. **Model Context Protocol (MCP) Bridge:** Built-in MCP server (`scripts/sketchforge-mcp-server.mjs`) exposes native tools to AI agents:
   - Inspection: `sketchforge_read_scene`, `sketchforge_list_objects`, `sketchforge_list_edges`.
   - Manipulation: `sketchforge_create_shape`, `sketchforge_update_object`, chamfer/fillet, hole cutting.
   - Vision validation: `sketchforge_capture_image` (renders viewport for multimodal feedback).
4. **Hermes Skill:** Registered skill `sketchforge-3d` at `/opt/hermes/skills/creative/sketchforge-3d/SKILL.md`.

## Verification
- Verified service state with `systemctl status sketchforge.service`.
- Web UI accessible on port 3030.
- Skill tested and registered in skill registry.
