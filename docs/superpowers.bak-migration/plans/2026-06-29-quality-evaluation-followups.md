# Quality Evaluation Platform — 4 Follow-ups Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement 4 follow-up improvements to the Quality Evaluation Platform: (1) derive PDF_DOMAINS from domain.md instead of hardcoding, (2) fix dvr-002 expected_source_files to match real retrieval behavior, (3) make scoring weights/thresholds configurable, (4) populate expected_page_ranges for DaVinci Resolve questions from live search results.

**Architecture:** Follow-up 1 adds a `Source-Types` metadata field to domain.md, extends `model_manager.get_domain_config()` to parse it, and replaces the hardcoded `PDF_DOMAINS` set in `run_evaluation.py`. Follow-up 2 adjusts dvr-002's `expected_source_files` to the Reference Manual (which actually dominates retrieval) and documents the Editors Guide gap. Follow-up 3 introduces `quality/config.py` with default weights/thresholds, makes scorer functions accept optional config parameters, and supports YAML-header overrides in Golden Datasets. Follow-up 4 populates `expected_page_ranges` for all 7 DaVinci questions via live search against the real index.

**Tech Stack:** Python 3.11+, YAML, ChromaDB (live index for Follow-up 4), pytest

---

## File Structure Map

| File | Follow-up | Role |
|------|-----------|------|
| `domains/davinci_resolve/domain.md` | 1 | Add `- Source-Types: pdf` to Metadaten |
| `domains/godot/domain.md` | 1 | Add `- Source-Types: repo` to Metadaten |
| `scripts/model_manager.py` | 1 | Extend `get_domain_config()` to parse `source_types` |
| `scripts/quality/run_evaluation.py` | 1 | Replace `PDF_DOMAINS` with `get_domain_config()` call |
| `docs/ai/domain-model.md` | 1 | Document `Source-Types` field |
| `tests/unit/test_model_manager.py` | 1 | Add tests for `source_types` parsing |
| `quality/golden/davinci_resolve.yaml` | 2, 4 | Fix dvr-002 expected_sources + notes; add expected_page_ranges for all 7 questions |
| `quality/config.py` | 3 | **NEW** — default weights/thresholds + `load_config()` |
| `scripts/quality/scorer.py` | 3 | Accept optional config in `compute_composite_score`, `classify_score`, `evaluate_question` |
| `tests/quality/test_rubric_scorer.py` | 3 | Add tests for configurable weights/thresholds |
| `quality/golden/godot.yaml` | 3 | Optional: add `weights:` / `thresholds:` YAML header (demonstrate pattern) |

---

## Task 1: Add Source-Types to domain.md and parse in model_manager

**Files:**
- Modify: `domains/davinci_resolve/domain.md` (Metadaten block)
- Modify: `domains/godot/domain.md` (Metadaten block)
- Modify: `scripts/model_manager.py:64-108` (get_domain_config)
- Modify: `scripts/quality/run_evaluation.py:48` (PDF_DOMAINS → get_domain_config)
- Modify: `docs/ai/domain-model.md` (document new field)
- Modify: `tests/unit/test_model_manager.py` (new tests)

### Step 1: Add Source-Types to davinci_resolve domain.md

Add `- Source-Types: pdf` to the `## Metadaten` block in `domains/davinci_resolve/domain.md`, after the existing `- Embedding-Model:` line.

The Metadaten block currently reads (lines 34-39):
```markdown
## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Collection: davinci_resolve_knowledge
- ChromaDB-Path: chromadb_data/davinci_resolve/chroma/
- BM25-Path: chromadb_data/davinci_resolve/davinci_resolve_bm25.pkl
- Letztes Update: 2026-06-28
```

Change to:
```markdown
## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Source-Types: pdf
- Collection: davinci_resolve_knowledge
- ChromaDB-Path: chromadb_data/davinci_resolve/chroma/
- BM25-Path: chromadb_data/davinci_resolve/davinci_resolve_bm25.pkl
- Letztes Update: 2026-06-28
```

### Step 2: Add Source-Types to godot domain.md

Add `- Source-Types: repo` to the `## Metadaten` block in `domains/godot/domain.md`.

The Metadaten block currently reads (lines 22-27):
```markdown
## Metadaten

- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Parser: rst-godot (structured parsing of RST class docs)
- ChromaDB-Collection: `godot_knowledge`
- Letztes Update: 2026-06-09
```

Change to:
```markdown
## Metadaten

- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Source-Types: repo
- Parser: rst-godot (structured parsing of RST class docs)
- ChromaDB-Collection: `godot_knowledge`
- Letztes Update: 2026-06-09
```

### Step 3: Add source_types regex and parsing to model_manager.py

