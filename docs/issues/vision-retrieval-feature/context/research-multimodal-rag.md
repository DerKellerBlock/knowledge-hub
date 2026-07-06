> Quelle: TowardsDataScience, Partha Sarkar, 2025-11-03
> https://towardsdatascience.com/building-a-multimodal-rag-with-text-images-tables-from-sources-in-response/

# Multimodal RAG mit Text, Bildern und Tabellen

## Kern-Erkenntnis: Context-Aware Image Summaries

Standard-Bild-Captions verlieren den Kontext. Ein LLM das ein Bild beschreibt
erzeugt z.B. „Tabelle mit Working-Capital-Optionen" — verfehlt aber ob es für
„primäre Produzenten" oder „Verarbeiter" ist.

Lösung: Context-Aware Image Summaries:
- Extrahiere Text ±200 Zeichen vor und nach dem Bild aus dem PDF
- Kombiniere: Autor-Caption (falls vorhanden) + umgebender Text + LLM-Beschreibung
- Resultat: Kontextuell korrekte Caption die zwischen ähnlichen Bildern unterscheidet

## Kern-Erkenntnis: Text-Response-Guided Image Selection

Bilder nicht gegen Query matchen (Query zu kurz), sondern gegen generierte
Text-Antwort:
1. Query → Top-5 Text-Chunks → generiere Text-Antwort via LLM
2. Text-Antwort → matche gegen Bild-Caption-Embeddings → Top-2 Bilder
3. Final: LLM generiert Display-Caption aus Bild-Caption + Bild

## Pipeline

### Extraction
- Adobe PDF Extract API (oder PyMuPDF4LLM): figures/ + tables/ + structuredData.json
- Text + Position + Bild-Pfad in JSON

### Captioning
- Pro Bild: Quality-Check („Good" vs „Poor" — logos, illegible aussortieren)
- Context extraction: ±200 chars um Bild-Position in JSON
- Caption = umgebender Text (NICHT LLM-Beschreibung des Bilds allein)

### Embedding
- Text-Chunks: text-embedding-3-small (OpenAI)
- Image-Captions: gleiche Embeddings (gleicher Vektorraum)
- FAISS-Index

### Retrieval
- Query → Top-5 Text-Chunks → LLM generiert Text-Antwort
- Text-Antwort → Top-2 Image-Caption-Matches
- LLM generiert Display-Caption aus Image-Caption + Bild

## Für uns relevant
- Context-Aware Image Summaries: umgebenden Text aus PDF extrahieren
- Text-Response-Guided Image Selection: Bilder gegen Antwort matchen, nicht Query
- Quality-Check: logos/illegible Bilder aussortieren
