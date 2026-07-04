# Quality Report: godot_eval_a — 2026-07-04

## Summary
- **Domain:** godot_eval_a
- **Date:** 2026-07-04
- **Questions evaluated:** 21
- **Composite Score:** 0.8281
- **Pass:** 18 (85.7%) | **Weak:** 3 (14.3%) | **Fail:** 0 (0.0%)

## Metric Averages
| Metric | Average |
|--------|---------|
| Source Recall | 0.9286 |
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
| godot-008 | Why is my 3D model not visible in Godot?... | 0.6406 | weak | 0.5 | N/A | 0.55 | 1.0 |
| godot-008-de | Warum sehe ich mein 3D-Modell nicht in G... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-009 | How do I set up an AnimationTree with a ... | 0.6406 | weak | 0.5 | N/A | 0.55 | 1.0 |
| godot-010 | How do I create a spatial shader in Godo... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-011 | How do I create a responsive UI in Godot... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-012 | How do I make an enemy AI chase the play... | 0.6406 | weak | 0.5 | N/A | 0.55 | 1.0 |
| godot-013 | How do I set up a basic authoritative mu... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-014 | How do I detect when the player presses ... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-015 | How do I play a looping background music... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-016 | How do I save and load player progress l... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-017 | How do I optimize a large 3D open-world ... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-018 | How do I create a 2D platformer level wi... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-019 | How do I create a custom Resource type i... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |
| godot-020 | How do I use the Godot Profiler to ident... | 0.8594 | pass | 1.0 | N/A | 0.55 | 1.0 |

## Weak / Fail Details
### godot-008 (weak, 0.6406)
- **Question:** Why is my 3D model not visible in Godot? I've added a MeshInstance3D but nothing shows up in the viewport.
- **Found sources:** ['godot-docs-3d-packed.md', 'godot-demos-packed.md', 'faq.md']
- **Recommendation:** Review index coverage for this question.

### godot-009 (weak, 0.6406)
- **Question:** How do I set up an AnimationTree with a BlendSpace2D for character locomotion in Godot 4? I want to blend between idle, walk, and run animations based on a Vector2 input direction.
- **Found sources:** ['tips.md', 'godot-docs-reference-packed.md']
- **Recommendation:** Review index coverage for this question.

### godot-012 (weak, 0.6406)
- **Question:** How do I make an enemy AI chase the player using NavigationAgent3D in Godot 4? I need the enemy to pathfind around obstacles and update its target position each frame.
- **Found sources:** ['tips.md', 'godot-docs-reference-packed.md']
- **Recommendation:** Review index coverage for this question.

## Truncation Warnings
- godot-001: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-002: 7 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-003: 6 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-004: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-005: 7 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-006: 9 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-007: 9 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-008: 9 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-008-de: 5 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-009: 9 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-010: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-011: 9 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-012: 9 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-013: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-014: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-015: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-016: 9 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-017: 9 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-018: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-019: 9 result(s) with text >= 5000 chars (heuristic, see LIM-003).
- godot-020: 10 result(s) with text >= 5000 chars (heuristic, see LIM-003).

## Real-World Source Comparison

Online source coverage and Hub top-3 snippets for manual solution-alignment review.

### godot-001: How do I rotate a Node3D around the Y axis in GDScript?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/classes/class_node3d.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/3d/using_transforms.html | official-docs | yes | — |

**Hub Top Snippets:**

1. s node's :ref:`basis<class_Node3D_property_basis>` around the ``axis`` by the given ``angle``, in radians. This operation is calculated in parent space (relative to the parent) and preserves the :ref:
2. ith the *origin*, a *transform* efficiently represents a unique translation, rotation, and scale in space.  .. image:: img/transforms_camera.png   One way to visualize a transform is to look at an obj
3. Location node.             var mobSpawnLocation = GetNode<PathFollow3D>("SpawnPath/SpawnLocation");             // And give it a random offset.             mobSpawnLocation.ProgressRatio = GD.Randf();

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
2. ## Jolt Physics + CharacterBody3D - **Problem:** CharacterBody3D fällt durch den Boden bei Jolt Physics in Godot 4.6 - **Ursache:** `move_and_slide()` ruft `PhysicsServer3D.body_test_motion()` auf, Jo
3. s function will be called from the Main scene.     func initialize(start_position, player_position):         # We position the mob by placing it at start_position         # and rotate it towards playe

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
2. ed some game assets you'll need to download so we can jump straight to the code.  You can download them by clicking the link below.  `dodge_the_creeps_2d_assets.zip <https://github.com/godotengine/god
3. box.  Go to *Project -> Project Settings*.  |image1|  If you still have *Input Map* open, switch to the *General* tab.  In the left menu, navigate down to *Display -> Window*. On the right, set the *V

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

