# ADR: AGPL Process Boundary for PyMuPDF

**Date:** 2026-06-27
**Status:** Accepted

## Context
PyMuPDF und PyMuPDF4LLM stehen unter AGPL-3.0 (starkes Copyleft). Der
Knowledge Hub ist MIT-lizenziert und öffentlich auf GitHub. Ein direkter
`import pymupdf` im Runtime-Code würde ein abgeleitetes Werk erzeugen und
den gesamten Knowledge Hub unter AGPL zwingen — inkompatibel mit MIT.

## Decision
PyMuPDF4LLM wird NUR im separaten Build-Script
`scripts/parse_pdf_to_markdown.py` verwendet, das per subprocess aufgerufen
wird. Der MIT-lizenzierte Runtime-Code liest nur fertige `.md`-Dateien und
importiert niemals PyMuPDF. Diese "Process Boundary" ist der Standardweg
für AGPL/GPL-Dependencies in MIT-Projekten (analog GCC aus proprietären
Build-Systemen).

## Consequences
- `requirements.txt` (MIT-Runtime) enthält kein pymupdf.
- `requirements-pdf.txt` (AGPL-Build-Tool) enthält pymupdf + pymupdf4llm.
- `scripts/parse_pdf_to_markdown.py` hat AGPL-3.0 SPDX-Header.
- `THIRD_PARTY_LICENSES.md` dokumentiert die Trennung.
- PDFs werden einmalig konvertiert, danach ist PyMuPDF nicht mehr nötig.
- Die Lizenz-Trennung ist verbindlich — keine Ausnahme.