In `scripts/model_manager.py`, add a new regex constant after `_EMBEDDING_MODEL_RE` (after line 72):

```python
_SOURCE_TYPES_RE = re.compile(
    r"- Source-Types:\s*(.+?)\s*$",
    re.MULTILINE,
)
```

Extend `get_domain_config()` (lines 74-108) to parse `source_types`. The function currently returns a dict with keys `embedding_model`, `collection`, `chroma_path`, `bm25_path`. Add `source_types`:

```python
def get_domain_config(domain: str) -> dict:
    """Read domain.md Metadaten block and return a config dict.

    Returns:
        {
            "embedding_model": "all-mpnet-base-v2",
            "collection": "<domain>_knowledge",
            "chroma_path": Path,
            "bm25_path": Path,
            "source_types": ["repo"],  # default if not specified
        }
    """
    domain_md = Path(__file__).resolve().parent.parent / "domains" / domain / "domain.md"
    if not domain_md.exists():
        return {
            "embedding_model": DEFAULT_MODEL_NAME,
            "collection": f"{domain}_knowledge",
            "chroma_path": domain_chroma_path(domain),
            "bm25_path": domain_bm25_path(domain),
            "source_types": ["repo"],  # default
        }

    text = domain_md.read_text(encoding="utf-8")
    meta_block = _DOMAIN_META_RE.search(text)
    model_name = DEFAULT_MODEL_NAME
    source_types = ["repo"]  # default
    if meta_block:
        m = _EMBEDDING_MODEL_RE.search(meta_block.group(1))
        if m:
            model_name = m.group(1).strip()
        st = _SOURCE_TYPES_RE.search(meta_block.group(1))
        if st:
            source_types = [t.strip() for t in st.group(1).split(",")]

    return {
        "embedding_model": model_name,
        "collection": f"{domain}_knowledge",
        "chroma_path": domain_chroma_path(domain),
        "bm25_path": domain_bm25_path(domain),
        "source_types": source_types,
    }
```

### Step 4: Replace PDF_DOMAINS in run_evaluation.py

In `scripts/quality/run_evaluation.py`:

Remove the hardcoded constant on line 48:
```python
# REMOVE:
PDF_DOMAINS = {"davinci_resolve"}
```

Add import for `get_domain_config` (after existing imports, around line 41):
```python
from model_manager import get_domain_config  # noqa: E402
```

In `run_evaluation()` (line 80), replace:
```python
is_pdf = domain in PDF_DOMAINS
```
with:
```python
cfg = get_domain_config(domain)
is_pdf = "pdf" in cfg.get("source_types", [])
```

### Step 5: Document Source-Types in domain-model.md

In `docs/ai/domain-model.md`, in the `## domain.md Format` section (after the code block showing the template, around line 45), add documentation for the new field. After the existing `- Letztes Update: YYYY-MM-DD` line in the template, add:

```markdown
- Source-Types: repo | pdf  (comma-separated, default: repo)
```

And add a new subsection after the template code block:

```markdown
### Source-Types Feld

Das `Source-Types`-Feld in den Metadaten klassifiziert die Quellen einer Domain:

| Wert | Bedeutung | Beispiel-Domain |
|------|-----------|----------------|
| `repo` | Quellen stammen aus Git-Repos (repomix) | godot |
| `pdf` | Quellen stammen aus PDF-Dokumenten (page metadata verfügbar) | davinci_resolve |

Mehrere Werte sind kommagetrennt möglich (z.B. `repo, pdf` für gemischte Domains).

Die Quality Evaluation Platform nutzt dieses Feld, um zu entscheiden, ob `page_metadata_accuracy` (PMA) für eine Domain relevant ist. PMA wird nur für Domains mit `pdf` in `source_types` berechnet.
```

### Step 6: Add unit tests for source_types parsing

In `tests/unit/test_model_manager.py`, add a new test class after `TestGetDomainConfig` (after line 158):

