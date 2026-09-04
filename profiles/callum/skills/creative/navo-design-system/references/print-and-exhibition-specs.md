# Print, Exhibition & Conference Stand Specifications (Web Summit & Expos)

Authoritative guide for preparing physical stand banners, exhibition boards, and print-ready vector assets for Navo24.

---

## 1. Web Summit & Conference Exhibition Boards

### 1.1 Technical Format Requirements
- **Required File Format:** Strictly **EPS (Encapsulated PostScript)** with `EPSF-3.0` conformance.
- **Maximum File Size:** Under 10MB (clean vector EPS files are typically 5KB - 50KB).
- **Color Space Requirement:** **100% Pure CMYK Process Colors** (`setcmykcolor`). Files containing RGB (`setrgbcolor`) or mixed spaces (`setgray` + `setrgbcolor`) trigger pre-flight warnings on conference portals.
- **Header Standard:**
  ```ps
  %!PS-Adobe-3.0 EPSF-3.0
  %%Creator: cairo 1.18.0
  %%DocumentProcessColors: Cyan Magenta Yellow Black
  %%Pages: 1
  %%BoundingBox: llx lly urx ury
  %%LanguageLevel: 2
  %%EndComments
  ```

### 1.2 Logo Selection for Print Banners
- **White / Light Backgrounds (e.g. Web Summit ALPHA Boards):**
  - Use the **Primary NAVO Dark Wordmark** (`#111111` or `#000000`) paired with the multi-color concentric target `o`.
  - Target ring hierarchy on light surfaces:
    - Outer ring: Deep Royal Blue (`#113EC9`)
    - Ring 2: Electric Cobalt (`#1F4FE6`)
    - Ring 3: Rate Red (`#E2231A`)
    - Ring 4: Signal Orange (`#FF8135`)
    - Inner center: Pure White (`#FFFFFF`) or Dark (`#111111`).
- **Dark Backgrounds (Graphite `#181818` / Navy `#0A1117`):**
  - Use the **Pure White Wordmark** (`#FFFFFF`) with the multi-color concentric target and white center point.

---

## 2. Generating 100% Pure CMYK EPS for Pre-Flight Compliance

When print pre-flight validators flag:
- *"Warning: This file uses RGB colors"*
- *"Warning: This file uses multiple color spaces"*

Execute this conversion script to output single-space CMYK PostScript:

```python
import re

def convert_eps_to_pure_cmyk(input_eps_path, output_eps_path):
    with open(input_eps_path, "r") as f:
        eps = f.read()

    # 1. Enforce EPSF-3.0 and Process Colors declaration
    if "%!PS-Adobe-3.0 EPSF-3.0" not in eps:
        eps = eps.replace("%!PS-Adobe-3.0", "%!PS-Adobe-3.0 EPSF-3.0", 1)

    process_header = "%%DocumentProcessColors: Cyan Magenta Yellow Black\n%%DocumentCustomColors:"
    if "%%DocumentProcessColors:" not in eps:
        eps = eps.replace("%%EndComments", process_header + "\n%%EndComments", 1)

    # 2. Bind CMYK operator in PostScript prolog and eliminate RGB/Gray definitions
    eps = eps.replace("/rg { setrgbcolor } bind def", "/k { setcmykcolor } bind def", 1)
    eps = eps.replace("/g { setgray } bind def", "% /g remapped to cmyk", 1)

    # 3. Map all brand colors to exact Process CMYK values
    # Wordmark Black: 100% Process Black (avoids misregistration)
    eps = re.sub(r"0(\.0+)?\s+g\b|0\.0666667\s+g\b", "0 0 0 1 k", eps)
    # Royal Blue (#113EC9) -> C:91% M:69% Y:0% K:21%
    eps = re.sub(r"0\.0666667\s+0\.243137\s+0\.788235\s+rg\b", "0.91 0.69 0 0.21 k", eps)
    # Cobalt Blue (#1F4FE6) -> C:86% M:66% Y:0% K:10%
    eps = re.sub(r"0\.121569\s+0\.309804\s+0\.901961\s+rg\b", "0.86 0.66 0 0.10 k", eps)
    # Rate Red (#E2231A) -> C:0% M:85% Y:88% K:11%
    eps = re.sub(r"0\.886275\s+0\.137255\s+0\.101961\s+rg\b", "0 0.85 0.88 0.11 k", eps)
    # Signal Orange (#FF8135) -> C:0% M:61% Y:86% K:0%
    eps = re.sub(r"1\s+0\.505882\s+0\.207843\s+rg\b", "0 0.61 0.86 0 k", eps)
    # Pure White Center -> C:0% M:0% Y:0% K:0%
    eps = re.sub(r"1(\.0+)?\s+g\b", "0 0 0 0 k", eps)

    with open(output_eps_path, "w") as f:
        f.write(eps)

    print(f"Successfully exported pure CMYK EPS to {output_eps_path}")
```

### 2.1 Ghostscript Verification Command
Verify CMYK rasterization without errors at 300 DPI:
```bash
gs -sDEVICE=pngalpha -r300 -o preview_300dpi.png file_cmyk.eps
```

---

## 3. Exhibition Board Copywriting & Stand Descriptions

Conference attendees spend 2-3 seconds glancing at stand banners. Avoid generic buzzword stuffing ("Ultimate AI First Digital Solutions..."). Use proven formulations from the Brandbook:

- **Formula 1 (Product & Protocol Native - Recommended):**
  > "One intelligent layer for global ocean & air freight. Composable MCP tools and APIs for container tracking, schedules, and spot rates."
- **Formula 2 (Autonomous Logistics / Operational):**
  > "Plan less. Move smarter. Autonomous logistics intelligence connecting 100+ ocean lines, schedules, and real-time container tracking."
- **Formula 3 (Developer & Enterprise AI):**
  > "The MCP-native freight infrastructure. Real-time container tracking, AIS milestone detection, and spot rates your AI agents can call directly."
