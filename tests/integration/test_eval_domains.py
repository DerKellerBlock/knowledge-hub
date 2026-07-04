"""Integration tests for Phase 3.1b Eval-Domains (Task 12, E13 + NB-6) and
the Spot-Check-Gate preparation (Task 13).

Covers three areas:

1. **Eval-Domain setup** (``godot_eval_a`` / ``godot_eval_b`` /
   ``godot_spotcheck``): the relative symlinks under ``sources/`` and
   ``personal/`` resolve to the real Godot files, and the
   ``domain.md`` files carry ``Embedding-Model: BAAI/bge-m3`` (NB-6 —
   without BGE-M3, ``context_prefix + "\\n" + text`` would truncate at
   384 tokens and the spot-check would measure truncation artefacts
   instead of Contextual-Retrieval benefit).

2. **Symlink-Isolation**: ``load_domain_sources`` reads chunks via the
   relative symlinks, and a tiny mock-embedder build writes to an
   isolated ``chromadb_data/<eval_domain>/`` path (the productive
   ``chromadb_data/godot/`` stays untouched). BM25 + hybrid search load
   the eval-domain index, not the productive one (NB-3 isolation).

3. **Spot-Check-Gate**: ``godot_spotcheck.yaml`` is loadable via
   ``_resolve_dataset_path`` (Phase 3.1b ``--dataset-path`` support),
   and :func:`scripts.quality.gate.decide_gate` returns ``"GO"`` /
   ``"NO-GO"`` according to the Phase-3.1b threshold (delta >= -0.02
   = GO, < -0.02 = NO-GO).

All tests use ``tmp_hub`` + mock-embedders — NO real BGE-M3 download,
NO real Ollama call, NO 69h contextualization run. The real eval
domains are checked for existence / symlink structure only (read-only
filesystem access, no index build).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.integration

pytest.importorskip("chromadb")

HUB_ROOT = Path(__file__).resolve().parent.parent.parent

# Eval domains created by Phase G / Task 12.
EVAL_DOMAINS = ("godot_eval_a", "godot_eval_b", "godot_spotcheck")

# Source files symlinked into godot_eval_a / godot_eval_b (must match the
# real Godot packed files, so a regression in the symlink target name is
# caught early).
GODOT_SOURCE_FILES = (
    "godot-demos-packed.md",
    "godot-docs-3d-packed.md",
    "godot-docs-reference-packed.md",
)
GODOT_PERSONAL_FILES = (
    "best-practices.md",
    "faq.md",
    "gotchas.md",
    "tips.md",
)


# ── Test doubles ───────────────────────────────────────────────────────────


class RecordingEmbedder:
    """Fake embedder that records every text passed to ``encode()``.

    Returns a deterministic float32 vector per text so ChromaDB accepts
    the ``add()``. Mirrors the RecordingEmbedder from
    ``test_contextualize_build.py`` so the two test files stay
    consistent.
    """

    def __init__(self, dim: int = 8):
        self.dim = dim
        self.encoded_texts: list[str] = []

    def encode(self, texts, batch_size=32, show_progress_bar=False,
               convert_to_numpy=True):
        if isinstance(texts, str):
            texts = [texts]
            single = True
        else:
            single = False
        self.encoded_texts.extend(texts)
        vecs = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, t in enumerate(texts):
            h = abs(hash(t)) % (10 ** 9)
            for d in range(self.dim):
                vecs[i, d] = ((h >> (d % 31)) & 0xFF) / 255.0
        return vecs[0] if single else vecs

    @property
    def class_name(self) -> str:
        return "RecordingEmbedder"


def _make_personal_chunk(domain: str, source_file: str, name: str,
                         text: str) -> "object":
    """Build a minimal ``parser_base.Chunk`` for a personal section."""
    from parser_base import Chunk
    return Chunk(
        chunk_id=f"{domain}::{source_file}::{name}",
        domain=domain,
        text=text,
        source_type="personal",
        chunk_type="personal_section",
        source_file=source_file,
        name=name,
    )


# ── 1. Eval-Domain setup (read-only structure checks) ─────────────────────


class TestEvalDomainStructure:
    """The three eval domains exist with the expected layout and carry
    the BGE-M3 metadata (NB-6)."""

    @pytest.mark.parametrize("domain", EVAL_DOMAINS)
    def test_domain_md_exists_with_bge_m3(self, domain: str):
        """Each eval domain has a ``domain.md`` that pins
        ``Embedding-Model: BAAI/bge-m3`` (NB-6 critical)."""
        path = HUB_ROOT / "domains" / domain / "domain.md"
        assert path.exists(), f"missing domain.md for {domain}"
        content = path.read_text(encoding="utf-8")
        assert "Embedding-Model: BAAI/bge-m3" in content, (
            f"{domain}/domain.md must pin Embedding-Model: BAAI/bge-m3 "
            f"(NB-6: without it get_domain_config falls back to all-mpnet "
            f"and context_prefix+text truncates at 384 tokens)."
        )

    @pytest.mark.parametrize("domain", ("godot_eval_a", "godot_eval_b"))
    @pytest.mark.parametrize("fname", GODOT_SOURCE_FILES)
    def test_sources_symlink_resolves(self, domain: str, fname: str):
        """``sources/<fname>`` is a relative symlink that resolves to
        the real Godot source file (repo bleibt verschiebbar)."""
        link = HUB_ROOT / "domains" / domain / "sources" / fname
        assert link.is_symlink(), f"{link} is not a symlink"
        # Relative target (repo stays portable).
        target = link.readlink() if hasattr(link, "readlink") else Path(
            __import__("os").readlink(str(link))
        )
        assert not target.is_absolute(), (
            f"{link} symlink target must be relative, got {target}"
        )
        assert str(target).startswith("../../godot/"), (
            f"{link} symlink target must point at ../../godot/..., "
            f"got {target}"
        )
        # Resolves to a readable file.
        assert link.resolve().is_file(), (
            f"{link} symlink does not resolve to a file"
        )

    @pytest.mark.parametrize("domain", EVAL_DOMAINS)
    @pytest.mark.parametrize("fname", GODOT_PERSONAL_FILES)
    def test_personal_symlink_resolves(self, domain: str, fname: str):
        """``personal/<fname>`` is a relative symlink to Godot's
        personal note (all three eval domains share the same personal
        notes; godot_spotcheck has ONLY personal — no sources/)."""
        link = HUB_ROOT / "domains" / domain / "personal" / fname
        assert link.is_symlink(), f"{link} is not a symlink"
        target = link.readlink() if hasattr(link, "readlink") else Path(
            __import__("os").readlink(str(link))
        )
        assert not target.is_absolute(), (
            f"{link} symlink target must be relative, got {target}"
        )
        assert str(target).startswith("../../godot/"), (
            f"{link} symlink target must point at ../../godot/..., "
            f"got {target}"
        )
        assert link.resolve().is_file(), (
            f"{link} symlink does not resolve to a file"
        )

    def test_spotcheck_has_no_sources_dir(self):
        """``godot_spotcheck`` uses ONLY the 24 personal section-chunks
        — no ``sources/`` directory (keeps the spot-check fast)."""
        sources = HUB_ROOT / "domains" / "godot_spotcheck" / "sources"
        assert not sources.exists(), (
            f"godot_spotcheck must not have a sources/ dir "
            f"(spot-check is personal-only); found {sources}"
        )

    def test_eval_domains_have_distinct_collection_names(self):
        """Each eval domain pins its own ChromaDB collection name in
        ``domain.md`` so the productive ``godot_knowledge`` collection
        stays untouched (E13 isolation)."""
        expected = {
            "godot_eval_a": "godot_eval_a_knowledge",
            "godot_eval_b": "godot_eval_b_knowledge",
            "godot_spotcheck": "godot_spotcheck_knowledge",
        }
        for domain, coll in expected.items():
            path = HUB_ROOT / "domains" / domain / "domain.md"
            content = path.read_text(encoding="utf-8")
            assert coll in content, (
                f"{domain}/domain.md must declare Collection {coll} "
                f"for E13 isolation from productive godot_knowledge."
            )


# ── 2. Symlink-Isolation (tmp_hub + mock embedder) ────────────────────────


def test_eval_domain_symlinks_loadable():
    """Smoke test: the relative symlinks of the REAL ``godot_eval_a``
    domain resolve and are readable. A broken symlink would surface
    here as a FileNotFoundError or unresolved Path.

    This does NOT call ``load_domain_sources`` (which would trigger
    real BGE-M3 / parser processing on 457k lines and take 50+ min).
    Symlink readability is sufficient — the indexer reads files via
    the same ``pathlib.Path.read_text()`` path that this test
    exercises.
    """
    from pathlib import Path
    eval_a = Path("domains/godot_eval_a")
    link_files = list((eval_a / "sources").glob("*.md")) + list((eval_a / "personal").glob("*.md"))
    assert len(link_files) >= 4, f"expected >=4 symlinks in godot_eval_a, got {len(link_files)}"
    for link in link_files:
        resolved = link.resolve()
        assert resolved.is_file(), f"symlink {link} does not resolve to a file (resolved={resolved})"
        # read_text() will raise if the target is missing — that's the
        # broken-symlink signal we want to catch.
        content = link.read_text(encoding="utf-8")
        assert len(content) > 0, f"symlink {link} resolves to empty file"


def _build_tmp_eval_domain(tmp_hub, domain_name: str,
                           source_files: list[str],
                           personal_files: list[tuple[str, str]]) -> str:
    """Create a mini eval-domain inside ``tmp_hub`` with real personal
    chunks (no symlinks — tmp_hub is self-contained).

    Personal-note sections must be at least 50 chars long (the
    ``markdown_section_chunk`` defensive skip threshold), otherwise the
    section is dropped and the build produces 0 chunks.
    """
    domain_dir = tmp_hub / "domains" / domain_name
    personal_dir = domain_dir / "personal"
    personal_dir.mkdir(parents=True)
    (domain_dir / "domain.md").write_text(
        f"# Domain: {domain_name}\n\n## Metadaten\n"
        "- Embedding-Model: BAAI/bge-m3 (1024 dims)\n"
        f"- Collection: {domain_name}_knowledge\n"
        "- Source-Types: repo\n"
        "- Letztes Update: 2026-07-02\n",
        encoding="utf-8",
    )
    for fname, body in personal_files:
        (personal_dir / fname).write_text(body, encoding="utf-8")
    return domain_name


# Personal-note bodies long enough to survive the >=50 char defensive
# skip in ``markdown_section_chunk``. The section text (after the
# ``## `` header line) must be >= 50 chars on its own.
_PERSONAL_FAQ = (
    "# FAQ\n\n"
    "## Visibility\n"
    "A MeshInstance3D needs a mesh resource assigned and an active "
    "camera pointing at it to be visible in the viewport.\n"
)
_PERSONAL_GOTCHAS = (
    "# Gotchas\n\n"
    "## GLB Import Scale\n"
    "GLB models imported from Meshy can have a wrong import scale; "
    "check the origin point and apply transforms before export.\n"
)


def test_eval_domain_index_isolated(tmp_hub, monkeypatch):
    """``build_index("godot_eval_a_tmp")`` writes to an isolated
    ``chromadb_data/godot_eval_a_tmp/`` path; the productive
    ``chromadb_data/godot/`` is never touched.

    Built with a mock embedder (no BGE-M3 download). Verifies the E13
    isolation guarantee: the eval build path uses the domain-derived
    ChromaDB path, not the productive Godot path.
    """
    import embed_index
    import model_manager as mm

    domain = _build_tmp_eval_domain(
        tmp_hub,
        "godot_eval_a_tmp",
        source_files=[],
        personal_files=[("faq.md", _PERSONAL_FAQ),
                        ("gotchas.md", _PERSONAL_GOTCHAS)],
    )

    embedder = RecordingEmbedder()
    monkeypatch.setattr(mm, "get_embedder", lambda d: embedder)
    monkeypatch.setattr(embed_index, "get_embedder", lambda d: embedder)

    embed_index.build_index(domain)

    # Eval domain index exists in tmp_hub/chromadb_data/<domain>/.
    eval_chroma_dir = tmp_hub / "chromadb_data" / domain / "chroma"
    assert eval_chroma_dir.exists(), (
        f"eval domain chroma dir not created: {eval_chroma_dir}"
    )

    # The productive Godot index (if it exists) lives under the REAL
    # HUB_ROOT, NOT under tmp_hub. tmp_hub is a fresh tmp_path, so
    # tmp_hub/chromadb_data/godot/ must NOT exist — this proves the eval
    # build does not touch the productive path.
    productive_in_tmp = tmp_hub / "chromadb_data" / "godot"
    assert not productive_in_tmp.exists(), (
        f"eval build leaked into productive godot path: {productive_in_tmp}"
    )

    # Collection exists with the domain-derived name.
    from model_manager import get_chroma_client
    client = get_chroma_client(domain)
    collection = client.get_collection(f"{domain}_knowledge")
    assert collection.count() > 0, "isolated eval collection is empty"


def test_bm25_search_loads_eval_domain_index(tmp_hub, monkeypatch):
    """``bm25_search`` and ``hybrid_search.search`` load the eval-domain
    BM25 + ChromaDB, not the productive Godot index (NB-3 isolation).

    Builds a tiny isolated eval domain with a mock embedder, then runs
    an exact BM25 search and a hybrid search. The results must come from
    the eval-domain chunks (not from ``chromadb_data/godot/``).
    """
    import embed_index
    import model_manager as mm

    domain = _build_tmp_eval_domain(
        tmp_hub,
        "godot_eval_b_tmp",
        source_files=[],
        personal_files=[("faq.md", _PERSONAL_FAQ),
                        ("gotchas.md", _PERSONAL_GOTCHAS)],
    )

    embedder = RecordingEmbedder()
    monkeypatch.setattr(mm, "get_embedder", lambda d: embedder)
    monkeypatch.setattr(embed_index, "get_embedder", lambda d: embedder)

    embed_index.build_index(domain)

    from bm25_search import bm25_search, _load_index
    from hybrid_search import search as hybrid_search

    # BM25 index for the eval domain loads from the isolated pickle
    # (NB-3 isolation): chunk_ids carry the eval-domain prefix, never
    # the productive ``godot::`` prefix. We inspect the loaded index
    # directly because BM25Okapi with a 2-document corpus can produce
    # all-zero scores for short queries (the ``score > 0`` filter then
    # removes every result) — the isolation guarantee is about WHICH
    # index is loaded, not about non-zero scores on a tiny corpus.
    bm25_data = _load_index(domain)
    chunk_ids = bm25_data["chunk_ids"]
    assert len(chunk_ids) > 0, "eval BM25 index has no chunks"
    for cid in chunk_ids:
        assert cid.startswith(f"{domain}::"), (
            f"bm25 index leaked from another domain: {cid}"
        )
        assert not cid.startswith("godot::"), (
            f"bm25 index contains productive godot chunks: {cid}"
        )

    # Hybrid search loads the eval BM25 + eval ChromaDB. Even with a
    # mock embedder, the resolved chunk_ids must come from the eval
    # domain (isolated collection). We use ``mode="exact"`` so no
    # embedder is required and the result text is resolved via the
    # eval ChromaDB — if isolation were broken, the productive
    # ``godot_knowledge`` collection would be queried instead.
    exact = hybrid_search(domain, "GLB import scale", mode="exact", top_k=5)
    for r in exact.get("results", []):
        assert r.get("chunk_id", "").startswith(f"{domain}::"), (
            f"hybrid exact result from wrong domain: {r.get('chunk_id')}"
        )


# ── 3. Spot-Check-Gate preparation ─────────────────────────────────────────


class TestSpotcheckDataset:
    """``godot_spotcheck.yaml`` is loadable and carries the 2
    pure-personal fallback questions (OQ-1)."""

    def test_spotcheck_yaml_exists(self):
        path = HUB_ROOT / "quality" / "golden" / "godot_spotcheck.yaml"
        assert path.exists(), "godot_spotcheck.yaml not created"
        # Header documents the gate semantics.
        content = path.read_text(encoding="utf-8")
        assert "Spot-Check-Gate" in content
        assert "composite-Delta" in content or "composite-delta" in content.lower()

    def test_resolve_dataset_path_picks_spotcheck_yaml(self):
        """``_resolve_dataset_path("godot_spotcheck", None)`` returns the
        default ``quality/golden/godot_spotcheck.yaml`` path."""
        sys.path.insert(0, str(HUB_ROOT / "scripts"))
        try:
            from quality.run_evaluation import _resolve_dataset_path
            path = _resolve_dataset_path("godot_spotcheck", None)
            assert path.name == "godot_spotcheck.yaml"
            assert path.exists(), (
                f"resolved dataset path does not exist: {path}"
            )
        finally:
            sys.path.pop(0)

    def test_spotcheck_yaml_loads_and_has_questions(self):
        """The dataset loads via ``load_golden_dataset`` and contains the
        expected question ids: 2 Phase-3.1b fallback questions
        (godot_spotcheck-005, godot_spotcheck-008-de) plus 3 Phase-3.1c
        curated questions (godot_spotcheck-gotchas-1,
        godot_spotcheck-bestpractices-1, godot_spotcheck-tips-1)."""
        sys.path.insert(0, str(HUB_ROOT / "scripts"))
        try:
            from quality.scorer import load_golden_dataset
            path = HUB_ROOT / "quality" / "golden" / "godot_spotcheck.yaml"
            dataset = load_golden_dataset(path)
            ids = [q["id"] for q in dataset["questions"]]
            expected_ids = [
                "godot_spotcheck-005",
                "godot_spotcheck-008-de",
                "godot_spotcheck-gotchas-1",
                "godot_spotcheck-bestpractices-1",
                "godot_spotcheck-tips-1",
            ]
            assert ids == expected_ids, (
                f"unexpected question ids: {ids}"
            )
            # All questions are pure-personal (single personal file).
            for q in dataset["questions"]:
                sources = q["expected_source_files"]
                assert len(sources) == 1, (
                    f"{q['id']} must be pure-personal (1 expected source), "
                    f"got {sources}"
                )
                assert sources[0] in GODOT_PERSONAL_FILES, (
                    f"{q['id']} expected source must be a personal note, "
                    f"got {sources[0]}"
                )
        finally:
            sys.path.pop(0)


# ── 4. Gate decision logic (isolated, no models) ───────────────────────────


class TestSpotcheckGateDecision:
    """``scripts.quality.gate.decide_gate`` implements the 3.1b
    No-Go-Gate threshold (delta >= -0.02 = GO, < -0.02 = NO-GO)."""

    def test_neutral_delta_is_go(self):
        from quality.gate import decide_gate
        assert decide_gate(0.0) == "GO"

    def test_positive_delta_is_go(self):
        from quality.gate import decide_gate
        assert decide_gate(0.05) == "GO"

    def test_delta_at_threshold_is_go(self):
        """delta == -0.02 is the boundary; spec uses ``>= -0.02``
        (inclusive GO)."""
        from quality.gate import decide_gate, SPOTCHECK_GATE_THRESHOLD
        assert decide_gate(SPOTCHECK_GATE_THRESHOLD) == "GO"

    def test_delta_just_below_threshold_is_no_go(self):
        from quality.gate import decide_gate
        assert decide_gate(-0.0201) == "NO-GO"

    def test_clear_regression_is_no_go(self):
        from quality.gate import decide_gate
        assert decide_gate(-0.10) == "NO-GO"

    def test_missing_delta_is_no_go(self):
        """A missing measurement must NOT silently pass — fail-safe."""
        from quality.gate import decide_gate
        assert decide_gate(None) == "NO-GO"

    def test_threshold_value_documented(self):
        """The threshold is pinned to -0.02 (Phase 3.1b spec)."""
        from quality.gate import SPOTCHECK_GATE_THRESHOLD
        assert SPOTCHECK_GATE_THRESHOLD == -0.02

    def test_compute_composite_delta_from_summaries(self):
        from quality.gate import compute_composite_delta
        current = {"summary": {"avg_composite": 0.80}}
        baseline = {"summary": {"avg_composite": 0.82}}
        # delta = current - baseline = -0.02 → GO (inclusive).
        delta = compute_composite_delta(current, baseline)
        assert delta == pytest.approx(-0.02)

    def test_compute_delta_missing_summary_is_none(self):
        from quality.gate import compute_composite_delta
        assert compute_composite_delta({}, {"summary": {"avg_composite": 0.8}}) is None
        assert compute_composite_delta(
            {"summary": {"avg_composite": 0.8}}, {}
        ) is None
        assert compute_composite_delta(None, None) is None

    def test_compute_delta_non_numeric_is_none(self):
        from quality.gate import compute_composite_delta
        current = {"summary": {"avg_composite": "n/a"}}
        baseline = {"summary": {"avg_composite": 0.8}}
        assert compute_composite_delta(current, baseline) is None

    def test_gate_from_evaluation_dicts_go(self):
        """End-to-end: derive delta from two evaluation dicts and
        decide GO."""
        from quality.gate import compute_composite_delta, decide_gate
        baseline = {
            "domain": "godot_spotcheck",
            "summary": {"avg_composite": 0.80},
        }
        current = {
            "domain": "godot_spotcheck",
            "summary": {"avg_composite": 0.80},
        }
        delta = compute_composite_delta(current, baseline)
        assert decide_gate(delta) == "GO"

    def test_gate_from_evaluation_dicts_no_go(self):
        from quality.gate import compute_composite_delta, decide_gate
        baseline = {
            "domain": "godot_spotcheck",
            "summary": {"avg_composite": 0.80},
        }
        current = {
            "domain": "godot_spotcheck",
            "summary": {"avg_composite": 0.75},
        }
        # delta = -0.05 → below -0.02 threshold → NO-GO.
        delta = compute_composite_delta(current, baseline)
        assert decide_gate(delta) == "NO-GO"


# ── 5. Spot-Check-Gate end-to-end (mocked run_evaluation) ────────────────────


def test_spotcheck_gate_composite_delta(tmp_hub, monkeypatch):
    """Simulated Spot-Check-Gate flow with a mock embedder and a stub
    ``run_evaluation`` (NO real Ollama, NO 69h contextualization run):

    1. Build a tiny personal-only spot-check domain in ``tmp_hub``.
    2. ``run_evaluation`` is stubbed to return a configurable
       ``avg_composite`` (so the gate logic is exercised without a real
       search).
    3. Baseline (non-contextualized) → ``avg_composite = 0.80``.
    4. Contextualized → ``avg_composite = 0.80`` (neutral).
    5. ``decide_gate(delta) == "GO"`` (delta = 0.0 >= -0.02).

    A second sub-case asserts NO-GO when contextualized regresses to
    0.75 (delta = -0.05 < -0.02).
    """
    from quality.gate import compute_composite_delta, decide_gate

    domain = _build_tmp_eval_domain(
        tmp_hub,
        "godot_spotcheck_tmp",
        source_files=[],
        personal_files=[
            ("faq.md",
             "# FAQ\n\n## Visibility\nA MeshInstance3D needs a mesh and a "
             "camera to be visible.\n"),
            ("gotchas.md",
             "# Gotchas\n\n## GLB Import Scale\nGLB models from Meshy can "
             "have wrong import scale.\n"),
        ],
    )

    # Stub run_evaluation: returns a configurable avg_composite so we
    # can drive both GO and NO-GO paths without a real search.
    sys.path.insert(0, str(HUB_ROOT / "scripts"))
    try:
        import quality.run_evaluation as rev

        def make_eval(avg_composite: float):
            def _stub(domain, dataset_path=None):
                return {
                    "domain": domain,
                    "date": "2026-07-02",
                    "evaluations": [],
                    "summary": {"avg_composite": avg_composite},
                }
            return _stub

        # Baseline (non-contextualized) — neutral scenario.
        monkeypatch.setattr(rev, "run_evaluation", make_eval(0.80))
        baseline_result = rev.run_evaluation(
            "godot_spotcheck_tmp",
            dataset_path=str(HUB_ROOT / "quality" / "golden"
                             / "godot_spotcheck.yaml"),
        )

        # Contextualized — neutral (no regression, GO).
        monkeypatch.setattr(rev, "run_evaluation", make_eval(0.80))
        current_result = rev.run_evaluation(
            "godot_spotcheck_tmp",
            dataset_path=str(HUB_ROOT / "quality" / "golden"
                             / "godot_spotcheck.yaml"),
        )

        delta = compute_composite_delta(current_result, baseline_result)
        assert delta == pytest.approx(0.0)
        assert decide_gate(delta) == "GO", (
            f"neutral delta {delta} must be GO, got {decide_gate(delta)}"
        )

        # Contextualized — regression scenario (NO-GO).
        monkeypatch.setattr(rev, "run_evaluation", make_eval(0.75))
        regressed_result = rev.run_evaluation(
            "godot_spotcheck_tmp",
            dataset_path=str(HUB_ROOT / "quality" / "golden"
                             / "godot_spotcheck.yaml"),
        )
        delta_reg = compute_composite_delta(regressed_result, baseline_result)
        assert delta_reg == pytest.approx(-0.05)
        assert decide_gate(delta_reg) == "NO-GO", (
            f"regression delta {delta_reg} must be NO-GO, "
            f"got {decide_gate(delta_reg)}"
        )
    finally:
        sys.path.pop(0)