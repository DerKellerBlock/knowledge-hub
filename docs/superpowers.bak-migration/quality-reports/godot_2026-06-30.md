# Quality Report: godot — 2026-06-30

## Summary
- **Domain:** godot
- **Date:** 2026-06-30
- **Questions evaluated:** 9
- **Composite Score:** 0.8594
- **Pass:** 9 (100.0%) | **Weak:** 0 (0.0%) | **Fail:** 0 (0.0%)

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
| godot-008 | Why is my 3D model not visible in Godot?... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-008-de | Warum sehe ich mein 3D-Modell nicht in G... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |

## Weak / Fail Details
- No weak or fail questions.

## Truncation Warnings
- godot-002: 1 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-004: 7 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-005: 5 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-006: 2 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-007: 4 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-008: 6 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-008-de: 2 result(s) with text >= 5000 chars (heuristic, see LIM-003).

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

1. ## CharacterBody3D Stair Stepping - CharacterBody3D hat native stair stepping (PR #114447, 2025-12-30, open): Properties `step_enabled`, `step_height` (default 0.3m), `step_smooth_enabled`, `step_smoo
2. Method: CharacterBody3D.move_and_slide Inherits: PhysicsBody3D → CollisionObject3D → Node3D → Node → Object  bool move_and_slide ( ) Moves the body based on velocity. If the body collides with another
3. ## Jolt Physics + CharacterBody3D - **Problem:** CharacterBody3D fällt durch den Boden bei Jolt Physics in Godot 4.6 - **Ursache:** `move_and_slide()` ruft `PhysicsServer3D.body_test_motion()` auf, Jo

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

1. ## Jolt Physics + CharacterBody3D - **Problem:** CharacterBody3D fällt durch den Boden bei Jolt Physics in Godot 4.6 - **Ursache:** `move_and_slide()` ruft `PhysicsServer3D.body_test_motion()` auf, Jo
2. ## Jolt: Reparenting CharacterBody3D triggert ferne Area3D - **Problem:** Reparenting CharacterBody3D mit `KeepGlobalTransform=true` triggert ferne Area3D-Nodes am World Origin - **Ursache:** Jolt Phy
3. ## CharacterBody3D Stair Stepping - CharacterBody3D hat native stair stepping (PR #114447, 2025-12-30, open): Properties `step_enabled`, `step_height` (default 0.3m), `step_smooth_enabled`, `step_smoo

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

1. e placed at or near the collision point:  .. image:: img/spring_arm_camera_collision.webp  Setting up the spring arm and camera ------------------------------------  Let's add a spring arm camera setu
2. ches or artifacts) in delicate areas such as rendering or physics. Make sure your artists always work in the right scale!  The Y coordinate is used for "up". As for the horizontal X/Z axes, Godot uses
3. ocity.y > 0 else 0   func start(pos): 	position = pos 	rotation = 0 	show() 	$CollisionShape2D.disabled = false   func _on_body_entered(_body): 	hide() # Player disappears after being hit. 	hit.emit()

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

1. ## GLB-Import — Mesh Origin Bug - **Problem:** Mesh origin point verschiebt sich vom World Origin weg beim Skalieren importierter GLB/OBJ-Geometrie (nicht bei Godot-nativen QuadMesh) - **Ursache:** Bu
2. ## GLB-Import Scale mit Meshy - **Problem:** GLB-Modell unsichtbar weil scale zu klein - **Ursache:** Meshy liefert Modelle mit unterschiedlichen nativen Größen - **Workaround:** `auto_size: true` + `
3. t to **Material Override** (or **Material** for individual CSG nodes). Choose **New StandardMaterial3D**. Click the newly created material's icon to edit it. Unfold the **Albedo** section and load a t

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

1. uashed)   func _on_player_hit(): 	$MobTimer.stop() 	$UserInterface/Retry.show() ```  ## File: 3d/squash_the_creeps/Mob.gd ``` extends CharacterBody3D  # Emitted when the player jumped on the mob. sign
2. ## CharacterBody3D Stair Stepping - CharacterBody3D hat native stair stepping (PR #114447, 2025-12-30, open): Properties `step_enabled`, `step_height` (default 0.3m), `step_smooth_enabled`, `step_smoo
3. hen reassigned. 		velocity.x = move_toward(velocity.x, 0, STOP_FORCE * delta) 	else: 		velocity.x += walk * delta 	# Clamp to the maximum horizontal movement speed. 	velocity.x = clamp(velocity.x, -WA

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-008: Why is my 3D model not visible in Godot? I've added a MeshInstance3D but nothing shows up in the viewport.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/classes/class_geometryinstance3d.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/classes/class_camera3d.html | official-docs | yes | — |

**Hub Top Snippets:**

1. nsparency_sorting>`   during LOD transitions.  The downside of dithering is that a "noisy" pattern is visible during LOD fade transitions. This may not be as noticeable at higher viewport resolutions
2. Godot 3.x workflow    (used to reference a non existing doc_importing_3d_meshes importer).  It is possible to import 3D models in Godot created in external tools. Depending on the format, you can impo
3. of a specific texture that may be too large to render, you can set the **Process > Size Limit** import option to a value greater than ``0``. This will reduce the texture's dimensions on import (preser

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-008-de: Warum sehe ich mein 3D-Modell nicht in Godot? Ich habe ein MeshInstance3D hinzugefügt, aber im Viewport erscheint nichts.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/classes/class_geometryinstance3d.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/classes/class_camera3d.html | official-docs | yes | — |

**Hub Top Snippets:**

1. ## Warum sehe ich mein 3D-Modell nicht? - **`visible` Flag**: `MeshInstance3D.visible` (geerbt von `Node3D`) prüfen — und die aller Parents (`get_parent().visible` etc.). Eine unsichtbare Parent-Kette
2. Godot 3.x workflow    (used to reference a non existing doc_importing_3d_meshes importer).  It is possible to import 3D models in Godot created in external tools. Depending on the format, you can impo
3. ches or artifacts) in delicate areas such as rendering or physics. Make sure your artists always work in the right scale!  The Y coordinate is used for "up". As for the horizontal X/Z axes, Godot uses

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

## Gaps & Recommendations
- No weak/fail questions. Domain coverage looks healthy.