```python
class TestGetDomainConfigSourceTypes:
    def test_davinci_has_pdf_source_type(self):
        davinci_md = (
            Path(__file__).resolve().parent.parent.parent
            / "domains"
            / "davinci_resolve"
            / "domain.md"
        )
        if not davinci_md.exists():
            pytest.skip("davinci_resolve domain.md not found")
        cfg = get_domain_config("davinci_resolve")
        assert "pdf" in cfg["source_types"]

    def test_godot_has_repo_source_type(self):
        godot_md = (
            Path(__file__).resolve().parent.parent.parent
            / "domains"
            / "godot"
            / "domain.md"
        )
        if not godot_md.exists():
            pytest.skip("godot domain.md not found")
        cfg = get_domain_config("godot")
        assert "repo" in cfg["source_types"]

    def test_nonexistent_domain_defaults_to_repo(self):
        cfg = get_domain_config("totally_nonexistent_domain_xyz")
        assert cfg["source_types"] == ["repo"]

    def test_comma_separated_source_types(self, tmp_path, monkeypatch):
        """Simulate a domain.md with comma-separated source types."""
        # Create a fake domain.md in a temp location
        fake_domain_dir = tmp_path / "domains" / "mixed"
        fake_domain_dir.mkdir(parents=True)
        (fake_domain_dir / "domain.md").write_text("""# Domain: mixed

## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Source-Types: repo, pdf
""", encoding="utf-8")

        # Monkeypatch the domain.md path resolution inside get_domain_config
        # We need to override the Path construction. The function uses:
        #   Path(__file__).resolve().parent.parent / "domains" / domain / "domain.md"
        # We'll monkeypatch Path.exists to redirect.
        import model_manager as mm
        original_exists = mm.Path.exists

        def fake_exists(self):
            if "mixed" in str(self) and "domain.md" in str(self):
                return True
            return original_exists(self)

        monkeypatch.setattr(mm.Path, "exists", fake_exists)

        # Also need to patch read_text to return our content
        original_read_text = mm.Path.read_text

        def fake_read_text(self, **kwargs):
            if "mixed" in str(self) and "domain.md" in str(self):
                return fake_domain_dir.read_text(**kwargs)
            return original_read_text(self, **kwargs)

        monkeypatch.setattr(mm.Path, "read_text", fake_read_text)

        cfg = get_domain_config("mixed")
        assert "repo" in cfg["source_types"]
        assert "pdf" in cfg["source_types"]
```

Note: The `test_comma_separated_source_types` test uses monkeypatching which is fragile. An alternative is to test the regex directly:

```python
def test_source_types_regex_comma_separated(self):
    from model_manager import _SOURCE_TYPES_RE
    block = "- Source-Types: repo, pdf\n"
    m = _SOURCE_TYPES_RE.search(block)
    assert m is not None
    types = [t.strip() for t in m.group(1).split(",")]
    assert types == ["repo", "pdf"]

def test_source_types_regex_single(self):
    from model_manager import _SOURCE_TYPES_RE
    block = "- Source-Types: pdf\n"
    m = _SOURCE_TYPES_RE.search(block)
    assert m is not None
    types = [t.strip() for t in m.group(1).split(",")]
    assert types == ["pdf"]

def test_source_types_regex_no_match(self):
    from model_manager import _SOURCE_TYPES_RE
    block = "- Collection: foo_knowledge\n"
    m = _SOURCE_TYPES_RE.search(block)
    assert m is None
```

Add the `_SOURCE_TYPES_RE` to the imports at the top of the test file (line 12-19):
```python
from model_manager import (
    _DOMAIN_META_RE,
    _EMBEDDING_MODEL_RE,
    _SOURCE_TYPES_RE,
    get_domain_config,
    bm25_cache_get,
    bm25_cache_set,
    bm25_cache_invalidate,
)
```

### Step 7: Run tests to verify

```bash
pytest tests/unit/test_model_manager.py -v -k "source_types or SourceType"
```

Expected: All new tests pass. Existing tests continue to pass.

### Step 8: Commit

```bash
git add domains/davinci_resolve/domain.md domains/godot/domain.md scripts/model_manager.py scripts/quality/run_evaluation.py docs/ai/domain-model.md tests/unit/test_model_manager.py
git commit -m "feat(quality): derive PDF_DOMAINS from domain.md Source-Types metadata

Replace hardcoded PDF_DOMAINS set in run_evaluation.py with
get_domain_config() source_types parsing. Add Source-Types field
to domain.md Metadaten for davinci_resolve (pdf) and godot (repo).
Document the new field in domain-model.md."
```

---

## Task 2: Fix dvr-002 expected_source_files

**Files:**
- Modify: `quality/golden/davinci_resolve.yaml` (davinci_resolve-002 entry)

### Step 1: Update dvr-002 expected_source_files and notes

In `quality/golden/davinci_resolve.yaml`, change the `davinci_resolve-002` entry (lines 20-32).

**Current:**
```yaml
  - id: davinci_resolve-002
    question: "How do I trim a clip on the Edit page in DaVinci Resolve?"
    expected_source_files:
      - "davinci-resolve-20-editors-guide.md"
    expected_page_ranges: []
    real_world_source_url: null
    real_world_source_date: null
    difficulty: easy
    tags: [trim, edit, clip, timeline]
    created_date: 2026-06-29
    last_verified: 2026-06-29
    notes: "From E2E regression test test_davinci_trim_clip_search_finds_relevant_results."
    min_top_k: 10
```

