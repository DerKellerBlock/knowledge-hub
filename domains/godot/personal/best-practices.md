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

## Custom Resource als Item-Daten-Container
- **Pattern:** Eigene Resource-Subklasse mit `class_name` und `@export`-Properties für Editor-Editierbarkeit. Im FileSystem "Create New Resource" → ItemData → .tres speichern. Pro Item eine eigene `.tres`-Datei.
- **Warum:** Custom Resources sind Godots Standard-Container für Daten (Items, Waffen, Skills, Konfiguration). Im Inspector editierbar, serialisierbar als `.tres`/`.res`, in Arrays sortierbar, als `@export var inventory: Array[ItemData]` typisiert.
- **Workflow:**
  1. Script `item_data.gd` mit `class_name ItemData extends Resource` anlegen.
  2. `@export var name: String`, `@export var icon: Texture2D`, `@export var stats: Dictionary`, etc.
  3. Im FileSystem-Dock: Rechtsklick → New Resource → "ItemData" suchen → Name vergeben, Felder im Inspector ausfüllen → "Save" als `iron_sword.tres` etc.
  4. Im Inventory-Script: `@export var items: Array[ItemData]` exponieren und im Inspector Items zuweisen.
- **Projekt:** nak-hopper-game (geplant für Inventar-System)

```gdscript
# item_data.gd — Custom Resource für Item-Definitionen (Godot 4 stable API)
class_name ItemData extends Resource

@export var name: String = ""
@export var description: String = ""
@export var icon: Texture2D
@export var stack_size: int = 1
@export var value: int = 0
# Stats sind ein Dictionary für flexible Item-Properties
@export var stats: Dictionary = {
    "damage": 0,
    "defense": 0,
    "weight": 0.0,
}
# Verschachtelte Custom Resources (z.B. Verbrauchs-Items)
@export var consumable_effect: Resource
```

```gdscript
# inventory.gd — Verwendung als typisiertes Array
@export var items: Array[ItemData] = []

func add_item(item: ItemData, count: int = 1) -> void:
    items.append(item)
    print("Added ", count, "x ", item.name)
```

- **Editor-Workflow Schritt-für-Schritt:**
  1. Im FileSystem-Panel: Rechtsklick auf den Ziel-Ordner → New Resource
  2. Im Suchfeld "ItemData" eingeben (erscheint via class_name) → Create
  3. Inspector zeigt die @export-Felder (name, icon, stack_size, value, stats)
  4. Dateiendung `.tres` wählen, Datei speichern
  5. Im Spiel: `var sword: ItemData = load("res://items/iron_sword.tres")` oder im Inspector einer @export-Property zuweisen
- **Runtime-API:**
  - `ResourceSaver.save(item, "user://inventory.tres")` speichert Instanzen zur Laufzeit (z.B. Spielstand)
  - `ResourceLoader.load("res://items/iron_sword.tres")` lädt zur Laufzeit
  - `item.duplicate()` für temporäre Kopien ohne Disk-I/O
  - `.tres` ist textuell (git-freundlich), `.res` ist binär (kleiner, schneller, aber nicht diff-bar)
- **Wichtige Tokens:** `Resource`, `custom resource`, `class_name`, `@export`, `item`, `data`, `icon`, `texture`, `stats`, `editor`, `ResourceSaver`, `ResourceLoader`, `.tres`, `.res`, `instance`, `inspector`, `Array[ItemData]`. Für Inventar-Systeme zusätzlich `duplicate()` und `ResourceSaver.save()` für Save-Game-Integration nutzen.

## 3D

### ChurchData.scale Drei-Modus-Semantik
- **Pattern:** Drei Modi je nach GLB-Typ: (a) native bottom-origin, (b) v2-Platzhalter-Kompensation, (c) real-world units
- **Warum:** Meshy-Modelle kommen in verschiedenen nativen Größen. Siehe docs/ai/best-practices.md.
- **Projekt:** nak-hopper-game

## 3D Open-World Performance: LOD + Occlusion + Visibility Ranges
- **Pattern:** Drei-Stufen-Strategie für mobile Open-World-Szenen: (a) Mesh-LOD per GLB-Import-Thresholds reduziert Vertex-Count bei Distanz, (b) `OccluderInstance3D` mit gebacktem Occluder verhindert Rendering hinter Wänden, (c) `GeometryInstance3D.visibility_range_begin` / `visibility_range_end` schaltet weit entfernte Nodes komplett ab.
- **Warum:** Ohne diese Maßnahmen zieht eine offene Szene mit 500+ MeshInstance3D-Nodes das Mobile-Framebuffer auf unter 30 FPS. LOD reduziert Draw-Calls pro Frame; Occlusion Culling überspringt Objekte komplett, die hinter Wänden sind; Visibility Ranges vermeiden, dass weit entfernte Props überhaupt in die Render-Pipeline gehen.
- **Setup:**
  1. **Mesh-LOD:** Im GLB-Import-Dialog "Generate LODs" aktivieren, Threshold in Pixeln setzen (Standard 4 Pixel — bei Mobile 8-12 für bessere Performance).
  2. **Visibility Range:** Pro `MeshInstance3D` im Inspector `Visibility Range Begin` und `End` setzen (z.B. 50m–200m), oder programmatisch:
  ```gdscript
  # Sichtbarkeitsrange pro Mesh setzen (Godot 4 stable API)
  for mesh in get_tree().get_nodes_in_group("props"):
      if mesh is GeometryInstance3D:
          mesh.visibility_range_begin = 50.0
          mesh.visibility_range_end = 200.0
          # Optional: fade-mode für weiche Übergänge
          mesh.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF
  ```
  3. **Occlusion Culling:** `OccluderInstance3D`-Node in die Szene, Bake-Button im Inspector klicken (erzeugt eine `.occ`-Datei mit den Silhouetten statischer Geometrie). Nur für statische Architektur sinnvoll — bewegliche Objekte brauchen Visibility Ranges.
