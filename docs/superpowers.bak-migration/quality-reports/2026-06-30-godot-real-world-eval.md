> **Archived Evaluation Report** | **Datum:** 2026-06-30 | **Evaluator:** orchestrator-knowledge
>
> Manuelle Bewertung der Real-World Source Comparison. Siehe `docs/superpowers/specs/2026-06-29-real-world-source-evaluation-design.md` für die Methodik.

# Quality Report: godot — 2026-06-30

## Summary
- **Domain:** godot
- **Date:** 2026-06-30
- **Questions evaluated:** 7
- **Composite Score:** 0.8594
- **Pass:** 7 (100.0%) | **Weak:** 0 (0.0%) | **Fail:** 0 (0.0%)

## Metric Averages
| Metric | Average |
|--------|---------|
| Source Recall | 1.0 |
| Page Metadata Accuracy | 0.0 |
| Top-K Relevance | 0.55 |
| Evidence Quality | 1.0 |

## Per-Question Results
| ID | Question | Score | Label | SR | PMA | TKR | EQ |
|----|----------|-------|-------|----|----|----|----|
| godot-001 | How do I rotate a Node3D around the Y ax... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-002 | How do I move a CharacterBody3D with gra... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-003 | What are the gotchas with CharacterBody3... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-004 | How do I set up a 3D camera that follows... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-005 | How do I fix GLB model import scale issu... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-006 | How do I use signals to communicate betw... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-007 | How do I create a 3D character controlle... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |

## Weak / Fail Details
- No weak or fail questions.

## Truncation Warnings
- godot-002: 1 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-004: 3 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-006: 3 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-007: 7 result(s) with text >= 5000 chars (heuristic, see LIM-003).

## Real-World Source Comparison

Online source coverage and Hub top-3 snippets for manual solution-alignment review.

### godot-001: How do I rotate a Node3D around the Y axis in GDScript?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/classes/class_node3d.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/3d/using_transforms.html | official-docs | yes | — |

**Hub Top Snippets:**

1. Method: Node3D.rotate_y Signature: rotate_y(angle\: float) Inherits: Node → Object  rotate_y ( angle\: float ) Rotates this node's basis around the Y axis by the given angle, in radians. This operatio
2. Method: Node3D.rotate_x Signature: rotate_x(angle\: float) Inherits: Node → Object  rotate_x ( angle\: float ) Rotates this node's basis around the X axis by the given angle, in radians. This operatio
3. Method: Node3D.rotate Signature: rotate(axis\: Vector3, angle\: float) Inherits: Node → Object  rotate ( axis\: Vector3, angle\: float ) Rotates this node's basis around the axis by the given angle, i

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet `godot-docs-reference-packed.md` das Node3D.rotate_y, rotate_x, rotate dokumentiert. Thematisch passend zu Online-Quelle (class_node3d.html).
- [x] Solution Alignment: PASS — Hub Top-3 Snippets zeigen `rotate_y(angle: float)`, `rotate_x`, `rotate(axis: Vector3, angle)` — genau die API-Methoden die auch die Online-Dokumentation als Lösung nennt.
- [x] Gap Detection: PASS — Keine Lücke. Hub deckt die Rotation-API vollständig ab.

### godot-002: How do I move a CharacterBody3D with gravity in Godot 4?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body… | official-docs | yes | — |
| https://github.com/godotengine/godot/issues/112656 | github-issue | no | 2025-11-12 |

**Hub Top Snippets:**