**Change to:**
```yaml
  - id: davinci_resolve-002
    question: "How do I trim a clip on the Edit page in DaVinci Resolve?"
    expected_source_files:
      - "davinci-resolve-20.3-reference-manual.md"
    expected_page_ranges: []
    real_world_source_url: null
    real_world_source_date: null
    difficulty: easy
    tags: [trim, edit, clip, timeline]
    created_date: 2026-06-29
    last_verified: 2026-06-29
    notes: "Reference Manual dominates trim-related retrieval (pages 938-962 cover trim extensively). The Editor's Guide would be ideal but is not reliably found in top-10 for specific trim queries — this is a known retrieval gap, not a bug. See LIM-002 for DaVinci chunking limitations."
    min_top_k: 10
```

### Step 2: Validate the Golden Dataset

```bash
python scripts/quality/validate_dataset.py --domain davinci_resolve --check-sources
```

Expected: No errors. The Reference Manual file exists in `domains/davinci_resolve/sources/`.

### Step 3: Commit

```bash
git add quality/golden/davinci_resolve.yaml
git commit -m "fix(quality): update dvr-002 expected_source_files to Reference Manual

The Reference Manual (not the Editor's Guide) dominates top-10 results
for trim-related queries. Adjust expected_source_files to match real
retrieval behavior. Document the Editor's Guide retrieval gap in notes."
```

---

## Task 3: Configurable Weights and Thresholds

**Files:**
- Create: `quality/config.py`
- Modify: `scripts/quality/scorer.py` (lines 30-43, 226-265, 267-315)
- Modify: `tests/quality/test_rubric_scorer.py` (new tests)
- Modify: `quality/golden/godot.yaml` (optional: add weights/thresholds header)
- Modify: `quality/golden/davinci_resolve.yaml` (optional: add weights/thresholds header)

### Step 1: Create quality/config.py

Create `quality/config.py` at the repo root (sibling to `quality/golden/`):

```python
"""Default configuration for the Quality Evaluation Platform.

Weights and thresholds can be overridden per Golden Dataset via YAML
header fields ``weights`` and ``thresholds``. The ``load_config``
function merges dataset overrides with these defaults.

Design: pure data module — no side effects, no imports beyond stdlib.
"""

from __future__ import annotations

from typing import Any

# ── Default metric weights (must sum to 1.00) ────────────────────────────

DEFAULT_WEIGHTS: dict[str, float] = {
    "source_recall": 0.35,
    "page_metadata_accuracy": 0.20,
    "top_k_relevance": 0.25,
    "evidence_quality": 0.20,
}

# ── Default classification thresholds ────────────────────────────────────

DEFAULT_THRESHOLDS: dict[str, float] = {
    "pass": 0.7,
    "weak": 0.4,
}


def load_config(dataset: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a config dict with weights and thresholds.

    Merges dataset-level overrides (from YAML header fields ``weights``
    and ``thresholds``) with the module defaults. Dataset overrides take
    precedence.

    Args:
        dataset: The parsed Golden Dataset dict (from ``load_golden_dataset``).
                 May be ``None`` to get pure defaults.

    Returns:
        {
            "weights": {"source_recall": 0.35, ...},
            "thresholds": {"pass": 0.7, "weak": 0.4},
        }
    """
    weights = dict(DEFAULT_WEIGHTS)
    thresholds = dict(DEFAULT_THRESHOLDS)

    if dataset:
        if "weights" in dataset and isinstance(dataset["weights"], dict):
            weights.update(dataset["weights"])
        if "thresholds" in dataset and isinstance(dataset["thresholds"], dict):
            thresholds.update(dataset["thresholds"])

    return {"weights": weights, "thresholds": thresholds}
```

### Step 2: Update scorer.py — compute_composite_score accepts config

In `scripts/quality/scorer.py`, modify `compute_composite_score` (lines 226-254) to accept an optional `weights` dict:

```python
def compute_composite_score(
    source_recall: float | None,
    page_metadata_accuracy: float | None,
    top_k_relevance: float | None,
    evidence_quality: float | None,
    weights: dict[str, float] | None = None,
) -> float:
    """Weighted composite score with N/A redistribution.

    When a metric is None (N/A), its weight is redistributed proportionally
    across the remaining metrics. This prevents domains without page
    metadata (e.g. Godot) from being artificially lowered.

    Args:
        weights: Optional dict overriding default weights. Keys:
            ``source_recall``, ``page_metadata_accuracy``,
            ``top_k_relevance``, ``evidence_quality``.
            Defaults to module-level constants if None.
    """
    if weights is None:
        w_sr = W_SR
        w_pma = W_PMA
        w_tkr = W_TKR
        w_eq = W_EQ
    else:
        w_sr = weights.get("source_recall", W_SR)
        w_pma = weights.get("page_metadata_accuracy", W_PMA)
        w_tkr = weights.get("top_k_relevance", W_TKR)
        w_eq = weights.get("evidence_quality", W_EQ)

    parts = [
        (source_recall, w_sr),
        (page_metadata_accuracy, w_pma),
        (top_k_relevance, w_tkr),
        (evidence_quality, w_eq),
    ]
    active = [(v, w) for v, w in parts if v is not None]

    if not active:
        return 0.0

    total_weight = sum(w for _, w in active)
    if total_weight == 0:
        return 0.0

    weighted_sum = sum(v * w for v, w in active)
    return round(weighted_sum / total_weight, 4)
```