1. als`, we'll build upon the relationship between scripts and nodes by having our nodes trigger code in scripts. ``````  ## File: getting_started/step_by_step/signals.rst ``````rst .. Intention: give th
2. displays information about the connection. This feature is only available when connecting nodes in the editor.  .. image:: img/signals_14_signals_connection_info.webp  Let's replace the line with the
3. ithout directly referencing one another. This keeps the code flexible and easier to manage. You can check whether an :ref:`Object<class_Object>` has a given signal name using :ref:`Object.has_signal()

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
2. d :ref:`Physics <toc-learn-features-physics>` sections will teach you more about 3D game creation in the    engine. 3. :ref:`Inputs <toc-learn-features-inputs>` is another important one for any game p
3. _back"))             {                 direction.Z += 1.0f;             }             if (Input.IsActionPressed("move_forward"))             {                 direction.Z -= 1.0f;             }

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

1. Godot 3.x workflow    (used to reference a non existing doc_importing_3d_meshes importer).  It is possible to import 3D models in Godot created in external tools. Depending on the format, you can impo
2. of a specific texture that may be too large to render, you can set the **Process > Size Limit** import option to a value greater than ``0``. This will reduce the texture's dimensions on import (preser
3. ## Warum sehe ich mein 3D-Modell nicht? - **`visible` Flag**: `MeshInstance3D.visible` (geerbt von `Node3D`) prüfen — und die aller Parents (`get_parent().visible` etc.). Eine unsichtbare Parent-Kette

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
3. ## 3D Open-World Performance: LOD + Occlusion + Visibility Ranges - **Pattern:** Drei-Stufen-Strategie für mobile Open-World-Szenen: (a) Mesh-LOD per GLB-Import-Thresholds reduziert Vertex-Count bei D

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-009: How do I set up an AnimationTree with a BlendSpace2D for character locomotion in Godot 4? I want to blend between idle, walk, and run animations based on a Vector2 input direction.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/animation/index.html | official-docs | yes | — |

**Hub Top Snippets:**

1. ## AnimationTree + BlendSpace2D für Character Locomotion  `AnimationTree` mit `AnimationNodeBlendSpace2D` ist das Standard-Pattern für richtungsabhängige Character-Locomotion (idle, walk, run). Der Tr
2. BlendSpace1D_method_get_blend_point_count>`  Returns the number of points on the blend axis.  .. rst-class:: classref-item-separator  ----  .. _class_AnimationNodeBlendSpace1D_method_get_blend_point_n
3. several 3D engines, as you can then inherit from and extend those scenes. You may create a Magician that extends your Character. Modify the Character in the editor and the Magician will update as wel

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-010: How do I create a spatial shader in Godot 4 that adds a glowing outline effect around a 3D object using the Fresnel node?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/in… | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/ind… | official-docs | yes | — |

**Hub Top Snippets:**

1. using Grow.  Note that in Godot 4.5 onwards, stencil buffer-based outlines are available using the **Outline** :ref:`stencil mode <doc_standard_material_3d_stencil>`. This can be used as an alternativ
2. ember to use a transparent albedo texture (or reduce the albedo color's alpha channel) to make refraction visible, as refraction relies on transparency to have a visible effect.  Refraction also takes
3. several 3D engines, as you can then inherit from and extend those scenes. You may create a Magician that extends your Character. Modify the Character in the editor and the Magician will update as wel

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-011: How do I create a responsive UI in Godot 4 that automatically scales and repositions elements for different screen sizes and aspect ratios using containers and anchors?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/ui/gui_skinning.html | official-docs | yes | — |

**Hub Top Snippets:**

1. ## Responsive UI mit Container + Anchor + Size Flags - **Pattern:** Für responsive UI über verschiedene Screen-Größen und Aspect-Ratios: Container-Hierarchie statt festen Positionen, Size-Flags (`SIZE
2. .rst ``````rst :github_url: hide  .. DO NOT EDIT THIS FILE!!! .. Generated automatically from Godot engine sources. .. Generator: https://github.com/godotengine/godot/tree/master/doc/tools/make_rst.py
3. rboxing") or the sides ("pillarboxing").  \ ``"keep_width"``: Keep aspect ratio when stretching the screen. If the screen is wider than the base size, black bars are added at the left and right (pilla

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-012: How do I make an enemy AI chase the player using NavigationAgent3D in Godot 4? I need the enemy to pathfind around obstacles and update its target position each frame.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_… | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_… | official-docs | yes | — |

