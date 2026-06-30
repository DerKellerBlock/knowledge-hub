# Quality Report: godot — 2026-06-30

## Summary
- **Domain:** godot
- **Date:** 2026-06-30
- **Questions evaluated:** 7
- **Composite Score:** 0.7761
- **Pass:** 6 (85.7%) | **Weak:** 1 (14.3%) | **Fail:** 0 (0.0%)

## Metric Averages
| Metric | Average |
|--------|---------|
| Source Recall | 0.8095 |
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
| godot-005 | How do I fix GLB model import scale issu... | 0.4219 | weak | 0.0 | N/A | 0.55 | 1.0 |
| godot-006 | How do I use signals to communicate betw... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-007 | How do I create a 3D character controlle... | 0.7136 | pass | 0.6667 | N/A | 0.55 | 1.0 |

## Weak / Fail Details
### godot-005 (weak, 0.4219)
- **Question:** How do I fix GLB model import scale issues from Meshy in Godot?
- **Found sources:** ['best-practices.md', 'godot-docs-reference-packed.md']
- **Recommendation:** Review index coverage for this question.

## Truncation Warnings
- godot-002: 1 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-004: 3 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-006: 3 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-007: 8 result(s) with text >= 5000 chars (heuristic, see LIM-003).

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

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-002: How do I move a CharacterBody3D with gravity in Godot 4?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body… | official-docs | yes | — |
| https://github.com/godotengine/godot/issues/112656 | github-issue | no | 2025-11-12 |

**Hub Top Snippets:**

1. # Godot Gotchas — Was nicht funktioniert hat  > Einträge hier werden vom Agent automatisch angelegt: "Füge das zu den Gotchas hinzu." > > Template: Problem → Ursache → Workaround → Datum → Status  ##
2. Class: CharacterBody3D extends PhysicsBody3D → CollisionObject3D → Node3D → Node → Object  :github_url: hide CharacterBody3D =============== A 3D physics body specialized for characters moved by scrip
3. is multiplied by these values, so you can make particles move in the opposite direction by setting a negative velocity.  Accelerations -------------  Gravity ~~~~~~~  The next few property groups work

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

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

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

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

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-005: How do I fix GLB model import scale issues from Meshy in Godot?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://github.com/godotengine/godot/issues/111653 | github-issue | no | 2025-10-14 |
| https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d… | official-docs | yes | — |
| https://github.com/godotengine/godot/issues/97022 | github-issue | yes | 2024-09-14 |

**Hub Top Snippets:**

1. # Godot Best Practices — Patterns die funktioniert haben  > Bewährte Patterns aus dem `nak-hopper-game`-Projekt.  ## GDScript  ### class_name + preload für cross-file Typen - **Pattern:** `const _Foo
2. Method: GLTFDocumentExtension._import_object_model_property Signature: _import_object_model_property(state\: GLTFState, split_json_pointer\: PackedStringArray, partial_paths\: Array\[NodePath\]) Inher
3. Method: GLTFDocument.import_object_model_property Signature: import_object_model_property(state\: GLTFState, json_pointer\: String) Inherits: Resource → RefCounted → Object  GLTFObjectModelProperty im

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

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

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

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

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

## Gaps & Recommendations
- 1 question(s) scored weak/fail. Review index coverage and source availability.