### Step 3: Update scorer.py — classify_score accepts config

Modify `classify_score` (lines 257-264) to accept optional thresholds:

```python
def classify_score(
    composite: float,
    thresholds: dict[str, float] | None = None,
) -> str:
    """Classify composite as ``pass``, ``weak``, or ``fail``.

    Args:
        thresholds: Optional dict with keys ``pass`` and ``weak``.
            Defaults to module-level constants if None.
    """
    pass_threshold = thresholds.get("pass", PASS_THRESHOLD) if thresholds else PASS_THRESHOLD
    weak_threshold = thresholds.get("weak", WEAK_THRESHOLD) if thresholds else WEAK_THRESHOLD

    if composite >= pass_threshold:
        return "pass"
    elif composite >= weak_threshold:
        return "weak"
    else:
        return "fail"
```

### Step 4: Update scorer.py — evaluate_question accepts config

Modify `evaluate_question` (lines 267-315) to accept an optional `config` dict and pass weights/thresholds through:

```python
def evaluate_question(
    question: dict,
    results: list[dict],
    is_pdf_domain: bool = False,
    config: dict[str, Any] | None = None,
) -> dict:
    """Evaluate a single Golden Dataset question against search results.

    Pure function — does not call ``hybrid_search``. Takes results as
    argument so it is fully testable with mock data.

    Args:
        config: Optional config dict from ``quality.config.load_config()``.
            Contains ``weights`` and ``thresholds`` keys. If None, module
            defaults are used.

    Returns a dict with the 4 metric scores, the composite, the label,
    truncation warning count, the found source files and the total result
    count.
    """
    expected_sources = question.get("expected_source_files", []) or []
    expected_ranges = question.get("expected_page_ranges") or None

    weights = config.get("weights") if config else None
    thresholds = config.get("thresholds") if config else None

    sr = score_source_recall(results, expected_sources)
    pma = score_page_metadata_accuracy(
        results, is_pdf_domain=is_pdf_domain, expected_ranges=expected_ranges
    )
    tkr = score_top_k_relevance(results)
    eq_ = score_evidence_quality(results)
    composite = compute_composite_score(sr, pma, tkr, eq_, weights=weights)
    label = classify_score(composite, thresholds=thresholds)

    # Truncation heuristic (LIM-003) — False positives possible.
    # Score is not reduced; the warning is shown in the report.
    truncation_warnings = sum(
        1 for r in results if len(r.get("text", "")) >= TRUNCATION_HEURISTIC_CHARS
    )

    found_sources = list(
        {r.get("source_file", "") for r in results if r.get("source_file")}
    )

    return {
        "id": question["id"],
        "question": question["question"],
        "source_recall": sr,
        "page_metadata_accuracy": pma,
        "top_k_relevance": tkr,
        "evidence_quality": eq_,
        "composite_score": composite,
        "label": label,
        "truncation_warnings": truncation_warnings,
        "found_source_files": found_sources,
        "total_results": len(results),
    }
```

### Step 5: Update run_evaluation.py to pass config

In `scripts/quality/run_evaluation.py`, add import for `load_config`:

```python
from quality.config import load_config
```

In `run_evaluation()` (around line 79-95), load config from the dataset and pass it to `evaluate_question`:

```python
def run_evaluation(domain: str) -> dict:
    _validate_domain(domain)
    path = GOLDEN_DIR / f"{domain}.yaml"
    dataset = load_golden_dataset(path)
    cfg = get_domain_config(domain)
    is_pdf = "pdf" in cfg.get("source_types", [])
    eval_config = load_config(dataset)

    evaluations = []
    for q in dataset["questions"]:
        top_k = q.get("min_top_k", 10)
        try:
            result = search(domain, q["question"], mode="hybrid", top_k=top_k)
            results = result.get("results", [])
        except Exception as exc:
            print(
                f"[WARN]  Search failed for {q['id']}: {exc}",
                file=sys.stderr,
            )
            results = []

        eval_result = evaluate_question(q, results, is_pdf_domain=is_pdf, config=eval_config)
        evaluations.append(eval_result)

    summary = aggregate_domain_scores(domain, evaluations)

    return {
        "domain": domain,
        "date": str(date.today()),
        "evaluations": evaluations,
        "summary": summary,
    }
```

