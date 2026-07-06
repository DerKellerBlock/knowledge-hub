> **Archived Evaluation Report** | **Datum:** 2026-06-30 | **Evaluator:** orchestrator-knowledge
>
> Manuelle Bewertung der Real-World Source Comparison. Siehe `docs/superpowers/specs/2026-06-29-real-world-source-evaluation-design.md` für die Methodik.

# Quality Report: davinci_resolve — 2026-06-30

## Summary
- **Domain:** davinci_resolve
- **Date:** 2026-06-30
- **Questions evaluated:** 7
- **Composite Score:** 0.7532
- **Pass:** 7 (100.0%) | **Weak:** 0 (0.0%) | **Fail:** 0 (0.0%)

## Metric Averages
| Metric | Average |
|--------|---------|
| Source Recall | 1.0 |
| Page Metadata Accuracy | 0.3286 |
| Top-K Relevance | 0.55 |
| Evidence Quality | 1.0 |

## Per-Question Results
| ID | Question | Score | Label | SR | PMA | TKR | EQ |
|----|----------|-------|-------|----|----|----|----|
| davinci_resolve-001 | How do I set up a Planar Tracker in DaVi... | 0.7475 | pass | 1.0 | 0.3 | 0.55 | 1.0 |
| davinci_resolve-002 | How do I trim a clip on the Edit page in... | 0.7475 | pass | 1.0 | 0.3 | 0.55 | 1.0 |
| davinci_resolve-003 | How do I use Primary Color Correction in... | 0.7475 | pass | 1.0 | 0.3 | 0.55 | 1.0 |
| davinci_resolve-004 | What is the difference between Point Tra... | 0.7475 | pass | 1.0 | 0.3 | 0.55 | 1.0 |
| davinci_resolve-005 | How do I render and deliver a finished p... | 0.7475 | pass | 1.0 | 0.3 | 0.55 | 1.0 |
| davinci_resolve-006 | How do I work with audio tracks and effe... | 0.7475 | pass | 1.0 | 0.3 | 0.55 | 1.0 |
| davinci_resolve-007 | What are the new features in DaVinci Res... | 0.7875 | pass | 1.0 | 0.5 | 0.55 | 1.0 |

## Weak / Fail Details
- No weak or fail questions.

## Truncation Warnings
- davinci_resolve-001: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- davinci_resolve-002: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- davinci_resolve-003: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- davinci_resolve-004: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- davinci_resolve-005: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- davinci_resolve-006: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- davinci_resolve-007: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).

## Real-World Source Comparison

Online source coverage and Hub top-3 snippets for manual solution-alignment review.

### davinci_resolve-001: How do I set up a Planar Tracker in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fusion | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. ve done this anyway, for example, framing someone’s moving face with a Circular window to lighten their highlights.  **3** To initiate tracking, do one of the following:     - Choose Color > Tracker >
2. hree parts. First, you’ll  need to track the flat surface as it moves. Then, using Fusion’s Paint tool, you’ll remove any  tracking markers to create a clean surface. Once that is complete, you can co
3. . Connecting the MediaIn or Loader node to the Lens Distort node displays controls for manually correcting lens distortion. If you use Synth Eyes, PFTrack or 3D Equalizer software, you can also import

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet Reference Manual (Tracking Nodes, Planar Tracker Node) und Fusion Visual Effects Training.
- [x] Solution Alignment: PASS — Hub Snippet 1 zeigt "Color > Tracker" Tracking-Initiierung, Snippet 2 zeigt "track the flat surface as it moves" + Paint tool. Online-Quelle (fusion page) beschreibt gleichen Workflow: connect clip, draw shape, track forward.
- [x] Gap Detection: PASS — Keine Lücke.

### davinci_resolve-002: How do I trim a clip on the Edit page in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/edit | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. n incoming edit on another track.   Selecting opposite outgoing video and incoming audio edit points in preparation for performing an asymmetric ripple trim   To select the outgoing video edit of one
2. ive frame.  **3** Right-click that clip, and choose Set Poster Frame, or press Command-P.   **To clear the custom poster frame of any clip:**   - Right-click a clip, and choose Clear Poster Frame, or
3. e to make room, click the Trim tool, and drag an edit point to a new position in the Timeline.   Selected outgoing half of an edit point before ripple   Rippled clip is shorter, the rest of the Timeli

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet Reference Manual (asymmetric ripple trim, poster frame, trim tool ripple).
- [x] Solution Alignment: PASS — Hub Snippets zeigen Trim-Werkzeuge (asymmetric ripple, trim tool drag edit point). Online-Quelle (edit page) beschreibt smart trim (ripple/roll/slip/slide). Thematisch übereinstimmend.
- [x] Gap Detection: PASS — Keine Lücke. Hinweis: Editors Guide wird bei Trim-Fragen nicht gefunden (Retrieval-Lücke, bereits in dvr-002 notes dokumentiert).