1. Class: CharacterBody3D extends PhysicsBody3D → CollisionObject3D → Node3D → Node → Object  :github_url: hide CharacterBody3D =============== A 3D physics body specialized for characters moved by scrip
2. # Godot Gotchas — Was nicht funktioniert hat  > Einträge hier werden vom Agent automatisch angelegt: "Füge das zu den Gotchas hinzu." > > Template: Problem → Ursache → Workaround → Datum → Status  ##
3. is multiplied by these values, so you can make particles move in the opposite direction by setting a negative velocity.  Accelerations -------------  Gravity ~~~~~~~  The next few property groups work

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet `godot-docs-reference-packed.md` (CharacterBody3D Klasse) und `gotchas.md`. Thematisch passend.
- [x] Solution Alignment: WEAK — Hub Snippet 1 zeigt CharacterBody3D-Klassendefinition, Snippet 2 zeigt Gotchas-Header (kein inhaltlicher Code), Snippet 3 zeigt Particle-API (Gravity-Properties aber nicht CharacterBody3D.move_and_slide). Die konkrete Lösung (`velocity += get_gravity() * delta; move_and_slide()`) ist nicht in Top-3 sichtbar.
- [x] Gap Detection: GAP — GitHub Issue #112656 (get_gravity ignoriert Area3D-Overrides) ist ein bestätigter Bug der im Hub NICHT dokumentiert ist. Die Gotchas.md erwähnt CharacterBody3D aber nicht diesen spezifischen Bug. Empfehlung: Bug als personal note erfassen oder als Known Issue dokumentieren.

### godot-003: What are the gotchas with CharacterBody3D and Jolt Physics in Godot 4.6?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://github.com/godotengine/godot/issues/117857 | github-issue | yes | 2026-03-26 |
| https://github.com/godotengine/godot/issues/112315 | github-issue | yes | 2025-11-02 |
| https://github.com/godotengine/godot/issues/113058 | github-issue | no | 2025-11-22 |

**Hub Top Snippets:**

1. # Godot Gotchas — Was nicht funktioniert hat  > Einträge hier werden vom Agent automatisch angelegt: "Füge das zu den Gotchas hinzu." > > Template: Problem → Ursache → Workaround → Datum → Status  ##
2. Class: CharacterBody3D extends PhysicsBody3D → CollisionObject3D → Node3D → Node → Object  :github_url: hide CharacterBody3D =============== A 3D physics body specialized for characters moved by scrip
3. Constant: PhysicsServer3D.SHAPE_CUSTOM Signature: SHAPE_CUSTOM = 10 Inherits: Object  ShapeType SHAPE_CUSTOM = 10 Constant used internally for a custom shape. Any attempt to create this kind of shape

**Manual Evaluation:**