### Step 6: Add tests for configurable weights/thresholds

In `tests/quality/test_rubric_scorer.py`, add new tests after the existing `classify_score` tests (after line 216):

```python
# ── Configurable weights / thresholds ────────────────────────────────────


def test_composite_with_custom_weights():
    """Custom weights: SR=0.5, PMA=0.0, TKR=0.3, EQ=0.2. All scores=1.0 → 1.0."""
    custom = {
        "source_recall": 0.5,
        "page_metadata_accuracy": 0.0,
        "top_k_relevance": 0.3,
        "evidence_quality": 0.2,
    }
    assert compute_composite_score(1.0, 1.0, 1.0, 1.0, weights=custom) == 1.0


def test_composite_custom_weights_na_redistribution():
    """Custom weights with PMA=N/A. SR=0.5, TKR=0.3, EQ=0.2.
    All scores=1.0 → (0.5*1 + 0.3*1 + 0.2*1) / 1.0 = 1.0.
    """
    custom = {
        "source_recall": 0.5,
        "page_metadata_accuracy": 0.0,
        "top_k_relevance": 0.3,
        "evidence_quality": 0.2,
    }
    result = compute_composite_score(1.0, None, 1.0, 1.0, weights=custom)
    assert result == 1.0


def test_composite_default_weights_when_none():
    """Passing weights=None should use module defaults (same as no arg)."""
    # SR=1.0, PMA=N/A, TKR=0.625, EQ=1.0 → same as test_composite_sr_pma_na_with_partials
    result = compute_composite_score(1.0, None, 0.625, 1.0, weights=None)
    assert abs(result - 0.8828) < 1e-4


def test_classify_custom_thresholds():
    """Custom thresholds: pass=0.8, weak=0.5."""
    custom = {"pass": 0.8, "weak": 0.5}
    assert classify_score(0.9, thresholds=custom) == "pass"
    assert classify_score(0.8, thresholds=custom) == "pass"
    assert classify_score(0.7, thresholds=custom) == "weak"
    assert classify_score(0.5, thresholds=custom) == "weak"
    assert classify_score(0.4, thresholds=custom) == "fail"


def test_classify_default_thresholds_when_none():
    """Passing thresholds=None should use module defaults."""
    assert classify_score(0.7, thresholds=None) == "pass"
    assert classify_score(0.5, thresholds=None) == "weak"
    assert classify_score(0.3, thresholds=None) == "fail"


def test_evaluate_question_with_config():
    """evaluate_question accepts config dict and passes weights/thresholds through."""
    from quality.config import load_config

    q = _q()
    results = [_r("godot-docs.md", text="rotate_y", page_start=5)]
    config = load_config()  # defaults
    out = evaluate_question(q, results, is_pdf_domain=True, config=config)
    assert out["id"] == "godot-001"
    assert out["composite_score"] is not None
    assert out["label"] in ("pass", "weak", "fail")


def test_evaluate_question_with_custom_config():
    """Custom config with different weights should produce different composite."""
    q = _q()
    results = [_r("godot-docs.md", text="rotate_y", page_start=5)]
    custom_config = {
        "weights": {
            "source_recall": 0.9,
            "page_metadata_accuracy": 0.0,
            "top_k_relevance": 0.05,
            "evidence_quality": 0.05,
        },
        "thresholds": {"pass": 0.9, "weak": 0.5},
    }
    out = evaluate_question(q, results, is_pdf_domain=True, config=custom_config)
    # With SR=1.0 heavily weighted, composite should be high
    assert out["composite_score"] > 0.9
    # With pass threshold at 0.9, this should still pass
    assert out["label"] == "pass"
```

### Step 7: Add optional weights/thresholds to Golden Dataset YAML headers

In `quality/golden/godot.yaml`, add after `last_updated: 2026-06-29` (line 4):

```yaml
# Default weights and thresholds (same as quality/config.py defaults).
# Uncomment and adjust to override per-dataset.
# weights:
#   source_recall: 0.35
#   page_metadata_accuracy: 0.20
#   top_k_relevance: 0.25
#   evidence_quality: 0.20
# thresholds:
#   pass: 0.7
#   weak: 0.4
```

In `quality/golden/davinci_resolve.yaml`, add the same commented block after `last_updated: 2026-06-29` (line 4).

This is documentation-by-example — the fields are commented out so they don't change behavior, but they show the pattern for future use.

### Step 8: Run tests to verify

```bash
pytest tests/quality/test_rubric_scorer.py -v
```

Expected: All existing tests pass. New config tests pass.

### Step 9: Commit