### davinci_resolve-003: How do I use Primary Color Correction in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/color | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. You can see that the color just doesn’t quite match.   **9** With clip 11 still selected in the timeline, right-click clip 10 and, from the menu, choose  Shot Match to this Clip, and DaVinci Resolve
2. to tint the ground green, matching the  overall look of the scene to clip 04. Apply a window to limit the correction to the field.   **Clip 11** —Use the Tilt-Shift Blur effect to create an artificial
3. gement schemes designed to solve the same problem. However, if you’re not in a specific ACES-driven cinema workflow, DaVinci Resolve Color Management can be simpler to use, and will give you all of th

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet Colorist Guide (Shot Match, window/field correction, ACES vs Resolve Color Management).
- [x] Solution Alignment: WEAK — Hub Snippets zeigen Shot Match, Tilt-Shift Blur, Color Management — nicht spezifisch "Primary Wheels (Lift/Gamma/Gain/Offset)" die die Online-Quelle als primäre Lösung nennt. Die Primary-Tools sind wahrscheinlich im Index aber nicht in Top-3.
- [x] Gap Detection: PASS — Keine kritische Lücke.

### davinci_resolve-004: What is the difference between Point Tracker and Planar Tracker in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fusion | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/color | official-docs | yes | — |

**Hub Top Snippets:**

1. e described in detail in the following “The Common Controls” section.      Fusion Page Effects | Chapter 119 Tracking Nodes **2767**     --- end of page=2766 ---  #### Planar Tracker Node [PTRA]  The
2. hree parts. First, you’ll  need to track the flat surface as it moves. Then, using Fusion’s Paint tool, you’ll remove any  tracking markers to create a clean surface. Once that is complete, you can co
3. r 59** ### Tracking Nodes  This chapter details the Tracking nodes available in Fusion.   The abbreviations next to each node name can be used in the Select Tool dialog when searching for tools and in

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet Reference Manual (Planar Tracker Node [PTRA], Tracking Nodes chapter) und Fusion Visual Effects Training.
- [x] Solution Alignment: PASS — Hub Snippet 1 zeigt "Planar Tracker Node [PTRA]", Snippet 3 zeigt "Tracking Nodes" chapter. Online-Quellen (fusion page + color page) unterscheiden 2D tracker vs Planar tracker. Hub deckt die Unterscheidung ab.
- [x] Gap Detection: PASS — Keine Lücke. Tracker-Verwechslungs-Falle (Point vs Planar) ist im Orchestrator-Prompt dokumentiert.

### davinci_resolve-005: How do I render and deliver a finished project in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/edit | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. ing**  ��������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������� 111  Chec
2. checkbox. If you do this, then DaVinci Resolve by default renders each of the video clips you selected, along with every speed effect, transform, and Color page operation that’s been applied to each
3. inishing**  Once you’re finished with your final grade, you’ll again use the controls of the Deliver page to render the program’s final media, either as individual clips for a round-trip workflow, or

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet Reference Manual (rendering, Deliver page, final grade render).
- [x] Solution Alignment: PASS — Hub Snippets zeigen rendering/finishing workflow, Deliver page controls. Online-Quelle (edit page) beschreibt Quick Export. Thematisch übereinstimmend.
- [x] Gap Detection: PASS — Keine Lücke. Hinweis: Snippet 1 hat Encoding-Artifakte () — mögliche Index-Qualitäts-Einschränkung.

### davinci_resolve-006: How do I work with audio tracks and effects in Fairlight in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fairlight | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. ered from voiceover to background ambience. ## **Showing and Hiding Tracks**   The Fairlight page in DaVinci Resolve offers a variety of tools at your fingertips to quickly  customize how you view the
2. our own sounds.   MORE INFO You can find more information about indexing other sound  collections into the Sound Library in the DaVinci Resolve User Manual available via  the DaVinci Resolve Help menu
3. ght FX, Track FX, and AI tools to your clips  and tracks to enhance your soundtrack; as well as mixing and automating tracks,  processes, effects, and more! Best of all, you no longer need to send pro

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet Fairlight Audio Post Guide (tracks, sound library, Fairlight FX, mixing/automation).
- [x] Solution Alignment: PASS — Hub Snippets zeigen "Showing and Hiding Tracks", "Sound Library indexing", "Fairlight FX, Track FX, AI tools + mixing/automation". Online-Quelle (fairlight page) beschreibt gleichen Funktionsumfang.
- [x] Gap Detection: PASS — Keine Lücke.

