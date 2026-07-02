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

## AnimationTree + BlendSpace2D für Character Locomotion

`AnimationTree` mit `AnimationNodeBlendSpace2D` ist das Standard-Pattern für richtungsabhängige Character-Locomotion (idle, walk, run). Der Tree bekommt einen `tree_root` vom Typ `AnimationNodeBlendSpace2D`, der mehrere `AnimationNodeAnimation`-Points entlang eines 2D-Koordinatensystems anordnet und zwischen ihnen interpoliert. Die X/Y-Achse des BlendSpace wird typischerweise an einen `Vector2` aus dem Input-Mapping gebunden (`Input.get_vector("left", "right", "forward", "back")`).

Setup-Schritte im Editor:
1. AnimationPlayer mit idle/walk/run-Animationen unter dem Character-Rig (Skeleton3D-Child).
2. AnimationTree-Node hinzufügen, `anim_player` auf den AnimationPlayer setzen, `active = true`.
3. Im Tree-Editor: Root = `AnimationNodeBlendSpace2D`, `min_space = Vector2(-1, -1)`, `max_space = Vector2(1, 1)`.
4. Pro Animation einen `AnimationNodeAnimation` mit `animation = "idle"` (oder walk/run) hinzufügen und mit `add_blend_point(node, position)` bei `Vector2(0,0)` / `Vector2(0,0.5)` / `Vector2(0,1)` platzieren.
5. `blend_mode = BLEND_MODE_INTERPOLATED` für saubere Übergänge.

Zur Laufzeit im `_physics_process(delta)` den `Vector2` setzen:

```gdscript
extends CharacterBody3D

@onready var anim_tree: AnimationTree = $AnimationTree
@export var run_speed := 6.0
@export var walk_speed := 2.5

func _physics_process(delta: float) -> void:
    # Input zu Vector2 mappen (Godot 4 API)
    var input_dir := Input.get_vector("left", "right", "forward", "back")
    # Speed berechnen: walk bei langsamer Bewegung, run bei gedrückter Shift-Taste
    var speed := input_dir.length()
    if Input.is_action_pressed("run"):
        speed *= run_speed
    # Locomotion-BlendSpace2D-Parameter setzen (Pfad: "parameters/Locomotion/blend_position")
    anim_tree.set("parameters/Locomotion/blend_position", input_dir)
    # Optional: Time-Scale für schnellere Animation beim Rennen
    var playback := anim_tree.get("parameters/Locomotion/playback")
    if playback is AnimationNodeBlendSpace2D:
        anim_tree.set("parameters/Locomotion/time_scale", 1.0 + speed * 0.1)
```

Wichtige Tokens: `AnimationTree`, `AnimationNodeBlendSpace2D`, `AnimationNodeAnimation`, `add_blend_point`, `blend_mode`, `set_blend_parameter`, `Skeleton3D`, `AnimationPlayer`, `active`. Der blend_position-Vector2 wird mit `Input.get_vector()` synchronisiert; für ein vollständiges Character-Rig empfiehlt sich zusätzlich ein `AnimationNodeStateMachine` für idle↔walk↔run-Übergänge mit `travel(state_name)`.

## NavigationAgent3D für Enemy AI Chase

`NavigationAgent3D` ist die Standard-Wahl für pathfindende 3D-Enemies. Voraussetzung: ein `NavigationRegion3D` mit gebackener `NavigationMesh` im Level. Der Agent wird als Child des Enemy-Rigidbody- oder CharacterBody3D-Nodes angelegt; `path_desired_distance` und `target_desired_distance` steuern das Annäherungsverhalten, `avoidance_enabled` aktiviert lokale RVO-Kollisionsvermeidung.

Setup im Editor:
1. NavigationRegion3D-Node im Level-Root, `NavigationMesh` zuweisen, im Editor "Bake NavigationMesh" klicken.
2. NavigationAgent3D-Node als Child des Enemy-Nodes.
3. `path_desired_distance = 0.5` (wie nah am Wegpunkt, bevor nächster gilt), `target_desired_distance = 1.0` (wie nah am Ziel).
4. `avoidance_enabled = true` damit Enemies sich gegenseitig ausweichen.
5. `agent_radius` und `agent_height` an die Enemy-Größe anpassen (in NavigationMesh).

Im `_physics_process(delta)` läuft der Chase-Loop:

```gdscript
extends CharacterBody3D

@onready var agent: NavigationAgent3D = $NavigationAgent3D
@export var move_speed := 4.0
@export var player_path: NodePath  # im Inspector auf den Player zeigen lassen

func _physics_process(delta: float) -> void:
    # Ziel-Position jeden Frame aktualisieren (chase player)
    var player := get_node(player_path)
    if player is Node3D:
        agent.target_position = player.global_position
    # velocity_computed-Signal: nur mit avoidance nötig
    if agent.avoidance_enabled:
        # NavigationServer map erwartet dieses Pattern für avoidance
        var next_pos := agent.get_next_path_position()
        var direction := (next_pos - global_position).normalized()
        velocity = direction * move_speed
        # Statt move_and_slide() direkt: Signal abwarten
        agent.velocity_computed.connect(_on_velocity_computed, CONNECT_ONE_SHOT)
        agent.set_velocity(velocity)
    else:
        # Ohne avoidance: direkt move_and_slide
        var next_pos := agent.get_next_path_position()
        var direction := (next_pos - global_position).normalized()
        velocity = direction * move_speed
        move_and_slide()
    # Prüfen, ob das Ziel erreicht wurde
    if agent.is_navigation_finished():
        # Idle-State, attack, etc.
        pass

func _on_velocity_computed(safe_velocity: Vector3) -> void:
    velocity = safe_velocity
    move_and_slide()
```

Wichtige Tokens: `NavigationAgent3D`, `NavigationRegion3D`, `NavigationMesh`, `target_position`, `get_next_path_position`, `is_navigation_finished`, `velocity_computed`, `set_velocity`, `avoidance_enabled`, `path_desired_distance`, `target_desired_distance`, `agent_radius`, `agent_height`. Das `velocity_computed`-Signal ist Pflicht sobald `avoidance_enabled = true` — Godot 4.2+ löst sonst `set_velocity`-Aufrufe ohne Connector in einer Fehlermeldung aus. Für statische Enemies reicht der Pfad ohne avoidance; für dynamische Gruppen ist avoidance der Schlüssel.

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