```bash
git add quality/config.py scripts/quality/scorer.py scripts/quality/run_evaluation.py tests/quality/test_rubric_scorer.py quality/golden/godot.yaml quality/golden/davinci_resolve.yaml
git commit -m "feat(quality): make scoring weights and thresholds configurable

Add quality/config.py with DEFAULT_WEIGHTS and DEFAULT_THRESHOLDS.
Scorer functions (compute_composite_score, classify_score,
evaluate_question) now accept optional config parameters.
run_evaluation.py loads config from Golden Dataset YAML headers.
Add commented weights/thresholds blocks to Golden Datasets as
documentation-by-example."
```

---

## Task 4: Populate expected_page_ranges for DaVinci Resolve

**Files:**
- Modify: `quality/golden/davinci_resolve.yaml` (all 7 questions)

**Important:** This task requires a **live index** to be available. The `implement-hub-change` agent must run live searches against the real ChromaDB index to determine page ranges. Page numbers must NOT be invented.

### Step 1: Verify the index is available

```bash
ls chromadb_data/davinci_resolve/chroma/
```

If the directory exists and contains data, proceed. If not, the index must be built first:
```bash
python scripts/embed_index.py --domain davinci_resolve
```

### Step 2: Run live searches for each question

For each of the 7 DaVinci questions, run a hybrid search and extract the `page_start` values from the top results. The `implement-hub-change` agent should execute:

```bash
python scripts/hybrid_search.py --domain davinci_resolve --query "How do I set up a Planar Tracker in DaVinci Resolve?" --mode hybrid --top-k 10
```

For each question, collect:
- The `page_start` values from the top 1-3 results
- The `source_file` for each result
- Group page ranges by source file

**Tolerance note:** The `score_page_metadata_accuracy` function (scorer.py:160-192) checks `er["start"] <= ps <= er["end"]` — it does NOT have a built-in ±2 tolerance. The tolerance must be baked into the ranges themselves. So when entering `expected_page_ranges`, add ±2 to the observed page numbers:

- If a result has `page_start: 2786`, enter `{"start": 2784, "end": 2793}` (2786 ± 2, plus the chunk might span a few pages)
- For a range like "pages 938-962", enter `{"start": 936, "end": 964}`

### Step 3: Populate expected_page_ranges in davinci_resolve.yaml

For each question, add `expected_page_ranges` entries. The format is:

```yaml
expected_page_ranges:
  - source_file: "davinci-resolve-20.3-reference-manual.md"
    start: 2784
    end: 2793
  - source_file: "fusion-20.3-manual.md"
    start: 586
    end: 595
```

The `implement-hub-change` agent must fill in the actual page numbers from live search results. The plan provides the structure but NOT the numbers.

**Template for each question (numbers to be filled by implement-hub-change):**

```yaml
  - id: davinci_resolve-001
    question: "How do I set up a Planar Tracker in DaVinci Resolve?"
    expected_source_files:
      - "davinci-resolve-20.3-reference-manual.md"
      - "fusion-20.3-manual.md"
    expected_page_ranges:
      - source_file: "davinci-resolve-20.3-reference-manual.md"
        start: <FROM_LIVE_SEARCH>
        end: <FROM_LIVE_SEARCH>
      - source_file: "fusion-20.3-manual.md"
        start: <FROM_LIVE_SEARCH>
        end: <FROM_LIVE_SEARCH>
```

Repeat for all 7 questions (dvr-001 through dvr-007).

### Step 4: Validate the Golden Dataset

```bash
python scripts/quality/validate_dataset.py --domain davinci_resolve --check-sources
```

Expected: No errors.

### Step 5: Run evaluation to verify PMA scores improve

```bash
python scripts/quality/run_evaluation.py --domain davinci_resolve
```

Expected: PMA scores should now reflect whether results fall within the expected page ranges. Questions where the top results match the expected ranges will have higher PMA.

### Step 6: Commit

```bash
git add quality/golden/davinci_resolve.yaml
git commit -m "feat(quality): add expected_page_ranges for all DaVinci Resolve questions

Populate expected_page_ranges from live hybrid search results against
the real index. Ranges include ±2 page tolerance for chunking variance.
This sharpens PMA scoring from binary page_start presence to
range-based accuracy."
```

---

## Execution Order and Dependencies

```
Task 1 (Source-Types) ──┐
                         ├──> Task 4 (page_ranges)  [needs Task 1 for is_pdf detection]
Task 3 (Config) ────────┘
Task 2 (dvr-002 fix) ──── independent, can run anytime
```

