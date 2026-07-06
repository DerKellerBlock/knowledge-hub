> Quelle: Ollama Blog, 2025-05-15 + GitHub Issue #5304, 2024-06-26
> https://ollama.com/blog/multimodal-models
> https://github.com/ollama/ollama/issues/5304

# Ollama Multimodal Support — Einschränkungen

## Was Ollama unterstützt
- Multimodale LLMs (Vision-Chat): Llama 4, Gemma 3, Qwen 2.5-VL, MiniMax M3,
  Mistral Small 3.1
- Bild-Input für Chat: `ollama run gemma3` + Bild hochladen
- API: `/api/chat` mit `images: [base64]` field

## Was Ollama NICHT unterstützt
- Multimodale Embedding-Modelle (CLIP, jina-clip-v2, SigLIP)
- Issue #5304 offen seit Juni 2024, kein Progress
- Embedding-API (`/api/embeddings`) akzeptiert nur Text, keine Bilder
- Community hat zu vLLM gewechselt für multimodale Embeddings

## Implikation für uns
- jina-clip-v2 kann NICHT via Ollama laufen
- Muss via transformers/sentence-transformers geladen werden (wie BGE-M3)
- model_manager.py muss neue Modell-Klasse hinzufügen (multimodal_embedder)
- Keine KH_LLM_MODEL env var, sondern KH_MULTIMODAL_MODEL oder ähnlich

## Vision-LLM (für Captioning) via Ollama
- Gemma 3 (gemma3:4b) unterstützt Vision, läuft via Ollama lokal
- Alternative: gemma4:cloud via Ollama Cloud
- API: `/api/chat` mit images field, base64-encoded
- Für Build-Only: lokal oder Cloud, wie Contextual-Retrieval