- [x] Source Coverage: WEAK — Hub findet `gotchas.md` und `godot-docs-reference-packed.md` (CharacterBody3D), aber Snippet 3 (PhysicsServer3D.SHAPE_CUSTOM) ist thematisch nur lose verwandt. Die Jolt-spezifischen Gotchas aus den 3 GitHub Issues sind im Hub nicht dokumentiert.
- [x] Solution Alignment: WEAK — Hub Snippets zeigen CharacterBody3D-Klasse und Gotchas-Header, aber nicht die spezifischen Jolt-Workarounds (move_and_collide from _process, apply_floor_snap catapulting, Reparenting Area3D trigger) die in den GitHub Issues stehen.
- [x] Gap Detection: GAP — 3 GitHub Issues (#117857, #112315, #113058) beschreiben Jolt-spezifische Bugs mit Workarounds die im Hub fehlen. Empfehlung: Diese Bugs als personal/gotchas.md Einträge kuratieren (z.B. "Jolt: move_and_collide from _process() liefert null collision → _physics_process() verwenden").

### godot-004: How do I set up a 3D camera that follows a player in Godot?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/classes/class_camera3d.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/3d/using_transforms.html | official-docs | yes | — |

**Hub Top Snippets:**

1. Class: CameraFeed extends RefCounted → Object  :github_url: hide CameraFeed ========== A camera feed gives you access to a single physical camera attached to your device. Description ----------- A cam
2. tests_menu.gd     tests.gd   platformer/     coin/       coin.gd     enemy/       enemy.gd     player/       bullet/         bullet.gd       follow_camera.gd       player.gd     stage/       stage.gd
3. Method: XRInterface.initialize Inherits: RefCounted → Object  bool initialize ( ) Call this to initialize this interface. The first interface that is initialized is identified as the primary interface

**Manual Evaluation:**

- [x] Source Coverage: WEAK — Hub findet CameraFeed (nicht Camera3D!), follow_camera.gd aus demos, und XRInterface. Snippet 1 (CameraFeed) ist thematisch verwandt aber nicht die primäre Camera3D-Klasse. Snippet 2 (follow_camera.gd) ist relevant. Snippet 3 (XRInterface) ist nicht relevant.
- [x] Solution Alignment: WEAK — Online-Quellen dokumentieren Camera3D-Klasse und Transforms-Tutorial (FPS-Kamera). Hub findet CameraFeed statt Camera3D und einen Demo-Code (follow_camera.gd). Die Camera3D-API ist wahrscheinlich im Index aber nicht in Top-3.
- [x] Gap Detection: PASS — Keine kritische Lücke (Camera3D ist im Index, nur Ranking-Schwäche).

### godot-005: How do I fix GLB model import scale issues from Meshy in Godot?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://github.com/godotengine/godot/issues/111653 | github-issue | no | 2025-10-14 |
| https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d… | official-docs | yes | — |
| https://github.com/godotengine/godot/issues/97022 | github-issue | yes | 2024-09-14 |

**Hub Top Snippets:**

1. # Godot Gotchas — Was nicht funktioniert hat  > Einträge hier werden vom Agent automatisch angelegt: "Füge das zu den Gotchas hinzu." > > Template: Problem → Ursache → Workaround → Datum → Status  ##
2. # Godot Best Practices — Patterns die funktioniert haben  > Bewährte Patterns aus dem `nak-hopper-game`-Projekt.  ## GDScript  ### class_name + preload für cross-file Typen - **Pattern:** `const _Foo
3. Method: GLTFDocumentExtension._import_object_model_property Signature: _import_object_model_property(state\: GLTFState, split_json_pointer\: PackedStringArray, partial_paths\: Array\[NodePath\]) Inher

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet `gotchas.md` (Top-1!) und `godot-docs-reference-packed.md` (GLTFDocumentExtension). Thematisch passend zur Frage und zu den Online-Quellen.
- [x] Solution Alignment: PASS — Hub Top-1 ist gotchas.md was genau den Meshy/GLB-Import-Scale-Gotcha behandelt. Online-Quelle (model_export_considerations.html) empfiehlt "1 unit = 1 meter, Apply Transforms" — das steht vermutlich in den Gotchas.
- [x] Gap Detection: GAP — GitHub Issues #111653 (Mesh origin shifts beim Skalieren, open) und #97022 (GLTF matrix vs TRS, fixed in 4.4) sind im Hub nicht dokumentiert. Empfehlung: #111653 als gotcha erfassen ("Mesh origin verschiebt sich beim Skalieren importierter GLB/OBJ — Disable LODs als Workaround-Pfad").

### godot-006: How do I use signals to communicate between nodes in GDScript?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html | official-docs | yes | — |

**Hub Top Snippets:**

1. Method: Object.connect Signature: connect(signal\: StringName, callable\: Callable, flags\: int = 0)  Error connect ( signal\: StringName, callable\: Callable, flags\: int = 0 ) Connects a signal by n
2. Class: Signal  :github_url: hide Signal ====== A built-in type representing a signal of an Object. Description ----------- Signal is a built-in Variant type that represents a signal of an Object insta
3. Method: Node.rpc Signature: rpc(method\: StringName, ...) Inherits: Object  Error rpc ( method\: StringName, ... ) Sends a remote procedure call request for the given method to peers on the network (a

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet `godot-docs-reference-packed.md` mit Object.connect, Signal-Klasse, Node.rpc. Thematisch passend.
- [x] Solution Alignment: PASS — Hub Top-1 zeigt `Object.connect(signal: StringName, callable: Callable, flags: int = 0)` — die Kern-API für Signal-Verbindungen. Online-Tutorial zeigt `timer.timeout.connect(_on_timer_timeout)` was die gleiche API ist.
- [x] Gap Detection: PASS — Keine Lücke. Hub deckt Signal-API vollständig ab.

### godot-007: How do I create a 3D character controller with movement, jumping, and gravity?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body… | official-docs | yes | — |
| https://github.com/godotengine/godot/pull/114447 | github-pr | yes | 2025-12-30 |

**Hub Top Snippets:**

1. te the vector based on the mob's Y rotation to move in the direction it's looking. 	velocity = velocity.rotated(Vector3.UP, rotation.y)  	$AnimationPlayer.speed_scale = random_speed / min_speed   func
2. _basis.x, -cam_basis.get_euler().x) 	dir = cam_basis * dir  	# Limit the input to a length of 1. `length_squared()` is faster to check 	# than `length()`. 	if dir.length_squared() > 1: 		dir /= dir.le
3. is multiplied by these values, so you can make particles move in the opposite direction by setting a negative velocity.  Accelerations -------------  Gravity ~~~~~~~  The next few property groups work

**Manual Evaluation:**

- [x] Source Coverage: PASS — Hub findet Demos (velocity.rotated, cam_basis) und Reference (Gravity properties). Thematisch passend.
- [x] Solution Alignment: WEAK — Hub Snippets zeigen Demo-Code (mob velocity.rotated, cam_basis movement) und Gravity-Properties, aber nicht die vollständige CharacterBody3D-Controller-Lösung (`get_gravity()`, `is_on_floor()`, `move_and_slide()`). Die Online-Tutorial-Lösung ist spezifischer.
- [x] Gap Detection: GAP — GitHub PR #114447 (native stair stepping, step_height 0.3m) ist ein neues Feature das im Hub nicht dokumentiert ist. Empfehlung: Als personal note erfassen falls relevant für Noahs Projekte.

## Gaps & Recommendations
- No weak/fail questions. Domain coverage looks healthy.

## Summary of Findings

### Verteilung nach Ebene

| Ebene | PASS | WEAK | GAP | Total |
|-------|------|------|-----|-------|
| Source Coverage | 4 | 3 | 0 | 7 |
| Solution Alignment | 3 | 4 | 0 | 7 |
| Gap Detection | 3 | 0 | 4 | 7 |
| **Total** | **10** | **7** | **4** | **21** |

### Top-Gaps und Empfehlungen

1. **godot-002 — get_gravity() ignoriert Area3D-Overrides** (GitHub Issue #112656): Bestätigter Bug, in Gotchas.md nicht dokumentiert. → Empfehlung: Als `domains/godot/personal/gotchas.md` Eintrag kuratieren ("CharacterBody3D.get_gravity() ignoriert Area3D gravity overrides — Workaround: eigene Gravity-Berechnung mit Area3D-Liste").

2. **godot-003 — Jolt-spezifische Gotchas** (3 GitHub Issues #117857, #112315, #113058): Bugs mit Workarounds die im Hub fehlen. → Empfehlung: Diese Bugs als gotchas.md Einträge kuratieren (z.B. "Jolt: move_and_collide from _process() liefert null collision → _physics_process() verwenden", "Jolt: apply_floor_snap catapulting nach Reparenting").

3. **godot-005 — Meshy/GLB Import-Scale Bug** (GitHub Issue #111653, offen): Mesh origin shift beim Skalieren. → Empfehlung: #111653 als gotcha erfassen ("Mesh origin verschiebt sich beim Skalieren importierter GLB/OBJ — Disable LODs als Workaround-Pfad"). #97022 (fixed in 4.4) muss nicht erfasst werden.

4. **godot-007 — Native Stair Stepping** (GitHub PR #114447): Neues step_height 0.3m Feature. → Empfehlung: Falls relevant für Noahs Projekte als personal note erfassen.

### Beobachtungen

- **Source Recall (SR)** ist 1.0 für alle 7 Fragen — der Hub findet die richtigen Quellen-Files.
- **Page Metadata Accuracy (PMA)** ist N/A — Godot-Sources sind keine PDFs (LIM-004 ist PDF-only).
- **Top-K Relevance (TKR)** ist konstant 0.55 — die Top-3 Snippets sind oft thematisch passend aber nicht immer die spezifischste Lösung.
- **Truncation Warnings** bei 4/7 Fragen (godot-002, -004, -006, -007) — LIM-003 bestätigt.
- **Composite Score 0.8594** trotzdem "pass" für alle 7 Fragen, weil die automatischen Metriken gut aussehen. Die manuelle Evaluation deckt aber 4 Gaps und 7 WEAKs auf, die Noah für die Inhalts-Kuratierung nutzen sollte.