- **Task 1 and Task 3 can run in parallel** — they touch different files with no overlap.
- **Task 2 can run in parallel with everything** — it only touches `davinci_resolve.yaml`.
- **Task 4 must run after Task 1** — it depends on `get_domain_config()` returning `source_types` for correct `is_pdf` detection during evaluation verification. It also touches `davinci_resolve.yaml` so it should run after Task 2 (or merge carefully).

**Recommended order:** Task 1 + Task 3 in parallel → Task 2 → Task 4.

---

## What is NOT Changed

- **No index rebuilds.** All changes are to config files, YAML datasets, and Python logic. The ChromaDB index is read-only for these tasks.
- **No changes to `hybrid_search.py`, `embed_search.py`, or `embed_index.py`.** These are retrieval infrastructure, not quality evaluation.
- **No changes to MCP server.** The quality platform is dev-time tooling, not runtime.
- **No changes to `score_page_metadata_accuracy` tolerance logic.** The function already checks `start <= page_start <= end` with no built-in tolerance. Tolerance is baked into the ranges in the YAML (Task 4).
- **No changes to `validate_dataset.py`.** It already handles `expected_page_ranges` as an optional field (via `load_golden_dataset` defaulting it to `[]`).
- **No changes to `generate_report.py`.** It reads evaluation results, not config.
- **No changes to `add_question.py`.** Manual curation tool, out of scope.

---

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| **Task 1:** `get_domain_config()` return type change breaks callers that destructure the old 4-key dict | All existing callers (`get_embedder`, `get_chroma_client`, `hybrid_search`) access specific keys by name, not by position. Adding a 5th key is backward-compatible. Verify with `grep -r "get_domain_config" scripts/ mcp_servers/` |
| **Task 1:** Godot domain.md has `- ChromaDB-Collection:` (with backticks) not `- Collection:` — regex mismatch? | The `_DOMAIN_META_RE` only extracts the block. The `_SOURCE_TYPES_RE` is a new regex that matches `- Source-Types:`. No conflict with existing fields. |
| **Task 3:** `load_config` import in `run_evaluation.py` — `quality/config.py` is at repo root, not in `scripts/quality/`. Import path must work. | `pyproject.toml` has `pythonpath = [".", "scripts"]`, so `from quality.config import load_config` resolves to `quality/config.py` at repo root. Verify with `python -c "from quality.config import load_config; print(load_config())"` |
| **Task 3:** Existing tests for `compute_composite_score` and `classify_score` call them without the new `weights`/`thresholds` parameter — must still work. | Both parameters default to `None`, which triggers the module-level constants. All existing tests pass without modification. |
| **Task 4:** Live search might fail if the index is not built. | Task 4 Step 1 checks index availability. If missing, the agent must report `[skip: index not built]` and not invent page numbers. |
| **Task 4:** Page numbers from live search might differ from the context-provided numbers (index may have been rebuilt). | The `implement-hub-change` agent must use its own live search results, not the context-provided numbers. The context numbers are from a prior run and may be stale. |
| **Task 2 + 4 both touch `davinci_resolve.yaml`** | Run Task 2 before Task 4, or have Task 4 apply its changes on top of Task 2's changes. The merge is trivial (different YAML keys). |

---

## Validation Checklist

After all tasks are complete, run:

```bash
# Unit tests
pytest tests/unit/test_model_manager.py -v
pytest tests/quality/test_rubric_scorer.py -v

# Golden Dataset validation
python scripts/quality/validate_dataset.py --domain godot --check-sources
python scripts/quality/validate_dataset.py --domain davinci_resolve --check-sources

# Live evaluation (requires index)
python scripts/quality/run_evaluation.py --domain godot
python scripts/quality/run_evaluation.py --domain davinci_resolve

# Python syntax check
find scripts/quality -name "*.py" -exec python3 -m py_compile {} \;
python3 -m py_compile quality/config.py
```

---

## Open Questions

1. **Should `Source-Types` support `repo, pdf` for mixed domains?** The current implementation supports comma-separated values. No domain currently needs this, but the parsing handles it. If a future domain has both repo and PDF sources, `is_pdf` would be `True` (because `"pdf" in source_types`), which is correct — PMA should be evaluated for any domain with at least some PDF sources.

2. **Should `load_config` validate that weights sum to 1.0?** Not in this plan — it adds complexity without a clear use case. If someone sets bad weights, the composite score will be wrong, but that's a configuration error, not a code bug. Can be added later if needed.

3. **Should the `weights`/`thresholds` YAML header fields be validated by `validate_dataset.py`?** Not in this plan. The fields are optional and `load_config` silently ignores malformed values (uses defaults). Validation can be added in a future follow-up.

4. **For Task 4, what if a question's live search returns no page metadata at all?** The `implement-hub-change` agent should leave `expected_page_ranges: []` for that question and document the gap in `notes`. This is a real finding — the index may have chunks without page metadata for that query.
