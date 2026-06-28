# AI Changelog

## 2026-06-27

- **feat:** Per-Domain ChromaDB-Isolation (eigene DB pro Domain)
- **feat:** Domain-Scoped MCP-Server (`--domains` CLI-Flag)
- **feat:** Central Model Manager (lazy loading, LRU cache, unload)
- **feat:** PDF → Markdown Build-Script (PyMuPDF4LLM, AGPL Process Boundary)
- **feat:** DaVinci Resolve Domain (10 Blackmagic PDF-Quellen)
- **feat:** Search regression validation script
- **feat:** Automatic legacy layout migration with backup
- **docs:** THIRD_PARTY_LICENSES.md, ADRs for isolation + AGPL boundary
- **refactor:** All search modules use model_manager instead of direct
  SentenceTransformer/CrossEncoder instantiation