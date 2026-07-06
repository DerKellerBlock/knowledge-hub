> Quelle: AugmentCode, Molisha Shah, 2025-10-10
> https://www.augmentcode.com/guides/multimodal-rag-development-12-best-practices-for-production-systems

# 12 Best Practices für Multimodal-RAG Production Systems

## Rule 1: Preserve Document Structure During Indexing
- Hierarchical chunking: parent_id fields in vector DB
- Tables bleiben mit captions verbunden, figures mit referenzen

## Rule 2: Generate Modality-Aware Embeddings Early
- Joint encoders (LLaVA, CLIP) in unified processing pipelines
- Single vector namespace per document
- Captions, alt-text, raw pixels teilen document identifiers

## Rule 3: Store Raw Assets Beside Vector Indexes
- S3/GCS URLs oder blob identifiers neben jeder vector row
- On-the-fly re-OCR oder higher-resolution crops bei response synthesis

## Rule 4: Combine Vector, Keyword, and Metadata Search
- Vector ANN: weight 0.6, BM25: weight 0.3, Metadata: weight 0.1
- HybridRAG benchmarks: „significantly outperform dense-only"

## Rule 5: Modularize the Extraction Pipeline
- Separate container services für text, image, table extraction
- Content hashing um unchanged documents zu überspringen
- Message queues für async processing

## Rule 6: Version Indexes, Prompts, and Encoders
- Vector DB: semantic version tags
- Prompt templates: Git-tracked
- Model versioning: env vars

## Rule 7: Build Modality-Aware Evaluation Harnesses
- Image-caption BLEU scores
- Table cell accuracy measurements
- Text exact-match validation
- Weighted averaging across modalities

## Rule 8: Cache Encoder Outputs to Control Cost
- Content-hash based caching (Redis/MongoDB)
- Fall back to GPU only on cache misses
- Monitor cache hit rates

## Rule 9: Monitor Retrieval Latency and Modality Mix
- OpenTelemetry tracing, Prometheus metrics, Grafana dashboards
- Track retrieval performance across modalities

## Rule 10: Guardrail Against Cross-Modal Hallucinations
- Structured schema validation für retrieved assets
- Verifier models checking response-asset consistency
- Grounding prompts requiring citation of specific asset URIs

## Rule 11: Close the Feedback Loop with Continuous Fine-Tuning
- Human feedback in golden datasets
- Monthly fine-tuning of retrieval thresholds and re-rankers
- A/B testing

## Rule 12: Design for Horizontal Scalability from Day One
- Sharded embedding stores
- Async ingestion queues
- GPU pools via vLLM
- Microservice architecture

## Für uns relevant (Solo-Hub, nicht Enterprise)
- Rule 1: Dokumentstruktur erhalten (parent_id, position)
- Rule 2: Joint-Encoder (jina-clip-v2), gemeinsamer Vektorraum
- Rule 3: Bild-Pfade in Metadaten (lokal, nicht S3)
- Rule 4: Hybrid haben wir schon (BM25 + Vector + RRF)
- Rule 8: Content-hash caching (lokal, SQLite wie context_cache)
- Rule 10: Hallucination-Guardrails (Verifier-Check)
