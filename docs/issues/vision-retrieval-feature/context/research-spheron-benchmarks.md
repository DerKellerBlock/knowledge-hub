> Quelle: Spheron Network, 2026-06-02
> https://www.spheron.network/blog/multimodal-embedding-models-gpu-cloud-siglip2-jinaclip-cohere/

# Multimodal Embedding Benchmarks und Deployment Guide

## Modell-Landschaft (Juni 2026)

| Modell | Arch | Output dim | Max image res | Open weights | Lizenz |
|---|---|---|---|---|---|
| SigLIP-2 ViT-SO400M | SigLIP dual-encoder | 1152 | 512x512 | Ja | Apache 2.0 |
| JinaCLIP-v2 | CLIP dual-encoder | 1024 (Matryoshka 64-1024) | 224x224 | Ja | Apache 2.0 |
| Cohere Embed-v4 | proprietary | 1024 | variable | commercial | — |
| Voyage-multimodal-3 | proprietary | 1024 | variable | nein (API) | — |
| NV-Embed-Multimodal | NVIDIA | 4096 | 336x336 | research | — |

## Empfehlung für uns
- **JinaCLIP-v2** — multilingual (89 Sprachen, passt zu BGE-M3/jina-reranker Stack),
  Matryoshka (1024 truncatable), Apache 2.0, 224x224 (niedriger als SigLIP-2
  aber ausreichend für UI-Screenshots)
- Alternative: SigLIP-2 (bessere accuracy, aber English-only, 512x512 = 4× mehr
  pixel throughput = langsamer)

## GPU Throughput Benchmarks (NVIDIA)

| GPU | JinaCLIP-v2 Batch | Throughput (pairs/hr) | $/hr |
|---|---|---|---|
| L40S 48GB | 256 | ~40-60k | $0.96 |
| A100 80GB | 512 | ~65k | $1.19 (spot) |
| H100 80GB | 512 | ~75-95k | $2.91 (spot) |
| B200 192GB | 1024 | ~120-160k | $2.68 (spot) |

## M1 Max MPS Schätzung (keine direkten Benchmarks verfügbar)
- M1 Max MPS ~5-10× langsamer als A100 (basierend auf BGE-M3 Erfahrung)
- Geschätzt: ~6.000-15.000 pairs/hr (vs A100 65.000)
- Bei 8.000 Bildern: ~30 min - 2h (MPS), 2-5h (CPU)

## Deployment: Infinity-Embedding (für uns nicht relevant)
- Infinity-Embedding ist ein Docker-Container-Server für production serving
- Für unseren Build-Only-Use-Case: direkte transformers-Nutzung (wie BGE-M3)

## Image Preprocessing (kritisch!)
- JinaCLIP-v2: mean [0.485, 0.456, 0.406], std [0.229, 0.224, 0.225], 224x224
- NIEMALS hardcoden — immer AutoProcessor.from_pretrained() verwenden
- Falsche normalization = niedrige cosine similarity (0.3 statt 0.6+)

## Latency Optimierung
- ONNX-Export: 20-40% speedup (Ampere/Hopper, MPS ungetestet)
- FP8 Quantization: nur Hopper/Blackwell, nicht M1 Max
- Dynamic Batching: offline indexing = batch 256-512, online = 64-128
- Warm-Up: 2-5s cold start, dummy request vor production traffic

## Modality Gap (wichtig für RRF-Fusion!)
- CLIP image und text embeddings clustern in verschiedenen Regionen
  der Einheitskugel
- Image-to-text retrieval accuracy 10-20% unter benchmark bei domain-shift
- Mitigation: fine-tune mit contrastive loss, oder late-interaction (ColPali)
- Für uns: RRF-Fusion muss Modality-Gap berücksichtigen

## Für uns relevant
- JinaCLIP-v2: 224x224 Input (nicht 512x512), Apache 2.0, multilingual
- AutoProcessor zwingend (keine hardcodierte normalization)
- MPS Speedup: ~5-10×, Pre-Flight-Test nötig
- Modality Gap: RRF-Fusion braucht angepasste Gewichtung
- ONNX-Export: optional, testen auf MPS
