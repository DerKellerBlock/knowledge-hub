#!/usr/bin/env python3
"""
Migrate legacy ChromaDB layout to Per-Domain isolated layout.

Legacy:
    chromadb_data/godot_knowledge/   (collection)
    chromadb_data/godot_bm25.pkl     (BM25 index)

New:
    chromadb_data/godot/chroma/godot_knowledge/
    chromadb_data/godot/godot_bm25.pkl

Idempotent: only runs if legacy layout exists and new layout doesn't.
Creates a backup before migrating.

License: MIT.
"""

import shutil
from pathlib import Path

CHROMA_DIR = Path(__file__).resolve().parent.parent / "chromadb_data"


def migrate_legacy_layout() -> bool:
    """Migrate legacy layout to per-domain layout. Returns True if migrated.

    Scans for legacy patterns: chromadb_data/<domain>_knowledge/ and
    chromadb_data/<domain>_bm25.pkl and moves them into chromadb_data/<domain>/.
    """
    if not CHROMA_DIR.is_dir():
        return False

    migrated = False
    backup_dir = CHROMA_DIR / "_legacy_backup"

    # Find legacy collections: directories named <domain>_knowledge
    for entry in sorted(CHROMA_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name == "_legacy_backup":
            continue
        # Match <domain>_knowledge pattern (exclude already-migrated <domain>/ dirs)
        if not entry.name.endswith("_knowledge"):
            continue

        domain = entry.name[: -len("_knowledge")]
        new_domain_dir = CHROMA_DIR / domain / "chroma"
        new_collection_dir = new_domain_dir / entry.name

        # Skip if already migrated
        if new_collection_dir.exists():
            continue

        # Create backup
        backup_dir.mkdir(exist_ok=True)
        backup_collection = backup_dir / entry.name
        if not backup_collection.exists():
            shutil.copytree(str(entry), str(backup_collection))
            print(f"[MIGRATION] Backup: {entry.name} → _legacy_backup/")

        # Migrate collection
        new_domain_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(entry), str(new_collection_dir))
        print(f"[MIGRATION] Collection: {entry.name} → {new_collection_dir.relative_to(CHROMA_DIR)}")
        migrated = True

        # Migrate BM25 if exists
        legacy_bm25 = CHROMA_DIR / f"{domain}_bm25.pkl"
        if legacy_bm25.exists():
            backup_bm25 = backup_dir / legacy_bm25.name
            if not backup_bm25.exists():
                shutil.copy2(str(legacy_bm25), str(backup_bm25))
            new_bm25 = CHROMA_DIR / domain / legacy_bm25.name
            shutil.move(str(legacy_bm25), str(new_bm25))
            print(f"[MIGRATION] BM25: {legacy_bm25.name} → {new_bm25.relative_to(CHROMA_DIR)}")

    # Second pass: migrate any orphaned legacy BM25 pickles whose collection
    # was already migrated in a previous run (the first pass skips the whole
    # domain when the collection dir already exists, which would leave the
    # BM25 pkl stranded at the root).
    for entry in sorted(CHROMA_DIR.iterdir()):
        if not entry.is_file():
            continue
        if not entry.name.endswith("_bm25.pkl"):
            continue
        domain = entry.name[: -len("_bm25.pkl")]
        new_dir = CHROMA_DIR / domain
        if not new_dir.is_dir():
            # Domain dir doesn't exist at all — nothing to migrate into
            continue
        new_bm25 = new_dir / entry.name
        if new_bm25.exists():
            # Already migrated
            continue
        backup_dir.mkdir(exist_ok=True)
        backup_bm25 = backup_dir / entry.name
        if not backup_bm25.exists():
            shutil.copy2(str(entry), str(backup_bm25))
        shutil.move(str(entry), str(new_bm25))
        print(f"[MIGRATION] Orphaned BM25: {entry.name} → {new_bm25.relative_to(CHROMA_DIR)}")
        migrated = True

    if migrated:
        print("[MIGRATION] Done. Backup in chromadb_data/_legacy_backup/")
    return migrated


if __name__ == "__main__":
    migrate_legacy_layout()