**Hub Top Snippets:**

1. ## NavigationAgent3D für Enemy AI Chase  `NavigationAgent3D` ist die Standard-Wahl für pathfindende 3D-Enemies. Voraussetzung: ein `NavigationRegion3D` mit gebackener `NavigationMesh` im Level. Der Ag
2. ed some game assets you'll need to download so we can jump straight to the code.  You can download them by clicking the link below.  `dodge_the_creeps_2d_assets.zip <https://github.com/godotengine/god
3. |  Click and drag on the curve, pulling it towards the left. This will make it ease-out, that is to say, transition fast initially and slow down as the time cursor reaches the next keyframe.  |image17

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-013: How do I set up a basic authoritative multiplayer game in Godot 4 using ENet? I need to handle peer connections, spawn players, and synchronize positions with RPC calls where the server has authority.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multip… | official-docs | yes | — |
| https://github.com/godotengine/godot/issues/57869 | github-issue | yes | — |

**Hub Top Snippets:**

1. ource: https://github.com/godotengine/godot/tree/master/modules/multiplayer/doc_classes/MultiplayerSpawner.xml.  .. _class_MultiplayerSpawner:  MultiplayerSpawner ==================  **Inherits:** :re
2. method is intended to be used in editor plugins and tools, but it also works in release builds. See also :ref:`is_editable_instance()<class_Node_method_is_editable_instance>`.  .. rst-class:: classre
3. d :ref:`Physics <toc-learn-features-physics>` sections will teach you more about 3D game creation in the    engine. 3. :ref:`Inputs <toc-learn-features-inputs>` is another important one for any game p

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-014: How do I detect when the player presses the spacebar in GDScript using the Input system? I want to trigger a jump action.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html | official-docs | yes | — |

**Hub Top Snippets:**

1. map.webp  Bind also the :kbd:`A` key, onto the action ``move_left``.  .. image:: img/02.player_input/keyboard_keys.webp  Let's now add support for a gamepad's left joystick. Click the "**+**" button a
2. ections.  In case the player presses, say, both W and D simultaneously, the vector will have a length of about ``1.4``. But if they press a single key, it will have a length of ``1``. We want the vect
3. need to assign a key to this action. Click the "+" icon on the right, to open the event manager window.  .. image:: img/input-mapping-add-key.webp  The "Listening for Input..." field should automatica

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-015: How do I play a looping background music track and a one-shot sound effect in Godot 4 using AudioStreamPlayer?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html | official-docs | yes | — |

**Hub Top Snippets:**

1. operty: ``Color``. Choose a color you like and select "Layout" -> "Anchors Preset" -> "Full Rect" either in the toolbar at the top of the viewport or in the inspector so that it covers the screen.  Yo
2. second 0 of the audio track. Compensate 			# with an offset setting. 			+ first_beat_offset_ms / 1000.0 			# Playback does not start immediately, but only when the next audio 			# chunk is processed (
3. f:`stream<class_AudioStreamPlayer_property_stream>` needs to be set to a valid :ref:`AudioStream<class_AudioStream>` resource. Playing more than one sound at the same time is also supported, see :ref:

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-016: How do I save and load player progress like level, score, and settings using ConfigFile in Godot 4? Where should I store the save file?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html | official-docs | yes | — |

