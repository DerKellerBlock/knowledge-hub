# Godot Tips — Kurze Hinweise

## Editor
- `Ctrl+Shift+F` sucht in allen Dateien (besser als Dateisystem-Suche)
- `F5` startet das Spiel mit der aktuellen Szene (nicht main scene)

## GDScript
- `@export var foo := 42` setzt Typinferenz auf int (nicht Variant)
- `$Node` ist Kurzform für `get_node("Node")` — nutzen!
- `call_deferred("method")` wenn du Signale in `_ready()` emitest

## 3D
- `QuadMesh` liegt standardmäßig in XY-Ebene → um -90° auf X rotieren für Boden
- `own_world_3d = true` in SubViewport für isolierte 3D-Contexts (Picker, Preview)

## CharacterBody3D Stair Stepping
- CharacterBody3D hat native stair stepping (PR #114447, 2025-12-30, open): Properties `step_enabled`, `step_height` (default 0.3m), `step_smooth_enabled`, `step_smooth_speed`
- Methode `get_visual_position()` für geglättete Kamera-Position
- Algorithmus: UP-FORWARD-DOWN Trace bei Wall-Kollision
- Alle Physics-Backends (GodotPhysics, Jolt), nur `MOTION_MODE_GROUNDED`
- Empfehlung: `CylinderShape3D` statt `BoxShape3D` für beste Ergebnisse
