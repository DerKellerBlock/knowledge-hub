# Explanation: Visual Question Answering via MCP

**Task-ID:** visual-question-answering
**Datum:** 2026-07-07

Anfängerfreundliche Erklärung der geänderten Dateien, der OpenCode-
Konfiguration, der Agenten, der Validierungsbefehle und der
Knowledge-QA-Abläufe.

## Was das Feature macht

Bisher konnte `search_knowledge` nur Text-Queries verarbeiten. Wenn ein
Nutzer in OpenCode ein Bild hochlädt und eine Frage dazu stellt (z.B.
„was ist das rechts unten bei Scope?"), konnte das LLM das Bild nicht
lesen → „this model does not support image input" Error.

Mit VQA reicht das LLM den Bild-Pfad an `search_knowledge(image_path=...)`
weiter. Der Knowledge Hub:

1. Lädt das Bild mit PIL.
2. Embeddet es mit SigLIP-2 (demselben Modell, das auch die DaVinci-
   Screenshots indexiert hat — sie leben im selben Vektorraum).
3. Sucht in ChromaDB `<domain>_images` (modality="image") per Cosine-
   Similarity nach den ähnlichsten Screenshots.
4. Gibt die Captions + Seitenzahlen der ähnlichsten Screenshots zurück.
5. Das LLM nutzt die Captions, um zu erklären was auf dem Nutzer-Bild
   zu sehen ist.

## Geänderte Dateien

### Code

| Datei | Änderung | Zweck |
|-------|----------|-------|
| `scripts/hybrid_search.py` | Neue Funktion `image_similarity_search()` (vor `rrf_fusion_4list`); `search()` um `image_path` Parameter erweitert mit Merge-Block am Ende | Kern-Logik: Bild embedden + ChromaDB query + image_match Treffer voranstellen |
| `mcp_servers/knowledge_hub/tools.py` | `search_knowledge()` um `image_path: str \| None = None` erweitert; reicht an `hybrid_search.search()` durch | MCP-Tool-Funktion erhält neuen Parameter |
| `mcp_servers/knowledge_hub/server.py` | `inputSchema` für `search_knowledge` um `image_path` Property erweitert (optional, nicht in `required`); `call_tool_handler` reicht `image_path` durch; Description aktualisiert | MCP-Tool-Schema deklariert neuen Parameter |
| `.opencode/agents/orchestrator-knowledge.md` | Neue Sektion „Visual Question Answering (Bild-Queries)" vor dem Untrusted-Quelleninhalt-Block | Orchestrator-Agent wird instruiert, image_path an search_knowledge weiterzugeben |

### Tests

| Datei | Änderung |
|-------|----------|
| `tests/unit/test_image_similarity.py` | NEU — 8 Unit-Tests: graceful errors, mocked ChromaDB, search_knowledge backward-compat, search() image_path propagation |

### Doku

| Datei | Änderung |
|-------|----------|
| `docs/ai/architecture.md` | Neue Sektion „Visual Question Answering (2026-07-07)" mit VQA Pipeline, search_knowledge image_path Integration, Modality-Werte Tabelle, Performance, MiniMax deferred |
| `docs/ai/best-practices.md` | Neue Sektion „Visual Question Answering (image_path, 2026-07-07)" mit Usage-Beispiel, Cache-Verhalten, Graceful Fallback, Einschränkungen |
| `docs/ai/known-issues.md` | Neue Sektion „Visual Question Answering (2026-07-07)" mit VQA-001 bis VQA-005 (nur DaVinci, keine OCR, Caption-basiert, MiniMax deferred, prepend bis 2*top_k) |
| `docs/issues/visual-question-answering/retrospective.md` | NEU — Retrospektive |
| `docs/issues/visual-question-answering/explanation.md` | NEU — diese Datei |

## OpenCode-Konfiguration

Die OpenCode-Konfiguration lebt in `.opencode/opencode.json`. Die
Agenten-Prompts sind in `.opencode/agents/*.md` ausgelagert (nicht
inline in `opencode.json`).

Für VQA relevant:

- `.opencode/agents/orchestrator-knowledge.md` — der Orchestrator-Agent
  hat jetzt eine VQA-Sektion die ihn instruiert, bei Bild-Uploads den
  `image_path` an `search_knowledge` weiterzugeben.
- Der MCP-Server `knowledge_hub` exponiert `search_knowledge` mit dem
  neuen optionalen `image_path` Parameter. Keine Änderung an
  `opencode.json` nötig — das Tool-Schema wird vom Server dynamisch
  deklariert.

## Validierungsbefehle

```bash
# Python-Syntax-Check aller Skripte + MCP-Server
.venv/bin/python -m py_compile scripts/*.py mcp_servers/knowledge_hub/*.py

# Unit-Tests (234 Tests, ~3.5s)
.venv/bin/pytest -m unit -q

# Workspace-Check (Struktur, JSON, Shell-Syntax)
./scripts/workspace_check.sh

# MCP-Server Quick-Test (Tool-Liste zeigt image_path)
.venv/bin/python -c "
import asyncio, json
from mcp_servers.knowledge_hub.server import list_tools_handler
tools = asyncio.run(list_tools_handler())
for t in tools:
    if t.name == 'search_knowledge':
        print('image_path' in t.inputSchema['properties'])
"

# Integration-Test (manuell, echtes Bild)
KH_MULTIMODAL_DEVICE=mps .venv/bin/python -c "
import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, '.')
from hybrid_search import image_similarity_search
img = 'domains/davinci_resolve/images/davinci-resolve-20.3-reference-manual/DaVinci_Resolve_20.3_Reference_Manual.pdf-3084-0.png'
results = image_similarity_search('davinci_resolve', img, top_k=5)
print(f'Got {len(results)} results, top-1 sim={results[0][\"similarity_score\"]}')
"
```

## Knowledge-QA-Ablauf

VQA ist ein Code-Feature (keine neuen Quellen, keine neuen Indizes).
Deshalb ist der Real-World-Test-Workflow nicht anwendbar (keine neuen
Domain-Quellen). Der Quality-Check erfolgte über:

1. **Unit-Tests** (`tests/unit/test_image_similarity.py`): 8 Tests mit
   mocked ChromaDB + mocked SigLIP-2 — testen graceful errors, korrekte
   Sortierung, backward-compat, image_path propagation.
2. **Manualer Integration-Test** (Task 6): echtes DaVinci-Screenshot
   als Query-Bild → Top-1 sim=1.0 (dasselbe Bild), Top-2/3 = ähnliche
   Color Wheels Panels aus anderen DaVinci-Kapiteln. Bestätigt dass
   SigLIP-2 + ChromaDB + Cache + Metadata-Enrichment funktionieren.

## Architektur-Entscheidungen

1. **SigLIP-2 für Query-Image-Embedding** (gleicher Vektorraum wie
   indexierte Screenshots). Alternative wäre ein separater Image-Encoder
   gewesen, hätte aber einen Vektorraum-Mismatch verursacht.
2. **`modality="query_image"` im Cache** (nicht `"image"`): verhindert
   Cache-Kollisionen zwischen Query-Image-Embeddings und indexierten
   Screenshot-Embeddings.
3. **`image_match` Treffer werden PREPENDED** (additiv, bis top_k):
   kombinierte Liste kann bis 2*top_k enthalten. Alternative wäre ein
   Merge-in-place gewesen, hätte aber image_match Treffer mit
   Text-Treffern um Ränge konkurrieren lassen. Prepend garantiert dass
   die ähnlichsten Screenshots am Anfang stehen.
4. **MiniMax M3 deferred:** Caption-basierte Antwort funktioniert ohne
   Vision-LLM. MiniMax M3 würde Antwortqualität bei niedriger Similarity
   verbessern, ist aber ohne API-Key nicht testbar.

## Siehe auch

- `docs/issues/visual-question-answering/spec.md` — Vollständige Spec
- `docs/issues/visual-question-answering/plan.md` — 8-Task-Plan
- `docs/ai/architecture.md` — VQA Pipeline Sektion
- `docs/ai/best-practices.md` — image_path Usage
- `docs/ai/known-issues.md` — VQA-001 bis VQA-005 Limitations