- **Projekt:** nak-hopper-game (geplant)
- **Wichtige Tokens:** `LOD`, `level of detail`, `occlusion culling`, `OccluderInstance3D`, `visibility range`, `GeometryInstance3D`, `visibility_range_begin`, `visibility_range_end`, `draw calls`, `mobile`, `performance`, `open-world`, `HLOD`. Für sehr große Welten zusätzlich `WorldEnvironment` mit `glow_enabled = false` auf Mobile und `RenderingServer.render_loop_enabled = false` während des Ladens von großen Szenen erwägen.

## UI

### CanvasLayer-Layer-Strategie
- **Pattern:** UI in dedizierten CanvasLayers: Controls (10), Buttons (15), Modals (20)
- **Warum:** Verhindert Z-Order-Konflikte, Mobile-tauglich.

## Responsive UI mit Container + Anchor + Size Flags
- **Pattern:** Für responsive UI über verschiedene Screen-Größen und Aspect-Ratios: Container-Hierarchie statt festen Positionen, Size-Flags (`SIZE_EXPAND_FILL`, `SIZE_SHRINK_BEGIN`, `SIZE_FILL`) für Skalierungsverhalten, `Anchor` als Preset (Full Rect für Root, Custom fürs Positionieren).
- **Warum:** Godot 4 Container passen ihre Children automatisch an Parent-Size an. Ohne Container skaliert UI auf Mobile oder 4K-Monitoren nicht — Controls überlappen, schneiden ab oder sind zu klein. Mit `MarginContainer`/`VBoxContainer`/`HBoxContainer`/`GridContainer`/`AspectRatioContainer` bleibt das Layout stabil.
- **Container-Bausteine:**
  - `MarginContainer` — hält konsistente Abstände zum Parent-Rand
  - `VBoxContainer` / `HBoxContainer` — vertikale/horizontale Anordnung
  - `GridContainer` — tabellarisches Layout (z.B. Inventar)
  - `AspectRatioContainer` — fixiert Aspect-Ratio (z.B. 16:9 Game-View)
  - `CenterContainer` — zentriert Child
  - `PanelContainer` / `ScrollContainer` — Decorations
- **Anchor-Presets:** im Inspector unter Layout: Full Rect (Standard für Root-Control), Center, Top Wide, etc. Custom Anchors mit Anchor Right = 1.0, Anchor Bottom = 1.0 für "dehnen an Parent".
- **Size Flags (Godot 4):** `size_flags_horizontal = SIZE_EXPAND_FILL` lässt ein Child den verbleibenden Platz einnehmen, `SIZE_SHRINK_CENTER` zentriert und schrumpft auf Minimal-Größe.
- **Beispiel-Hierarchie** (responsive Settings-Menü, funktioniert auf Mobile + Desktop):

```gdscript
# Root-Control: Anchor = Full Rect (Inspector), damit es den Viewport füllt
# MarginContainer (margins 16px rundum) → VBoxContainer (Title, Body, Buttons)
#   Title: Label "Settings", size_flags_vertical = SIZE_SHRINK_TOP
#   Body: HBoxContainer (size_flags_vertical = SIZE_EXPAND_FILL)
#     Left: VBoxContainer mit Option-Buttons
#     Right: AspectRatioContainer mit Preview
#   Buttons: HBoxContainer, size_flags_vertical = SIZE_SHRINK_BOTTOM
#     Spacer (Control mit size_flags_horizontal = SIZE_EXPAND_FILL)
#     OK-Button, Cancel-Button
```

```gdscript
# Programmatisch (Godot 4 stable API):
var margin := MarginContainer.new()
margin.add_theme_constant_override("margin_left", 16)
margin.add_theme_constant_override("margin_right", 16)
add_child(margin)

var vbox := VBoxContainer.new()
vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
margin.add_child(vbox)

var label := Label.new()
label.text = "Settings"
label.size_flags_vertical = Control.SIZE_SHRINK_CENTER
vbox.add_child(label)
```

- **Wichtige Tokens:** `Container`, `MarginContainer`, `VBoxContainer`, `HBoxContainer`, `GridContainer`, `AspectRatioContainer`, `CenterContainer`, `Anchor`, `responsive`, `screen size`, `aspect ratio`, `size flags`, `SIZE_EXPAND_FILL`, `SIZE_SHRINK_CENTER`, `Control`, `theme`, `add_theme_constant_override`. Für Theme-Switching (Dark/Light Mode) zusätzlich `Theme`-Resource auf Root-Control setzen und mit `theme_type_variation` arbeiten.
