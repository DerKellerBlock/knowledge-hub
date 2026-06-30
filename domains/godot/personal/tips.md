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

### Integration in einen vollständigen CharacterBody3D-Controller

Das folgende GDScript-Snippet zeigt einen kompletten 3D-Character-Controller mit Gravity, Jumping, Movement und smooth stair stepping. Es kombiniert dokumentierte Godot-4-Stable-APIs (`CharacterBody3D`, `move_and_slide`, `is_on_floor`, `Input`, `ProjectSettings`) mit den PR-#114447-APIs (`step_height`, `get_visual_position`), die noch nicht in Godot stable sind.

```gdscript
extends CharacterBody3D

# Geschwindigkeit und Sprunghöhe im Inspector editierbar
@export var speed := 5.0
@export var jump_velocity := 4.5

# Native stair stepping (requires PR #114447, not yet in Godot stable):
# step_enabled und step_height sind erst mit PR #114447 verfügbar.
# In Godot stable: nur manuelle workarounds via Raycast.
@export var step_height := 0.3  # PR #114447 property
@export var step_enabled := true  # PR #114447 property

# Standard-3D-Gravity aus den ProjectSettings (Godot 4 stable API)
var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")


func _physics_process(delta: float) -> void:
	# Gravity anwenden, solange wir nicht am Boden stehen
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Sprung nur vom Boden aus (Godot 4 stable API)
	# Input action "jump" muss in ProjectSettings > Input Map definiert sein
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity

	# Horizontal-Bewegung via Input-Actions (Godot 4 stable API)
	# "left", "right", "forward", "back" müssen in ProjectSettings > Input Map definiert sein
	var input_dir := Input.get_vector("left", "right", "forward", "back")
	var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

	if direction:
		velocity.x = direction.x * speed
		velocity.z = direction.z * speed
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		velocity.z = move_toward(velocity.z, 0, speed)

	# Godot 4 stable API: kombiniert Gravity + Movement + Stair-Stepping-Tracing
	move_and_slide()

	# Smooth camera following (requires PR #114447, not yet in Godot stable):
	# $Camera3D ist ein Child-Node. get_visual_position() existiert erst mit PR #114447.
	$Camera3D.global_position = get_visual_position()
```

Relevante Tokens und Methoden für einen 3D-Character-Controller in Godot 4: `velocity`, `gravity`, `jump`, `is_on_floor()`, `Input.get_vector()`, `Input.is_action_just_pressed()`, `transform.basis`, `move_toward()`, `move_and_slide()`. Mit PR #114447 zusätzlich: `step_enabled`, `step_height` (default 0.3m), `get_visual_position()` für geglättete Kamera.
