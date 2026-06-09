# Godot Best Practices — Patterns die funktioniert haben

> Bewährte Patterns aus dem `nak-hopper-game`-Projekt.

## GDScript

### class_name + preload für cross-file Typen
- **Pattern:** `const _Foo := preload("res://path.gd")` statt reine `class_name`-Referenz
- **Warum:** Vermeidet Parse-Races beim Auto-Reload. Siehe docs/ai/fixes.md FX-001.
- **Projekt:** nak-hopper-game

### Wiring-by-@export NodePath + @onready
- **Pattern:** Nodes via `@export var path: NodePath` + `@onready var node = get_node(path)` referenzieren
- **Warum:** Entkopplung im Editor-Inspector konfigurierbar, tolerant gegenüber Scene-Tree-Änderungen.

## 3D

### ChurchData.scale Drei-Modus-Semantik
- **Pattern:** Drei Modi je nach GLB-Typ: (a) native bottom-origin, (b) v2-Platzhalter-Kompensation, (c) real-world units
- **Warum:** Meshy-Modelle kommen in verschiedenen nativen Größen. Siehe docs/ai/best-practices.md.
- **Projekt:** nak-hopper-game

## UI

### CanvasLayer-Layer-Strategie
- **Pattern:** UI in dedizierten CanvasLayers: Controls (10), Buttons (15), Modals (20)
- **Warum:** Verhindert Z-Order-Konflikte, Mobile-tauglich.
