# Case: Navo24 PPTX Presentation & Design System Automation

## Summary
- **Date**: 2026-08-03
- **Domain**: business
- **Context**: Generating professional presentation decks from Excel data matching Navo24 design standards.

## Symptom / Challenge
- Automated PowerPoint generation truncated numerical data and created non-scrollable/broken slide transitions on slide 11.

## Solution & Method
- Built `build_navo24_pptx_presentation.py` to convert `Для презентации.xlsx` rows into python-pptx slide elements.
- Applied Navo24 color palette, Tahoma font hierarchies, and auto-calculating text frame bounding boxes.
- Created `fix_slide11_to_pptx.py` to fix multi-column table layout and numerical padding.

## Key Lesson
- When building PowerPoint slides programmatically, explicitly calculate font sizes and text box height bounds to prevent truncation of numbers and titles.
