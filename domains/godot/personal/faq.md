# Godot FAQ — Noah's Answers

## Wann passiert was? (Lifecycle)
- **`_enter_tree()`** läuft, sobald der Node in den SceneTree eingehängt wird (auch bei jedem Reparenting). Children sind hier noch nicht garantiert im Tree.
- **`_ready()`** läuft **einmalig** genau dann, wenn der Node und **alle seine Children** im Tree sind. Das ist der richtige Ort für Setup, das Kinder referenziert (`get_node("Child")`, `$Path/To/Node`).
- **`_process(delta)`** läuft jeden Render-Frame mit variablem Delta. Für Input, UI, Kosmetik.
- **`_physics_process(delta)`** läuft im fixed Timestep (Standard 60 Hz, einstellbar in den Project Settings). Für Bewegung, Physik, Character-Controller.
- **`_exit_tree()`** läuft, wenn der Node aus dem SceneTree entfernt wird (z.B. vor `queue_free()`, bei Reparenting, bei Szenenwechsel).

**Häufiger Fehler:** `get_node()` in `_init()` aufrufen — Children sind zu diesem Zeitpunkt noch nicht im Tree, also existieren die Pfade nicht. Folge: `null` und spätere `null`-Dereferenz-Crashes. Lösung: `get_node()` erst in `_ready()` (oder in Funktionen, die nach dem `_ready()` laufen).

**Reihenfolge im Lifecycle:** `Node._init()` → `_enter_tree()` → `_ready()` (rekursiv Children zuerst) → wiederholt `_process()` / `_physics_process()` → `_exit_tree()` → `_notification(NOTIFICATION_PREDELETE)`.

```gdscript
extends Node

func _ready() -> void:
    # Children sind jetzt im Tree — sichere Referenzen.
    var child = $Child
    print("Child gefunden: ", child)
```

## Wie speichert man Daten?
- **`ConfigFile`** für INI-ähnliche `.cfg`-Dateien (Sections, Keys, Werte). Gut für Settings, einfache Save-Games.
- **`FileAccess`** für rohen I/O (`store_string`, `store_line`, `store_buffer`; `get_as_text`, `get_as_bytes`). Universal, aber du baust Format selbst.
- **`JSON.stringify(value)` + `JSON.parse_string(text)`** für strukturierte Daten (Dictionaries, Arrays, Strings, Zahlen, bool).
- **`ResourceSaver.save(resource, "user://...tres")`** für Godot-`Resource`-Instanzen (`.tres` textuell, `.res` binär). Ideal für Item-Daten, Waffen-Stats, Level-Layouts.
- **`user://`-Pfad** zeigt auf das plattformspezifische User-Datenverzeichnis (`~/.local/share/godot/app_userdata/<Name>/` auf Linux, `~/Library/Application Support/Godot/app_userdata/<Name>/` auf macOS, `%APPDATA%\Godot\app_userdata\<Name>\` auf Windows). Wird vom Sandbox-System korrekt behandelt, immer relativ zu `user://` speichern — nie in `res://` (read-only nach Export).

```gdscript
# Save
var config = ConfigFile.new()
config.set_value("player", "name", "Noah")
config.set_value("player", "level", 7)
config.save("user://save.cfg")

# Load
var config = ConfigFile.new()
var err = config.load("user://save.cfg")
if err == OK:
    var name = config.get_value("player", "name", "Default")
```

## Warum sehe ich mein 3D-Modell nicht?
- **`visible` Flag**: `MeshInstance3D.visible` (geerbt von `Node3D`) prüfen — und die aller Parents (`get_parent().visible` etc.). Eine unsichtbare Parent-Kette macht alles darunter unsichtbar.
- **`Camera3D.current`**: Nur eine `Camera3D` im Szenenbaum darf `current = true` haben. Wenn keine aktiv ist oder die falsche aktiv ist, siehst du schwarz. Mit `Camera3D.make_current()` oder im Inspector setzen.
- **`cull_mask` / `layers`**: `Camera3D.cull_mask` (Layer-Bitmask) und `GeometryInstance3D.layers` (Layer-Bitmask) müssen überlappen. Wenn dein Mesh auf Layer 1 ist und die Kamera nur Layer 2 rendert, ist es weg.
- **`process_mode`**: Wenn der Node in einem pausierten Subtree hängt (`process_mode = PROCESS_MODE_DISABLED` oder `PROCESS_MODE_PAUSABLE` in einem pausierten Tree), werden weder `_process()` noch Visual-Updates ausgeführt.
- **Scale / Position plausibel?** Modell könnte (1) extrem klein, (2) hinter der Kamera oder (3) unter der Welt positioniert sein. Im Editor auf den Node klicken und Transform prüfen.
- **Material-Transparenz**: `BaseMaterial3D.transparency = TRANSPARENCY_ALPHA` mit `alpha = 0` macht das Mesh unsichtbar. Auch `BaseMaterial3D.shading_mode = SHADING_MODE_UNSHADED` mit `albedo_color.a = 0`.

```gdscript
# Schnellcheck für Camera + MeshInstance3D-Sichtbarkeit
var cam := $Camera3D
if not cam.current:
    print("WARN: Kamera ist nicht current — mesh wird nicht gerendert")
    cam.make_current()

var mesh := $MeshInstance3D
if not mesh.visible or not mesh.get_parent().visible:
    print("WARN: Mesh oder Parent ist visible=false")
```
