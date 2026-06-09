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