**Hub Top Snippets:**

1. ## Wie speichert man Daten? - **`ConfigFile`** für INI-ähnliche `.cfg`-Dateien (Sections, Keys, Werte). Gut für Settings, einfache Save-Games. - **`FileAccess`** für rohen I/O (`store_string`, `store_
2. |  Click and drag on the curve, pulling it towards the left. This will make it ease-out, that is to say, transition fast initially and slow down as the time cursor reaches the next keyframe.  |image17
3. operty: ``Color``. Choose a color you like and select "Layout" -> "Anchors Preset" -> "Full Rect" either in the toolbar at the top of the viewport or in the inspector so that it covers the screen.  Yo

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-017: How do I optimize a large 3D open-world scene in Godot 4 for mobile performance? I need to reduce draw calls and manage which objects are rendered based on distance.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/3d/mesh_lod.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/3d/occlusion_culling.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/3d/visibility_ranges.html | official-docs | yes | — |

**Hub Top Snippets:**

1. of a specific texture that may be too large to render, you can set the **Process > Size Limit** import option to a value greater than ``0``. This will reduce the texture's dimensions on import (preser
2. ey render in Blender. This means that   materials in Godot will have their cull mode set to **Disabled**. This can   decrease performance since backfaces will be rendered, even when they are   being c
3. ## 3D Open-World Performance: LOD + Occlusion + Visibility Ranges - **Pattern:** Drei-Stufen-Strategie für mobile Open-World-Szenen: (a) Mesh-LOD per GLB-Import-Thresholds reduziert Vertex-Count bei D

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-018: How do I create a 2D platformer level with tile-based collision in Godot 4 using TileMapLayer and TileSet? I want different tiles for ground, walls, and platforms.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html | official-docs | yes | — |

**Hub Top Snippets:**

1. ary`) that can be placed on a grid, as if you were building a level with an unlimited amount of Lego blocks.  Collisions and navigation can also be added to the meshes, just like you would do with the
2. abbr:`static (This method doesn't need an instance to be called, so it can be called directly using the class name.)` .. |operator| replace:: :abbr:`operator (This method describes a valid operator to
3. several 3D engines, as you can then inherit from and extend those scenes. You may create a Magician that extends your Character. Modify the Character in the editor and the Magician will update as wel

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-019: How do I create a custom Resource type in GDScript to store item data like name, icon texture, and stats? I want to create individual item instances in the editor.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_… | official-docs | yes | — |

**Hub Top Snippets:**

1. ## Custom Resource als Item-Daten-Container - **Pattern:** Eigene Resource-Subklasse mit `class_name` und `@export`-Properties für Editor-Editierbarkeit. Im FileSystem "Create New Resource" → ItemData
2. s>`\] = 6\ ) :ref:`🔗<class_@GDScript_annotation_@export_custom>`  Allows you to set a custom hint, hint string, and usage flags for the exported property. Note that there's no validation done in GDScr
3. deblock for convenience.  .. image:: img/scripting_first_script_rotating_godot.gif  .. seealso:: To learn more about GDScript, its keywords, and its syntax, head to              the :ref:`doc_gdscript

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### godot-020: How do I use the Godot Profiler to identify which scripts or functions are causing frame rate drops in my game? I want to find performance bottlenecks.

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler… | official-docs | yes | — |
| https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_pan… | official-docs | yes | — |

**Hub Top Snippets:**

1. leton is a globally accessible object. Godot    provides access to several in scripts. It's the right tool to check for input    every frame.  We're going to use the ``Input`` singleton here as we nee
2. e measure the rate at which a game produces images in     Frames Per Second (FPS). Most games aim for 60 FPS, although you might find     figures like 30 FPS on slower mobile devices or 90 to 240 for
3. als`, we'll build upon the relationship between scripts and nodes by having our nodes trigger code in scripts. ``````  ## File: getting_started/step_by_step/signals.rst ``````rst .. Intention: give th

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

## Gaps & Recommendations
- 3 question(s) scored weak/fail. Review index coverage and source availability.