### davinci_resolve-007: What are the new features in DaVinci Resolve 21?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/whatsnew | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/support | official-docs | yes | — |

**Hub Top Snippets:**

1. odove toolset adds over 70 new graphics to Fusion, Fairlight folders simplify audio track management, plus there are improvements to keyframing, MultiMaster trim passes, layer list node graphs.   The
2. ack layers in DaVinci Resolve 21 has been increased from four to eight. ### **Film Look Creator adds Aurora** **Preset and Fade Rolloff Controls**  The Film Look Creator in DaVinci Resolve 21 adds a n
3. oves rapidly across the frame, such as from one corner to another within a few seconds.   New Features Guide DaVinci Resolve 21 | AI Tools **59**     --- end of page=58 ---  ## Cut and Edit  ### **Can

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet New Features Guide (Krokodove toolset 70+ graphics, Fairlight folders, keyframing, MultiMaster, Film Look Creator Aurora).
- [x] Solution Alignment: PASS — Hub Snippets zeigen Krokodove, Fairlight folders, Film Look Creator — konkrete neue Features. Online-Quelle (whatsnew page) listet dieselben Features.
- [x] Gap Detection: PASS — Keine Lücke.

## Gaps & Recommendations
- No weak/fail questions. Domain coverage looks healthy.

## Summary of Findings

### Verteilung nach Ebene

| Ebene | PASS | WEAK | GAP | Total |
|-------|------|------|-----|-------|
| Source Coverage | 7 | 0 | 0 | 7 |
| Solution Alignment | 6 | 1 | 0 | 7 |
| Gap Detection | 7 | 0 | 0 | 7 |
| **Total** | **20** | **1** | **0** | **21** |

### Top-Gaps und Empfehlungen

Keine kritischen Gaps identifiziert. Domain ist gut abgedeckt.

### Beobachtungen und Schwächen (WEAK)

1. **davinci_resolve-003 — Primary Color Correction Tools in Top-3 schwach**: Hub Snippets zeigen Shot Match, Tilt-Shift Blur, Color Management, aber nicht die spezifischen "Primary Wheels (Lift/Gamma/Gain/Offset)". Die Primary-Tools sind wahrscheinlich im Index aber nicht in Top-3. → Empfehlung: Retrieval-Tuning prüfen (Chunks für "Primary Wheels" / "Primary Correction" sollten höher ranken bei dieser Frage). Eventuell einen personal note zu "Primary Color Correction Workflow" anlegen, der die Lift/Gamma/Gain/Offset-Struktur zusammenfasst.

### Hinweise (keine Gaps)

- **davinci_resolve-002 Editors Guide**: Wird bei Trim-Fragen nicht in Top-3 gefunden (Retrieval-Lücke, bereits in Golden Dataset notes dokumentiert). Index-Tuning könnte die Recall verbessern, ist aber kein Inhalts-Gap.

- **davinci_resolve-005 Encoding-Artefakte**: Snippet 1 zeigt Encoding-Artifakte (Mojibake/Zeichensalat) — mögliche Index-Qualitäts-Einschränkung beim Parsen des PDF. → Empfehlung: PyMuPDF4LLM-Encoding prüfen oder betroffenes PDF re-indizieren.

- **Page Metadata Accuracy (PMA)** liegt bei 0.3286 — niedrig weil die meisten Fragen PMA-Score 0.3 haben (PMA wird nur gezählt wenn `page_start`/`page_end` Metadaten vorhanden und im ±2 Seitentoleranz-Bereich der `expected_page_ranges` sind, siehe LIM-004). Die Frage 007 (New Features) erreicht PMA 0.5 — die einzige Frage die Page-Metadaten gut trifft.

- **Truncation Warnings** bei allen 7 Fragen (jeweils 10/10 Truncations) — LIM-003 bestätigt. DaVinci-Fallback-Chunks können bis ~8000 Zeichen groß sein und werden auf 5000 trunkiert. Das ist eine systematische Limitation der DaVinci-Indexierung ohne domain-spezifischen Parser (LIM-002).

- **Composite Score 0.7532** für alle 7 Fragen "pass", weil Source Recall 1.0 und Evidence Quality 1.0 die niedrige TKR (0.55) kompensieren. Die manuelle Evaluation zeigt aber, dass die DaVinci-Domain inhaltlich sehr gut abgedeckt ist — die einzige WEAK-Bewertung betrifft die Ranking-Reihenfolge bei einer Frage, nicht die Inhalts-Abdeckung.