"""Integration tests for migration.migrate_legacy_layout.

Uses tmp_path to simulate legacy and per-domain layouts without touching
the real chromadb_data/.
"""

import pickle
import pytest
from pathlib import Path

pytestmark = pytest.mark.integration


def test_migration_no_chroma_dir(tmp_path, monkeypatch):
    """If chromadb_data doesn't exist, migration returns False."""
    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", tmp_path / "nonexistent")
    assert migration.migrate_legacy_layout() is False


def test_migration_empty_chroma_dir(tmp_path, monkeypatch):
    """Empty chromadb_data → nothing to migrate → False."""
    (tmp_path / "chroma").mkdir()
    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", tmp_path / "chroma")
    assert migration.migrate_legacy_layout() is False


def test_migration_idempotent_empty(tmp_path, monkeypatch):
    """Running migration twice on empty dir should both return False."""
    (tmp_path / "chroma").mkdir()
    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", tmp_path / "chroma")
    assert migration.migrate_legacy_layout() is False
    assert migration.migrate_legacy_layout() is False


def test_migration_moves_legacy_collection(tmp_path, monkeypatch):
    """Legacy <domain>_knowledge/ dir should be moved to <domain>/chroma/."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    # Create legacy collection dir
    legacy_coll = chroma / "testdomain_knowledge"
    legacy_coll.mkdir()
    (legacy_coll / "somefile.txt").write_text("data")

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    result = migration.migrate_legacy_layout()
    assert result is True
    # New location
    assert (chroma / "testdomain" / "chroma" / "testdomain_knowledge" / "somefile.txt").exists()
    # Old location gone
    assert not legacy_coll.exists()


def test_migration_moves_legacy_bm25(tmp_path, monkeypatch):
    """Legacy <domain>_bm25.pkl should be moved to <domain>/."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    # Create legacy collection + bm25
    (chroma / "testdomain_knowledge").mkdir()
    (chroma / "testdomain_knowledge" / "f.txt").write_text("x")
    legacy_bm25 = chroma / "testdomain_bm25.pkl"
    with open(legacy_bm25, "wb") as f:
        pickle.dump({"index": "fake"}, f)

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    result = migration.migrate_legacy_layout()
    assert result is True
    assert (chroma / "testdomain" / "testdomain_bm25.pkl").exists()
    assert not legacy_bm25.exists()


def test_migration_creates_backup(tmp_path, monkeypatch):
    """Migration should create a _legacy_backup/ with copies."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    (chroma / "td_knowledge").mkdir()
    (chroma / "td_knowledge" / "f.txt").write_text("x")

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    migration.migrate_legacy_layout()
    assert (chroma / "_legacy_backup" / "td_knowledge" / "f.txt").exists()


def test_migration_skips_already_migrated(tmp_path, monkeypatch):
    """If new layout already exists, migration should skip (no error)."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    # Create both legacy AND new layout
    (chroma / "td_knowledge").mkdir()
    (chroma / "td_knowledge" / "old.txt").write_text("old")
    (chroma / "td" / "chroma" / "td_knowledge").mkdir(parents=True)
    (chroma / "td" / "chroma" / "td_knowledge" / "new.txt").write_text("new")

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    result = migration.migrate_legacy_layout()
    # First pass skips because new collection dir exists → False from first pass
    # But orphaned BM25 pass might also be False
    assert result is False
    # Legacy dir should still be there (not moved)
    assert (chroma / "td_knowledge").exists()


def test_migration_orphaned_bm25_second_pass(tmp_path, monkeypatch):
    """Orphaned BM25 pkl (collection already migrated) should be moved."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    # Domain dir exists (collection already migrated) but BM25 still at root
    (chroma / "td" / "chroma").mkdir(parents=True)
    legacy_bm25 = chroma / "td_bm25.pkl"
    with open(legacy_bm25, "wb") as f:
        pickle.dump({"index": "fake"}, f)

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    result = migration.migrate_legacy_layout()
    assert result is True
    assert (chroma / "td" / "td_bm25.pkl").exists()
    assert not legacy_bm25.exists()